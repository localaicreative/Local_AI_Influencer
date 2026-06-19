# Research Vault — Architektur v2

**Erstellt:** 2026-06-19 | **Status:** Entwurf zur Review

---

## 0. AKTUELLE PROBLEME (Warum wir neu denken)

| Problem | Symptom | Auswirkung |
|---------|---------|------------|
| **Leere Notes** | Auto-generierte Notes haben nur Titel + Link, keine Zusammenfassung | Vault wachst mit leeren Schalen statt Wissen |
| **Keine Trennung Inbox/Wissen** | Alles landet direkt in `trends/`, `hardware-configs/` etc. | Kein kuratorischer Schritt — Rohdaten und Wissen vermischen sich |
| **Reddit komplett blockiert** | RSS, JSON API, Playwright = alle 403 | Größte Quelle liefert nur Titelschalen |
| **Keine Attention-Bewertung** | Keyword-Matching (high/medium/low) ist zu grob | Können nicht unterscheiden was Blog-würdig ist vs. Noise |
| **Keine Synthese** | Notes sind isoliert, keine Verbindungen | "Was wissen wir über Qwen3?" → muss manuell durch 12 Notes suchen |
| **Blog-Kategorien nicht abgeleitet** | Research und Content-Erstellung sind entkoppelt | Manuelle Brücke zwischen Vault und Blog nötig |

---

## PUNKT 1: INBOX vs WISSENSDATENBANK

### Konzept

```
ROH-SIGNAL                          KURIERTES WISSEN
(inbox/)                             (knowledge/)
─────────────                        ───────────────
Auto-generiert                       Manuell oder nach Review
Chronologisch                         Thematisch vernetzt
"Was kam heute rein?"                "Was wissen wir über X?"
Keine Qualitätsgarantie              Validiert, kontextualisiert
Jeder Cron-Lauf fügt hinzu           Nur was den Filter passiert
```

### Neue Verzeichnisstruktur

```
research-vault/
├── _inbox/                          ← NEU: Roh-Signale aus der Pipeline
│   ├── 2026-06-19/                  ← Datum-basiert
│   │   ├── reddit_stop-using-ollama.md
│   │   ├── youtube_gemma4-webgpu.md
│   │   └── github_llama-cpp-v3.5.md
│   └── 2026-06-20/
│
├── knowledge/                       ← NEU: Kuratiertes Wissen
│   ├── topics/                      ← Themen-Synthesen
│   │   ├── qwen-family.md           ← "Alles was wir über Qwen wissen"
│   │   ├── ollama-alternatives.md   ← Aggregiert aus mehreren Quellen
│   │   └── webgpu-inference.md      ← Browser-basierte Inference Trend
│   ├── hardware/                    ← Validierte Hardware-Configs
│   ├── models/                      ← Model-Profile mit Benchmarks
│   └── use-cases/                   ← Getestete Use-Cases
│
├── trends/                          ← BESTEHEND: bleibt für manuelle Deep-Dive Notes
├── hardware-configs/                ← BESTEHEND:同上
├── use-cases/                       ← BESTEHEND:同上
├── _templates/                      ← BESTEHEND
└── _scripts/                        ← NEU: Pipeline-Scripts lokal im Vault
```

### Workflow: Von Inbox zu Knowledge

```
Cron-Lauf → _inbox/YYYY-MM-DD/signal.md  (auto, roh)
                ↓
        [Täglich/Wöchentlich Review]
                ↓
        ┌───────┴────────┐
        │                 │
    VERWERFEN         BEHALTEN + ERWEITERN
    (löschen)         knowledge/topics/thema.md
                            ↓
                    Backlinks zu verwandten Notes
                    Synthese: "Was bedeutet das?"
                    Status: new → reviewed → established
```

### Umsetzung

**Schritt 1:** `run_research.py` ändern — alle auto-generierten Notes landen in `_inbox/DATE/` statt direkt in Kategorien.

**Schritt 2:** Neues Script `curate_inbox.py`:
- Scannt `_inbox/` nach unverarbeiteten Notes
- Gruppiert ähnliche Topics (z.B. alle Qwen-Notes zusammen)
- Vorschlag: "Diese 5 Notes könnten zu `knowledge/topics/qwen-family.md` werden"

**Schritt 3:** Synthese-Template für Knowledge-Notes:
```markdown
---
topic: [Thema]
status: reviewed|established|outdated
last-updated: YYYY-MM-DD
sources: [Anzahl Notes in inbox die hierin fließen]
---

# [Thema] — Was wir wissen

## Zusammenfassung (3 Sätze)

## Quellen (verlinkt auf Inbox-Notes)

## Hardware-Kontext

## Community-Stimmung (positiv/negativ/neutral)

## Blog-Potenzial: JA/NEIN + warum
```

---

## PUNKT 2: ATTENTION SCORING

### Konzept

Aktuell: Keyword-Matching (`>=3 matches = high`). Zu grob.

