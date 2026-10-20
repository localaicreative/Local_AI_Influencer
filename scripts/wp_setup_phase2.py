#!/usr/bin/env python3
"""WP Setup Script — Pages, Categories, Settings für localaicreative.com"""
import json
import base64
import urllib.request
import urllib.error
import sys

BASE = "https://localaicreative.com/wp-json/wp/v2"
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
        print(f"  ERROR {e.code} on {path}: {e.read().decode()[:200]}")
        return None

# --- CATEGORIES ---
print("=== Kategorien erstellen ===")
for name, slug in [("Tutorials", "tutorials"), ("Projekte", "projekte"), ("Reviews", "reviews"), ("News", "news"), ("Guides", "guides")]:
    r = api("POST", "categories", {"name": name, "slug": slug})
    if r:
        print(f"  OK: {name}")

# --- PAGES ---
print("\n=== Seiten erstellen ===")

pages = {}

# HOME
home_content = """<!-- wp:group {"style":{"spacing":{"padding":{"top":"var:preset|spacing|80","bottom":"var:preset|spacing|80"}},"dimensions":{"minHeight":"60vh"}},"layout":{"type":"constrained"},"className":"hero-section"} -->
<div class="wp-block-group hero-section" style="min-height:60vh;padding-top:var(--wp--preset--spacing--80);padding-bottom:var(--wp--preset--spacing--80)"><!-- wp:heading {"level":1,"textAlign":"center","fontSize\":\"huge\"} -->
<h1 class="has-text-align-center has-huge-font-size">Local AI Creative</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center","style":{"typography":{"fontSize":"1.5rem"}}} -->
<p class="has-text-align-center" style="font-size:1.5rem">KI-gestützte Kreativität — lokal, privat, souverän.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link">Entdecke unsere Inhalte</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->"""

pages["home"] = api("POST", "pages", {
    "title": "Home",
    "slug": "home",
    "content": home_content,
    "status": "publish"
})
print(f"  Home: {'OK' if pages['home'] else 'FAIL'}")

# ABOUT
about_content = """<!-- wp:heading -->
<h2>Über Local AI Creative</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Local AI Creative ist ein Projekt, das sich mit der lokalen Nutzung von KI-Technologien für kreative Zwecke beschäftigt. Wir erforschen, dokumentieren und teilen Wissen über lokale LLMs, Stable Diffusion, ComfyUI und alles, was dazugehört.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Unsere Mission</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>KI muss nicht in der Cloud stehen. Wir zeigen, wie du mit lokaler Hardware — von Consumer-GPUs bis zu Workstations — eigene KI-Modelle betreibst, trainierst und für kreative Projekte nutzt. Privatsphäre, Kontrolle, Kreativität.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Was du hier findest</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul><li><strong>Tutorials:</strong> Schritt-für-Schritt Anleitungen für lokale KI-Setups</li><li><strong>Projekte:</strong> Unsere eigenen kreationen mit lokaler KI</li><li><strong>Reviews:</strong> Hardware, Software und Modell-Vergleiche</li><li><strong>Guides:</strong> Deep Dives in spezifische Themen</li></ul>
<!-- /wp:list -->"""

pages["about"] = api("POST", "pages", {
    "title": "Über uns",
    "slug": "about",
    "content": about_content,
    "status": "publish"
})
print(f"  Über uns: {'OK' if pages['about'] else 'FAIL'}")

# BLOG (placeholder — Kadence handles blog layout)
pages["blog"] = api("POST", "pages", {
    "title": "Blog",
    "slug": "blog",
    "content": "<!-- wp:paragraph -->\n<p>Alle Beiträge und Updates findest du hier.</p>\n<!-- /wp:paragraph -->",
    "status": "publish"
})
print(f"  Blog: {'OK' if pages['blog'] else 'FAIL'}")

# CONTACT (DSGVO-konform)
contact_content = """<!-- wp:heading -->
<h2>Kontakt</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Hast du Fragen, Ideen oder möchtest zusammenarbeiten? Schreib uns!</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>E-Mail:</strong> <a href="mailto:kontakt@localaicreative.com">kontakt@localaicreative.com</a></p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:paragraph {"fontSize":"small"} -->
<p class="has-small-font-size"><strong>Datenschutz-Hinweis:</strong> Durch das Absenden einer E-Mail an die oben genannte Adresse werden deine Angaben (Name, E-Mail-Adresse, Nachricht) an uns übermittelt und von uns gespeichert. Wir verwenden diese Daten ausschließlich zur Bearbeitung deiner Anfrage.</p>
<!-- /wp:paragraph -->"""

pages["contact"] = api("POST", "pages", {
    "title": "Kontakt",
    "slug": "contact",
    "content": contact_content,
    "status": "publish"
})
print(f"  Kontakt: {'OK' if pages['contact'] else 'FAIL'}")

# --- LEGAL PAGES (DSGVO) ---
print("\n=== Rechtliche Seiten ===")

