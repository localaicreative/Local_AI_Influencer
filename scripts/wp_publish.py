#!/usr/bin/env python3
"""
WordPress Publisher — Push blog drafts to WordPress via REST API.

Usage:
    # Publish a single draft
    python3 wp_publish.py /path/to/blog-drafts/01-article.md
    
    # List all existing drafts on WordPress
    python3 wp_publish.py --list-drafts
    
    # Preview (dry run) without publishing
    python3 wp_publish.py /path/to/draft.md --dry-run

Auth: Uses Basic Auth from environment or hardcoded credentials.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import markdown2
except ImportError:
    print("WARN: markdown2 nicht installiert — roher Markdown-Text wird gesendet.")
    markdown2 = None

# ─── CONFIG ──────────────────────────────────────────────────────

WP_URL = "https://www.grosse-schule.de/wp-json/wp/v2"
WP_USER = "hermesbot"
WP_PASS = "vV1wjxnVetckNi9WklqPqPjZ"

# Category name → ID mapping (ermitteln via GET /wp-json/wp/v2/categories)
CATEGORY_MAP = {
    # TODO: Echte IDs nachschlagen
    "research-spotlight": None,
    "trend-analysis": None,
    "hardware-guide": None,
    "opinion-piece": None,
    "practical-guide": None,
}


# ─── FRONTMATTER PARSING ────────────────────────────────────────

def parse_frontmatter(content):
    """Extract YAML-like frontmatter and body from markdown."""
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    fm_text = parts[1].strip()
    body = parts[2].strip()
    
    frontmatter = {}
    tags_list = []
    current_key = None
    in_list = False
    
    for line in fm_text.split('\n'):
        # Check indentation — indented lines are sub-items, not top-level keys
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        
        if not stripped:
            continue
        
        # Indented lines belong to the current list/key — skip as top-level
        if indent > 0:
            in_list = True
            # Handle list items at first level of indentation (e.g., - tag)
            if indent == 2 and stripped.startswith('- '):
                value = stripped[2:].strip().strip('"').strip("'")
                if current_key == 'tags':
                    tags_list.append(value)
            continue
        
        # Top-level key (no indentation)
        in_list = False
        if ':' in stripped and not stripped.startswith('#') and not stripped.startswith('-'):
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()
            current_key = key
            
            # Remove quotes from values
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            if key == 'tags':
                # Inline tags like [tag1, tag2]
                inline = re.findall(r'\[([^\]]+)\]', value)
                if inline:
                    tags_list.extend([t.strip() for t in inline[0].split(',')])
                elif value:
                    tags_list.append(value)
            else:
                frontmatter[key] = value
    
    frontmatter['tags'] = tags_list
    return frontmatter, body


# ─── MARKDOWN → HTML ────────────────────────────────────────────

def md_to_html(md_text):
    """Convert markdown to HTML for WordPress."""
    if markdown2:
        return markdown2.markdown(md_text, extras=['fenced-code-blocks', 'tables'])
    
    # Fallback: wrap in simple WordPress-compatible format
    # WordPress can render basic markdown natively in some themes
    return md_text


# ─── WORDPRESS API ──────────────────────────────────────────────

import urllib.request
import urllib.error


def wp_request(method, endpoint, data=None):
    """Make a request to the WordPress REST API."""
    url = f"{WP_URL}/{endpoint}" if not endpoint.startswith('http') else endpoint
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {__import__("base64").b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()}',
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if hasattr(e, 'read') else str(e)
        print(f"  HTTP {e.code}: {body[:200]}")
        return None


def list_drafts():
    """List all draft posts on WordPress."""
    print("\nWordPress Drafts:")
    print("=" * 60)
    
    posts = wp_request('GET', 'posts?status=draft&per_page=10&_fields=id,title,date,status')
    if not posts:
        return
    
    for post in posts:
        print(f"  #{post['id']} — {post['title'].get('rendered', '?')} ({post.get('date', '?')[:10]})")


def get_categories():
    """Fetch and display WordPress categories."""
    cats = wp_request('GET', 'categories?per_page=50')
    if not cats:
        return {}
    
    cat_map = {}
    print("\nWordPress Kategorien:")
    print("=" * 40)
    for cat in cats:
        name = cat.get('slug', '?')
        cid = cat['id']
        count = cat.get('count', 0)
        parent = f" (unter {cat.get('parent_name', '')})" if cat.get('parent') else ""
        print(f"  [{cid}] {name} ({count} Posts){parent}")
        cat_map[name] = cid
    
    return cat_map


def publish_draft(draft_path, dry_run=False):
    """Publish a markdown draft to WordPress."""
    path = Path(draft_path)
    if not path.exists():
        print(f"Fehler: Datei nicht gefunden: {path}")
        return False
    
    content = path.read_text(encoding='utf-8')
    fm, body = parse_frontmatter(content)
    
    # Build WordPress post data
    title = fm.get('title', path.stem.replace('-', ' ').title())
    slug = fm.get('slug', '')
    status = fm.get('status', 'draft')
    tags = fm.get('tags', [])
    
    # Convert markdown to HTML
    html_content = md_to_html(body)
    
    post_data = {
        "title": title,
        "content": html_content,
        "status": status,  # draft or publish
        "tags": [t.strip() for t in tags if t],
    }
    
    if slug:
        post_data["slug"] = slug
    
    # Category mapping (if IDs are configured)
    category_name = fm.get('category', '')
    cat_id = CATEGORY_MAP.get(category_name)
    if cat_id:
        post_data["categories"] = [cat_id]
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}WordPress Post:")
    print("=" * 60)
    print(f"  Titel:   {title}")
    print(f"  Slug:    {slug or '(auto)'}")
    print(f"  Status:  {status}")
    print(f"  Tags:    {', '.join(tags)}")
    print(f"  Kategorie: {category_name or '(keine)'}")
    print(f"  Content: {len(html_content)} Zeichen HTML")
    
    if dry_run:
        print("\n  → Dry Run abgeschlossen. Nichts gesendet.")
        return True
    
    # Send to WordPress
    result = wp_request('POST', 'posts', post_data)
    if result and 'id' in result:
        link = result.get('link', '(kein Link)')
        print(f"\n  ✓ Post erstellt! ID: {result['id']}")
        print(f"  Link: {link}")
        return True
    else:
        print("\n  ✗ Fehler beim Erstellen des Posts.")
        return False


# ─── MAIN ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="WordPress Publisher for Local AI Influencer")
    parser.add_argument("draft", nargs='?', help="Path to markdown draft file")
    parser.add_argument("--list-drafts", action="store_true", help="List existing drafts on WordPress")
    parser.add_argument("--categories", action="store_true", help="Show WordPress categories")
    parser.add_argument("--dry-run", action="store_true", help="Preview without publishing")
    args = parser.parse_args()
    
    if args.categories:
        get_categories()
        return
    
    if args.list_drafts:
        list_drafts()
        return
    
    if not args.draft:
        parser.print_help()
        print("\nTippe 'python3 wp_publish.py --categories' um Kategorien zu sehen.")
        return
    
    publish_draft(args.draft, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
