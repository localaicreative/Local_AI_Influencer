#!/usr/bin/env python3
"""
LocalLLM Research Runner — Collect trends from web sources, write notes to inbox.

Usage:
    python3 run_research.py [vault_path] [--sources youtube github huggingface reddit]

Sources:
  - youtube: RSS feeds from AI/ML channels (Two Minute Papers, etc.)
  - github: GitHub trending repos related to local LLMs
  - huggingface: Trending models on HuggingFace
  - reddit: r/LocalLLaMA top posts via RSS

Each source is queried and new items are written as .md notes to _inbox/YYYY-MM-DD/.
Notes include attention-score, source-type, blog-potential in frontmatter.
"""

import argparse
import hashlib
import html
import json
import re
import ssl
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request


# ─── CONFIG ──────────────────────────────────────────────────────

YOUTUBE_RSS_FEEDS = [
    ("Two Minute Papers", "https://www.youtube.com/feeds/videos.xml?channel_id=UCbfYPyITQ-7l4upoX8nvctg"),
    ("AI Explained", "https://www.youtube.com/feeds/videos.xml?channel_id=UCBjkbmzVplPgVF-GheNYWCg"),
    ("Fferri's AI Newsletter", "https://www.youtube.com/feeds/videos.xml?channel_id=UCiRRuzgwrWMWw3GqWAtxOuQ"),
    ("LocalLLaMA", "https://www.youtube.com/feeds/videos.xml?channel_id=UC-Gb4Qs8Uq_rJeK0JQ8ANNA"),
    ("LlamaIndex", "https://www.youtube.com/feeds/videos.xml?channel_id=UCeRjipR4_SsCddq9VZ2AeKg"),
    ("Digital Spaceport", "https://www.youtube.com/feeds/videos.xml?channel_id=UCiaQzXI5528Il6r2NNkrkJA"),
    ("Zero To MVP", "https://www.youtube.com/feeds/videos.xml?channel_id=UCvN3QmpWy_eFG8gIU_Ij-RQ"),
    ("Manolo Remiddi", "https://www.youtube.com/feeds/videos.xml?channel_id=UCK_jrlrPtFRPskVKBhGCqMw"),
]

GITHUB_TRENDING_URL = "https://api.github.com/search/repositories"

HUGGINGFACE_TRENDING_URL = "https://huggingface.co/api/models?sort=likes&direction=-1&limit=20"

REDDIT_RSS_FEEDS = [
    ("r/LocalLLaMA Top", "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=week"),
]

# Keywords that indicate local LLM relevance
LOCAL_LLM_KEYWORDS = [
    "llama", "qwen", "mistral", "gemma", "glm", "local llm", "local ai",
    "gguf", "llama.cpp", "ollama", "inference", "quantization", "model",
    "open source ai", "uncensored", "webgpu", "consumer gpu", "lm studio",
    "koboldcpp", "vllm", "transformers", "deepseek", "fable", "mythos",
]


# ─── HELPER FUNCTIONS ────────────────────────────────────────────

def is_local_llm_relevant(title, description="", tags=None):
    """Check if a title/description is relevant to local LLMs."""
    text = (title + " " + description + " " + " ".join(tags or [])).lower()
    matches = sum(1 for kw in LOCAL_LLM_KEYWORDS if kw.lower() in text)
    return matches >= 1  # At least 1 keyword match (was 2, too strict for HF)


def calculate_attention_score(source_type, title, content_length):
    """Calculate attention score (0-50)."""
    score = 0

    # Source type base
    source_scores = {"youtube": 15, "github": 12, "huggingface": 10, "reddit": 10}
    score += source_scores.get(source_type.lower(), 5)

    # Content length bonus
    if content_length > 2000:
        score += 10
    elif content_length > 500:
        score += 5

    # Controversial/engaging keywords
    controversial = ["banned", "stop using", "jailbreak", "uncensored",
                     "takedown", "forced", "controversial"]
    controversy = sum(5 for kw in controversial if kw.lower() in title.lower())
    score += min(controversy, 15)

    # Entity mentions
    entities = ["qwen", "llama", "deepseek", "claude", "nvidia", "anthropic",
                "glm", "fable", "mythos", "mistral"]
    entity_count = sum(1 for e in entities if e.lower() in title.lower())
    score += min(entity_count * 3, 9)

    return min(score, 50)


def slugify(title):
    """Create a filename-safe slug from a title."""
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
    slug = re.sub(r'[\s_]+', '-', slug).lower()
    return slug[:80]  # Max 80 chars


def blog_potential(score, source_type):
    """Estimate blog potential based on score and source."""
    if score >= 35:
        return "high"
    elif score >= 25:
        return "medium"
    return "low"


# ─── SOURCE SCRAPERS ─────────────────────────────────────────────

