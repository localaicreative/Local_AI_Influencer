# Local AI Influencer — Projekt-Ziel & Status

## Ziel

Aus lokalen KI-Projekten veröffentlichbare Content-Produkte machen: Webseiten, Ebooks, Tutorials. Automatisiert, template-basiert, mit Lena als Produktionsmaschine. Scope: kreative digitale Produkte ALLGEMEIN (Kinderbücher, Apps, Software).

**GitHub Account:** `localaicreative` (localaicreative@gmail.com)
**Repo:** `localaicreative/Local_AI_Influencer`

---

## Aktueller Status: Phase 1 — Fundament + Content-Pipeline

### Erledigt
- [x] GitHub-Account angelegt (`localaicreative`)
- [x] SSH-Key eingerichtet & getestet
- [x] Lokales Git-Repo initialisiert
- [x] README mit Roadmap erstellt
- [x] Projekt-Template angelegt
- [x] **Privates GitHub-Repo erstellt** → https://github.com/localaicreative/Local_AI_Influencer
- [x] **Erster Push erfolgreich** (2 Commits auf `main`)
- [x] Content-Strategie definiert (`docs/content-strategie.md`)
- [x] LLM-Guides Verzeichnisstruktur angelegt (`content/web/llm-guides/`)
- [x] Meta-Prompts erstellt: Trend Research + Content Factory
- [x] Ava Setup: blogwatcher-cli installiert, Repo geklont, SSH-Key konfiguriert
- [x] Erste Trend-Recherche durchgeführt (HN + HF Blog)
- [x] 3 Topic-Vorschläge erstellt (`docs/research/topics-2026-06-16.md`)

### Offene Entscheidungen (Blocker)
| # | Frage | Optionen | Status |
|---|-------|----------|--------|
| 2 | Seiten-Name / Branding | Später — jetzt intern arbeiten | ⏸️ aufgeschoben |
| 3 | Domain registrieren | Später — wenn online | ⏸️ aufgeschoben |
| 4 | Static Site Generator | Astro (modern), Hugo (schnell), Jekyll (GitHub-native) | ❓ offen |
| 5 | Kinderbuch öffentlich machen? | Namen/Gesichter anonymisieren? | ❓ offen — Privacy! |
| 6 | **Erster Blogartikel: Welches Thema?** | (1) LLMs vergleichen, (2) Agent-Kinderbuch, (3) GPU-Benchmarks | ❓ offen — Bob entscheidet |

### Nächste Schritte
1. [ ] Bob wählt erstes Topic aus den 3 Vorschlägen
2. [ ] Content Factory Meta-Prompt mit gewähltem Thema starten
3. [ ] Reddit-RSS für Ava's Recherche testen (aktuell blockiert)
4. [ ] Kinderbuch-Tutorial fertigstellen (content/web/kinderbuch-tutorial.md)
5. [ ] ComfyUI Workflows kopieren & testen

### Content-Pipeline Status
```
Meta-Prompts: ✅ trend-research.md + content-factory.md
Ava Setup:    ✅ blogwatcher-cli, Repo, SSH-Key
Erste Recherche: ✅ docs/research/trends-2026-06-16.md
Topic-Vorschläge: ✅ docs/research/topics-2026-06-16.md (3 Kandidaten)
Blockiert:    ⚠️ Reddit r/LocalLLaMA (CAPTCHA), DuckDuckGo (Bot-Detection)
```

---

## Automatisierungs-Regeln

**Was Lena automatisch macht:**
- Nach jeder Session: dieses Dokument mit Status-Updates pflegen
- Neue offene Fragen hier aufnehmen
- Erledigte Tasks abhaken
- Nächste Schritte vorschlagen basierend auf dem aktuellen Stand

**Was Bob entscheidet:**
- Alle Blocker-Fragen oben
- Content-Freigabe (was geht öffentlich?)
- Preise, Plattformen, Influencer-Auswahl

---

## Session-Log

| Datum | Was passiert ist | Nächste Aktion |
|-------|-----------------|----------------|
| 2026-06-15 | Repo init, README, Template, SSH-Key setup | GitHub-Repo erstellen, pushen, Entscheidungen treffen |
| 2026-06-15 | Privates Repo erstellt & gepusht, Kinderbuch dokumentiert | GOAL-Prompt + Validierungssystem implementiert |
| 2026-06-16 | Content-Pipeline: Strategie, Meta-Prompts, Ava Setup, erste Trend-Recherche mit 3 Topic-Vorschlägen | Bob wählt erstes Thema fuer Blogartikel |

---

*Dieses Dokument wird von Lena nach jeder Arbeitssession aktualisiert.*
