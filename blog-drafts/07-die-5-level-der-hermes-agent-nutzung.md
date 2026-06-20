---
title: "Die 5 Level der Hermes-Agent-Nutzung — Wo stehst du?"
slug: die-5-level-der-hermes-agent-nutzung
category: guide
tags: [hermes-agent, local-ai, tutorial, produktivitaet]
status: published
created: 2026-06-20
sources: []
---

# Die 5 Level der Hermes-Agent-Nutzung — Wo stehst du?

Hermes Agent ist nicht nur ein Chatbot. Es ist ein Framework — und wie bei jedem Framework gibt es verschiedene Stufen der Meisterschaft. Hier sind die 5 Level, von "Ich frage mal was" bis "Ich baue autonome Systeme".

## Level 1: Chatbot-Ersatz (Der Einstieg)

**Was du tust:** Einfache Fragen stellen, Texte zusammenfassen, Code-Snippets generieren.

```bash
hermes chat -q "Erkläre mir wie Cronjobs in Hermes funktionieren"
```

**Typische Prompts:**
- "Schreibe eine E-Mail an..."
- "Was bedeutet dieser Fehler?"
- "Fasse diesen Text zusammen"

**Du bist hier, wenn:** Du Hermes primär als smarteren ChatGPT-Clone nutzt. Kein Problem — jeder fängt so an!

**Nächster Schritt:** Probier mal `hermes chat -q "Schau dir die Dateien in ~/projects/ an und liste sie auf"` — plötzlich hast du Dateizugriff, nicht nur Text.

---

## Level 2: Tool-Nutzer (Der Praktiker)

**Was du tust:** Du nutzt die integrierten Tools — Terminal, File-System, Browser, Web-Suche.

```bash
hermes chat -q "Installiere flask und erstelle eine einfache API"
hermes chat -q "Suche nach 'local LLM benchmarks 2026' und fasse die Top 3 Ergebnisse zusammen"
```

**Was du kannst:**
- Shell-Befehle ausführen (Terminal)
- Dateien lesen/schreiben/editieren
- Web-Suchen machen und Ergebnisse verarbeiten
- Browser-Aktionen automatisieren

**Typischer Workflow:** "Lies meine .env Datei, extrahiere die API Keys und erstelle eine neue Config für..."

**Du bist hier, wenn:** Du Hermes als produktiven Assistenten nutzt, der wirklich Dinge erledigt — nicht nur Text generiert.

**Nächster Schritt:** Erstelle deinen ersten Skill! Ein Skill ist ein wiederverwendbarer Workflow.

---

## Level 3: Skill-Bauer (Der Automatisierer)

**Was du tust:** Du erstellst eigene Skills für wiederkehrende Aufgaben.

```bash
hermes chat -q "Erstelle einen Skill namens 'research-collector' der automatisch nach AI News sucht"
```

**Was ein Skill ist:** Eine SKILL.md Datei mit:
- Trigger-Bedingungen (wann wird er geladen?)
- Schritt-für-Schritt Anweisungen
- Templates und Scripts
- Best Practices und Anti-Patterns

**Beispiel-Skills:**
- `coding-quality-gate` — Code Review Pipeline
- `local-llm-research` — Automatisierte Research-Sammlung
- `social-media-content` — Content-Erstellung für Social Media

**Du bist hier, wenn:** Du Workflows baust die du immer wieder nutzt. Ein Skill einmal schreiben, hunderte Male verwenden.

**Nächster Schritt:** Kombiniere Skills mit Cronjobs für echte Autonomie.

---

## Level 4: System-Architekt (Der Builder)

**Was du tust:** Du baust komplette autonome Systeme mit Profiles, Cronjobs und Multi-Agent-Workflows.

```bash
# Profil erstellen
hermes --profile lena-intimate chat -q "Richte ein Research-System ein"

# Cronjob für tägliche Research
cronjob action=create schedule="0 11 * * *" prompt="Führe den Research Runner aus..."

# Multi-Agent mit delegate_task
hermes chat -q "Spawn 3 Subagenten die parallel verschiedene Domänen recherchieren"
```

**Was du aufbaust:**
- **Profiles:** Isolierte Umgebungen mit eigenen Skills/Memory/Cronjobs
- **Cronjobs:** Autonome Tasks die regelmäßig laufen (Research, Monitoring, Reports)
- **delegate_task:** Parallele Subagenten für komplexe Workflows
- **Memory:** Persistentes Wissen über Sessions hinweg

**Beispiel-System:** Research Pipeline → Auto-Curation → Blog Drafts → Dashboard Monitoring

**Du bist hier, wenn:** Du Systeme baust die ohne dich arbeiten. Du definierst die Regeln, Hermes führt sie aus.

**Nächster Schritt:** Contribue zur Community — teile deine Skills und Extensions.

---

## Level 5: Hermes-Guru (Der Meister)

**Was du tust:** Du erweiterst Hermes selbst — Custom Tools, eigene Provider, Community-Contributions.

```bash
# Eigene Toolset erstellen
hermes tools create my-custom-tool

# Custom Model Provider konfigurieren
hermes config set provider.custom "http://localhost:1234"

# Skill für die Community veröffentlichen
git push origin main  # auf Hermes Skills Repo
```

**Was du beherrschst:**
- **Custom Extensions:** Eigene Tools schreiben und in Hermes integrieren
- **Multi-Provider Setup:** Verschiedene Modelle für verschiedene Tasks (lokal + Cloud)
- **Skill-Architektur:** Komplexe Skills mit Templates, Scripts und Referenzen
- **Community:** Deine Workflows anderen zur Verfügung stellen

**Beispiel-Projekte von Gurus:**
- Komplette Content-Factories (Research → Drafts → Publishing)
- Hardware-Monitoring-Dashboards mit autonomen Alerts
- Multi-Agent-Orchestrierung für komplexe Forschungsprojekte

**Du bist hier, wenn:** Du nicht nur Hermes nutzt — du erweiterst es. Deine Skills nutzen andere. Du contribuiest zum Ökosystem.

---

## Wo stehst DU?

| Level | Zeit bis dahin | Was du brauchst |
|-------|---------------|-----------------|
| 1 → 2 | 1-2 Tage | Tools ausprobieren, nicht nur chatten |
| 2 → 3 | 1 Woche | Ersten Skill erstellen (ich helfe!) |
| 3 → 4 | 2-4 Wochen | Cronjobs + Profiles verstehen |
| 4 → 5 | 1-3 Monate | Custom Extensions schreiben |

**Mein Rat:** Bleib nicht auf Level 1 stecken. Der Sprung zu Level 2 ist der wichtigste — sobald du merkst dass Hermes wirklich Dinge *erledigt* statt nur Text zu generieren, gibt es kein Zurück mehr.

---

*Hast du Fragen? Nutze `hermes chat -q "Ich bin auf Level X und will zu Level Y"` — ich erstelle dir einen personalisierten Lernplan.*
