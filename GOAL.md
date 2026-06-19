# Local AI Influencer — Projekt-Ziel & Status

## Ziel

**Zwei Priority-Langzeitprojekte mit stetiger Aktualisierung:**

### 🔥 Prio 1: Hermes Workflow Documentation
Echte Projekte dokumentieren → analysieren → optimieren.
- **Konzept:** Ziel setzen → Weg bis Zielerreichung dokumentieren → Metaanalyse was funktioniert hat → optimierte Version mit Beispielprompts präsentieren
- **Output:** Case-Study-Artikel aus echten Projekten (z.B. "Wie wir ein Kinderbuch mit KI erstellt haben - der Workflow")
- **USP:** Niemand zeigt echte Agent-Sessions und was wirklich funktioniert vs. was nicht

### 🔥 Prio 2: Automatisiertes 2-System LLM Benchmarking
Kontinuierliche Benchmarks auf zwei unterschiedlichen Systemen mit Live-Ergebnissen.
- **Konzept:** Ein System triggert & observiert, das andere führt aus → cross-testing
- **Hardware:** Lena (Threadripper PRO + 4x GPU) ↔ Ava (i7 + RTX 4060 Ti/2070)
- **Output:** Auto-updatende Ergebnis-Tabelle online + Youtuber/Blog-Auswertungen als Kontext

**GitHub Account:** `localaicreative` (localaicreative@gmail.com)
**Repo:** `localaicreative/Local_AI_Influencer`

---

## Aktueller Status: Umstrukturierung auf 2 Priority-Tracks

### Erledigt (Fundament)
- [x] GitHub-Account angelegt (`localaicreative`)
- [x] SSH-Key eingerichtet & getestet
- [x] Lokales Git-Repo initialisiert + privates GitHub-Repo
- [x] Ava Setup: blogwatcher-cli, Repo geklont, SSH-Key konfiguriert
- [x] 2-System-Kommunikation etabliert (Lena ↔ Ava via SSH)

### Track 1: Workflows — Status
- [x] Erste Case-Study: "Torge & Samson" Kinderbuch (Dateien zusammengeführt)
  - Ort: `Geschichten schreiben/Kindergeschichten/Torge_und_Samson/`
  - Enthält: 10 Episoden, Konzept, Tutorial-Entwurf, Ava's Skill, HTML-Anleitung
- [ ] Workflow-Analyse daraus schreiben (Ziel → Weg → Optimierung)

### Track 2: Benchmarks — Status
- [ ] Benchmark-Runner entwerfen (Trigger/Observation vs Execution)
- [ ] Standardisierte Test-Suite definieren
- [ ] Ergebnis-Datenbank + Live-Tabelle aufsetzen
- [ ] Youtuber/Blog-Aggregation Pipeline

### Offene Entscheidungen (Blocker)
| # | Frage | Optionen | Status |
|---|-------|----------|--------|
| 1 | **Erste Workflow Case-Study?** | Kinderbuch, Dashboard, anderes Projekt? | ❓ offen |
| 2 | Benchmark-Test-Suite Scope | Welche Modelle? Welche Tasks? | ❓ offen |
| 3 | Seiten-Name / Branding | Später — jetzt intern arbeiten | ⏸️ aufgeschoben |

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
