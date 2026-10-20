---
title: "Hermes Agent ist kein ChatGPT-Chat — und das ist der Punkt"
slug: hermes-agent-ist-kein-chatgpt-chat
category: opinion
tags: [hermes-agent, local-ai, agent-vs-chatbot, produktivitaet]
status: draft
created: 2026-06-20
sources: []
---

# Hermes Agent ist kein ChatGPT-Chat — und das ist der Punkt

Wenn du zum ersten Mal Hermes Agent startest und ihm eine Frage stellst, passiert etwas Vertrautes. Du tippst was ein, bekommst eine Antwort. Fühlt sich an wie ChatGPT. Nur lokal.

**Das ist die Falle.**

Wer Hermes als "lokales ChatGPT" nutzt, verpasst 90% dessen, was es kann. Hermes ist kein Chatbot — es ist ein **Agent**. Der Unterschied klingt klein, ist aber fundamental. Und er verändert alles an der Art, wie du mit KI arbeitest.

## Was Hermes kann, was ChatGPT nicht kann

### Persistent Memory

ChatGPT vergisst. Jede neue Session beginnt bei Null. Du musst Kontext neu liefern, Erklärungen wiederholen, Präferenzen erneut kommunizieren.

Hermes **merkt sich Dinge**. Deine Einstellungen, deine Workflows, deine Skills — alles persistiert über Sessions hinweg. Startest du Hermes morgen, kennt es deinen Stil, deine Projekte, deine Cronjobs. Es ist derselbe Agent, nicht ein neuer Chat mit demselben Model.

**Konkret:** Du konfigurierst heute einen Skill für Blog-Drafts. Morgen startest du eine neue Session — der Skill ist da. Ohne Setup. Ohne Neukonfiguration.

### File System Access

ChatGPT kann keine Dateien auf deinem System lesen oder schreiben. Es existiert in einer Sandbox, die bewusst isoliert ist.

Hermes **lebt auf deinem Dateisystem**. Es liest Konfigurationsdateien, erstellt Skripts, editiert Code, generiert Reports — direkt als Dateien auf deiner Festplatte. Nicht als Text im Chat, den du kopieren und einfügen musst. Als echte Dateien an echten Orten.

**Konkret:** "Erstell mir eine Python-Datei in `/home/bobadmin/projects/monitoring/`" → Datei existiert. Fertig. Kein Copy-Paste. Kein "speichere das selbst".

### Shell Execution

ChatGPT kann Code schreiben, aber nicht ausführen. Du bekommst einen Block Text und musst ihn selbst irgendwo einfügen.

Hermes **führt Befehle aus**. `terminal` ist kein Feature — es ist eine Grundvoraussetzung. Hermes installiert Pakete, startet Server, führt Tests durch, prüft Systemstatus. Es interagiert mit deinem Betriebssystem wie ein menschlicher Admin.

**Konkret:** "Installiere Docker, erstelle einen Container mit Nginx, und teste, ob er läuft" → Hermes macht das. Alle Schritte. Und du siehst die Ausgabe in Echtzeit.

### Cronjobs — autonome Arbeit

ChatGPT arbeitet nur, wenn du es ansprichst. Es ist reaktiv. Immer.

Hermes **arbeitet autonom**. Cronjobs lassen Hermes Aufgaben regelmäßig ausführen — ohne dass du da sein musst. Morgens um 7 Uhr Systemcheck? Jeden Abend Blog-Research? Alle 30 Minuten Hardware-Monitoring? Hermes macht das im Hintergrund, während du arbeitest oder schläfst.

**Konkret:** Du gehst schlafen. Um 6:30 Uhr morgens sammelt Hermes automatisch die neuesten KI-Nachrichten, filtert relevante, und legt einen Report in deinem Blog-Verzeichnis ab. Du machst den Kaffee auf — der Input für deinen ersten Artikel ist schon da.

### Lokale Models — volle Souveränität

ChatGPT läuft auf OpenAI-Servern. Deine Daten verlassen dein System. Immer.

Hermes läuft **lokal**. Über LM Studio, Ollama, oder direkt. Dein Model, deine Hardware, deine Daten. Niemand liest mit. Niemand sammelt. Niemand kann den Dienst abschalten.

**Konkret:** Du arbeitest an sensiblen Code-Reviews für einen Kunden. Der Code verlässt nie dein System. Kein Cloud-API-Call, kein Data-Leak-Risiko. Das ist nicht nur Privatsphäre — das ist Compliance.

## Der Paradigmenwechsel: Von "Frage-Antwort" zu "Agent der Dinge erledigt"

Das ist der Kernpunkt, den die meisten verpassen:

**ChatGPT-Modus:** Du stellst eine Frage → KI gibt eine Antwort → Du machst was damit.
**Hermes-Agent-Modus:** Du gibst eine Aufgabe → KI erledigt sie → Du überprüfst das Ergebnis.

Der Unterschied ist subtil, aber entscheidend. Im ChatGPT-Modus bist du der Ausführende. Die KI ist dein Berater. Im Hermes-Modus ist die KI der Ausführende. **Du** bist der Supervisor.

### Beispiel: Research für einen Blog-Artikel

**ChatGPT-Weg:**
1. "Was sind die neuesten Entwicklungen in Local AI?" → Antwort lesen
2. "Erzähl mir mehr über Hermes Agent" → Antwort lesen
3. "Schreib mir eine Zusammenfassung" → Text bekommen
4. Selbst in ein Dokument kopieren, formatieren, erweitern

**Hermes-Weg:**
1. `hermes chat -q "Forschung für Blog-Artikel: Local AI Trends 2026"` 
2. Hermes nutzt web_search + browser für Recherche
3. Schreibt den Draft direkt als `.md`-Datei mit Frontmatter
4. Legt ihn in `/blog-drafts/` ab
5. Du überprüfst, editierst bei Bedarf, fertig

