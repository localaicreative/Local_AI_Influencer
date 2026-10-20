#!/usr/bin/env python3
"""Create first blog post for localaicreative.com"""
import json
import base64
import urllib.request
import urllib.error

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
        print(f"  ERROR {e.code}: {e.read().decode()[:200]}")
        return None

# Get categories
cats = api("GET", "wp/v2/categories?per_page=50")
cat_map = {c['slug']: c['id'] for c in cats}
print(f"Categories: {cat_map}")

post_content = """<!-- wp:paragraph -->
<p>In einer Welt, in der KI-Dienste immer mehr in die Cloud wandern, vergessen wir leicht eine einfache Wahrheit: <strong>KI muss nicht bei Google, OpenAI oder Microsoft laufen.</strong> Mit moderner Consumer-Hardware kannst du leistungsfähige KI-Modelle direkt auf deinem eigenen Rechner betreiben — privat, kontrolliert und unabhängig.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Warum lokale KI?</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul><li><strong>Datenschutz:</strong> Deine Daten verlassen nie dein Gerät. Keine Telemetrie, keine Tracking-Pixel, keine unbekannten Third-Party-Services.</li><li><strong>Kontrolle:</strong> Du entscheidest, welche Modelle du lädst, wie sie konfiguriert sind und was mit den Ergebnsten passiert.</li><li><strong>Keine Abos:</strong> Einmal Hardware gekauft — für immer KI nutzen. Keine monatlichen Gebühren pro Token oder API-Call.</li><li><strong>Lernwert:</strong> Wer lokale KI betreibt, versteht, wie sie wirklich funktioniert. Kein Black Box Thinking mehr.</li></ul>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2>Was brauchst du?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Die Hürden sind niedriger als du denkst. Du brauchst:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul><li><strong>Eine GPU mit mindestens 8 GB VRAM</strong> (NVIDIA empfohlen, AMD wird besser)</li><li><strong>Ein Linux-System</strong> (Ubuntu, Pop!_OS, Fedora — alles funktioniert)</li><li><strong>Grundlegendes Terminal-Wissen</strong> (git clone, python3, pip)</li></ul>
<!-- /wp:list -->

<!-- wp:heading {"level":2} -->
<h2>Dein erster Stack</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Hier ist ein bewährter Einstiegspunkt für lokale KI:</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns"><!-- wp:column {"width":"50%"} -->
<div class="wp-block-column" style="flex-basis:50%"><!-- wp:heading {"level":3} -->
<h3>Text-KI (LLM)</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>LM Studio</strong> oder <strong>Ollama</strong> — beides bringt dir eine lokale Chat-Oberfläche mit einem Klick. Modelle wie Qwen 3.6 35B laufen flüssig auf einer RTX 3090.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column {"width":"50%"} -->
<div class="wp-block-column" style="flex-basis:50%"><!-- wp:heading {"level":3} -->
<h3>Bild-KI (Image Generation)</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Stable Diffusion WebUI</strong> oder <strong>ComfyUI</strong> — erzeuge Bilder, Illustrationen und Kunstwerke lokal. Mit Modellen wie SDXL, Flux oder Ideogram 4.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:heading {"level":2} -->
<h2>Der erste Schritt</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Du musst nicht alles auf einmal machen. Starte klein:</p>
<!-- /wp:paragraph -->

<!-- wp:orderedList -->
<ol><li>Installiere <strong>Ollama</strong> (<code>curl -fsSL https://ollama.com/install.sh | sh</code>)</li><li>Zieh dir ein Modell: <code>ollama run qwen3.6:35b</code></li><li>Probiere es aus — schreibe, frage, experimentiere</li></ol>
<!-- /wp:orderedList -->

<!-- wp:paragraph -->
<p>Schon hast du deine erste lokale KI am Laufen. Kein Account, kein Abo, keine Cloud.</p>
<!-- /wp:paragraph -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:quote -->
<blockquote><p>Lokale KI ist nicht nur eine technische Entscheidung — es ist eine Haltung. Die Haltung, dass Kreativität und Intelligenz gehören denen, die sie nutzen, nicht den Servern, auf denen sie hosten.</p></blockquote>
<!-- /wp:quote -->

<!-- wp:paragraph -->
<p>In den kommenden Wochen zeigen wir hier Schritt für Schritt, wie du deinen lokalen KI-Stack aufbaust — von der Hardware-Auswahl über Modell-Optimierung bis hin zu autonomen Workflows. Bleib dran.</p>
<!-- /wp:paragraph -->"""

post_data = {
    "title": "Lokale KI betreiben — Dein erster Schritt zur digitalen Souveränität",
    "slug": "lokale-ki-betreiben-erster-schritt-digitale-souveranitat",
    "content": post_content,
    "status": "publish",
    "categories": [cat_map.get('guides', 1), cat_map.get('news', 1)],
    "excerpt": "KI muss nicht in der Cloud stehen. Mit moderner Hardware betreibst du leistungsfähige Modelle privat und unabhängig — hier ist dein Einstieg.",
}

result = api("POST", "wp/v2/posts", post_data)
if result:
    print(f"Post created: id={result['id']}, slug={result['slug']}")
    print(f"URL: https://localaicreative.com/{result['slug']}/")
else:
    print("FAILED to create post")
