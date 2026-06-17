---
title: "Lokale LLMs vergleichen: So findest du das richtige Model fuer dich"
category: model-review
status: draft
date: 2026-06-17
---

# Lokale LLMs vergleichen: So findest du das richtige Model fuer dich

Du hast dir eine GPU gekauft. Oder nutzt die, die eh schon im Rechner steckt. Du installierst LM Studio oder Ollama — und landest vor der groessten Frage aller Local-LLM-Anfänger:

**Welches Model soll ich nehmen?**

HuggingFace hat ueber 100.000 Modelle. Die Community postet taeglich neue Benchmarks. Und trotzdem: Das Model, das auf dem Benchmark-Thron sitzt, laeuft bei dir vielleicht schlechter als die Haelfte davon.

Warum? Weil Benchmarks nicht deine Nutzung abbilden. Hier zeige ich dir, wie du selbst vergleichst — mit deiner Hardware, fuer deinen Use-Case.

---

## 1. Benchmark vs. Praxis: Warum Zahlen luegen koennen

### Was Benchmarks messen

Die bekannten Benchmarks (MMLU, GSM8K, HumanEval) testen spezifische Faehigkeiten:

- **MMLU** — Allgemeinwissen in Multiple-Choice-Fragen
- **GSM8K** — Mathematik und logisches Reasoning
- **HumanEval** — Code-Generierung

Ein Model kann MMLU=85 erreichen und trotzdem bei Rollenspiel oder kreativem Schreiben schlecht sein. Benchmarks messen *Breite*, nicht *Tiefe* in deinem Anwendungsfall.

### Was du stattdessen misst

Statt nach Benchmark-Zahlen zu suchen, stell dir diese Fragen:

**Frage 1: Was will ich damit machen?**
- Chat und Begleitung? → Fokus auf Persona-Konsistenz und Ton
- Code schreiben? → HumanEval + eigene Tests mit deinem Tech-Stack
- Texte verfassen? → Langkontext, Stiluebernahme, Kreativitaet
- Alles ein bisschen? → Dann brauchst du ein Allrounder-Model

**Frage 2: Welche Hardware habe ich?**
- RTX 3060 (12GB VRAM)? → Max ~13B Parameter bei Q4_K_M Quantisierung
- RTX 3090/4090 (24GB VRAM)? → Bis ~35B Parameter, oder 70B stark quantisiert
- Nur CPU? → Bleib unter 14B, nutze Q2/Q3 Quantisierung

**Frage 3: Wie schnell muss es sein?**
- Echtzeit-Chat? → Tokens/sec > 20 ist angenehm
- Hintergrund-Jobs (Texte schreiben, Code generieren)? → 5-10 tok/s reicht

---

## 2. Einfache Tests die jeder zu Hause machen kann

Du brauchst keine Benchmark-Suite. Drei Tests reichen fuer einen ersten Eindruck:

### Test A: Der "Erzaehle mir etwas" Test (Kreativitaet)

Prompt: *"Schreib eine kurze Geschichte ueber einen Hund, der zum ersten Mal Schnee sieht."*

Was du beobachtest:
- **Originalitaet:** Ist es generisch oder hat es Charakter?
- **Sprache:** Fliesst der Text natuerlich?
- **Laenge:** Haltet das Model die Struktur durch, oder verliert es den Faden?

### Test B: Der "Erklaer mir" Test (Verstaendnis)

Prompt: *"Erklaer mir, wie Quantencomputer funktionieren, als waere ich 12 Jahre alt."*

Was du beobachtest:
- **Anpassungsfahigkeit:** Passt das Model den Ton an die Zielgruppe an?
- **Genauigkeit:** Ist der Inhalt korrekt oder halluziniert es?
- **Struktur:** Nutzt es Analogien? Bleibt es logisch?

### Test C: Der "Mach das fuer mich" Test (Anweisungen folgen)

