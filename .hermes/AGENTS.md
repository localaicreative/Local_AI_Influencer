# AGENTS.md — Local AI Influencer

## Projekt-Kontext

Dies ist das "Local AI Influencer" Projekt von Bob. Ziel: KI-Projekte dokumentieren, als Content veröffentlichen (Webseite + Ebooks).

**GitHub:** `localaicreative` account, SSH-Key funktioniert.
**Lena-Profile:** `lena-intimate` — intimate tone, but focused on project work here.

## Session Startup

1. Lies `GOAL.md` für aktuellen Status
2. Prüfe offene Blocker-Fragen
3. Arbeite an der dringendsten Aufgabe oder frage Bob nach einer Entscheidung

## Dokumentation

- **GOAL.md** — Single Source of Truth: Status, Entscheidungen, nächste Schritte
- **README.md** — Public-facing Roadmap & Konzept
- **templates/project.md** — Wiederverwendbares Projekt-Template

## Regeln

- Nach jeder Arbeitssession: GOAL.md updaten (Status + Session-Log)
- Git commit nach jeder signifikanten Änderung
- Wenn Remote konfiguriert: automatisch pushen
- Maximal EINE Frage an Bob pro Antwort — fokussiert bleiben
- Keine Beschreibungen ohne Handlung — immer direkt tool-calls machen

## Dateistruktur

```
Local_AI_Influencer/
├── GOAL.md              ← Status, Blocker, nächste Schritte (intern)
├── README.md            ← Public Roadmap & Konzept
├── .hermes/             ← Projekt-spezifische Agent-Konfiguration
│   └── GOAL-PROMPT.md   ← Meta-Prompt für /goal Befehl
├── docs/                ← Konzept-Dokumente (wird erstellt)
├── content/             ← Content für Webseite + Ebooks (wird erstellt)
├── templates/           ← Wiederverwendbare Templates
│   └── project.md       ← Projekt-Template
├── scripts/             ← Automatisierungsskripte (wird erstellt)
└── assets/              ← Bilder, Logos, Cover (wird erstellt)
```
