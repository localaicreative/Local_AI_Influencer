#!/usr/bin/env python3
"""WP Phase 3-5: Menus, Settings, DSGVO cleanup via REST API"""
import json
import base64
import urllib.request
import urllib.error
import sys

BASE = "https://localaicreative.com/wp-json"
USER = "localaicreative@gmail.com"
APP_PW = "M9vl nvFs NgHs oinO mBH7 XVJ7"

def auth():
    creds = base64.b64encode(f"{USER}:{APP_PW}".encode()).decode()
    return f"Basic {creds}"

def api(method, path, data=None):
    url = f"{BASE}/{path}"
    headers = {"Authorization": auth(), "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        print(f"  [{e.code}] {path}: {body}")
        return None

# --- DISCOVER available endpoints ---
print("=== Endpoint Discovery ===")
spec = api("GET", "index?context=edit")
if spec:
    namespaces = list(spec.get('namespaces', []))
    routes = list(spec.keys()) if isinstance(spec, dict) else []
    # Filter for interesting ones
    interesting = [r for r in spec.keys() if any(k in r for k in ['menu','option','theme','widget','customizer'])]
    print(f"  Namespaces: {namespaces}")
    print(f"  Interesting routes ({len(interesting)}):")
    for r in sorted(interesting)[:20]:
        methods = spec[r].get('args', {}) if isinstance(spec.get(r), dict) else {}
        print(f"    {r}")

# --- Try Kadence-specific endpoints ---
print("\n=== Kadence API Check ===")
kadence_routes = [
    "kadence/v1/settings",
    "kadence/v1/header-builder",
    "kadence/v1/footer-builder",
]
for route in kadence_routes:
    r = api("GET", route)
    if r:
        print(f"  OK: {route} -> {type(r).__name__}")

# --- Try to set theme_mods (Customizer settings) ---
print("\n=== Theme Mods / Customizer ===")
theme_mods_attempts = [
    ("POST", "wp/v2/theme-mods/kadence_color_palette", {"value": [{"color":"#6C5CE7","name":"Primary"},{"color":"#00B894","name":"Secondary"}]}),
]

for method, path, data in theme_mods_attempts:
    r = api(method, path, data)
    if r:
        print(f"  OK: {path}")
    # else already printed error above

# --- Delete Sample Page ---
print("\n=== Cleanup ===")
pages = api("GET", "wp/v2/pages?per_page=100&context=edit")
if pages:
    for p in pages:
        if p["slug"] == "sample-page":
            r = api("DELETE", f"wp/v2/pages/{p['id']}")
            print(f"  Deleted Sample Page: {'OK' if r else 'FAIL'}")

# --- Check existing posts count ---
posts = api("GET", "wp/v2/posts?per_page=1&context=edit")
print(f"  Posts remaining: {len(posts) if posts else '?'}")

# --- Generate manual tasks checklist ---
print("\n=== Manuel im Dashboard erledigen ===")
print("""
1. Einstellungen > Lesen:
   - "Eine statische Seite anzeigen" auswählen
   - Startseite: Home (id=9)
   - Beitragsseite: Blog (id=11)

2. Erscheinungsbild > Menüs:
   Hauptmenü erstellen:
     - Home (/home/)
     - Blog (/blog/)
     - Über uns (/about/)
     - Kontakt (/contact/)
   Footer-Menü erstellen:
     - Impressum (/impressum/)
     - Datenschutz (/datenschutz/)
     - Cookies (/cookies/)

3. Kadence Customizer (Erscheinungsbild > Anpassen):
   Farben:
     - Primary: #6C5CE7
     - Secondary: #00B894
   Typografie:
     - Headings: Inter
     - Body: Source Sans Pro
   Layout:
     - Blog Grid 3-Spalten
     - Button Style: Rounded

4. Plugins installieren (Erscheinungsbild > Plugins > Hinzufügen):
   a) Complianz (Cookie Consent + DSGVO)
      - Nach Installation: Wizard durchlaufen
      - Cookie-Banner aktivieren
      - Kategorien: Notwendig, Analytik (falls später), Marketing (deaktiviert)
   
   b) Wordfence Security
      - Nach Installation: Setup Wizard kurz durch
   
   c) WPForms Lite (Kontaktformular)
      - Optional, falls du ein Formular statt nur E-Mail willst

5. Einstellungen > Datenschutz:
   - Seite "Datenschutzerklärung" -> /datenschutz/ zuweisen
""")

print("\n=== DONE ===")
