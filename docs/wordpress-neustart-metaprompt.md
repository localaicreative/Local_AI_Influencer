# WordPress localaicreative.com — Neustart Metaprompt

## Kontext
Frische WordPress-Installation auf `localaicreative.com` (nur "Hello world!" Post vorhanden).
Ziel: Kompletter Neustart mit neuem Theme, professionellem Design, und DSGVO/TTDSG-Konformität.

## API-Zugang
- Endpoint: `https://localaicreative.com/wp-json/wp/v2/`
- User: `Hermes Lena`, Email: `localaicreative@gmail.com`
- Passwort: `HG$j1o^FbULX59E^tHqvkWd5`
- App-Passwort: `M9vl nvFs NgHs oinO mBH7 XVJ7`

---

## PHASE 1: Theme & Design

### 1.1 Theme Installation
**Empfohlenes Theme:** Kadence WP (kostenlos)
- Installiere via REST API oder wegzugriff
- Aktiviere als Standard-Theme

### 1.2 Design-Konzept "Local AI Creative"

**Farbschema:**
- Primary: `#6C5CE7` (Lila/Akzent — kreativ, tech-nah)
- Secondary: `#00B894` (Grün/CTA — positiv, aktiv)
- Background Light: `#FAFAFA`
- Background Dark: `#1A1A2E`
- Text Primary: `#2D3436`
- Text Secondary: `#636E72`

**Typografie:**
- Headings: Inter (Google Fonts, lokal gehostet für DSGVO)
- Body: Source Sans Pro oder System-Stack
- Code/Mono: JetBrains Mono

**Layout:**
- Header: Logo links, Navigation rechts, Dark/Light Toggle
- Hero Section: Großer Titel "Local AI Creative" + Subtitle + CTA Button
- Blog Grid: 3-Spalten auf Desktop, Karten mit Featured Image
- Footer: 3-Spalten (Über uns, Links, Kontakt) + Copyright

**Design-Prinzipien:**
- Clean, modern, viel Whitespace
- Subtile Animationen (hover effects, fade-in)
- Mobile-first responsive
- Performance: Lazy Loading, optimierte Bilder

### 1.3 Customizer Einstellungen (via REST API / WP-CLI wenn verfügbar)
```
Theme Mods:
- header_layout: logo-left-nav-right
- blog_layout: grid-3-col
- colorscheme: light-with-dark-toggle
- typography_heading: Inter
- typography_body: Source Sans Pro
- button_style: rounded
- accent_color: #6C5CE7
- secondary_color: #00B894
```

---

## PHASE 2: Seitenstruktur

### 2.1 Pflichtseiten erstellen (via REST API)

**Startseite (Home)**
- Slug: `home`
- Template: Full-width hero + Blog Grid
- Content: Hero Section mit Titel, Subtitle, CTA "Entdecke unsere Inhalte"
- Setze als statische Startseite

**Über uns (About)**
- Slug: `about`
- Content: Wer wir sind, Mission, was Local AI Creative bedeutet
- Platzhalter-Text der später angepasst wird

**Blog**
- Slug: `blog`
- Template: Blog Grid Layout
- Setze als Beitragsseite

**Kontakt**
- Slug: `contact`
- Content: Kontaktformular (DSGVO-konform, siehe Phase 3)
- Keine externen Services

### 2.2 Kategorien/Taxonomien
Erstelle initiale Kategorien:
- Tutorials
- Projekte
- Reviews
- News
- Guides

---

## PHASE 3: DSGVO/TTDSG Konformität

### 3.1 Pflichtseiten (Rechtliches)
**Datenschutzerklärung**
- Slug: `datenschutz`
- Content: Vollständige DSGVO-konforme Datenschutzerklärung
- Muss enthalten: Verantwortlicher, Datenverarbeitungszwecke, Rechtsgrundlagen, Betroffenenrechte, Cookies, externe Services
- Link im Footer

**Impressum**
- Slug: `impressum`
- Content: TMG/RSGB konformes Impressum
- Platzhalter für Name, Adresse, Kontakt (Bob muss ausfüllen)
- Link im Footer

**Cookie-Einwilligung**
- Slug: `cookies`
- Content: Cookie-Richtlinie mit Übersicht aller verwendeten Cookies

### 3.2 Technische DSGVO-Maßnahmen

**A. Google Fonts lokal hosten**
```css
/* NICHT von Google CDN laden */
/* Stattdessen: Font-Dateien auf Server hochladen und via @font-face referenzieren */
@font-face {
  font-family: 'Inter';
  src: url('/wp-content/themes/kadence/assets/fonts/inter.woff2') format('woff2');
}
```

