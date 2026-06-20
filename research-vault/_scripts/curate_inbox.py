#!/usr/bin/env python3
"""
Inbox Curator — Cluster inbox notes by topic, suggest knowledge synthesis & blog content.

Usage:
    python3 curate_inbox.py [vault_path] [--days 7]  # Scan last N days of inbox
    python3 curate_inbox.py /path/to/vault --suggest-blog  # Only show blog suggestions

Example:
    python3 curate_inbox.py "/home/bobadmin/projects/Local_AI_Influencer/research-vault/" --days 7
"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict


# ─── BLOG KATEGORIE-MATRIX ──────────────────────────────────────

BLOG_CATEGORIES = {
    "model_spotlight": {
        "name": "Model Spotlight",
        "trigger_keywords": ["qwen", "llama", "mistral", "gemma", "glm", "fable", "model"],
        "title_template": "{topic}: Was sich geandert hat",
        "description": "Deep-Dive zu einem spezifischen Model oder Release",
    },
    "hardware_guide": {
        "name": "Hardware Guide",
        "trigger_keywords": ["gpu", "rtx", "setup", "benchmark", "tok/s", "inference speed", "webgpu"],
        "title_template": "{topic}: So laeuft es auf Consumer-Hardware",
        "description": "Praktische Hardware-Guides mit echten Benchmarks",
    },
    "opinion_piece": {
        "name": "Opinion Piece",
        "trigger_keywords": ["stop using", "don't use", "banned", "controversial", "better than", "switched"],
        "title_template": "{topic}: Was die Community wirklich denkt",
        "description": "Kontroverse Themen mit Community-Stimme",
    },
    "practical_guide": {
        "name": "Practical Guide",
        "trigger_keywords": ["tutorial", "guide", "how to", "setup", "install", "step by step"],
        "title_template": "{topic}: Schritt-fuer-Schritt Anleitung",
        "description": "Anleitungen die Leser sofort anwenden koennen",
    },
    "trend_analysis": {
        "name": "Trend Analysis",
        "trigger_keywords": ["distillation", "interpretability", "quantization", "local ai trend"],
        "title_template": "{topic}: Der Trend der Local AI veraendert",
        "description": "Uebersicht ueber Trends die ueber mehrere Wochen laufen",
    },
    "weekly_digest": {
        "name": "Weekly Digest",
        "trigger_keywords": [],  # Always available
        "title_template": "LocalLLM News: Woche {week}",
        "description": "Woechentliche Uebersicht der Top-Themen",
    },
}


# ─── TOPIC CLUSTERING ──────────────────────────────────────────

# ─── ENTITY EXTRACTION (NER-LIKE) ──────────────────────────────

# Named entity dictionaries — expanded for better coverage
ENTITY_MODELS = {
    "qwen", "llama", "mistral", "gemma", "glm", "fable", "mixtral",
    "claude", "gpt", "phi", "deepseek", "yi", "command r", "mythos",
    "inflect-nano", "heretic grimoire", "ollama", "koboldcpp",
}

ENTITY_COMPANIES = {
    "anthropic", "nvidia", "deepmind", "hashicorp", "google", "meta",
    "microsoft", "openai", "zai org", "huggingface", "ggerganov", "ggml",
}

ENTITY_TOOLS = {
    "llama.cpp", "webgpu", "comfyui", "lm studio", "vllm", "koboldcpp",
    "text generation webui", "ollama", "transformers", "bitsandbytes",
}

ENTITY_CONCEPTS = {
    "distillation", "quantization", "local ai", "open source", "jailbreak",
    "interpretability", "inference", "benchmark", "gguf", "webgpu",
    "uncensored", "sparse attention", "mtp", "multi-token prediction",
}

STOP_WORDS = {
    "new", "update", "release", "announced", "introducing", "stop using",
    "we should", "is now", "is a", "the", "and", "but", "for", "with",
    "using", "on", "in", "vs", "versus", "ahead of", "behind", "now",
    "just", "really", "actually", "finally", "again", "still", "also",
}


def extract_entities(title):
    """Extract named entities from a title using dictionary-based NER.
    
    Returns dict with keys: models, companies, tools, concepts, fallback_words
    Prioritizes longer matches first to avoid partial matches (e.g., 'glm' before 'gl').
    """
    cleaned = title.lower()
    
    # Remove possessive suffixes for matching ("claude's" -> "claudes")
    cleaned_for_match = re.sub(r"'s\b", '', cleaned)
    
    entities = {"models": [], "companies": [], "tools": [], "concepts": []}
    
    # Multi-pass extraction: longer phrases first to avoid partial matches
    all_entities = sorted(ENTITY_MODELS | ENTITY_TOOLS, key=len, reverse=True)
    all_companies = sorted(ENTITY_COMPANIES, key=len, reverse=True)
    all_concepts = sorted(ENTITY_CONCEPTS, key=len, reverse=True)
    
    # Track matched spans to avoid overlapping matches
    matched_spans = []
    
    def overlaps(span_start, span_end):
        for s, e in matched_spans:
            if span_start < e and span_end > s:
                return True
        return False
    
    def find_and_record(text, entity_set, category):
        for entity in entity_set:
            idx = text.find(entity)
            while idx != -1:
                if not overlaps(idx, idx + len(entity)):
                    entities[category].append(entity)
                    matched_spans.append((idx, idx + len(entity)))
                idx = text.find(entity, idx + 1)
    
    # Extract in priority order: models > companies > tools > concepts
    find_and_record(cleaned_for_match, all_entities, "models")
    find_and_record(cleaned_for_match, all_companies, "companies")
    find_and_record(cleaned_for_match, all_concepts, "concepts")
    
    # Fallback: extract meaningful words not covered by entities
    if not any(entities.values()):
        # Remove stop words individually (not the whole tail after them)
        words = re.findall(r'\w{3,}', cleaned)
        filtered = [w for w in words if w not in STOP_WORDS]
        entities["fallback_words"] = filtered[:3]
    
    return entities


def extract_topic(title):
    """Extract the main topic from a title using entity-based clustering.
    
    Returns a normalized PRIMARY topic string for effective clustering.
    Uses only the highest-priority single entity so related notes cluster together
    even if they mention different secondary entities (e.g., 'glm' clusters both
    'GLM-5.2 on Design Arena' and 'GLM-5.2 is a win for local AI').
    """
    ents = extract_entities(title)
    
    # Use only the PRIMARY entity for clustering — prevents fragmentation
    if ents["models"]:
        return ents["models"][0].lower().replace(" ", "-")
    elif ents["companies"]:
        return ents["companies"][0].lower().replace(" ", "-")
    elif ents["concepts"]:
        return ents["concepts"][0].lower().replace(" ", "-")
    elif ents["fallback_words"]:
        return ents["fallback_words"][0].lower()
    
    return "general"


def extract_topic_label(title):
    """Human-readable topic label for display (e.g., 'GLM-5.2', 'Fable Ban')."""
    ents = extract_entities(title)
    
    if ents["models"]:
        return " + ".join(m.title() for m in ents["models"][:2])
    elif ents["companies"]:
        # Capitalize company names properly
        name_map = {"anthropic": "Anthropic", "nvidia": "NVIDIA", "deepmind": "DeepMind",
                    "hashicorp": "HashiCorp", "google": "Google", "meta": "Meta"}
        labels = [name_map.get(c, (c or "").title()) for c in ents["companies"][:2]]
        return " + ".join(str(l) for l in labels)
    elif ents["concepts"]:
        return " + ".join(c.title() for c in ents["concepts"][:2])
    
    # Fallback: first meaningful words from title
    cleaned = re.sub(r'^(?:new |update: |release: |announced: |introducing )', '', title.lower())
    words = re.findall(r'\w{3,}', cleaned)
    filtered = [w for w in words if w not in STOP_WORDS]
    return " + ".join(w.title() for w in filtered[:2]) if filtered else "General"


def _parse_note_file(note_file, date_str):
    """Parse a single .md note file and return its metadata dict or None."""
    try:
        content = note_file.read_text(encoding='utf-8')[:2000]

        # Extract title from frontmatter or first heading
        title = ""
        for line in content.split('\n'):
            if line.startswith('# ') and not line.startswith('---'):
                title = line[2:].strip()
                break

        if not title:
            return None

        # Extract attention score from frontmatter
        att_match = re.search(r'attention-score:\s*(\d+)', content)
        score = int(att_match.group(1)) if att_match else 0

        blog_pot_match = re.search(r'blog-potential:\s*(\w+)', content)
        blog_potential = blog_pot_match.group(1) if blog_pot_match else "low"

        source_match = re.search(r'source-type:\s*(.+)', content)
        source_type = source_match.group(1).strip() if source_match else "unknown"

        topic = extract_topic(title)

        return {
            "title": title,
            "file": str(note_file),
            "score": score,
            "blog_potential": blog_potential,
            "source_type": source_type,
            "date": date_str,
        }
    except Exception:
        return None


def cluster_inbox_notes(inbox_dir, trends_dir=None):
    """Scan inbox directory (+ optional trends dir) and cluster notes by topic.

    Primary source: _inbox/DATE/*.md  (structured daily inbox)
    Fallback source: trends/*.md      (flat trend notes from research runs)

    Notes are deduplicated by title to avoid double-counting when the same
    note exists in both locations.
    """
    clusters = defaultdict(list)
    seen_titles = set()

    def add_note(note_file, date_str):
        meta = _parse_note_file(note_file, date_str)
        if meta is None:
            return
        # Deduplicate by title (normalize whitespace)
        key = re.sub(r'\s+', ' ', meta["title"].lower())
        if key in seen_titles:
            return
        seen_titles.add(key)
        topic = meta.pop("topic") if "topic" in meta else extract_topic(meta["title"])
        # Re-derive topic from the returned meta (it was computed inside _parse_note_file)
        clusters[extract_topic(meta["title"])].append(meta)

    # 1. Primary: scan _inbox/DATE/*.md
    if inbox_dir.exists():
        for day_dir in sorted(inbox_dir.iterdir()):
            if not day_dir.is_dir():
                continue
            for note_file in day_dir.glob("*.md"):
                add_note(note_file, day_dir.name)

    # 2. Fallback: scan trends/*.md (flat files without date subdirs)
    if trends_dir and trends_dir.exists():
        for note_file in sorted(trends_dir.glob("*.md")):
            # Derive date from filename suffix like _260619 or file mtime
            stem = note_file.stem
            date_match = re.search(r'_(\d{6})$', stem)
            if date_match:
                raw = date_match.group(1)
                date_str = f"20{raw[:2]}-{raw[2:4]}-{raw[4:6]}"
            else:
                # Use file modification time as fallback
                mtime = note_file.stat().st_mtime
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
            add_note(note_file, date_str)

    # Sort each cluster by score descending
    for topic in clusters:
        clusters[topic].sort(key=lambda x: x["score"], reverse=True)

    return clusters


# ─── BLOG SUGGESTION ENGINE ──────────────────────────────────────

def suggest_blog_content(clusters):
    """Generate blog content suggestions from clustered topics"""
    suggestions = []

    for topic, notes in clusters.items():
        if len(notes) < 1:
            continue

        # Calculate cluster metrics
        avg_score = sum(n["score"] for n in notes) / len(notes)
        max_score = max(n["score"] for n in notes)
        has_high_potential = any(n["blog_potential"] == "high" for n in notes)
        source_diversity = len(set(n["source_type"] for n in notes))

        # Determine best blog category for this cluster
        best_category = None
        best_match_score = 0

        topic_lower = topic.lower()
        all_titles = " ".join(n["title"].lower() for n in notes)

        for cat_key, cat_info in BLOG_CATEGORIES.items():
            if cat_key == "weekly_digest":
                continue  # Handle separately

            keyword_matches = sum(1 for kw in cat_info["trigger_keywords"] if kw in all_titles)
            if keyword_matches > best_match_score:
                best_match_score = keyword_matches
                best_category = cat_key

        # Default to model_spotlight if no clear match but we have multiple notes
        if not best_category and len(notes) >= 2:
            best_category = "trend_analysis"
        elif not best_category:
            best_category = "model_spotlight"

        cat_info = BLOG_CATEGORIES[best_category]

        # Generate title suggestion
        title_suggestion = cat_info["title_template"].format(
            topic=topic.title(),
            week=datetime.now().strftime("%W/%Y"),
        )

        suggestions.append({
            "topic": topic,
            "category": best_category,
            "category_name": cat_info["name"],
            "title_suggestion": title_suggestion,
            "notes_count": len(notes),
            "avg_score": round(avg_score, 1),
            "max_score": max_score,
            "has_high_potential": has_high_potential,
            "source_diversity": source_diversity,
            "top_note": notes[0]["title"],
            "notes": [n["title"] for n in notes[:5]],  # Top 5 titles
        })

    # Sort by max score descending
    suggestions.sort(key=lambda x: x["max_score"], reverse=True)

    return suggestions


# ─── REPORT GENERATION ──────────────────────────────────────────

def print_cluster_report(clusters):
    """Print a human-readable cluster report"""
    print(f"\n{'='*60}")
    print(f"  INBOX CURATION REPORT")
    print(f"  {len(clusters)} Topics gefunden")
    print(f"{'='*60}")

    for topic, notes in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        avg_score = sum(n["score"] for n in notes) / len(notes)
        sources = set(n["source_type"] for n in notes)

        print(f"\n  [{len(notes)} Notes] {topic.title()}")
        print(f"    Avg Score: {avg_score:.0f} | Quellen: {', '.join(sources)}")

        for i, note in enumerate(notes[:3], 1):
            pot_marker = "!!" if note["blog_potential"] == "high" else ""
            print(f"    {i}. [{note['score']}pts] {note['title']}{pot_marker}")

        if len(notes) > 3:
            print(f"    ... und {len(notes) - 3} weitere")


def print_blog_suggestions(suggestions):
    """Print blog content suggestions"""
    if not suggestions:
        print("\n  Keine Blog-Vorschlaege — Inbox ist leer oder keine relevanten Topics.")
        return

    print(f"\n{'='*60}")
    print(f"  BLOG-CONTENT VORSCHLAEGE")
    print(f"  {len(suggestions)} Themen identifiziert")
    print(f"{'='*60}")

    for i, sug in enumerate(suggestions[:5], 1):  # Top 5
        pot_badge = " **HIGH**" if sug["has_high_potential"] else ""
        diversity_note = f" ({sug['source_diversity']} Quellen)" if sug["source_diversity"] > 1 else ""

        print(f"\n  {i}. [{sug['category_name']}]\"{sug['title_suggestion']}\"")
        print(f"     Topic: {sug['topic'].title()} | Max Score: {sug['max_score']}pts{pot_badge}{diversity_note}")
        print(f"     Notes im Cluster: {sug['notes_count']}")

        if sug["notes"]:
            print(f"     Top Note: \"{sug['top_note']}\"")


def write_curation_file(vault_path, clusters, suggestions):
    """Write curation report to a file for reference"""
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = vault_path / "_inbox"
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / f"curation_{today}.md"

    content = f"""---
created: {datetime.now().strftime('%Y-%m-%d')}
type: curation-report
topics: {len(clusters)}
blog_suggestions: {len(suggestions)}
---

# Inbox Curation Report — {today}

## Topic Clusters ({len(clusters)})

"""

    for topic, notes in sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True):
        avg_score = sum(n["score"] for n in notes) / len(notes)
        content += f"\n### {topic.title()} ({len(notes)} Notes, Avg Score: {avg_score:.0f})\n\n"

        for note in notes[:5]:
            pot_marker = " ⭐" if note["blog_potential"] == "high" else ""
            content += f"- [{note['score']}pts] {note['title']}{pot_marker}\n"

    content += f"\n---\n\n## Blog-Vorschlaege ({len(suggestions)})\n\n"

    for sug in suggestions[:5]:
        pot_badge = " **HIGH**" if sug["has_high_potential"] else ""
        content += f"""### {sug['title_suggestion']}
- **Kategorie:** {sug['category_name']}
- **Topic:** {sug['topic'].title()}
- **Max Score:** {sug['max_score']}pts{pot_badge}
- **Notes im Cluster:** {sug['notes_count']}

"""

    filepath.write_text(content, encoding='utf-8')
    print(f"\n[CURATION] Report gespeichert: {filepath}")


# ─── MAIN ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Inbox Curator — Cluster + Blog Suggestions")
    parser.add_argument("vault_path", help="Path to Obsidian vault")
    parser.add_argument("--days", type=int, default=7, help="Scan last N days of inbox (default: 7)")
    parser.add_argument("--suggest-blog", action="store_true", help="Only show blog suggestions")
    args = parser.parse_args()

    vault_path = Path(args.vault_path)
    inbox_dir = vault_path / "_inbox"
    trends_dir = vault_path / "trends"

    # Cluster notes from inbox (primary) + trends (fallback)
    clusters = cluster_inbox_notes(inbox_dir, trends_dir=trends_dir)

    if not args.suggest_blog:
        print_cluster_report(clusters)

    suggestions = suggest_blog_content(clusters)
    print_blog_suggestions(suggestions)

    # Write curation file
    write_curation_file(vault_path, clusters, suggestions)


if __name__ == "__main__":
    main()