def fetch_xml(url):
    """Fetch XML content from a URL."""
    try:
        ctx = ssl.create_default_context()
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 LocalLLM-Research/1.0"})
        with urlopen(req, timeout=30, context=ctx) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}")
        return None


def fetch_json(url):
    """Fetch JSON content from a URL."""
    try:
        ctx = ssl.create_default_context()
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 LocalLLM-Research/1.0",
            "Accept": "application/json",
        })
        with urlopen(req, timeout=30, context=ctx) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}")
        return None


def parse_youtube_rss(xml_content):
    """Parse YouTube RSS feed (Atom format) and extract items."""
    if not xml_content:
        return []

    items = []
    # Simple XML parsing without external deps
    entry_pattern = re.compile(r'<entry>(.*?)</entry>', re.DOTALL)
    for entry in entry_pattern.findall(xml_content):
        title_m = re.search(r'<title>(.*?)</title>', entry)
        # Atom format: <link rel="alternate" href="...">  (not just <link href="...">)
        link_m = re.search(r'<link\s+[^>]*href="([^"]+)"', entry)
        if not link_m:
            link_m = re.search(r'yt:videoId>([^<]+)', entry)
            if link_m:
                # Fallback: construct URL from video ID
                link_m = type('M', (), {'group': lambda s, i: f"https://www.youtube.com/watch?v={entry.split('yt:videoId>')[1].split('<')[0]}"})()
        desc_m = re.search(r'<media:description.*?>(.*?)</media:description>', entry, re.DOTALL)
        pub_m = re.search(r'<published>(.*?)</published>', entry)

        if title_m and link_m:
            title = html.unescape(title_m.group(1).strip())
            url = link_m.group(1)
            description = html.unescape(desc_m.group(1).strip()) if desc_m else ""
            published = pub_m.group(1)[:10] if pub_m else ""

            items.append({
                "title": title,
                "url": url,
                "description": description[:500],
                "published": published,
            })

    return items


def fetch_youtube(sources):
    """Fetch from YouTube RSS feeds."""
    all_items = []
    for name, url in YOUTUBE_RSS_FEEDS:
        print(f"  [YOUTUBE] Fetching {name}...")
        xml = fetch_xml(url)
        items = parse_youtube_rss(xml)
        for item in items:
            item["source_name"] = name
        all_items.extend(items)
    return all_items


def fetch_github():
    """Fetch trending repos from GitHub."""
    print("  [GITHUB] Fetching trending local LLM repos...")
    # Search for recent repos with local LLM keywords (URL-encoded queries)
    queries = ["local+llm+inference", "llama.cpp+gguf", "quantized+model"]
    all_items = []

    for q in queries:
        params = f"?q={q}+created%3A%3E2026-05-01&sort=stars&order=desc&per_page=10"
        data = fetch_json(GITHUB_TRENDING_URL + params)
        if data and "items" in data:
            for repo in data["items"]:
                all_items.append({
                    "title": f"{repo['full_name']} — {repo.get('description', '')[:100]}",
                    "url": repo["html_url"],
                    "description": repo.get("description", "") or "",
                    "published": repo.get("created_at", "")[:10],
                    "source_name": "GitHub Trending",
                })

    return all_items


def fetch_huggingface():
    """Fetch trending models from HuggingFace — only recent ones (<30 days)."""
    print("  [HUGGINGFACE] Fetching trending models...")
    data = fetch_json(HUGGINGFACE_TRENDING_URL)
    items = []

    if not data:
        return items

    # Filter: only models modified in last 30 days (skip established/old models)
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=30)

    for model in data:
        title = model.get("modelId", "")
        likes = model.get("likes", 0)
        tags = model.get("tags", [])
        pipeline_tag = model.get("pipeline_tag", "")
        last_modified = model.get("lastModified", "")

        # Skip old models (no lastModified or >30 days old)
        if last_modified:
            try:
                mod_date = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
                if mod_date < cutoff:
                    continue  # Too old, skip
            except (ValueError, TypeError):
                pass  # Parse failed, include anyway

        description = f"{likes} likes | {pipeline_tag}" if pipeline_tag else f"{likes} likes"

        items.append({
            "title": title,
            "url": f"https://huggingface.co/{title}",
            "description": description,
            "published": last_modified[:10] if last_modified else "",
            "source_name": "HuggingFace Trending",
            "tags": tags,  # Pass tags for relevance check
        })

    return items