**B. Cookie-Banner einrichten**
- Nutze Kadence Built-in Cookie Banner ODER Plugin "Complianz" (kostenlos)
- Kategorien: Notwendig, Analytik, Marketing
- Blockiere nicht-notwendige Scripts bis Einwilligung
- Consent muss protokolliert werden

**C. Externe Services prüfen und entfernen/blockieren**
```
Muss entfernt/geblockt werden:
- Google Analytics → ersetzen mit Matomo (self-hosted) oder Plausible
- Google Fonts CDN → lokal hosten (siehe oben)
- YouTube Embeds → nutzen nur mit Privacy-Mode (nocookie)
- Social Media Plugins → entfernen, nutze statische Links statt Widgets
- Gravatar → deaktivieren oder ersetzen mit lokalen Avataren

WordPress Core prüfen:
- Emojis Script entfernen (wp-deregister-script 'wp-emoji-release')
- REST API nonce hardening
- XML-RPC deaktivieren wenn nicht benötigt
```

**D. Kontaktformular DSGVO-konform**
- Nutze WPForms Lite ODER Contact Form 7 mit DSGVO-Erweiterung
- Checkbox für Datenschutzerklärung (Pflichtfeld)
- Keine Daten an Dritte weiterleiten
- Server-seitige Validierung

### 3.3 Privacy Settings in WordPress
```
Einstellungen → Datenschutz:
- Seite "Datenschutzerklärung": verlinken auf /datenschutz/
- Seite "Impressum": verlinken auf /impressum/
- Tools → Datenexport/Datenlöschung Seiten konfigurieren
```

### 3.4 .htaccess / Server Security Headers
```apache
# Privacy & Security Headers
Header set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set Permissions-Policy "geolocation=(), microphone=(), camera=()"
```

---

## PHASE 4: Plugins (DSGVO-konform ausgewählt)

### Empfohlene Plugins
1. **Kadence Blocks** — Gutenberg Extensions (kein Tracking)
2. **Complianz** oder **Borlabs Cookie** — DSGVO Cookie Consent
3. **WPForms Lite** — DSGVO-konforme Formulare
4. **Wordfence Security** — Firewall + Malware Scan
5. **UpdraftPlus** — Backups (lokal speichern)
6. **Autoptimize** oder **WP Rocket** — Performance/Caching

### Verbotene Plugins (DSGVO-Problematisch)
- Yoast SEO (sendet Daten an Yoast Cloud) → nutze Rank Math statt
- MonsterInsights / SiteKit by Google → sendet an Google
- Jetpack → sendet an WordPress.com/automattic
- Social Media Share Plugins mit Tracking

---

## PHASE 5: Navigation & Footer

### Hauptnavigation
```
Home | Blog | Über uns | Kontakt
```

### Footer Links
```
© 2026 Local AI Creative | Impressum | Datenschutz | Cookies
```

---

## EXECUTION PLAN (Schritt-für-Schritt)

1. [ ] Theme Kadence installieren & aktivieren
2. [ ] Customizer: Farben, Typografie, Layout konfigurieren
3. [ ] Pflichtseiten erstellen (Home, About, Blog, Kontakt)
4. [ ] Kategorien anlegen
5. [ ] Rechtliche Seiten erstellen (Datenschutz, Impressum, Cookies)
6. [ ] Cookie-Banner einrichten & konfigurieren
7. [ ] Google Fonts lokal hosten / externe Scripts entfernen
8. [ ] Plugins installieren (DSGVO-konforme Auswahl)
9. [ ] Navigation & Footer konfigurieren
10. [ ] Security Headers setzen
11. [ ] Finale Prüfung: Seite auf DSGVO-Konformität testen

---

## WICHTIGE HINWEISE FÜR DIE AUSFÜHRUNG

- **Vor jeder Änderung:** Backup des aktuellen Zustands (auch wenn nur Hello World)
- **API-Auth:** Nutze Application Passwords für REST API Calls
- **Testen:** Jede Phase nach Abschluss testen (Seite aufrufen, Console prüfen)
- **Platzhalter:** Rechtliche Texte sind PLATZHALTER — Bob muss diese mit echten Daten ausfüllen lassen (Anwalt/Rechtsberatung empfohlen)
- **Performance:** Nach jedem Plugin installieren: Seite auf Performance-Einbußen prüfen
