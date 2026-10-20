#!/usr/bin/env python3
"""WP-CLI via SSH — Phase 2-5 completion for localaicreative.com"""
import subprocess
import sys

SSH_CMD = 'sshpass -p "AdamSL1210a7#mediengrs2017#" ssh -o StrictHostKeyChecking=no su1074596@access-5020741406.webspace-host.com'

def wpcli(args, workdir="/home/www"):
    cmd = f'{SSH_CMD} "cd {workdir} && wp {args}"'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        print(f"  STDERR: {r.stderr.strip()[:200]}")
    return r.stdout.strip(), r.returncode

# --- Find WP root ---
print("=== WP Root finden ===")
out, _ = wpcli("--allow-root eval 'echo ABSPATH;'")
print(f"  WP Root: {out}")

# Try common paths
wp_root = None
for path in ["/home/www", "/home/www/htdocs", "/var/www/vhosts/localaicreative.com/httpdocs"]:
    out, rc = wpcli("--allow-root core version", path)
    if rc == 0 and "WP" not in out:
        print(f"  Found WP at {path}: v{out}")
        wp_root = path
        break

if not wp_root:
    # Try to find it
    out, _ = wpcli("--allow-root eval 'echo ABSPATH;'", "/home/www")
    if out and "ABSPATH" not in out:
        wp_root = out.strip()
        print(f"  WP Root via eval: {wp_root}")

if not wp_root:
    # Brute force search
    out, _ = subprocess.run(
        f'{SSH_CMD} "find /home/www -maxdepth 4 -name wp-config.php 2>/dev/null | head -3"',
        shell=True, capture_output=True, text=True, timeout=15
    )
    print(f"  Search result: {out.strip()}")
    if out.strip():
        wp_root = out.strip().split('\n')[0].replace('/wp-config.php', '')
        print(f"  Using: {wp_root}")

if not wp_root:
    print("  COULD NOT FIND WP ROOT — aborting")
    sys.exit(1)

WPCMD = f'--allow-root --path={wp_root}'

def wp(args):
    full_args = f"{WPCMD} {args}"
    return wpcli(full_args, "/home/www")

# --- PHASE 2: Set static front page ---
print("\n=== Phase 2: Startseite setzen ===")
pages_out, _ = wp("post list --post_type=page --format=json")
import json
pages = json.loads(pages_out) if pages_out else []
home_id = None
blog_id = None
for p in pages:
    if p.get('post_name') == 'home':
        home_id = p['ID']
    elif p.get('post_name') == 'blog':
        blog_id = p['ID']

print(f"  Home page ID: {home_id}, Blog page ID: {blog_id}")

if home_id and blog_id:
    out, rc = wp(f"option update page_on_front {home_id}")
    print(f"  page_on_front={home_id}: {'OK' if rc==0 else 'FAIL'} ({out})")
    
    out, rc = wp(f"option update page_for_posts {blog_id}")
    print(f"  page_for_posts={blog_id}: {'OK' if rc==0 else 'FAIL'} ({out})")
    
    out, rc = wp("option update show_on_front page")
    print(f"  show_on_front=page: {'OK' if rc==0 else 'FAIL'} ({out})")

# --- PHASE 3: Menus ---
print("\n=== Phase 3: Menüs erstellen ===")

# Delete existing menus first
menus_out, _ = wp("menu list --format=json")
if menus_out:
    for m in json.loads(menus_out):
        wp(f"menu delete {m['term_id']}")
        print(f"  Deleted old menu: {m.get('name','')}")

# Create primary menu
out, rc = wp("menu create 'Primary Menu'")
print(f"  Create Primary Menu: {'OK' if rc==0 else out}")

if rc == 0:
    # Add items to primary menu
    for slug, label in [("home", "Home"), ("blog", "Blog"), ("about", "Über uns"), ("contact", "Kontakt")]:
        out, _ = wp(f"menu item add-url 'Primary Menu' '{label}' 'https://localaicreative.com/{slug}/'")
        print(f"    + {label}: {'OK' if 'created' in out.lower() or rc==0 else out[:80]}")

# Create footer menu
out, rc = wp("menu create 'Footer Menu'")
print(f"  Create Footer Menu: {'OK' if rc==0 else out}")

if rc == 0:
    for slug, label in [("impressum", "Impressum"), ("datenschutz", "Datenschutz"), ("cookies", "Cookies")]:
        out, _ = wp(f"menu item add-url 'Footer Menu' '{label}' 'https://localaicreative.com/{slug}/'")
        print(f"    + {label}: {'OK' if 'created' in out.lower() or rc==0 else out[:80]}")

# Assign menus to locations
out, _ = wp("option get theme_mods_kadence 2>/dev/null || echo '{}'")
print(f"  Theme mods check: {out[:100] if out else 'N/A'}")

# Try to assign via menu location
locations_out, _ = wp("menu location list --format=json")
if locations_out:
    print(f"  Available locations: {json.loads(locations_out)}")
    for loc in json.loads(locations_out):
        loc_name = loc.get('name', '')
        if 'primary' in loc_name.lower() or 'main' in loc_name.lower():
            out, _ = wp("menu location assign 'Primary Menu' primary")
            print(f"  Assigned Primary to {loc_name}: {'OK' if rc==0 else out[:80]}")
        elif 'footer' in loc_name.lower():
            out, _ = wp("menu location assign 'Footer Menu' footer")
            print(f"  Assigned Footer to {loc_name}: {'OK' if rc==0 else out[:80]}")

# --- PHASE 4: Kadence Customizer Settings ---
print("\n=== Phase 4: Kadence Theme Settings ===")

# Set colors via theme_mods
color_settings = [
    ("kadence_color_palette", json.dumps([{"color":"#6C5CE7","name":"Primary"},{"color":"#00B894","name":"Secondary"}])),
]

for key, val in color_settings:
    out, rc = wp(f"theme mod set '{key}' '{val}'")
    print(f"  {key}: {'OK' if rc==0 else out[:100]}")

# Set typography preferences
typo_settings = [
    ("kadence_typography_heading_font_family", "Inter"),
    ("kadence_typography_body_font_family", "'Source Sans Pro', sans-serif"),
]

for key, val in typo_settings:
    out, rc = wp(f"theme mod set '{key}' '{val}'")
    print(f"  {key}: {'OK' if rc==0 else out[:100]}")

# --- PHASE 5: Privacy Settings ---
print("\n=== Phase 5: WordPress Privacy ===")

out, _ = wp("option get privacy_policy_page_id")
print(f"  Current privacy page ID: {out}")

if home_id:
    # Find datenschutz page ID
    for p in pages:
        if p.get('post_name') == 'datenschutz':
            out, rc = wp(f"option update privacy_policy_page_id {p['ID']}")
            print(f"  Privacy policy page set to id={p['ID']}: {'OK' if rc==0 else out[:80]}")

# Disable XML-RPC if possible
out, _ = wp("config is-disabled xmlrpc 2>/dev/null || echo 'checking...'")
print(f"  XML-RPC check: {out}")

# --- Check installed plugins ---
print("\n=== Installed Plugins ===")
plugins_out, _ = wp("plugin list --format=json")
if plugins_out:
    for p in json.loads(plugins_out):
        print(f"  [{p['status']}] {p['name']} v{p.get('version','?')}")

print("\n=== WP Version ===")
out, _ = wp("core version")
print(f"  WordPress: {out}")

out, _ = wp("theme list --format=json")
if out:
    for t in json.loads(out):
        print(f"  Theme [{t['status']}]: {t['name']} v{t.get('version','?')}")

print("\n=== DONE ===")
