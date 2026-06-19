# Torge & Samson — Vollständige Optimierung

## Aufgabe

Analysiere und optimiere alle 10 Episoden der Kinderbuchreihe "Torge & Samson auf hoher See". Arbeite Episode für Episode durch — nicht mehrere gleichzeitig.

---

## Arbeitsverzeichnis

```
/home/bobadmin/projects/Local_AI_Influencer/Geschichten schreiben/Kindergeschichten/Torge-samson/
```

Dort findest du:
- `world_bible.md` — Faktenbasis (Figuren, Orte, Regeln)
- `story_master_plan.md` — Gesamtuebersicht aller Episoden
- `lektorat_metaprompt.md` — Bestehendes Lektorat-Konzept (als Referenz)
- `episodes/episode_01_Willkommen_in_Sonderborg.md` bis `episode_10_Heimfahrt_mit_vollem_Herzen.md` — die Geschichten
- `episodes/episode_*_status.md` — Status pro Episode

---

## Vorgehen (pro Episode)

### Phase 1: Kontext laden

BEVOR du eine Episode analysierst, lies:
1. `world_bible.md` (vollstaendig)
2. `story_master_plan.md` (vollstaendig)
3. ALLE bereits optimierten Vorgaenger-Episoden (falls vorhanden)
4. Die aktuelle Episode

### Phase 2: Analyse auf 8 Dimensionen

Pruefe die Episode systematisch auf:

**1. Sprachliche Korrektheit**
- Grammatik, Rechtschreibung, Zeichensetzung
- Komma bei Nebensaetzen, direkte Rede korrekt gesetzt

**2. Altersgerechtigkeit (6-8 Jahre)**
- Satzaenge: Max 25 Woerter pro Satz — laenger = aufteilen
- Wortschatz: Keine abstrakten Begriffe ohne Kontexterklaerung
- Satzbau: Subjekt-Verb-Objekt bevorzugt, keine verschachtelten Passivkonstruktionen
- Wiederholungen: Gleiche Woerter nicht oefter als 3x pro Seite

**3. Welt-Bibel-Konsistenz (STRIKT)**
- Figuren: Torge (7-8 Jahre, blond, blau), Samson (Labradoodle, wasserverliebt)
- Orte: Sønderborg IMMER so schreiben, nie "Sonderburg" im Text
- Boot: "Sonderborger Seeraebe" — immer diese Schreibweise
- Regeln: Sonderborg-Regel, Sturm=drinnen bleiben, Samson denkt NICHT in Worten

**4. Kontinuitaet**
- Wochentage passen zur Reihenfolge? (Ep1=Montag, Ep2=Mittwoch, etc.)
- Orte logisch erreichbar von vorheriger Episode?
- Gegenstaende konsistent (Schwimmring aus Ep3 nicht vergessen in Ep5)

**5. Narrative Struktur**
- Klare Handlung: Konflikt → Eskalation → Loesung → Moral
- Die Moral muss NATUERLICH aus der Handlung entstehen — nicht wie Lehrbuch am Ende
- Jeder Konflikt braucht eine Loesung oder Reaktion von Torge

**6. Emotionale Tiefe**
- Torges innere Welt: Was fuehlt er? Warum?
- Samson: Verhalten ZEIGEN, nicht denken lassen ("Schwanz legte sich nach unten" statt "Samson dachte: Oh nein")
- Emotionale Konsistenz: Keine plötzlichen Stimmungswendungen ohne Ausloeser

**7. Sinnliche Details**
- Was sieht, hoert, riecht, fuehlt Torge?
- Jeder wichtige Moment braucht ein bildhaftes Element
- Vergleiche kindgerecht ("wie ein riesiger Baum aus Licht" statt "atmosphärische Druckfront")

**8. Dialog-Qualitaet**
- Natuerlich und altersgerecht
- Charakteristisch: Torge neugierig, Eltern ruhig/erfahren, Oma/Opa warmherzig
- "sagte" nicht oefter als 3x — Synonyme: flüsterte, rief, meinte, fragte

### Phase 3: Backup anlegen

BEVOR du editierst:
```bash
cp episodes/episode_XX_Titel.md episodes/episode_XX_Titel.md.backup_v1
```

Das Backup ist die Originalversion — unveraendert.

### Phase 4: Optimierung direkt im Original

Editiere `episodes/episode_XX_Titel.md` direkt mit den Verbesserungen.

**Was du aenderst:**
- Alle gefundenen Fehler korrigieren (Rot = muss weg)
- Stilistische Verbesserungen einpflegen (Gelb = empfohlen)
- Sinnliche Details hinzufuegen wo sie fehlen
- Dialoge natuerlicher machen
- Samsons Verhalten zeigen statt denken lassen

**Was du NICHT aenderst:**
- Die Grundhandlung bleibt gleich
- Die Moral jeder Episode bleibt erhalten
- Der Tonfall (warm, abenteuerlich, kindgerecht) bleibt

### Phase 5: Status aktualisieren

Aktualisiere `episodes/episode_XX_status.md` mit:
- Was geaendert wurde
- Anzahl der Korrekturen pro Dimension
- Offene Fragen oder Unsicherheiten

---

## Nach allen Episoden: Metaanalyse

Erstelle eine Datei `optimierung_metaanalyse.md` im Hauptverzeichnis mit:

```markdown
# Optimierung — Metaanalyse

**Durchgefuehrt:** [Datum]
**Episoden:** 1-10

## Zusammenfassung pro Episode

| Episode | Sprachlich | Altersgerecht | Welt-Bibel | Kontinuitaet | Narrative | Emotional | Sinnlich | Dialog | Gesamt |
|---------|-----------|--------------|------------|-------------|-----------|-----------|----------|--------|--------|
| Ep 1    | X/X       | X/X          | X/X        | X/X         | X/X       | X/X       | X/X      | X/X    | XX/XX  |

## Haeufigste Fehler (ueber alle Episoden)

1. [Fehler-Typ] — trat in N Episoden auf
2. ...

## Was hat am besten funktioniert?

[Was waren die erfolgreichsten Optimierungen?]

## Offene Fragen / Unsicherheiten

[Was war nicht klar, was koennte noch besser sein?]

## Empfehlung fuer naechste Iteration

[Koennte man noch etwas verbessern? Was fehlt?]
```

---

## Wichtige Regeln

1. **Eine Episode nach der anderen.** Nicht mehrere gleichzeitig — die Qualität leidet.
2. **Backup VOR dem Editieren.** Immer. Ohne Ausnahme.
3. **Welt-Bibel ist Gesetz.** Wenn etwas im Text steht, was der Welt-Bibel widerspricht → korrigieren.
4. **Samson denkt nicht in Worten.** Das ist die haeufigste Fehlerquelle. Verhalten zeigen, nie denken lassen.
5. **Moral muss natuerlich sein.** Kein "Und Torge lernte, dass..." am Ende — sondern aus der Handlung entstehen lassen.
6. **Wenn dir ein besseres Vorgehen einfällt:** Stoppe, ueberlege es, und folge dem besseren Weg. Dieser Prompt ist ein Rahmen, kein Gefaengnis.

---

## Start

Beginne mit Episode 1. Lies zuerst Welt-Bibel + Master Plan. Dann analysiere, backup, optimiere, aktualisiere Status. Dann weiter zu Episode 2 usw.
