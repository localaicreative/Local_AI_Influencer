#!/usr/bin/env python3
"""
Static site generator for Local AI Influencer blog.

Reads markdown files from blog-drafts/, renders them to HTML,
and outputs a complete static site ready for GitHub Pages.

Usage:
    python3 build_site.py                    # Build full site
    python3 build_site.py --serve            # Build + serve locally on :8080
"""

import argparse
import os
import re
from pathlib import Path
from datetime import datetime

try:
    import markdown2
except ImportError:
    print("WARN: pip install markdown2")
    markdown2 = None


# ─── CONFIG ──────────────────────────────────────────────────────

SITE_DIR = Path(__file__).parent.parent / "site"
BLOG_DIR = Path(__file__).parent.parent / "blog-drafts"
SITE_TITLE = "Local AI Influencer"
SITE_DESC = "Research, Trends & Insights aus der Local LLM Community"


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
    
    for line in fm_text.split('\n'):
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        
        if not stripped:
            continue
        
        if indent > 0:
            if indent == 2 and stripped.startswith('- '):
                value = stripped[2:].strip().strip('"').strip("'")
                if current_key == 'tags':
                    tags_list.append(value)
            continue
        
        if ':' in stripped and not stripped.startswith('#') and not stripped.startswith('-'):
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()
            current_key = key
            
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            if key == 'tags':
                inline = re.findall(r'\[([^\]]+)\]', value)
                if inline:
                    tags_list.extend([t.strip() for t in inline[0].split(',')])
                elif value:
                    tags_list.append(value)
            else:
                frontmatter[key] = value
    
    frontmatter['tags'] = tags_list
    return frontmatter, body


# ─── HTML TEMPLATES ─────────────────────────────────────────────

BASE_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #0d1117; color: #c9d1d9; line-height: 1.7;
}