def fetch_reddit():
    """Fetch from Reddit RSS feeds."""
    all_items = []
    for name, url in REDDIT_RSS_FEEDS:
        print(f"  [REDDIT] Fetching {name}...")
        xml = fetch_xml(url)
        if not xml:
            continue

        # Parse RSS items
        item_pattern = re.compile(r'<item>(.*?)</item>', re.DOTALL)
        for item in item_pattern.findall(xml):
            title_m = re.search(r'<title>(.*?)</title>', item)
            link_m = re.search(r'<link>(.*?)</link>', item)
            desc_m = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
            pub_m = re.search(r'<pubDate>(.*?)</pubDate>', item)

            if title_m and link_m:
                title = html.unescape(title_m.group(1).strip())
                url_link = link_m.group(1).strip()
                description = html.unescape(desc_m.group(1).strip()[:500]) if desc_m else ""
                published = pub_m.group(1)[:10] if pub_m else ""

                all_items.append({
                    "title": title,
                    "url": url_link,
                    "description": description,
                    "published": published,
                    "source_name": name,
                })

    return all_items


# ─── NOTE WRITING ────────────────────────────────────────────────

def write_note(inbox_dir, item, source_type):
    """Write a research note to the inbox directory."""
    title = item["title"]
    url = item["url"]
    description = item.get("description", "")
    published = item.get("published", "")
    source_name = item.get("source_name", "Unknown")

    # Calculate score and blog potential
    content_length = len(description)
    score = calculate_attention_score(source_type, title, content_length)
    bp = blog_potential(score, source_type)

    # Create slug and filename
    slug = slugify(title)
    date_suffix = datetime.now().strftime("%y%m%d")
    filename = f"{slug}_{date_suffix}.md"

    filepath = inbox_dir / filename

    # Skip if already exists (deduplication)
    if filepath.exists():
        return False, "exists"

    # Build note content
    source_type_map = {
        "youtube": "Video",
        "github": "Code",
        "huggingface": "Model",
        "reddit": "Community",
    }
    st_display = source_type_map.get(source_type.lower(), "Unknown")

    content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
tags: [research, auto-generated]
status: new
source: {source_name}
source-type: {st_display}
attention-score: {score}
blog-potential: {bp}
url: {url}
---

# {title}

## Zusammenfassung

{description[:800]}

## Quelle

- **Feed:** [{source_name}]({url})
- **Typ:** {st_display}
- **Attention Score:** {score}pts
- **Blog-Potenzial:** {bp.upper()}

## Nchste Schritte

- [ ] Deep Dive durchfuhren falls Score >= 30
- [ ] In richtige Kategorie verschieben falls notig
- [ ] Backlinks zu verwandten Notes hinzufugen

## Verwandte Notes

- [[ ]]
"""

    filepath.write_text(content, encoding='utf-8')
    return True, score


# ─── MAIN ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LocalLLM Research Runner")
    parser.add_argument("vault_path", nargs="?", default=".")
    parser.add_argument("--sources", nargs="+",
                        choices=["youtube", "github", "huggingface", "reddit"],
                        default=["youtube", "github", "huggingface", "reddit"])
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    inbox_dir = vault_path / "_inbox" / datetime.now().strftime("%Y-%m-%d")
    inbox_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"  LocalLLM Research Runner — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Quellen: {', '.join(args.sources)}")
    print(f"{'='*50}\n")

    total_new = 0
    total_skipped = 0
    total_irrelevant = 0

    # Fetch from each source
    if "youtube" in args.sources:
        items = fetch_youtube("youtube")
        for item in items:
            if is_local_llm_relevant(item["title"], item.get("description", "")):
                ok, result = write_note(inbox_dir, item, "youtube")
                if ok:
                    print(f"  [NEW] {item['title'][:60]}... ({result}pts)")
                    total_new += 1
                else:
                    total_skipped += 1
            else:
                total_irrelevant += 1

    if "github" in args.sources:
        items = fetch_github()
        for item in items:
            ok, result = write_note(inbox_dir, item, "github")
            if ok:
                print(f"  [NEW] {item['title'][:60]}... ({result}pts)")
                total_new += 1
            else:
                total_skipped += 1

    if "huggingface" in args.sources:
        items = fetch_huggingface()
        for item in items:
            tags = item.pop("tags", None)  # Extract tags before writing note
            if is_local_llm_relevant(item["title"], item.get("description", ""), tags):
                ok, result = write_note(inbox_dir, item, "huggingface")
                if ok:
                    print(f"  [NEW] {item['title'][:60]}... ({result}pts)")
                    total_new += 1
                else:
                    total_skipped += 1
            else:
                total_irrelevant += 1

    if "reddit" in args.sources:
        items = fetch_reddit()
        for item in items:
            if is_local_llm_relevant(item["title"], item.get("description", "")):
                ok, result = write_note(inbox_dir, item, "reddit")
                if ok:
                    print(f"  [NEW] {item['title'][:60]}... ({result}pts)")
                    total_new += 1
                else:
                    total_skipped += 1
            else:
                total_irrelevant += 1

    print(f"\n{'='*50}")
    print(f"  Ergebnis: {total_new} neue Notes, {total_skipped} Duplikate, {total_irrelevant} irrelevant")
    print(f"  Gespeichert in: {inbox_dir}")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    main()
