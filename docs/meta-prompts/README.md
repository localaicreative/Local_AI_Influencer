# Meta-Prompts — Local AI Influencer Content Pipeline

Diese Meta-Prompts steuern den autonomen Content-Workflow. Jeder ist ein selbststaendiges Dokument, das Lena als Instruktion folgt.

## Ueberblick

```
TREND RESEARCH (woechentlich)          CONTENT FACTORY (bei Freigabe)
┌─────────────────────┐               ┌──────────────────────┐
│ Quellen durchsuchen │               │ Input: Thema +       │
│ r/LocalLLaMA        │               │ Kategorie            │
│ Hacker News         │               ├──────────────────────┤
│ HuggingFace Blog    │               │ 1. Recherchefahrplan │
│ Lil'Log RSS         │               │ 2. Blogartikel       │
├─────────────────────┤               │ 3. Insta Carousel    │
│ Must-Have Filter    │               │ 4. Insta Single Post │
│ (4 Kriterien)       │               │ 5. Bob vorlegen      │
├─────────────────────┤               └──────────────────────┘
│ Top 3-5 Kandidaten  │
│ an Bob vorlegen     │
└─────────────────────┘
         │
         │ Bob freigibt Thema
         ▼
   Trigger Content Factory
```

## Dateien

| Datei | Zweck | Trigger |
|-------|-------|---------|
| `trend-research.md` | Woechentliche Trend-Recherche + Topic-Auswahl | Manuel oder Cronjob (montags 10 Uhr) |
| `content-factory.md` | Blogartikel + Insta-Derivate aus freigegebenem Thema | Nach Bob's Freigabe eines Topics |

## Nutzung

### Manuel

```bash
# Trend-Recherche starten:
hermes --profile lena-intimate chat -q '/goal "Lies docs/meta-prompts/trend-research.md und fuehre die woechentliche Recherche aus."'

# Content fuer ein Thema erstellen:
hermes --profile lena-intimate chat -q '/goal "Lies docs/meta-prompts/content-factory.md. Erstelle Content fuer: [THEMA]. Kategorie: [KATEGORIE]."'
```

### Als Cronjob (Trend Research)

```bash
# Woechentlich montags um 10 Uhr:
hermes cron add \
  --schedule "0 10 * * 1" \
  --prompt "$(cat docs/meta-prompts/trend-research.md)" \
  --name "Local AI Influencer: Trend Research"
```

## Output-Pfade

```
docs/research/                    ← Rohdaten + Topic-Vorschlaege
content/web/llm-guides/hardware/  ← Blogartikel (Hardware)
content/web/llm-guides/model-reviews/  ← Blogartikel (Model Reviews)
content/web/llm-guides/setup-tutorials/    ← Blogartikel (Tutorials)
content/web/llm-guides/use-cases/     ← Blogartikel (Use Cases)
```

Jeder Blogartikel hat optionale Insta-Derivate im gleichen Verzeichnis:
- `[slug]-insta-carousel.md` -- Carousel-Slides + Caption
- `[slug]-insta-single.md` -- Single Post + Bild-Konzept

## Optimierung

Beide Meta-Prompts haben eine Versionsnummer am Ende. Bei Aenderungen:
1. Datei direkt editieren
2. Versionsnummer erhoehen
3. Kurze Notiz was sich geaendert hat (am Ende der Datei)
