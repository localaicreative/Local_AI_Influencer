# Local AI Influencer 🤖✨

## Projekt-Konzept

**Local AI Influencer** ist eine automatisierte Content-Maschine für KI-gestützte Kreativprojekte. Das Ziel: Projekte dokumentieren, als Anleitungen veröffentlichen und als Ebooks monetarisieren — mit minimal manuellem Aufwand.

### Kernprinzipien

1. **Bob liefert die Idee** → Konzept, Richtung, Entscheidungen
2. **Lena baut das Gerüst** → Dokumentation, Struktur, Automatisierung
3. **Maschine macht die Arbeit** → Templates, Skripte, Workflows
4. **Content = Produkt** → Jede Projekt-Doku wird zum Freebie oder Ebook

### Was wir bauen

- **Webseite** (GitHub Pages) — Portfolio + Anleitungen als Content-Hub
- **Ebooks** — Premium-Versionen der Tutorials (Gumroad/LemonSilo)
- **Influencer-Pipeline** — Outreach, Kooperationen, Social Proof
- **Projekt-Templates** — Wiederverwendbare Gerüste für neue Projekte

### Zielgruppe

- Eltern die personalisierte Kinderbücher erstellen wollen
- KI-Creator die ComfyUI/SD WebUI lernen möchten
- Fitness-Enthusiasten die AI-gestützte Tools nutzen wollen
- Influencer die Kooperationen suchen

---

## Roadmap

### Phase 1: Fundament (Woche 1-2)

**Ziel:** Infrastruktur steht, erste Seite ist live.

```
├── [ ] Git-Account & Repo strukturieren
│   ├── Repository anlegen
│   ├── GitHub Pages aktivieren
│   └── Basis-Theme wählen (Astro/Jekyll/Hugo?)
├── [ ] Domain & Branding
│   ├── Name der Seite entscheiden
│   ├── Domain registrieren (.com/.de)
│   └── Logo/Identität skizzieren
└── [ ] Seiten-Gerüst
    ├── Landing Page (Über uns, Projekte)
    ├── Projekt-Template (wiederverwendbar)
    └── Kontakt/Impressum
```

**Entscheidungen die Bob treffen muss:**
- Repo-Name & Account
- Seiten-Name/Branding
- Theme-Wahl

---

### Phase 2: Kinderbuch als Lead-Projekt (Woche 3-5)

**Ziel:** Erstes Projekt dokumentiert, Webseite befüllt.

```
├── [ ] Content erstellen
│   ├── "So haben wir ein personalisiertes Kinderbuch gemacht"
│   ├── ComfyUI-Illustrations-Tutorial (Schritt-für-Schritt)
│   └── Prozess-Dokumentation mit Vorher/Nachher
├── [ ] Webseite befüllen
│   ├── Projektseite: Torge & Samson
│   ├── Galerie der Illustrationen
│   └── Download/Anleitung als Freebie
└── [ ] Ebook-Vorbereitung
    ├── Anleitung strukturieren (Markdown → PDF/ePub)
    ├── Cover-Design generieren
    └── Plattform wählen (Gumroad? LemonSilo?)
```

**Entscheidungen die Bob treffen muss:**
- Welche Details sind öffentlich teilbar? (Namen, Gesichter?)
- Ebook-Preis
- Plattform-Wahl

---

### Phase 3: Influencer-Strategie (Woche 4-6)

**Ziel:** Outreach-Pipeline läuft, erste Kontakte initiiert.

```
├── [ ] Ziel definieren
│   ├── Zielgruppe festlegen (Eltern? Creator? KI-Enthusiasten?)
│   └── Angebot klar formulieren (Co-Creation? Gastbeiträge?)
├── [ ] Outreach-Material
│   ├── Media Kit / One-Pager erstellen
│   ├── Kooperation-Vorschlag (Template)
│   └── Beispiel-Content kuratieren
└── [ ] Pipeline aufbauen
    ├── Liste potenzieller Influencer erstellen
    ├── Kontakt-Strategie definieren (DM? Email?)
    └── Tracking-System einrichten
```

