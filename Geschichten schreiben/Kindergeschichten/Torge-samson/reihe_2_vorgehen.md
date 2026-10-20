# Reihe 2 — Vorgehensplan

**Erstellt:** 25. Juni 2026
**Status:** Wartet auf Brainstorming mit Bob

---

## Was aus Reihe 1 existiert (Fundament)

- `world_bible.md` — Extrem detaillierte Recherche zu Sonderborg, Hoersuphav, Gråsten (Hafenpreise, Gebäude, Telefonnummern, Straßennamen)
- `story_master_plan.md` — 10 Episoden, alle abgeschlossen
- `optimierung_metaprompt.md` — 8-Dimensionen Lektorat mit Backup-Regel
- `lektorat_metaprompt.md` — 3-Ebenen Prüfung (Sprache, Semantik, Logik) + Anti-Patterns
- `optimierung_metaanalyse.md` — Häufigste Fehler dokumentiert (Samson denkt in Worten: 27x!, Doppelkommas, Torge wedelt mit Schwanz)
- Episoden-Texte in `episodes/` und `projekt-dokumentation/`

---

## Gefundene Lücken (müssen vor Reihe 2 geschlossen werden)

### 1. Keine neuen recherchierten Orte
Die Welt-Bibel deckt nur die Häfen der ersten 10 Episoden ab:
- **Gut recherchiert:** Sonderborg, Hoersuphav, Gråsten
- **Nur Skizze (5-10 Zeilen):** Augustenborg Yachthavn, Aabenraa Yachthafen
- **Nicht recherchiert:** Nordborg Slot, Sollerod/Als Østkyst

**Für Reihe 2 brauchen wir:** Detailrecherche zu neuen Hafenzielen im selben Format wie Sonderborg/Hoersuphav (Gebäude, Preise, Spielplätze, Natur, Orientierung für Geschichten).

### 2. Keine `welt_bible_kurz.md`
Das Kindergeschichten-Framework verlangt zwei Dateien:
- **Kurz (<80 Zeilen):** Für die KI-Generierung pro Episode — nur Fakten die immer relevant sind
- **Detail (alle Details):** Referenz, wird nur geladen wenn spezifische Details benötigt werden

Die aktuelle `world_bible.md` hat 241 Zeilen — zu lang als Kontext für eine einzelne Generierung.

### 3. Kein Brainstorming-Dokument
Reihe 1 wurde "manuell" geschrieben ohne strukturiertes Brainstorming. Für Reihe 2: `brainstorming_notizen.md` erstellen nach Framework-Template.

---

## Vorgehen Reihe 2 (Schritt-für-Schritt)

### Schritt 1: Brainstorming mit Bob (interaktiv)
Fragen:
- Wie viele Episoden? (Wieder 10?)
- Neue Route oder gleiche Häfen vertiefen?
- Neue Nebenfiguren? (Hafenmeister, andere Kinder, neue Tiere?)
- Neues Setting? (Andere Jahreszeit? Winterpause?)
- Soll Adam wieder personalisiert vorkommen?
- Was sollen die Kinder diesmal lernen? (Moral-Themen)

### Schritt 2: Recherche der neuen Orte
Für jeden neuen Hafen/Ort recherchiere ich im selben Detail-Level wie Sonderborg:
- Lage & Gesamtanlage
- Gebäude & Einrichtungen (nummeriert, West→Ost)
- Freizeit & Natur
- Technische Einrichtungen
- Hafenpreise
- Orientierung für die Geschichten

### Schritt 3: Welt-Bibel aufteilen und erweitern
- `welt_bible_kurz.md` erstellen (<80 Zeilen, KI-ready)
- `welt_bible_detail.md` aus aktueller `world_bible.md` + neue Recherche
- Neue Orte einfügen

### Schritt 4: Story Master Plan Reihe 2
- Episoden skizzieren mit Ort, Handlung, Moral, Figuren
- Kontinuität zu Reihe 1 wahren (Torge ist jetzt etwas älter? Sommerferien Teil 2?)

### Schritt 5: Generierung
Zwei Optionen:
- **Manuell:** Episode für Episode im Chat, Bob gibt Feedback
- **Autonom:** Pipeline-Skript (`run_pipeline.py`) jede Episode in eigener Session

### Schritt 6: Lektorat + Optimierung
- Pro Episode: 8-Dimensionen Prüfung per `optimierung_metaprompt.md`
- Anti-Patterns beachten (Samson denkt NICHT, keine Doppelkommas)
- Backup vor jedem Editieren

### Schritt 7: Metaanalyse Reihe 2
- Tabelle pro Episode
- Häufigste Fehler vs. Reihe 1
- Empfehlungen für Reihe 3

---

## Wichtige Lessons Learned aus Reihe 1 (immer beachten!)

1. **Samson denkt NICHT in Worten** — Verhalten zeigen, nie denken lassen
2. **Doppelkommas vermeiden** — Suche nach ", ," als schneller Test
3. **"rief" max 3x pro Episode** — danach Synonyme
4. **Satzlänge <=25 Wörter** für Zielgruppe 6-8 Jahre
5. **Moral muss natürlich aus der Handlung entstehen** — kein Lehrbuch am Ende
6. **Python-Skripte mit UTF-8 statt Patch-Tool** für deutsche Umlaute
7. **Eine Episode nach der anderen** — nicht parallel

---

## Nächster Schritt (wenn Bob zurück ist)

Brainstorming starten: "Produktivität oder Intimität?" → dann direkt in die Fragen oben einsteigen.
