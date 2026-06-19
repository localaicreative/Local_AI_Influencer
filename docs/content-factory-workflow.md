# Content Factory — Vom Research-Signal zum Blogartikel

## Pipeline Uebersicht

```
Phase 1: RESEARCH (automatisch, 3x taeglich)
    Cronjobs → run_research.py → Notes in _inbox/DATE/
    [EXISTIERT]

Phase 2: CURATION (manuell oder woechentlich automatisch)
    curate_inbox.py → Topic Clusters + Blog-Vorschlaege
    [EXISTIERT, Entity Extraction gerade gefixt]

Phase 3: DRAFT GENERATION (Content Factory — NEU)
    content_factory.py → Blog Drafts aus Research Notes
    [WIRD JETZT GEBAUT]

Phase 4: REVIEW GATE (Bob entscheidet)
    Bob liest Drafts → edit/approve/reject
    [MANUELL]

Phase 5: PUBLISH (automatisch nach Approval)
    wp_publish.py → WordPress REST API → Live oder Draft
    [WIRD JETZT GEBAUT]
```

## Verzeichnisstruktur

```
Local_AI_Influencer/
├── research-vault/
│   ├── _inbox/                    ← Roh-Signale (auto)
│   │   ├── 2026-06-19/            ← Datum-basiert
│   │   └── curation_2026-06-19.md ← Curator-Report
│   ├── knowledge/                 ← Kuratiertes Wissen
│   ├── trends/                    ← Manuelle Deep-Dive Notes
│   └── _scripts/                  ← Pipeline Scripts
├── blog-drafts/                   ← Generierte Blogartikel (NEU)
│   ├── 01-claude-mind-interpreter.md
│   └── 02-glm-fable-local-ai-win.md
├── scripts/
│   ├── content_factory.py         ← Draft Generator (NEU)
│   └── wp_publish.py              ← WordPress Publisher (NEU)
└── docs/
    └── content-factory-workflow.md ← Dieses Dokument
```

## Content Factory: Wie es funktioniert

### Input
- Curated Topic Cluster aus `curate_inbox.py`
- Alle zugehoerigen Research Notes mit Content
- Blog-Kategorie-Vorschlag (Model Spotlight, Opinion Piece, etc.)

### Prozess
1. **Notes sammeln:** Alle Notes im Cluster laden
2. **Content extrahieren:** Zusammenfassungen, Quellen, Fakten
3. **Struktur waehlen:** Template basierend auf Kategorie
4. **Draft schreiben:** AI-generierter Artikel mit:
   - Frontmatter (title, slug, tags, sources)
   - Einleitung mit Hook
   - Hauptteil mit Fakten + Kontext
   - Fazit mit Local AI Relevanz
5. **Qualitaetscheck:** Mindestens 2 Quellen, Hardware-Kontext, keine Hype-Claims ohne Validierung

### Output
- Markdown Datei in `blog-drafts/`
- Frontmatter mit Metadaten fuer WordPress
- Status: `draft` (wartet auf Bob's Review)

## WordPress Publishing

### API Endpunkte
```
POST /wp-json/wp/v2/posts          ← Neuen Post erstellen
PUT  /wp-json/wp/v2/posts/{id}     ← Existierenden Post aktualisieren
GET  /wp-json/wp/v2/posts?status=draft ← Alle Drafts lesen
```

### Mapping: Markdown Frontmatter → WordPress Fields
| Markdown | WordPress |
|----------|-----------|
| title    | title.rendered |
| slug     | slug |
| category | categories (ID lookup) |
| tags     | tags |
| status   | status (draft/publish) |
| content  | content.rendered (Markdown → HTML via markdown2) |

### Kategorien (WordPress IDs muessen ermittelt werden)
- research-spotlight
- trend-analysis
- hardware-guide
- opinion-piece
- practical-guide

## Automatisierung: Wann was passiert?

| Trigger | Aktion | Frequenz |
|---------|--------|----------|
| Cron Research | Notes in _inbox/ | 3x taeglich (11/16/21 Uhr) |
| Manuelles Kommando | curate_inbox.py → Blog-Vorschlaege | On-demand |
| Manuelles Kommando | content_factory.py → Draft aus Cluster | On-demand |
| Bob's Approval | wp_publish.py → WordPress | On-demand |

**Wichtig:** Content-Erstellung bleibt MANUELL getriggert (Modell B).
Bob entscheidet WAS blog-wuerdig ist. Die Factory hilft nur beim Schreiben.

## TODO / Offene Punkte

- [ ] content_factory.py implementieren (AI-generierte Drafts aus Research Notes)
- [ ] wp_publish.py implementieren (WordPress REST API Integration)
- [ ] WordPress Kategorie-IDs ermitteln und mappen
- [ ] Markdown → HTML Konfiguration (markdown2 oder similar)
- [ ] Inbox Routing fixen: run_research.py soll in _inbox/ schreiben, nicht trends/
- [ ] Woechentlicher Curation Cronjob? (Sonntag 10 Uhr?)