Neu: **Multi-Faktor Attention Score** (0-100) mit 4 Dimensionen:

| Dimension | Gewicht | Messung | Beispiel |
|-----------|---------|---------|----------|
| **Signal Strength** | 35% | Upvotes, Views, Stars, Comment Count | Reddit Post mit 500 upvotes = hoch |
| **Novelty** | 25% | Ist das wirklich neu? (Vergleich mit existierenden Notes) | "Qwen3.6" wenn wir schon Qwen3.5 haben = niedrig |
| **Audience Fit** | 25% | Trifft es unsere Zielgruppe? (LocalLLM-Anfänger bis Fortgeschrittene) | "WebGPU Inference im Browser" = hoch (praktisch, neu) |
| **Emotional Hook** | 15% | Kontrovers? Überraschend? Praktisch nützlich? | "Stop using Ollama" = hoch (kontrovers) |

### Attention Score Berechnung

```python
def calculate_attention_score(signal):
    score = 0
    
    # Signal Strength (0-35)
    if signal.upvotes > 200:      score += 35
    elif signal.upvotes > 100:    score += 25
    elif signal.upvotes > 50:     score += 15
    elif signal.upvotes > 10:     score += 8
    
    # Novelty (0-25) — Vergleich mit existierenden Notes im Vault
    if is_topic_new(signal.title, vault):   score += 25
    elif is_topic_fresh(signal.title, vault): score += 15
    else:                                    score += 5
    
    # Audience Fit (0-25) — Keywords die unsere Zielgruppe interessieren
    audience_keywords = ["consumer gpu", "rtx 4090", "local", "run locally", 
                         "tutorial", "guide", "how to", "setup"]
    matches = sum(1 for kw in audience_keywords if kw in signal.text.lower())
    score += min(matches * 5, 25)
    
    # Emotional Hook (0-15) — kontroverse/überraschende Signale
    hook_patterns = ["stop using", "don't use", "banned", "shocking", 
                     "game changer", "finally", "better than"]
    if any(p in signal.title.lower() for p in hook_patterns):
        score += 15
    
    return min(score, 100)
```

### Output: Attention-Tags + Top-3

Jede Note im Inbox bekommt:
```yaml
attention-score: 72
attention-tags: [trending, controversial]
blog-potential: high  # auto: score >= 65 → high, >= 40 → medium, < 40 → low
```

**Top-3 Report pro Cron-Lauf:**
```
=== TOP 3 (Attention Score) ===

1. [82pts] "Stop using Ollama" — trending, controversial
   → Blog-Potenzial: HIGH (kontroverses Thema, große Community-Reaktion)

2. [76pts] "Gemma 4 E2B running in-browser at 255 tok/s" — breakthrough, practical  
   → Blog-Potenzial: HIGH (praktisch, neu, Hardware-relevant)

3. [68pts] "Anthropic forced to disable Fable 5" — trending
   → Blog-Potenzial: MEDIUM (interessant aber eher Cloud-News)
```

### Umsetzung

**Schritt 1:** `calculate_relevance()` in `run_research.py` durch `calculate_attention_score()` ersetzen.

**Schritt 2:** Upvotes/Views aus RSS extrahieren wo verfügbar (Reddit RSS hat `<comments>` Count als Proxy).

**Schritt 3:** Novelty-Check: vor Note-Erstellung existierende Notes im Vault scannen (`os.listdir()`) auf Titel-Überschneidung.

**Schritt 4:** Top-3 Report am Ende jedes Cron-Laufs ausgeben (wird an Bob geliefert).

---

## PUNKT 3: BLOG-KATEGORIEN AUS RECHERCHE ABLEITEN

### Konzept

Statt Blog-Kategorien im Voraus zu definieren, **emergieren sie aus den Daten**. Die Pipeline erkennt Muster und schlägt Content vor.

### Auto-Detektion von Blog-würdigen Themen

```
Inbox-Notes clustern nach Topic → Cluster mit >=3 Notes = "Thema etabliert"
    ↓
Cluster bewerten: Attention Score Durchschnitt + Vielfalt der Quellen
    ↓
Blog-Kategorie vorschlagen basierend auf Cluster-Typ
```

### Blog-Kategorien-Matrix (auto-abgeleitet)

| Wenn im Vault... | Dann Blog-Kategorie... | Beispiel |
|------------------|----------------------|----------|
| Mehrere Notes über ein Model/Release | **Model Spotlight** | "Qwen3.6: Was sich geändert hat" |
| Hardware-Configs mit Benchmarks | **Hardware Guide** | "Was läuft auf RTX 4090? Juni 2026" |
| Kontroverse Diskussion (hoher Emotional Hook) | **Opinion Piece** | "Solltest du Ollama wirklich stoppen?" |
| Tutorial/How-To Notes | **Practical Guide** | "Lokale LLMs im Browser mit WebGPU" |
| Trend über mehrere Wochen | **Trend Analysis** | "Warum alle auf Qwen setzen" |
| Weekly Roundup der Top-3 | **Weekly Digest** | "LocalLLM News: Woche 25/2026" |