**Entscheidungen die Bob treffen muss:**
- Wer ist die Zielgruppe?
- Was ist das konkrete Angebot?
- Welche Influencer kontaktieren?

---

### Phase 4: Monetarisierung & Skalierung (Woche 6+)

**Ziel:** Erstes Ebook live, weitere Projekte in der Pipeline.

```
├── [ ] Ebook veröffentlichen
│   ├── Launch auf Webseite + Social Media
│   └── Feedback sammeln & iterieren
├── [ ] Weitere Projekte hinzufügen
│   ├── Workout-App Tutorial
│   ├── BesorgEsLena → Kindersoftware-Konzepte
│   └── Creative Vault (wenn relevant)
└── [ ] Automatisierung
    ├── Newsletter einrichten?
    ├── SEO optimieren
    └── Analytics + Tracking
```

---

## Projekt-Struktur

```
Local_AI_Influencer/
├── README.md              ← Du bist hier
├── docs/                  ← Konzept-Dokumente, Meeting Notes
│   └── roadmap.md         ← Detaillierte Roadmap (später)
├── content/               ← Content für Webseite + Ebooks
│   ├── web/               ← Webseiten-Artikel (Markdown)
│   └── ebooks/            ← Ebook-Manuskripte
├── ebooks/                ← Fertige Ebooks (PDF/ePub)
├── templates/             ← Wiederverwendbare Templates
│   ├── project.md         ← Projekt-Template
│   ├── tutorial.md        ← Tutorial-Template
│   └── outreach-email.md  ← Influencer-Kontakt Template
├── scripts/               ← Automatisierungsskripte
│   ├── build-ebook.py     ← Markdown → PDF/ePub Konverter
│   └── deploy.sh          ← GitHub Pages Deploy
└── assets/                ← Bilder, Logos, Cover
```

---

## Metaprompt: Projekt-Gerüst Generator

**Zweck:** Aus einer Projekt-Idee automatisch das komplette Gerüst erstellen.

**Input von Bob:**
- Projektname
- Kurzbeschreibung (1-2 Sätze)
- Zielgruppe
- Deliverables (Webseite? Ebook? Beides?)

**Output von Lena:**
```
1. Konzept-Dokument (docs/PROJECT.md)
   ├── Problem & Lösung
   ├── Zielgruppe
   ├── Content-Plan
   └── Timeline

2. Webseite-Skelett (content/web/)
   ├── Landing Page Draft
   ├── Projektseite Template
   └── SEO Meta-Tags

3. Ebook-Gerüst (ebooks/)
   ├── Kapitel-Struktur
   ├── Cover-Briefing für SD/ComfyUI
   └── Preis-Empfehlung

4. Influencer-Paket (templates/)
   ├── Media Kit Outline
   ├── Outreach Email Drafts
   └── Hashtag/Vorschlag-Liste

5. Automatisierung (scripts/)
   ├── Build-Skript für dieses Projekt
   └── Deploy-Konfiguration
```

**Trigger:** `/project [Name] [Beschreibung]`

---

## Offene Fragen

| Frage | Status | Entscheidung |
|-------|--------|--------------|
| Git-Account & Repo-Name | Offen | |
| Seiten-Name/Branding | Offen | |
| Domain (.com/.de) | Offen | |
| Kinderbuch: Öffentlich teilbar? | Offen | |
| Ebook-Plattform | Offen | |
| Influencer-Zielgruppe | Offen | |

---

## Automatisierungs-Level

**Was automatisch läuft:**
- ✅ Gerüst-Erstellung aus Metaprompt
- ✅ Template-basierte Dokumentation
- ✅ Markdown → PDF/ePub Konvertierung
- ✅ GitHub Pages Deploy
- ✅ SEO Meta-Tags generieren

**Was Bob entscheidet:**
- 🎯 Projekt-Ideen & Richtung
- 🎯 Content-Freigabe (was geht öffentlich?)
- 🎯 Preise & Plattformen
- 🎯 Influencer-Auswahl & Outreach

---

*Erstellt: 2026-06-15 | Status: Phase 1 — Fundament*