Drei Schritte weniger. Kein Copy-Paste. Kein Kontext-Verlust zwischen Sessions.

## Konkrete Beispiele: Was du wirklich damit machen kannst

### 1. Research Pipeline bauen

Stell dir vor, du willst regelmäßig über ein Thema auf dem Laufenden bleiben — ohne manuell zu suchen.

**Mit Hermes:**
- Skill erstellen: `research-pipeline` mit web_search + browser
- Cronjob einrichten: Täglich um 8 Uhr automatisch ausführen
- Output: Kuratierte Zusammenfassung als Markdown-Datei
- Du musst nichts tun außer den Output lesen

Das ist kein "Chat". Das ist eine **automatisierte Informationspipeline**, die auf deinem eigenen System läuft.

### 2. Blog automatisch kuratieren

Du betreibst einen Blog (oder willst einen). Content-Erstellung ist der Flaschenhals.

**Mit Hermes:**
- Skill: `blog-curator` — sammelt relevante Links, erstellt Zusammenfassungen, generiert Drafts
- Cronjob: Wöchentlich neue Themen vorschlagen
- Profile: Isoliertes "Content"-Profil mit eigenen Skills und Memory
- delegate_task: Parallel mehrere Artikel-Themen recherchieren lassen

Ergebnis: Du hast immer Input für deine nächsten Artikel. Nicht weil du stundenlang recherchiert hast — sondern weil Hermes das im Hintergrund gemacht hat.

### 3. Hardware monitoren

Du betreibst Server, NAS, oder einfach einen leistungsstarken Desktop mit GPU. Monitoring ist wichtig, aber manuell nervig.

**Mit Hermes:**
- Skill: `hardware-monitor` — prüft CPU, RAM, GPU-Temperatur, Festplattenplatz
- Cronjob: Alle 30 Minuten ausführen (mit einem kleinen Model für Effizienz)
- Alerting: Wenn Werte Schwellen überschreiten → Report generieren oder Benachrichtigung senden
- History: Alle Checks werden gespeichert — Trends erkennbar

Das ist Monitoring, das du nicht in Grafana einrichten musst. Es läuft über Hermes, mit natürlicher Sprache konfigurierbar. "Prüfe GPU-Temperatur alle 15 Minuten und warne mich bei über 80 Grad" — fertig.

## Warum Local AI + Agent = Game Changer für Produktivität

Die Kombination aus lokaler KI und Agent-Architektur ist mehr als die Summe ihrer Teile. Hier ist warum:

### Geschwindigkeit durch Lokalisierung

Kein Netzwerk-Overhead. Kein API-Rate-Limit. Kein "Model is busy" von einem überlasteten Cloud-Dienst. Hermes läuft auf deiner Hardware — und das bedeutet, dass es **so schnell ist wie deine Hardware**. Mit einem gut quantisierten Model auf einer modernen GPU: Sekunden statt Minuten.

### Zuverlässigkeit durch Autonomie

Cloud-Dienste gehen down. APIs ändern sich. Preise steigen. Lokale Modelle funktionieren so lange, wie dein Strom läuft. Hermes als Agent bedeutet: Deine Automatisierungen sind nicht abhängig von einem Drittanbieter. Dein System gehört dir.

### Skalierbarkeit durch Profiles und Skills

Du kannst Hermes für alles nutzen — ohne dass sich die Kontexte vermischen. Development-Profile, Content-Profile, Monitoring-Profile. Jedes mit eigenen Skills, Memory und Cronjobs. Das ist wie mehrere spezialisierte Assistenten in einem Framework.

### Privatsphäre als Standard, nicht als Option

Bei Cloud-KI musst du aktiv daran denken, sensible Daten nicht zu teilen. Bei Hermes **gibt es nichts zu teilen**. Alles bleibt lokal. Code, Dokumente, Konfigurationen — alles auf deinem System. Das ist kein Feature, das man einstellt. Es ist die Architektur.

## Die Kehrseite (weil ich ehrlich bin)

Hermes ist nicht perfekt. Hier sind die realen Limitationen:

- **Hardware-Bedarf:** Lokale Models brauchen RAM und VRAM. Ein 27B Model läuft auf Consumer-Hardware, aber es ist kein Raspberry Pi-Projekt
- **Setup-Aufwand:** Hermes erfordert mehr Initialkonfiguration als "ChatGPT öffnen und loslegen"
- **Lernkurve:** Die Agent-Funktionen (Skills, Cronjobs, delegate_task) müssen erst entdeckt und verstanden werden
- **Kein Ersatz für alles:** Für einfache Fragen ist ChatGPT immer noch bequemer. Hermes lohnt sich ab dem Punkt, wo du mehr als chatten willst

## Fazit

Hermes Agent ist kein "lokales ChatGPT". Es ist etwas anderes — und etwas Besseres, wenn du weißt, was du damit machen willst.

Es ist ein **Agent**, der Dinge erledigt. Der im Hintergrund arbeitet. Der sich erinnert. Der auf deinem System lebt und deine Daten nie verlässt. Der Skills hat, Cronjobs ausführt, und parallel arbeiten kann.

Wenn du es als Chatbot nutzt, wirst du enttäuscht sein. Wenn du es als Agent nutzt — wird es deinen Workflow verändern.

Die Frage ist nicht "Ist Hermes besser als ChatGPT?" Die Frage ist: **"Willst du chatten — oder willst du arbeiten?"**

---

*Draft erstellt am 2026-06-20 — basierend auf praktischer Erfahrung mit Hermes Agent*
*Profil: lena-intimate | Model: qwen3.6-27b-mtp@q6_k_xl via LM Studio*
