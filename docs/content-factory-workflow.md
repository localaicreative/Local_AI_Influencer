# Content Factory Workflow — Dokumentation

**Letzte Aktualisierung:** 2026-06-20
**Status:** Live mit 3 Blog-Artikeln

---

## Pipeline-Uebersicht

```
[Research Cronjobs] → [Inbox] → [Curation] → [Knowledge] → [Blog Drafts] → [GitHub Pages]
     3x taeglich         _inbox/    Sonntag       knowledge/    blog-drafts/    Auto-Build
   (11/16/21 Uhr)   YYYY-MM-DD/   10 Uhr        (auto)        (manuell)      bei Push
```

## Komponenten

### 1. Research Collection (3x taeglich)

**Cronjobs:**
- `ade9c348ea01` — 11:00 Uhr
- `768b7978d086` — 16:00 Uhr
- `e168947ee1d3` — 21:00 Uhr

**Script:** `research-vault/_scripts/run_research.py`

**Quellen:**
- YouTube RSS (Two Minute Papers, AI Explained)
- GitHub Trending (lokale LLM Repos)
- HuggingFace Trending Models
- Reddit RSS (r/LocalLLaMA Top)

**Output:** `_inbox/YYYY-MM-DD/*.md` mit Frontmatter:
```yaml
created: 2026-06-20
source-type: Video|Community|Model|Code
attention-score: 18-50
blog-potential: low|medium|high
url: https://...
```

### 2. Inbox Router (Legacy)

**Script:** `research-vault/_scripts/inbox_router.py`

Verschiebt alte Notes aus `trends/` nach `_inbox/YYYY-MM-DD/` und berechnet fehlende Attention Scores. Einmalig notwendig fuer bestehende Daten — neue Notes landen direkt im Inbox.

### 3. Auto-Curation (woechentlich)

**Cronjob:** `a0006c3cd5c6` — Sonntag 10:00 Uhr

**Script:** `research-vault/_scripts/curate_inbox.py`

Scannt `_inbox/DATE/*.md`, clustert nach Topics, generiert Blog-Vorschlaege.

**Output:** `_inbox/curation_YYYY-MM-DD.md` mit:
- Topic Clusters (Notes gruppiert nach Entity)
- Blog-Vorschlaege (Top 5 nach Score sortiert)
- Kategorie-Zuordnung (Model Spotlight, Hardware Guide, Opinion Piece, etc.)

### 4. Knowledge Migration (manuell oder auto)

**Script:** `research-vault/_scripts/migrate_to_knowledge.py`

Verschiebt hochbewertete Notes (_inbox/) nach `knowledge/` mit Synthese.

**Auto-Kriterien:**
- Max Score >= 35pts
- Oder >= 2 Notes zum gleichen Topic mit Avg >= 25pts
- Oder Blog-Potenzial: medium/high

**Output:** `knowledge/{models|topics|hardware|use-cases}/SLUG.md`

### 5. Blog Draft Generation (manuell)

**Workflow:**
1. Auto-Curation liefert Top-Themen
2. Bob waehlt Topic
3. Lena schreibt Draft basierend auf Knowledge Notes + Inbox Sources
4. Draft landet in `blog-drafts/NN-titel.md`
5. Bob reviewt → "Ja, push" oder "Nein, anders"

**Kein Auto-Push!** Modell B — Bob behaelt Kontrolle.

### 6. Site Build & Deploy (automatisch)

**Script:** `scripts/build_site.py`

**GitHub Actions:** `.github/workflows/pages.yml`
- Triggert bei Push auf main (paths: blog-drafts/, scripts/build_site.py)
- Baut Markdown zu HTML
- Deployt nach GitHub Pages

**Live:** https://localaicreative.github.io/Local_AI_Influencer/

---

## Dateistruktur

```
research-vault/
├── _scripts/
│   ├── run_research.py      ← Research Collection (3x taeglich)
│   ├── inbox_router.py       ← Legacy: trends/ → _inbox/
│   ├── curate_inbox.py       ← Curation + Blog-Vorschlaege
│   └── migrate_to_knowledge.py ← Inbox → Knowledge Migration
├── _inbox/
│   ├── 2026-06-20/           ← Taeliche Notes (YYYY-MM-DD)
│   │   ├── deepseek-*.md
│   │   └── ...
│   ├── archive/              ← Migrierte Notes (Historie)
│   └── curation_YYYY-MM-DD.md ← Woechentliche Reports
├── knowledge/
│   ├── models/               ← Model-spezifisches Wissen
│   ├── topics/               ← Allgemeine Themen
│   └── hardware/             ← Hardware-Konfigurationen
└── _templates/               ← Note-Templates

blog-drafts/
├── 01-claude-mind-interpreter.md
├── 02-glm-fable-local-ai-win.md
└── 03-deepseek-visual-primitives.md

scripts/
└── build_site.py             ← Statischer Site Generator

site/                         ← Generierte HTML (GitHub Pages Source)
```

---

## Attention Score Berechnung

| Faktor | Punkte |
|--------|--------|
| **Source Type** | Video: 15, Community: 10, Model: 10, Code: 12 |
| **Content Length** | >2000 chars: +10, >500: +5 |
| **Transcript/Full Content** | +10 (oder +5 bei >1000 chars) |
| **Kontrovers Keywords** | +5 pro Keyword (max +15) |
| **Entity Mentions** | +3 pro Entity (max +9) |
| **Maximum** | 50pts |

## Blog Kategorien

| Kategorie | Trigger | Titel-Vorlage |
|-----------|---------|---------------|
| Model Spotlight | Model-Namen im Titel | "{topic}: Was sich geandert hat" |
| Hardware Guide | GPU, Benchmark, Setup | "{topic}: So laeuft es auf Consumer-Hardware" |
| Opinion Piece | "stop using", "banned" | "{topic}: Was die Community wirklich denkt" |
| Practical Guide | Tutorial, How-to | "{topic}: Schritt-fuer-Schritt Anleitung" |
| Trend Analysis | Multiple Notes, Distillation | "{topic}: Der Trend der Local AI veraendert" |
| Weekly Digest | Immer verfuegbar | "LocalLLM News: Woche {week}" |

---

## Wichtige Konfigurationen

- **GitHub Pages:** https://localaicreative.github.io/Local_AI_Influencer/
- **Repo:** localaicreative/Local_AI_Influencer (main branch)
- **Research Cronjobs:** ade9c348ea01, 768b7978d086, e168947ee1d3
- **Auto-Curation Cronjob:** a0006c3cd5c6 (Sonntag 10 Uhr)
- **WordPress Credentials:** NUR fuer grosse-schule.de (Schulblog), NICHT fuer Local AI Content

---

*Erstellt: 2026-06-20 — Dokumentation des Content Factory Workflows*
