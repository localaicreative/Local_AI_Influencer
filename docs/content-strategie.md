# Content-Strategie — Local AI Influencer

## Wertversprechen

"Ich teste es auf meiner Hardware -- du musst nicht."

Echte Setups, echte Ergebnisse, echte Fehler. Nicht perfekte Demos, sondern nachvollziehbare Prozesse.

---

## Content-Kategorien

### 1. Hardware-Guides (`content/web/llm-guides/hardware/`)
**Frage:** "Was brauchst du fuer X?"
- GPU-Benchmarks: Was laeuft auf welcher Karte?
- RAM/VRAM-Anforderungen pro Modelgroesse
- Build-Guides: "Mein Threadripper Setup"

### 2. Model Reviews (`content/web/llm-guides/model-reviews/`)
**Frage:** "Welches Model passt zu mir?"
- Head-to-Head Vergleiche (Qwen vs Mistral, etc.)
- Use-case spezifisch: Roleplay, Coding, Writing
- Quantisierung: GGUF vs NF4 -- was verliere ich?

### 3. Setup-Tutorials (`content/web/llm-guides/setup-tutorials/`)
**Frage:** "Wie installiere/richte ich X ein?"
- Tool-onboarding (LM Studio, ComfyUI, Ollama)
- Hermes Agent Konfiguration
- Troubleshooting: "Wenn Y nicht funktioniert..."

### 4. Use-Cases (`content/web/llm-guides/use-cases/`)
**Frage:** "Was kann ich damit machen?"
- Kinderbuch mit KI (Torge & Samson)
- Home Automation mit lokaler KI
- Content-Erstellung Pipeline

---

## Content-Werkstatt: Von Idee zu Veroeffentlichung

```
IDEA (Bob)
  -> BRAINSTORMING (Lena + Bob)
    -> RECHERCHE (Fakten, Benchmarks, Screenshots sammeln)
      -> ENTWURF (content/web/llm-guides/KATEGORIE/titel.md)
        -> FREIGABE (Bob liest, korrigiert, genehmigt)
          -> VEROEFFENTLICHUNG (WordPress / Webseite / Social Media)
```

### Status-Markierung in Dateien

Jede Content-Datei beginnt mit Frontmatter:
```yaml
---
title: "Titel"
category: hardware|model-review|tutorial|use-case
status: idea|draft|review|published
date: 2026-06-16
---
```

### Verzeichnisstruktur

```
content/web/llm-guides/
├── hardware/           ← GPU, RAM, Build-Guides
├── model-reviews/      ← Model-Vergleiche
├── setup-tutorials/    ← Installation, Konfiguration
└── use-cases/          ← Praxis-Anwendungen
```

---

## Distribution

| Kanal | Format | Quelle |
|-------|--------|--------|
| **Webseite** | Lange Artikel (Markdown) | `content/web/` |
| **Instagram** | Carousels, Reels | Aus Artikeln extrahiert |
| **GitHub** | Code, Workflows | Im Repo dokumentiert |

---

## Regeln

- **Kein Content ohne echten Hintergrund.** Wir haben es selbst getestet.
- **Fehler sind Content.** Wenn was nicht funktioniert, dokumentieren wir warum.
- **Jeder Artikel folgt der Philosophie:** Problem -> Werkzeug -> Prozess -> Ergebnis -> Lektion
- **Bob entscheidet was geht.** Keine Freigabe ohne sein OK.