Prompt: *"Erstelle eine Tabelle mit 5 Python-Bibliotheken fuer Datenanalyse. Spalten: Name, Hauptzweck, Lernkurve (einfach/mittel/hart)."*

Was du beobachtest:
- **Format-Treue:** Hält es sich an die Tabellenvorgabe?
- **Vollstaendigkeit:** Sind alle 5 Zeilen und 3 Spalten da?
- **Inhalt:** Sinnvolle Auswahl oder Zufallswahl?

---

## 3. Aktuelle Top-Modelle fuer lokale Nutzung (Juni 2026)

**Mein Setup:** AMD Ryzen Threadripper PRO 3945WX (12 Kerne), 4x NVIDIA GPUs (inkl. RTX 3090 mit 24GB VRAM), 125 GB RAM, LM Studio als Haupt-Inference-Engine.

### Qwen3-32B — Der aktuelle Allrounder-Koenig

**Release:** 2025 | **Lizenz:** Apache 2.0 | **Parameter:** 32B

**Staedke:**
- Sehr stark im Reasoning und Code-Generierung
- Ausgezeichnete Deutsch-Sprachunterstuetzung
- Hält Kontext gut ueber lange Konversationen (128K Kontextfenster)
- Bei 32B noch schnell genug auf RTX 3090 mit Q6 Quantisierung (~15-20 tok/s)
- Apache 2.0 Lizenz — kommerziell nutzbar ohne Einschränkungen

**Schwaechen:**
- Braucht ~20GB VRAM bei Q6 — auf kleineren Karten muss man zu Q4 runtergehen
- Kreativschreiben ist gut, aber nicht herausragend

**VRAM-Anforderung:** Q6 = ~20GB | Q5 = ~17GB | Q4 = ~14GB

### Qwen3.6-27B — Multimodal mit Vision

**Release:** April 2026 | **Lizenz:** Apache 2.0 | **Parameter:** 28B (gesamt)

**Staedke:**
- Kann BILDER verstehen und beschreiben (Image-Text-to-Text)
- Solide Text-Leistung, leicht unter Qwen3-32B
- Perfekt fuer Use-Cases wo du Bilder analysieren musst
- Noch kompakter als 32B — passt auf mehr Hardware

**Schwaechen:**
- Reiner Text: Qwen3-32B ist etwas besser
- Vision-Faehigkeit braucht etwas mehr VRAM

**VRAM-Anforderung:** Q6 = ~18GB | Q5 = ~15GB | Q4 = ~12GB

### Llama 4 Scout 17B — Massives Kontextfenster

**Release:** 2025 | **Lizenz:** Llama 4 Community | **Parameter:** 17B

**Staedke:**
- **10 Millionen Token Kontextfenster** — das ist enorm!
- Multimodal: kann auch Bilder verarbeiten
- Sehr effizient fuer seine Groesse
- Laeuft fluessig auf 16GB VRAM Karten

**Schwaechen:**
- Llama 4 Lizenz erfordert Genehmigung bei grosser Nutzerzahl (>700M MAU)
- Bei komplexem Reasoning hinter Qwen3 zurueck
- Deutsch ist OK, aber nicht so natuerlich wie Qwen

**VRAM-Anforderung:** Q6 = ~12GB | Q5 = ~10GB | Q4 = ~8GB

### Granite 3.3 8B — Der Geschwindigkeits-Meister

**Release:** 2025 | **Lizenz:** Apache 2.0 | **Parameter:** 8B

**Staedke:**
- **Extrem schnell: bis zu 633 tok/s** gemessen auf Artificial Analysis
- Laeuft auf ALLEM: 6GB VRAM, sogar CPU-only machbar
- Ueberraschend gut fuer die kleine Groessenklasse
- Apache 2.0 — voll kommerziell nutzbar

**Schwaechen:**
- Bei komplexen Aufgaben klar unterlegen gegen 32B+ Modelle
- Halluziniert haeufiger bei Faktenfragen
- Eher fuer einfache Tasks und schnelle Antworten geeignet

