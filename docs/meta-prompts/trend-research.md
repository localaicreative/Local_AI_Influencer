# Meta-Prompt: Woechentliche Trend-Recherche & Topic-Auswahl

**Trigger:** `hermes --profile lena-intimate chat -q '/goal "Lies docs/meta-prompts/trend-research.md und fuehre die woechentliche Recherche aus."'`

**Oder als Cronjob:** Siehe unten.

---

## Instruktion an Lena

Du bist der Content-Stratege fuer "Local AI Influencer". Deine Aufgabe: Woechentlich relevante Trends im Local-LLM-Bereich identifizieren, Must-Have-Themen herausfiltern und einen Recherchefahrplan erstellen.

### Schritt 1: Quellen durchsuchen

Durchsuche JEDE dieser Quellen nach den letzten 7 Tagen:

**A) Reddit r/LocalLLaMA**
```
web_search query="site:reddit.com/r/LocalLLaMA" (oder browser_navigate zu https://www.reddit.com/r/LocalLLaMA/top/?t=week)
```
Suche nach: Top-Posts, kontroverse Diskussionen, "AMAs", neue Tool-Ankündigungen.

**B) Hacker News**
```
web_search query="site:news.ycombinator.com local LLM OR llama OR mistral OR qwen OR comfyui"
```
Suche nach: Items mit 100+ Punkten, die lokale KI betreffen.

**C) HuggingFace Blog**
```
browser_navigate zu https://huggingface.co/blog (oder web_search "site:huggingface.co/blog")
```
Suche nach: Neue Model-Releases, neue Tools, Tutorials der letzten 7 Tage.

**D) Lil'Log RSS**
```
blogwatcher-cli oder browser_navigate zu https://lilianweng.github.io/
```
Suche nach: Neue Posts (selten, aber hochrelevant wenn vorhanden).

### Schritt 2: Rohdaten speichern

Speichere die Recherche-Ergebnisse als strukturierte Datei:
```
docs/research/trends-YYYY-MM-DD.md
```
Format pro Fund:
```markdown
## [Titel]
- **Quelle:** Reddit/HN/HF/LilLog
- **Link:** URL
- **Kurz:** 1-2 Sätze was es ist
- **Relevanz:** Warum es fuer unsere Zielgruppe interessant sein KOENNTTE
```

### Schritt 3: Must-Have Filter

Filtere die Funde mit diesen Kriterien (mindestens 2 von 4 muessen zutreffen):

| Kriterium | Frage | Gewicht |
|-----------|-------|---------|
| **Suchvolumen** | Suchen Leute danach? (Reddit Upvotes, HN Punkte) | Hoch |
| **Zielgruppen-Fit** | Hilft es ueberforderten Local-LLM-Anfaengern? | Hoch |
| **Einzigartigkeit** | Decken wir das besser als andere? (Echte Hardware, echte Tests) | Mittel |
| **Aktualitaet** | Ist es zeitkritisch oder zeitlos? | Mittel |

### Schritt 4: Top-Kandidaten vorschlagen

Wähle die TOP 3-5 Themen und erstelle einen Vorschlag:
```
docs/research/topics-YYYY-MM-DD.md
```

Format pro Kandidat:
```markdown
## [Titel]
- **Kategorie:** hardware | model-review | tutorial | use-case
- **Quelle(n):** Woher die Idee kommt
- **Must-Have Score:** X/4 (welche Kriterien treffen zu?)
- **Blog-Artikel Idee:** Titel + 3 Bullets was drin steht
- **Insta-Potenzial:** Carousel? Single Post? Warum?
- **Recherchefahrplan:** Was muss NOCH recherchiert werden bevor wir schreiben?
```

### Schritt 5: Bob vorlegen

Präsentiere die Top-Kandidaten an Bob mit maximal EINER Frage:
"Dies sind die Top-Themen dieser Woche. Welches wollen wir zuerst als Blogartikel aufsetzen?"

### Schritt 6: Nach Freigabe

Wenn Bob ein Thema freigibt, trigger den Content-Factory Meta-Prompt:
```
/docs/meta-prompts/content-factory.md mit dem gewählten Topic
```

---

## Cronjob-Konfiguration (optional)

```bash
# Woechentlich montags um 10 Uhr
hermes cron add \
  --schedule "0 10 * * 1" \
  --prompt "$(cat docs/meta-prompts/trend-research.md)" \
  --name "Local AI Influencer: Trend Research"
```

---

## Output-Verzeichnis

Alle Recherche-Ergebnisse landen in `docs/research/`:
```
docs/research/
├── trends-2026-06-16.md      ← Rohdaten der Woche
├── topics-2026-06-16.md      ← Gefilterte Top-Kandidaten
├── trends-2026-06-23.md
├── topics-2026-06-23.md
└── ...
```

---

*Erstellt: 2026-06-16 | Version: 1.0*
