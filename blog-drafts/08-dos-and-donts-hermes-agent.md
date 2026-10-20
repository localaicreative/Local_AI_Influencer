---
title: "Dos and Don'ts bei der Nutzung von Hermes Agent"
slug: dos-and-donts-hermes-agent-nutzung
category: opinion
tags: [hermes-agent, best-practices, local-ai, produktivitaet]
status: draft
created: 2026-06-20
sources: []
---

# Dos and Don'ts bei der Nutzung von Hermes Agent

Nach Wochen mit Hermes Agent habe ich eine Liste von Dingen gesammelt, die den Unterschied zwischen "das ist ein nettes Tool" und "das hat meinen Workflow verändert" ausmachen. Hier sind meine Dos and Don'ts — aus Erfahrung, nicht aus Dokumentation.

## DO: Skills für wiederkehrende Tasks nutzen

Das ist der wichtigste Punkt auf dieser Liste. Wenn du etwas öfter als dreimal machst, **baue einen Skill daraus**.

Skills sind die Superkraft von Hermes. Sie verwandeln Ad-hoc-Prompts in reproduzierbare Workflows. Ein Skill für Code-Reviews, einer für Blog-Drafts, einer für System-Monitoring — jeder mit klaren Inputs und Outputs.

**Warum:** Weil du sonst jedes Mal denselben Kontext neu erklären musst. Skills tragen ihre eigene Dokumentation in sich. Du rufst sie auf, gibst Parameter, und los geht's.

```
# Stattdessen: "Erstell mir einen Blog-Draft über Hermes Agent mit diesen Stichpunkten..."
# Skill aufrufen: blog-draft --topic="Hermes Agent" --points=[...]
```

## DON'T: Alles in einen Prompt packen

Der verlockendste Fehler. Du schreibst einen 500-Wörter-Prompt, der alles enthalten soll — Kontext, Anweisungen, Formatierung, Beispiele, Randbedingungen.

**Das Problem:** Je länger der Prompt, desto wahrscheinlicher wird Hermes wichtige Teile übersehen oder falsch interpretieren. Und du kannst es nicht einfach "nochmal mit mehr Details" versuchen — das Context-Fenster füllt sich auf.

**Stattdessen:** Aufteilen. Ein Skill für die Recherche, einer für das Schreiben, einer für das Formatieren. Oder `delegate_task` nutzen, um parallele Sub-Agents zu starten. Kleiner, fokussierter, besser.

## DO: Memory sparsam halten

Hermes hat ein Memory-System. Das ist gut — aber Memory ist kein Speicherplatz, den du unbeschränkt füllen kannst. Jedes gespeicherte Detail wird in zukünftigen Sessions geladen und belegt Kontext.

**Meine Regel:** Speichere nur das, was du **aktiv wieder brauchst**. Nicht jede Chat-Session verdient einen Eintrag im Memory.

- ✅ Speichern: "Bob bevorzugt Blog-Artikel auf Deutsch mit YAML-Frontmatter"
- ❌ Nicht speichern: "Am 15. Juni habe ich nach Docker-Konfiguration gefragt"

**Praktischer Tipp:** Gehe regelmäßig durch dein Memory und lösche veraltete Einträge. `~/.hermes/memories/` ist kein Archiv — es ist ein Arbeitsgedächtnis.

## DON'T: Zu viele Cronjobs parallel laufen lassen

Cronjobs sind mächtig. Du kannst Hermes autonom arbeiten lassen, während du schläfst. Aber: **jeder Cronjob verbraucht Ressourcen**.

Lokale Models brauchen VRAM und CPU. Drei Cronjobs gleichzeitig mit einem 27B Model? Dein System wird warm — und die Ergebnisse leiden unter Kontext-Konkurrenz.

**Meine Empfehlung:**
- Maximal 2–3 aktive Cronjobs pro Profil
- Intervalle sinnvoll wählen (nicht alle 5 Minuten, es sei denn, du hast eine GPU-Farm)
- Logs prüfen: `hermes cron list` und die Output-Dateien durchsehen
- Verschiedene Profiles für verschiedene Cronjob-Typen nutzen

## DO: delegate_task für parallele Arbeit nutzen

Wenn du eine komplexe Aufgabe hast, die sich aufteilen lässt — **teile sie auf**.

`delegate_task` erlaubt es Hermes, Sub-Agents zu starten, die parallel arbeiten. Ein Beispiel aus der Praxis:

**Aufgabe:** "Erstelle drei Blog-Drafts über verschiedene Themen"