**VRAM-Anforderung:** Q6 = ~7GB | Q5 = ~6GB | Q4 = ~5GB

### Llama 3.1 8B — Der bewaehrte Einsteiger-Freund

**Release:** Sept 2024 | **Lizenz:** Llama 3 Community | **Parameter:** 8B

**Staedke:**
- Sehr gut dokumentiert und getestet
- Grosses Ollama/LM Studio Support
- Solide fuer einfache Chat-Aufgaben
- Laeuft auf fast jeder Hardware

**Schwaechen:**
- Veraltet im Vergleich zu Qwen3 und Granite 3.3
- Bei komplexen Aufgaben klar unterlegen
- Llama Lizenz mit Einschränkungen

**VRAM-Anforderung:** Q6 = ~7GB | Q5 = ~6GB | Q4 = ~5GB

---

## 4. Quantisierung: Was verlierst du wirklich?

Quantisierung reduziert den Speicherbedarf, indem sie die Praezision der Gewichte verringert. Aber was kostet das?

| Quantisierung | Speicher (35B Model) | Qualitaetsverlust | Empfindung |
|---|---|---|---|
| Q8_0 | ~20 GB | Minimal | Fast wie Original |
| Q6_K_XL | ~16 GB | Kaum spuerbar | Mein Sweet Spot |
| Q5_K_M | ~14 GB | Leicht bei Nuancen | Immer noch sehr gut |
| Q4_K_M | ~12 GB | Spuerbar bei komplexen Aufgaben | Noch brauchbar |
| Q3_K_M | ~10 GB | Deutlich | Nur fuer schnelle Tests |
| Q2_K | ~8 GB | Stark | Oft nicht mehr nutzbar |

**Meine Regel:** Geh nie unter Q4_K_M, es sei denn, du hast keine Wahl. Der Unterschied zwischen Q6 und Q4 ist bei kreativem Text spuerbar — Q4 wird "flacher" und wiederholter.

---

## 5. Fazit: So waehlst du dein Model (Juni 2026)

1. **Definiere deinen Use-Case** — Chat, Code, Writing, Bilder verstehen?
2. **Check deine Hardware** — VRAM ist der Flaschenhals
3. **Test mit den drei Prompts oben** — das sagt mehr als jeder Benchmark
4. **Starte mit Q6/Q5 Quantisierung** — runtergehen kannst du immer noch
5. **Wechsle nicht zu oft** — lerne ein Model kennen, bevor du das naechste probierst

### Konkrete Empfehlungen nach Hardware:

| Hardware | Empfohlenes Model | Quantisierung | VRAM |
|----------|-------------------|---------------|------|
| RTX 3090/4090 (24GB) | Qwen3-32B | Q6 | ~20GB |
| RTX 3080/4070 (10-12GB) | Llama 4 Scout 17B | Q5 | ~10GB |
| RTX 3060 (12GB) | Granite 3.3 8B | Q6 | ~7GB |
| 6GB VRAM / CPU | Granite 3.3 8B | Q4 | ~5GB |

**Mein aktueller Favorit:** **Qwen3-32B bei Q6 Quantisierung** auf der RTX 3090. Es ist der beste Allrounder fuer die meisten Aufgaben — stark im Reasoning, gute Deutsch-Unterstuetzung, und Apache 2.0 Lizenz bedeutet keine kommerziellen Einschraenkungen.

Fuer Use-Cases wo du **Bilder verstehen** musst: **Qwen3.6-27B** ist aktuell die beste Wahl. Und wenn du **extrem lange Dokumente** verarbeiten musst: **Llama 4 Scout 17B** mit seinem 10M-Token-Kontextfenster hat keine Konkurrenz.

---

*Dieser Artikel basiert auf eigenen Tests mit Threadripper PRO + NVIDIA GPU Hardware. Alle Benchmarks und Eindrücke stammen aus dem praktischen Einsatz, nicht aus Benchmark-Suiten.*
