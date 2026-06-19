# Recherche-Strategie — Local AI Influencer Content

## Ziel
Systematische, nachvollziehbare Recherche fuer Blogartikel. Keine oberflaechlichen Ueberblicke mehr — echte Daten aus echten Quellen.

---

## Oberkategorien & Recherche-Methoden

### 1. Model-Vergleiche (model-reviews)
**Frage:** "Welches Model passt zu mir?"

| Methode | Quelle | Was wir sammeln |
|---------|--------|-----------------|
| **Google Custom Search API** | `curl` mit Key + CX ID | Aktuelle Blogartikel, Reviews, Benchmarks |
| **HuggingFace Models** | Browser: `huggingface.co/models?sort=lastModified` | Neueste Releases, Parameter, Lizenz |
| **Artificial Analysis** | Browser: `artificialanalysis.ai/models` | Intelligence Index, Speed, Preis |
| **YouTube Tests** | Bob postet Links in `youtube-research.md` | Echte Inference-Tests mit Screenshots |
| **Open LLM Leaderboard** | Browser: HF Space | MMLU-Pro, IFEval, BBH Scores |

**Workflow:**
1. Google Search API → aktuelle Artikel finden
2. YouTube-Links von Bob → `youtube-research.md` posten
3. Ich schaue mir Videos an (Transcript/Description)
4. HuggingFace → Model-Daten verifizieren
5. Artificial Analysis → Benchmark-Zahlen
6. Alles zusammenfassen im Artikel

---

### 2. Hardware-Guides (hardware)
**Frage:** "Was brauchst du fuer X?"

| Methode | Quelle | Was wir sammeln |
|---------|--------|-----------------|
| **Eigene Tests** | Threadripper + 4x GPU Setup | VRAM, Latenz, tok/s pro Model |
| **YouTube Benchmarks** | Bob postet Links | Vergleich mit anderen Setups |
| **Reddit r/LocalLLaMA** | Browser (CAPTCHA-Problem) | Community-Erfahrungen |

---

### 3. Setup-Tutorials (setup-tutorials)
**Frage:** "Wie installiere/richte ich X ein?"

| Methode | Quelle | Was wir sammeln |
|---------|--------|-----------------|
| **Eigene Erfahrung** | Eigene Installationen | Screenshots, Commands, Fehler |
| **Offizielle Docs** | Browser: Projekt-Websites | Installationsanleitungen |
| **YouTube Tutorials** | Bob postet Links | Visuelle Bestaetigung |

---

### 4. Use-Cases (use-cases)
**Frage:** "Was kann ich damit machen?"

| Methode | Quelle | Was wir sammeln |
|---------|--------|-----------------|
| **Eigene Projekte** | Kinderbuch, Home Automation | Echte Screenshots, Commands |
| **Community Stories** | Reddit, Discord | Andere Use-Cases |
| **YouTube Demos** | Bob postet Links | Inspiration fuer eigene Tests |

---

## YouTube Research Collection

Bob postet YouTube-Links hier: `docs/research/youtube-research.md`

Format:
```markdown
## [Datum] - [Titel des Videos]
- Link: https://youtube.com/watch?v=...
- Kanal: Name
- Thema: Model-Vergleich / Hardware / Setup / Use-Case
- Wichtige Timestamps: 0:00 Intro, 2:30 Benchmark, ...
- Meine Notizen: (Lena fuegt nach der Analyse hinzu)
```

---

## Google Custom Search API

**Status:** CX ID vorhanden (`1220688da569d4970`), API Key fehlt noch.

**Setup (wenn Key da ist):**
```bash
export GOOGLE_API_KEY="AIzaSy..."
export GOOGLE_CX="1220688da569d4970"

# Test
curl "https://www.googleapis.com/customsearch/v1?key=$GOOGLE_API_KEY&cx=$GOOGLE_CX&q=best+local+LLM+June+2026&num=10"
```

**Typische Suchanfragen:**
- `best local LLM June 2026`
- `Qwen3 vs Llama4 benchmark comparison`
- `Gemma 4 local inference test`
- `Granite 3.3 review local GPU`
- `open weight LLM release June 2026`

---

## Regeln

1. **Kein Artikel ohne echte Daten.** Mindestens 3 Quellen pro Behauptung.
2. **YouTube-Links von Bob sind Gold.** Echte Tests > meine Recherche.
3. **Human in the loop ist notwendig.** Ich recherchiere, Bob entscheidet was relevant ist.
4. **Alles wird dokumentiert.** Jede Recherche landet in `docs/research/` mit Datum und Quelle.

---

*Erstellt: 2026-06-17 | Status: Aktiv*