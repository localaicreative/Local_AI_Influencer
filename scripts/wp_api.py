#!/usr/bin/env python3
"""WordPress REST API Helper für localaicreative.com"""
import json
import base64
import urllib.request
import urllib.error
import sys

BASE = "https://localaicreative.com/wp-json/wp/v2"
USER = "localaicreative@gmail.com"
APP_PW = "M9vl nvFs NgHs oinO mBH7 XVJ7"

def auth_header():
    creds = base64.b64encode(f"{USER}:{APP_PW}".encode()).decode()
    return f"Basic {creds}"

def get(path, params=None):
    url = f"{BASE}/{path}"
    if params:
        qs = "&".join(f"{k}={v}" for k,v in params.items())
        url += f"?{qs}"
    req = urllib.request.Request(url, headers={"Authorization": auth_header()})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()[:200]}")
        sys.exit(1)

def post(path, data):
    url = f"{BASE}/{path}"
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST",
        headers={"Authorization": auth_header(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()[:200]}")
        sys.exit(1)

def delete(path):
    url = f"{BASE}/{path}"
    req = urllib.request.Request(url, method="DELETE",
        headers={"Authorization": auth_header()})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()[:200]}")
        sys.exit(1)

# Command dispatch
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    
    if cmd == "test":
        u = get("users/me")
        print(f"Auth OK: {u.get('name')} ({u.get('slug')})")
    
    elif cmd == "themes":
        themes = get("themes?status=active")
        for t in themes:
            print(f"  Active: {t['name']} v{t.get('version','?')} (slug: {t.get('slug','')})")
    
    elif cmd == "posts":
        posts = get("posts", {"per_page": 10})
        for p in posts:
            print(f"  [{p['status']}] {p['title']['rendered']}")
    
    elif cmd == "pages":
        pages = get("pages", {"per_page": 20})
        for p in pages:
            print(f"  [{p['status']}] {p['title']['rendered']} ({p['slug']})")
    
    elif cmd == "settings":
        opts = get("options?context=edit")
        if isinstance(opts, list):
            for o in opts:
                key = o.get('option_name', '')
                val = str(o.get('value', ''))[:80]
                print(f"  {key}: {val}")
        else:
            print(json.dumps(opts, indent=2)[:500])
    
    elif cmd == "create-page":
        title = sys.argv[2] if len(sys.argv) > 2 else "Test Page"
        slug = sys.argv[3] if len(sys.argv) > 3 else title.lower().replace(" ", "-")
        content = sys.argv[4] if len(sys.argv) > 4 else ""
        result = post("pages", {
            "title": title,
            "slug": slug,
            "content": content,
            "status": "draft"
        })
        print(f"Created page: id={result['id']}, slug={result['slug']}")
    
    elif cmd == "delete-hello-world":
        posts = get("posts", {"per_page": 100})
        for p in posts:
            if p["title"]["rendered"] == "Hello world!":
                result = delete(f"posts/{p['id']}")
                print(f"Deleted Hello World post (trashed)")
                break
    
    elif cmd == "categories":
        cats = get("categories", {"per_page": 50})
        for c in cats:
            print(f"  [{c['id']}] {c['name']} ({c['slug']})")
    
    elif cmd == "create-category":
        name = sys.argv[2] if len(sys.argv) > 2 else "New Category"
        slug = sys.argv[3] if len(sys.argv) > 3 else name.lower().replace(" ", "-")
        result = post("categories", {"name": name, "slug": slug})
        print(f"Created category: id={result['id']}, slug={result['slug']}")
    
    elif cmd == "plugins":
        # Needs admin context - may not work via REST API without plugin
        plugins = get("plugins?context=edit", )
        for p in plugins:
            print(f"  {p.get('name','')} v{p.get('version','')} ({p.get('status','')})")
    
    elif cmd == "options-read":
        key = sys.argv[2] if len(sys.argv) > 2 else ""
        opts = get("options", {"context": "edit"})
        for o in (opts if isinstance(opts, list) else [opts]):
            if key and o.get('option_name') != key:
                continue
            print(f"  {o.get('option_name','')}: {str(o.get('value',''))[:120]}")
    
    elif cmd == "options-write":
        key = sys.argv[2] if len(sys.argv) > 2 else ""
        value = sys.argv[3] if len(sys.argv) > 3 else ""
        # Find existing option ID first
        opts = get("options", {"context": "edit"})
        opt_id = None
        for o in (opts if isinstance(opts, list) else [opts]):
            if o.get('option_name') == key:
                opt_id = o['id']
                break
        data = {"value": value}
        if opt_id:
            # PUT update
            url = f"{BASE}/options/{opt_id}"
            req = urllib.request.Request(url, data=json.dumps(data).encode(), method="PUT",
                headers={"Authorization": auth_header(), "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                result = json.loads(r.read().decode())
        else:
            result = post("options", data)
        print(f"Set {key} -> {result.get('value','')[:80]}")
    
    else:
        print("Commands: test, themes, posts, pages, settings, create-page, delete-hello-world, categories, create-category, plugins, options-read, options-write")
