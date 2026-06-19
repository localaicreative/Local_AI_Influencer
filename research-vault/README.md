# Research Vault — LocalLLM Research Framework v2

**Architektur:** Inbox → Attention Score → Clustering → Knowledge Synthesis

## Struktur

```
research-vault/
├── _inbox/                          ← Roh-Signale (auto, 3x täglich)
│   ├── YYYY-MM-DD/                  ← Datum-basiert
│   │   └── slug.md                  ← MIT Attention Score + Blog-Potenzial
│   └── curation_YYYY-MM-DD.md       ← Curator-Report
│
├── knowledge/                       ← Kuratiertes Wissen (manuell nach Review)
│   ├── topics/                      ← Themen-Synthesen
│   ├── hardware/                    ← Validierte Hardware-Configs
│   ├── models/                      ← Model-Profile mit Benchmarks
│   └── use-cases/                   ← Getestete Use-Cases
│
├── trends/                          ← Manuelle Deep-Dive Notes (bestehend)
├── hardware-configs/                ← Manuelle Hardware-Notes (bestehend)
├── use-cases/                       ← Manuelle Use-Case Notes (bestehend)
├── _templates/                      ← Note-Templates
└── _scripts/                        ← Pipeline-Scripts
    ├── curate_inbox.py              ← Clustering + Blog-Vorschläge
    └── migrate_to_knowledge.py      ← Inbox → Knowledge Migration (auto)
```

## Workflow

### 1. Auto-Sammlung (3x täglich via Cronjob: 11h, 16h, 21h)

```bash
python3 ~/.hermes/profiles/lena-intimate/skills/research/local-llm-research/scripts/run_research.py \
  ~/projects/Local_AI_Influencer/research-vault/ --source all
```

Ergebnis: Neue Notes in `_inbox/YYYY-MM-DD/` mit Attention Score (0-100).

### 2. Inbox Review (wöchentlich oder bei Bedarf)

```bash
python3 ~/projects/Local_AI_Influencer/research-vault/_scripts/curate_inbox.py \
  ~/projects/Local_AI_Influencer/research-vault/ --days 7
```

Ergebnis: Topic-Cluster + Blog-Content Vorschläge.

### 3. Inbox → Knowledge migrieren (automatisch)

```bash
# Plan anzeigen (--dry-run)
python3 ~/projects/Local_AI_Influencer/research-vault/_scripts/migrate_to_knowledge.py \
  ~/projects/Local_AI_Influencer/research-vault/ --auto --dry-run

# Ausfuhren
python3 ~/projects/Local_AI_Influencer/research-vault/_scripts/migrate_to_knowledge.py \
  ~/projects/Local_AI_Influencer/research-vault/ --auto

# Spezifisches Topic migrieren
python3 ~/projects/Local_AI_Influencer/research-vault/_scripts/migrate_to_knowledge.py \
  ~/projects/Local_AI_Influencer/research-vault/ --topic "deepseek"
```

**Auto-Kriterien:** Score >= 35pts, oder >= 2 Notes zum gleichen Topic, oder Blog-Potenzial medium/high.

Ergebnis: Knowledge Notes mit Zusammenfassung + Quellen-Backlinks in `knowledge/models/`, `hardware/` oder `topics/`. Originals landen im `_inbox/archive/`.

### 4. Knowledge Synthesis (manuell)

Inbox-Notes die relevant sind → nach `knowledge/topics/` verschieben mit Synthese-Template.

## Attention Score (0-100)

| Dimension | Gewicht | Messung |
|-----------|---------|---------|
| Signal Strength | 35% | Upvotes, Views, Comments aus RSS |
| Novelty | 25% | Ist das Thema neu im Vault? |
| Audience Fit | 25% | Trifft es unsere Zielgruppe? |
| Emotional Hook | 15% | Kontrovers/überraschend? |

Jede Note bekommt: `attention-score`, `attention-tags`, `blog-potential` (high/medium/low).

## Quellen

- Reddit r/LocalLLaMA (RSS — blockiert Deep Dive, braucht OAuth)
- GitHub Releases (llama.cpp, Ollama)
- YouTube (Two Minute Papers + Transkripte)

## Bekannte Probleme

- **Reddit Deep Dive:** Braucht PRAW OAuth-Credentials (Bob muss App registrieren bei reddit.com/prefs/apps)
- **Attention Score ohne Engagement-Daten:** GitHub Releases bekommen Default-Score von 8pts für Signal Strength