datenschutz_content = """<!-- wp:heading -->
<h2>Datenschutzerklärung</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"fontSize":"small"} -->
<p class="has-small-font-size"><em>Stand: Juli 2026 — Diese Datenschutzerklärung ist ein Platzhalter und sollte durch eine rechtskonforme Fassung ersetzt werden.</em></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>1. Verantwortlicher</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Robert Korell<br>An der Schildwiese 94<br>38302 Wolfenbüttel<br>E-Mail: kontakt@localaicreative.com</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>2. Erhebung und Speicherung personenbezogener Daten</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Bei der Nutzung unserer Website werden automatisch Informationen vom Browser übermittelt und in Logfiles gespeichert:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>Browsertyp und -version</li><li>Verwendetes Betriebssystem</li><li>Referrer URL</li><li>IP-Adresse (anonymisiert)</li><li>Uhrzeit der Serveranfrage</li></ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Diese Daten werden nicht mit anderen Datenquellen zusammengeführt und nach 7 Tagen gelöscht.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>3. Cookies</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Diese Website verwendet nur technisch notwendige Cookies. Marketing- und Tracking-Cookies werden nicht eingesetzt. Ihre Einwilligung zu Cookies wird über einen Cookie-Banner eingeholt und kann jederzeit widerrufen werden.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>4. Rechte der betroffenen Personen</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch gemäß Art. 15-21 DSGVO.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>5. WordPress</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Diese Website wird durch WordPress betrieben. WordPress ist ein Open-Source-CMS, das auf einem Server in Deutschland gehostet wird. Es werden keine Daten an Dritte übermittelt.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>6. Änderungen dieser Datenschutzerklärung</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Wir behalten uns vor, diese Datenschutzerklärung anzupassen, um sie den aktuellen gesetzlichen Anforderungen oder Änderungen unserer Dienste anzupassen.</p>
<!-- /wp:paragraph -->"""

pages["datenschutz"] = api("POST", "pages", {
    "title": "Datenschutzerklärung",
    "slug": "datenschutz",
    "content": datenschutz_content,
    "status": "publish"
})
print(f"  Datenschutz: {'OK' if pages['datenschutz'] else 'FAIL'}")

impressum_content = """<!-- wp:heading -->
<h2>Impressum</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3>Angaben gemäß § 5 TMG</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Robert Korell<br>An der Schildwiese 94<br>38302 Wolfenbüttel</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Kontakt</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>E-Mail: kontakt@localaicreative.com</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Robert Korell<br>An der Schildwiese 94<br>38302 Wolfenbüttel</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:paragraph {"fontSize":"small"} -->
<p class="has-small-font-size"><strong>Haftungsausschluss:</strong> Die Inhalte dieser Website wurden mit größtmöglicher Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen.</p>
<!-- /wp:paragraph -->"""

pages["impressum"] = api("POST", "pages", {
    "title": "Impressum",
    "slug": "impressum",
    "content": impressum_content,
    "status": "publish"
})
print(f"  Impressum: {'OK' if pages['impressum'] else 'FAIL'}")

cookies_content = """<!-- wp:heading -->
<h2>Cookie-Richtlinie</h2>
<!-- /wp:heading -->

<!-- wp:paragraph {"fontSize":"small"} -->
<p class="has-small-font-size"><em>Stand: Juli 2026</em></p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Was sind Cookies?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Cookies sind kleine Textdateien, die auf Ihrem Endgerät gespeichert werden. Sie helfen uns, die Website bedarfsgerecht zu gestalten und sicher zu betreiben.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Welche Cookies verwenden wir?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Technisch notwendige Cookies:</strong></p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li>WordPress-Sessions (Authentifizierung)</li><li>Cookie-Einwilligungs-Status</li><li>CSRF-Token (Sicherheit)</li></ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Diese Cookies sind für den Betrieb der Website erforderlich und werden ohne Ihre Einwilligung gesetzt.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Ihre Rechte</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Sie können Ihre Cookie-Einstellungen jederzeit über den Cookie-Banner auf unserer Website ändern oder Cookies in Ihren Browsereinstellungen deaktivieren.</p>
<!-- /wp:paragraph -->"""

pages["cookies"] = api("POST", "pages", {
    "title": "Cookie-Richtlinie",
    "slug": "cookies",
    "content": cookies_content,
    "status": "publish"
})
print(f"  Cookies: {'OK' if pages['cookies'] else 'FAIL'}")

# --- SETTINGS: Static Front Page ---
print("\n=== WordPress Einstellungen ===")

if pages["home"] and pages["blog"]:
    # Set page_on_front and page_for_posts via options API
    api("PUT", f"options/1", {"value": pages["home"]["id"]})  # page_on_front is usually option id 1
    api("PUT", f"options/2", {"value": pages["blog"]["id"]})   # page_for_posts is usually option id 2
    
    # Check what options we actually have
    opts = api("GET", "options?context=edit")
    if opts:
        for o in (opts if isinstance(opts, list) else [opts]):
            name = o.get('option_name', '')
            if 'page' in name.lower() or 'show_on_front' in name.lower():
                print(f"  {name}: {o.get('value')}")

print("\n=== DONE ===")
print("Erstellte Seiten:")
for k, v in pages.items():
    status = f"id={v['id']}" if v else "FEHLGESCHLAGEN"
    print(f"  {k}: {status}")