### Content-Pipeline: Von Research zu Blog

```
PHASE A: SAMMLUNG (auto, 3x täglich)
Cron-Lauf → _inbox/ → Attention Score → Top-3 Report
                    ↓
PHASE B: CLUSTERING (wöchentlich, auto)
Inbox scannen → Topics clustern → "Etablierte Themen" identifizieren
                    ↓
PHASE C: VORSCHLAG (wöchentlich, an Bob)
"Diese 3 Themen sind blog-würdig:"
1. [Thema] — Kategorie: Model Spotlight — Warum: ...
2. [Thema] — Kategorie: Hardware Guide — Warum: ...
3. [Thema] — Kategorie: Opinion Piece — Warum: ...
                    ↓
PHASE D: ERSTELLUNG (manuell, Bob triggert)
Bob wählt Thema → Content Factory Meta-Prompt → Blogartikel + Insta-Derivate
```

### Konkreter Vorschlag für die erste Woche

Basierend auf den aktuellen Notes im Vault:

| Note-Cluster | Blog-Kategorie | Titel-Vorschlag |
|--------------|---------------|-----------------|
| GLM-5.2 (2 Notes) + Fable ban | Model Spotlight | "GLM-5.2 & Fable-Ban: Was das für Local AI bedeutet" |
| Gemma 4 WebGPU + Browser Inference | Practical Guide | "LLMs im Browser: 255 tok/s ohne GPU — so geht's" |
| "Stop using Ollama" (kontrovers) | Opinion Piece | "Ollama-Alternativen: Was die Community wirklich will" |
| Qwen3.5 Distillation + Claude Mind Interpreter | Trend Analysis | "Distillation & Interpretierbarkeit: Die zwei Trends die Local AI verändern" |

---

## UMSETZUNGSPLAN (Priorisiert)

### Phase 1: Inbox-Struktur (Tag 1)
- [ ] `_inbox/` Ordner erstellen
- [ ] `run_research.py` ändern: auto-notes → `_inbox/YYYY-MM-DD/`
- [ ] Bestehende Notes aus `trends/` etc. bleiben (manuelle Deep-Dives)
- [ ] **Aufwand:** ~30 Min

### Phase 2: Attention Score (Tag 1-2)
- [ ] `calculate_attention_score()` implementieren
- [ ] Upvotes/Views aus RSS extrahieren
- [ ] Novelty-Check gegen existierende Notes
- [ ] Top-3 Report am Ende jedes Laufs
- [ ] **Aufwand:** ~1-2 Std

### Phase 3: Clustering + Blog-Vorschläge (Tag 2-3)
- [ ] `curate_inbox.py` Script: Topics clustern, Synthese vorschlagen
- [ ] Blog-Kategorie-Matrix implementieren
- [ ] Wöchentlicher "Content Vorschlag" Report
- [ ] **Aufwand:** ~2-3 Std

### Phase 4: Knowledge-Basis + Migration (ERLEDIGT ✓)
- [x] `knowledge/topics/` Struktur erstellen
- [x] Synthese-Template fur Knowledge-Notes
- [x] `migrate_to_knowledge.py`: Inbox → Knowledge mit Auto-Detection
- [x] Topic Clustering + Entity Extraction (Model-Namen, Tools, Hardware)
- [x] Original Notes nach `_inbox/archive/` (History bleibt)
- [x] Testlauf: 10 Notes migriert, 10 Knowledge Notes erstellt
- **Aufwand:** ~2 Std

### Phase 5: Reddit OAuth (wenn Bob Credentials liefert)
- [ ] PRAW Integration in `run_research.py` aktivieren
- [ ] Deep Dive funktioniert → Notes haben echten Content statt Schalen
- [ ] **Aufwand:** ~30 Min

---

## WAS SICH NICHT ÄNDERT

- Cronjobs bleiben 3x täglich (11/16/21 Uhr)
- YouTube Deep Dive mit Transkripten bleibt wie es ist (funktioniert gut)
- GitHub RSS Feeds bleiben
- Manuelles Trigger von Content-Erstellung bleibt (Modell B)
- Bestehende manuelle Notes in `trends/`, `hardware-configs/` etc. bleiben

---

## RISIKEN & OFFENE FRAGEN

| Risiko | Wahrscheinlichkeit | Impact | Minderung |
|--------|-------------------|--------|-----------|
| Inbox wächst zu schnell | Mittel | Niedrig | Automatische Bereinigung nach 7 Tagen |
| Attention Score zu komplex | Niedrig | Mittel | Starten mit einfacher Version, iterativ verbessern |
| Clustering ungenau | Mittel | Mittel | Manuelle Korrektur möglich, Script nur Vorschlag |
| Reddit OAuth nie kommt | Hoch | Mittel | Pipeline funktioniert trotzdem mit YouTube + GitHub |

---

*Entwurf von Lena — bereit für Bob's Review und Feedback.*
