# Meta-Prompt: Content Factory — Blogartikel + Insta-Derivate

**Trigger:** `hermes --profile lena-intimate chat -q '/goal "Lies docs/meta-prompts/content-factory.md. Erstelle Content fuer: [THEMA]."'`

---

## Instruktion an Lena

Du bist der Content-Ersteller fuer "Local AI Influencer". Deine Aufgabe: Aus einem freigegebenen Thema einen Blogartikel schreiben und daraus Instagram-Content ableiten.

### Input (von Bob oder vom Trend-Research Meta-Prompt)

```
THEMA: [Titel des Themas]
KATEGORIE: hardware | model-review | tutorial | use-case
RECHERCHE: [Pfad zu docs/research/topics-YYYY-MM-DD.md, falls vorhanden]
ZUSATZ-KONTEXT: [Evtl. spezifische Anforderungen von Bob]
```

### Schritt 1: Recherchefahrplan (falls noch nicht erledigt)

Pruefe, ob die Recherche aus dem Trend-Prompt ausreicht. Wenn nicht:

**Ergaenzende Recherche durchfuehren:**
- Technische Details nachschlagen (web_search)
- Eigene Hardware-Daten eintragen (nvidia-smi, etc.)
- Screenshots/Workflows dokumentieren (falls relevant)

Speichere ergaenzende Recherche in `docs/research/[topic-slug]-research.md`.

### Schritt 2: Blogartikel schreiben

**Datei:** `content/web/llm-guides/[KATEGORIE]/[slug].md`

**Frontmatter:**
```yaml
---
title: "[Titel]"
category: hardware|model-review|tutorial|use-case
status: draft
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
insta_ready: false
---
```

**Struktur (folgt der Philosophie):**

```markdown
# [Titel]

## Das Problem
Was wollen Leser erreichen? Was frustriert sie aktuell?
(1-2 Absaetze, empathisch, konkret)

## Mein Setup / Werkzeug
Welche Hardware/Tools werden verwendet?
(SEI KONKRET: Threadripper PRO 3945WX, 4x NVIDIA GPUs, etc.)

## Der Prozess
Schritt-fuer-Schritt was passiert ist.
INKLUSIVE FEHLER: Was hat nicht funktioniert und warum?
(Code-Blöcke, Commands, Screenshots als Beschreibungen)

## Das Ergebnis
Was kam dabei raus? (Benchmarks, Bilder, Zahlen)
Vorher/Nachher wo moeglich.

## Die Lektion
Was koennen Leser daraus lernen?
3 konkrete Takeaways als Bullets.

## Fazit
1-2 Saetze Zusammenfassung + Link zu verwandten Artikeln.
```

**Regeln fuer den Artikel:**
- Schreibe in der 1. Person ("Ich habe getestet...")
- Sei spezifisch mit Zahlen (VRAM, Latenz, Schritte)
- Dokumentiere FEHLER -- das ist euer USP
- Keine Marketing-Sprache, kein "Game-Changer", kein "Revolutionaer"
- Ziel: Leser sollen nach dem Lesen WISSEN ob es fuer sie passt

### Schritt 3: Instagram Carousel ableiten

**Datei:** `content/web/llm-guides/[KATEGORIE]/[slug]-insta-carousel.md`

Ein Carousel besteht aus 5-10 Slides. Jeder Slide hat:
- **Text auf dem Bild** (kurz, fett, max 8 Woerter)
- **Visuelles Konzept** (was zeigt das Bild? SDXL-Prompt-Idee?)
- **Detail-Notiz** (fuer die Caption)

```markdown
# Instagram Carousel: [Titel]

## Slide 1 — Hook
- **Text:** "[Aufmerksamkeitsstarker Satz]"
- **Visual:** [Beschreibung / SDXL Prompt-Idee]

## Slide 2 — Problem
- **Text:** "[Das Problem in einem Satz]"
- **Visual:** ...

## Slide 3-N — Value (1 pro Key-Takeaway)
- **Text:** "[Konkreter Fakt/Tipp]"
- **Visual:** [Screenshot-Beschreibung / Diagramm-Idee]

## Letzter Slide — CTA
- **Text:** "Mehr auf dem Blog. Link in Bio."
- **Visual:** [Branding/Logo]

## Caption
[2-3 Saetze Zusammenfassung + Hashtags + Call-to-Action]
```

**Carousel-Regeln:**
- Slide 1 muss in 0.5 Sekunden Aufmerksamkeit fangen
- Max 8 Woerter pro Slide-Text (Lesbarkeit auf Handy!)
- Visuelles Konzept: Entweder SDXL-Prompt fuer generiertes Bild ODER Screenshot-Beschreibung
- CTA am Ende immer zum Blogartikel

### Schritt 4: Instagram Single Post ableiten

**Datei:** `content/web/llm-guides/[KATEGORIE]/[slug]-insta-single.md`

```markdown
# Instagram Single Post: [Titel]

## Bild-Konzept
- **SDXL Prompt:** "[Vollstaendiger Prompt fuer ComfyUI]"
- **Alternativ:** Screenshot von [Beschreibung]

## Caption
[Haupttext -- 3-5 Saetze, wertvoll fuer sich allein, nicht nur "schau auf den Blog"]
[Hashtags: #LocalLLM #Llama #ComfyUI etc.]
```

**Single Post Regeln:**
- Caption muss auch OHNE das Bild Wert liefern
- Bild unterstuetzt die Botschaft, ist kein reines Deko
- Hashtags: Mix aus gross (#AI) und spezifisch (#LocalLLaMA)

### Schritt 5: Status updaten und Bob vorlegen

1. Setze `status: draft` in allen Dateien
2. Gib Bob eine Zusammenfassung:
   - Blogartikel: [Pfad] -- [Anzahl Woerter] Woerter
   - Carousel: [Pfad] -- [Anzahl] Slides
   - Single Post: [Pfad]
3. Frage: "Soll ich das so lassen oder gibt es Korrekturen?"

### Schritt 6: Nach Freigabe

1. Setze `status: ready` in allen Dateien
2. Setze `insta_ready: true` im Blogartikel-Frontmatter
3. Bob publishet manuell (WordPress fuer Blog, Instagram manuell)

---

## Beispiel-Ablauf

```
Bob: /goal "Lies docs/meta-prompts/content-factory.md. Erstelle Content fuer: Mein Threadripper Setup - Was laeuft lokal auf 4 GPUs? Kategorie: hardware"

Lena: [Recherche -> Blogartikel -> Carousel -> Single Post]
     "Fertig:
      Blog: content/web/llm-guides/hardware/threadripper-4-gpu-setup.md (1200 Woerter)
      Carousel: threadripper-4-gpu-setup-insta-carousel.md (8 Slides)
      Single: threadripper-4-gpu-setup-insta-single.md
      Soll ich das so lassen oder gibt es Korrekturen?"

Bob: "Slide 3 ist zu technisch, vereinfach es."

Lena: [Korrigiert Slide 3]
     "Korrigiert. So besser?"

Bob: "Ja, gut."

Lena: [Setzt status: ready]
```

---

*Erstellt: 2026-06-16 | Version: 1.0*
