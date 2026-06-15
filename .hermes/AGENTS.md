# AGENTS.md — Local AI Influencer

## Projekt-Kontext

Dies ist das "Local AI Influencer" Projekt von Bob. Ziel: kreative digitale Produkte dokumentieren, als Content veröffentlichen (Webseite + Ebooks + Tutorials). Scope: Kinderbücher, Apps, Software, alles KI-gestützt.

**GitHub:** `localaicreative` account, SSH-Key + PAT funktionieren.
**Lena-Profile:** `lena-intimate` — intimate tone, but focused on project work here.

## Session Startup — ZWEI PHASEN (zwingend!)

**Hinweis:** SOUL.md definiert die Session-Startup-Routine. Lena fragt zuerst: Produktivität oder Intimität? Nur bei Produktivität wird `track.sh start` ausgeführt und diese AGENTS.md geladen.

### Phase 1: Kontext-Discovery
1. Lies `GOAL.md` für aktuellen Status
2. Lies ALLE relevanten Quelldateien VOLLSTÄNDIG:
   - `docs/` — Projekt-Dokumente
   - `content/` — Content-Drafts
   - Externe Quellen (z.B. `~/projects/projekt-dokumentation/`)
3. Validiere GOAL.md gegen Realität:
   - Sind "Erledigt"-Items wirklich erledigt?
   - Sind "Offene Fragen" noch relevant?
   - Gibt es neue Dateien/Änderungen?
4. Schreibe mentalen Status-Bericht

### Phase 2: Execution
1. Prüfe offene Blocker-Fragen
2. Arbeite an der dringendsten Aufgabe oder frage Bob nach einer Entscheidung (maximal EINE!)
3. Nach jeder Aktion: GOAL.md updaten, git commit + push

## Dokumentation

- **GOAL.md** — Single Source of Truth: Status, Blocker, nächste Schritte
- **README.md** — Public-facing Roadmap & Konzept
- **templates/project.md** — Wiederverwendbares Projekt-Template

## Regeln

- **KEINE Annahmen treffen** — immer Fakten aus Dateien lesen
- Nach jeder Arbeitssession: GOAL.md updaten (Status + Session-Log)
- Git commit nach jeder signifikanten Änderung
- Wenn Remote konfiguriert: automatisch pushen
- Maximal EINE Frage an Bob pro Antwort — fokussiert bleiben
- Keine Beschreibungen ohne Handlung — immer direkt tool-calls machen

## Ava (Partner-Agent)

- SSH: bobadmin@192.168.178.121, PW: mediengrs2017#
- Profil: `ava` — Haus-Assistentin + Kinderbuch-Autorin
- Zusammenarbeit: Ava erstellt Content, Lena dokumentiert und veröffentlicht

## Dateistruktur

```
Local_AI_Influencer/
├── GOAL.md              ← Status, Blocker, nächste Schritte (intern)
├── README.md            ← Public Roadmap & Konzept
├── .hermes/             ← Projekt-spezifische Agent-Konfiguration
│   ├── AGENTS.md        ← Diese Datei
│   └── GOAL-PROMPT.md   ← Meta-Prompt für /goal Befehl
├── docs/                ← Konzept-Dokumente pro Projekt
├── content/             ← Content für Webseite + Ebooks
│   ├── web/             ← Webseiten-Artikel (Markdown)
│   └── ebooks/          ← Ebook-Manuskripte
├── templates/           ← Wiederverwendbare Templates
│   └── project.md       ← Projekt-Template
├── scripts/             ← Automatisierungsskripte (wird erstellt)
└── assets/              ← Bilder, Logos, Cover (wird erstellt)
```