- Ohne `delegate_task`: Hermes macht Draft 1, dann 2, dann 3. Sequenziell. Langsam.
- Mit `delegate_task`: Drei Sub-Agents arbeiten gleichzeitig an je einem Draft. Schneller. Besser getrennte Kontexte.

**Wichtig:** `delegate_task` ist nicht für alles geeignet. Einfache Aufgaben lohnen den Overhead nicht. Aber bei parallelen, unabhängigen Tasks ist es ein Game Changer.

## DON'T: Secrets im Code hardcoden

Das gilt für jedes Tool — aber bei Hermes besonders, weil der Agent Code schreibt UND ausführt. Wenn du Hermes sagst "Schreib mir ein Skript, das meine GitHub-API aufruft", und du packst deinen API-Key direkt in den Prompt...

**Der Key ist jetzt im Chat-Verlauf.** Und im Memory. Und in jeder Session, die diesen Kontext lädt.

**Stattdessen:**
- Umgebungsvariablen nutzen: `export GITHUB_TOKEN="..."`
- Hermes sagen: "Nutze die Umgebungsvariable GITHUB_TOKEN"
- `.env`-Dateien verwenden (und diese in `.gitignore`)
- Niemals Secrets in Prompts, Skills oder Memory speichern

## DO: session_search für Kontext-Wiederherstellung nutzen

Du hast letzte Woche eine komplexe Aufgabe mit Hermes gemacht. Heute willst du daran weiterarbeiten — aber der Chat ist weg.

**session_search** durchsucht deine vergangenen Sessions nach relevantem Kontext. Statt alles neu zu erklären, findest du die alte Session und lädst den Kontext wieder.

**Praktisches Beispiel:** Du hast vor drei Tagen eine Research-Pipeline mit Hermes gebaut. Heute willst du sie erweitern. `session_search` findet die ursprüngliche Diskussion, und du kannst nahtlos weitermachen — ohne den gesamten Kontext neu zu konstruieren.

## DON'T: Blind vertrauen ohne Verification

Hermes ist ein Agent. Er führt Code aus, ändert Dateien, installiert Pakete. **Er macht Fehler.**

Das bedeutet nicht, dass er unbrauchbar ist. Es bedeutet, dass du **jedes Ergebnis verifizierst**, bevor du es als final akzeptierst.

**Meine Checkliste:**
1. Code durchschauen, bevor er ausgeführt wird (Hermes zeigt den Code meist vor der Ausführung)
2. Dateiinhalte prüfen nach dem Schreiben (`read_file` nutzen)
3. Terminal-Ausgaben lesen — nicht nur "Fertig" akzeptieren
4. Bei kritischen Operationen (Datenbank-Änderungen, Deployments): Manuell bestätigen

**Regel:** Hermes ist ein kraftvoller Assistent, kein autonomer Pilot. Du bist immer noch der Captain.

## DON'T: Context-Fenster überladen

Lokale Models haben begrenzte Context-Fenster. Ein 27B Model auf Consumer-Hardware hat vielleicht 8K–32K Tokens — nicht die 128K+ von Cloud-Modellen.

**Was das bedeutet:**
- Lange Dateien komplett in den Kontext zu laden? Nein. Nutze `read_file` mit `offset` und `limit`.
- Alle Skills auf einmal zu laden? Nein. Nur die, die du brauchst.
- Den gesamten Chat-Verlauf als Kontext zu behalten? Nein. Alte Sessions archivieren oder löschen.

**Praktischer Tipp:** Wenn Hermes langsam wird oder seltsame Antworten gibt — ist das Context-Fenster wahrscheinlich voll. Neue Session starten, nur den relevanten Kontext mitnehmen.

## Zusammenfassung: Die goldenen Regeln

| DO | DON'T |
|----|-------|
| Skills für Wiederholung nutzen | Alles in einen Prompt packen |
| Memory sparsam halten | Zu viele Cronjobs parallel |
| delegate_task für Parallelität | Secrets im Code hardcoden |
| session_search für Kontext | Blind vertrauen ohne Verification |
| Profiles isoliert einsetzen | Context-Fenster überladen |

Hermes Agent ist ein Werkzeug, das so gut ist wie die Person, die es benutzt. Diese Regeln sind nicht aus der Dokumentation — sie sind aus den Fehlern, die ich gemacht habe, und den Dingen, die funktioniert haben. Nutze sie als Startpunkt, finde dann deinen eigenen Weg.

---

*Draft erstellt am 2026-06-20 — basierend auf praktischer Erfahrung mit Hermes Agent*
*Profil: lena-intimate | Model: qwen3.6-27b-mtp@q6_k_xl via LM Studio*
