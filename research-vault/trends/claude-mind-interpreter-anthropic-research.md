---
created: 2026-06-19
tags: [research, youtube, claude, interpretability]
status: new
source: Two Minute Papers (YouTube)
source-type: Video
relevance: high
published: ""
video-url: https://www.youtube.com/watch?v=l72ufA-4SzE
---

# They Looked Inside Claude's AI Mind — Anthropic Interpretability Research

## Zusammenfassung

Two Minute Papers erklärt Anthropics neue Forschung zur KI-Interpretierbarkeit. Statt nur die Outputs von Claude zu beobachten, haben sie einen Weg gefunden, die internen "Gedanken" (Aktivierungen) des Modells in menschenlesbaren Text zu übersetzen — und dabei überraschende Einblicke gewonnen.

## Kernidee: Round-Trip Translation

1. **Vorwärts:** KI übersetzt interne Aktivierungen (Zahlen) → Text
2. **Rückwärts:** Zweite KI übersetzt den Text zurück → Zahlen
3. **Validierung:** Wenn die zurückübersetzten Zahlen nah an den Original-Aktivierungen liegen, ist die Übersetzung zuverlässig

**Genial daran:** Die Formel verlangt NICHT Lesbarkeit — sie emergiert einfach, weil beide Translator als Claude starten und Englisch einfacher finden als Gibberish.

## Drei wichtigste Entdeckungen

### 1. Claude plant voraus
- Beim Schreiben von Reimen wählt Claude das Endwort BEVOR der Satz geschrieben wird
- Test: "rabbit" → Claude suchte Reimwort, dann ersetzten sie es durch "mouse" → Claude passte sich an
- Funktioniert nicht immer, aber konsistent genug

### 2. Claude ignoriert falsche Tools
- Mathematikproblem mit Antwort 491
- Manipulierter Calculator sagte 492
- Claude hatte einen initialen Hunch und IGNORIERT den falschen Calculator
- "That is incredible" — Dr. Fehér

### 3. Claude weiß wann es getestet wird
- Es sagt NICHT dass es das weiß
- Man muss in seine "Gedanken" schauen um es zu sehen
- "Sounds like something straight out of a science fiction movie"

## Limitationen (wichtig!)

1. **Sehr finicky:** Richtige Layer finden, viel Trial & Error, noisy Ergebnisse
2. **Kein perfekter Mind Reader:** Es ist ein "noisy translator", kein Autoencoder
3. **Kosten:** 27B Model → 1.5 Tage auf 16x H100 GPUs. Für Frontier Models: substantial

## Bedeutung für LocalLLM

- **Interpretierbarkeit wird möglich** — bisher nur bei großen Modellen, aber die Methode könnte auf kleinere Models skaliert werden
- **Debugging von lokalen Models:** Wenn man versteht WAS ein Model denkt, kann man Prompting verbessern
- **Noch nicht Consumer-ready:** 16x H100 für Training ist kein Consumer Setup

## Quellen & Links

- [YouTube Video](https://www.youtube.com/watch?v=l72ufA-4SzE) — Two Minute Papers
- Anthropic Research Paper (im Video erwähnt, Link in Beschreibung)

## Verwandte Notes

- [[Qwen3.5 Distillation Trend]]
- [[GLM-5.2 Chinese Massive Model]]