a { color: #58a6ff; text-decoration: none; }
a:hover { text-decoration: underline; }

.container { max-width: 800px; margin: 0 auto; padding: 2rem 1.5rem; }

/* Header */
header { border-bottom: 1px solid #30363d; padding: 2rem 0; margin-bottom: 2rem; }
header h1 { font-size: 1.8rem; color: #f0f6fc; }
header p { color: #8b949e; margin-top: 0.5rem; }
nav { margin-top: 1rem; }
nav a { margin-right: 1rem; font-size: 0.9rem; }

/* Blog list */
.post-card {
    border: 1px solid #30363d; border-radius: 8px; padding: 1.5rem;
    margin-bottom: 1rem; transition: border-color 0.2s;
}
.post-card:hover { border-color: #58a6ff; }
.post-card h2 { font-size: 1.3rem; color: #f0f6fc; margin-bottom: 0.5rem; }
.post-card .meta { color: #8b949e; font-size: 0.85rem; margin-bottom: 0.75rem; }
.post-card .excerpt { color: #c9d1d9; font-size: 0.95rem; }
.post-card .tags { margin-top: 0.75rem; }
.tag {
    display: inline-block; background: #21262d; border: 1px solid #30363d;
    border-radius: 12px; padding: 2px 10px; font-size: 0.75rem; color: #8b949e; margin-right: 0.5rem;
}

/* Post page */
.post-header { margin-bottom: 2rem; }
.post-header h1 { font-size: 2rem; color: #f0f6fc; line-height: 1.3; }
.post-header .meta { color: #8b949e; font-size: 0.9rem; margin-top: 0.5rem; }

.post-content h2 { color: #f0f6fc; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #30363d; }
.post-content h3 { color: #e6edf3; margin: 1.5rem 0 0.75rem; }
.post-content p { margin-bottom: 1rem; }
.post-content ul, .post-content ol { margin: 1rem 0 1rem 2rem; }
.post-content li { margin-bottom: 0.3rem; }
.post-content blockquote { border-left: 3px solid #58a6ff; padding: 0.75rem 1rem; margin: 1rem 0; background: #161b22; border-radius: 0 8px 8px 0; }
.post-content code { background: #161b22; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
.post-content pre { background: #161b22; padding: 1rem; border-radius: 8px; overflow-x: auto; margin: 1rem 0; }
.post-content pre code { background: none; padding: 0; }
.post-content table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
.post-content th, .post-content td { border: 1px solid #30363d; padding: 0.5rem 0.75rem; text-align: left; }
.post-content th { background: #161b22; color: #f0f6fc; }

.back-link { display: inline-block; margin-bottom: 2rem; font-size: 0.9rem; }

footer { border-top: 1px solid #30363d; padding: 1.5rem 0; margin-top: 3rem; text-align: center; color: #484f58; font-size: 0.85rem; }
"""


def html_page(title, body_html):
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{BASE_CSS}</style>
</head>
<body>
<div class="container">
{body_html}
<footer>&copy; {datetime.now().year} Local AI Influencer &mdash; Research aus der Community.</footer>
</div>
</body>
</html>"""


# ─── BUILD FUNCTIONS ────────────────────────────────────────────

def load_posts():
    """Load all blog posts from blog-drafts/."""
    if not BLOG_DIR.exists():
        return []
    
    posts = []
    for f in sorted(BLOG_DIR.glob("*.md")):
        content = f.read_text(encoding='utf-8')
        fm, body = parse_frontmatter(content)
        
        # Convert markdown to HTML
        if markdown2:
            html_body = markdown2.markdown(body, extras=['fenced-code-blocks', 'tables'])
        else:
            html_body = body.replace('\n\n', '</p><p>').replace('\n', '<br>')
        
        posts.append({
            'file': f.name,
            'slug': fm.get('slug', f.stem),
            'title': fm.get('title', f.stem.replace('-', ' ').title()),
            'date': fm.get('created', ''),
            'category': fm.get('category', ''),
            'tags': fm.get('tags', []),
            'body_html': html_body,
            'excerpt': body[:200].replace('\n', ' ') + '...',
        })
    
    # Sort by date descending
    posts.sort(key=lambda p: p['date'] or '', reverse=True)
    return posts


def build_index(posts):
    """Build the main index page."""
    header = f"""<header>
<h1>{SITE_TITLE}</h1>
<p>{SITE_DESC}</p>
<nav><a href="index.html">Blog</a></nav>
</header>"""
    
    if not posts:
        return html_page(SITE_TITLE, header + '<p>Noch keine Posts vorhanden.</p>')
    
    cards = []
    for p in posts:
        date_str = p['date'][:10] if p['date'] else ''
        tags_html = ''.join(f'<span class="tag">{t}</span>' for t in p['tags'])
        cards.append(f"""<div class="post-card">
<h2><a href="{p['slug']}.html">{p['title']}</a></h2>
<div class="meta">{date_str}{' &middot; ' + p['category'].replace('-', ' ').title() if p['category'] else ''}</div>
<div class="excerpt">{p['excerpt']}</div>
<div class="tags">{tags_html}</div>
</div>""")
    
    return html_page(SITE_TITLE, header + '\n'.join(cards))


def build_post(p):
    """Build an individual post page."""
    date_str = p['date'][:10] if p['date'] else ''
    tags_html = ''.join(f'<span class="tag">{t}</span>' for t in p['tags'])
    
    body = f"""<header>
<h1>{SITE_TITLE}</h1>
<p>{SITE_DESC}</p>
<nav><a href="index.html">Blog</a></nav>
</header>

<a class="back-link" href="index.html">&larr; Zurueck zum Blog</a>

<div class="post-header">
<h1>{p['title']}</h1>
<div class="meta">{date_str}{' &middot; ' + p['category'].replace('-', ' ').title() if p['category'] else ''}</div>
<div class="tags" style="margin-top:0.5rem;">{tags_html}</div>
</div>

<div class="post-content">
{p['body_html']}
</div>"""
    
    return html_page(f"{p['title']} — {SITE_TITLE}", body)


def build_site():
    """Build the complete static site."""
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    
    posts = load_posts()
    
    # Index page
    index_html = build_index(posts)
    (SITE_DIR / "index.html").write_text(index_html, encoding='utf-8')
    print(f"  [OK] index.html ({len(posts)} Posts)")
    
    # Individual post pages
    for p in posts:
        post_html = build_post(p)
        out_path = SITE_DIR / f"{p['slug']}.html"
        out_path.write_text(post_html, encoding='utf-8')
        print(f"  [OK] {p['slug']}.html")
    
    # robots.txt
    (SITE_DIR / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding='utf-8')
    
    return len(posts)


# ─── MAIN ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Build static site for Local AI Influencer")
    parser.add_argument("--serve", action="store_true", help="Serve locally on :8080 after building")
    args = parser.parse_args()
    
    print("\nBuilding site...")
    count = build_site()
    print(f"\nSite built: {SITE_DIR}/ ({count} posts)")
    print(f"Open in browser: file://{SITE_DIR / 'index.html'}")
    
    if args.serve:
        import http.server
        port = 8080
        os.chdir(str(SITE_DIR))
        handler = http.server.SimpleHTTPRequestHandler
        server = http.server.HTTPServer(('0.0.0.0', port), handler)
        print(f"\nServing on http://localhost:{port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
