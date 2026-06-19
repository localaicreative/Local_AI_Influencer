# Model-Recherche — Juni 2026

**Datum:** 2026-06-17
**Quelle:** HuggingFace, Artificial Analysis, Browser-Recherche

---

## Aktuelle Top-Modelle fuer lokale Nutzung (Juni 2026)

### Qwen3 Familie (Alibaba/Qwen)

| Model | Parameter | Release | Lizenz | VRAM (Q6) | Besonderheiten |
|-------|-----------|---------|--------|-----------|----------------|
| Qwen3-0.6B | 0.8B | Jul 2025 | Apache 2.0 | ~1GB | Edge Devices, extrem schnell |
| Qwen3-8B | 8B | Jul 2025 | Apache 2.0 | ~7GB | Einsteiger-Freundlich |
| Qwen3-32B | 32B | 2025 | Apache 2.0 | ~20GB | **Allrounder-Koenig**, 128K Kontext |

**Qwen3-32B Details:**
- Sehr stark im Reasoning und Code
- Ausgezeichnete Deutsch-Sprachunterstuetzung
- 128K Kontextfenster
- Apache 2.0 — voll kommerziell nutzbar
- HF: `Qwen/Qwen3-32B`

---

### Gemma 4 Familie (Google DeepMind)

| Model | Parameter | Release | Lizenz | VRAM (Q6) | Besonderheiten |
|-------|-----------|---------|--------|-----------|----------------|
| Gemma 4 E2B | 2B | 2025 | Apache 2.0 | ~2GB | Edge, Multimodal |
| Gemma 4 E4B | 4B | 2025 | Apache 2.0 | ~3GB | Edge, Multimodal |
| **Gemma 4 12B** | 12B | Jun 2026 | Apache 2.0 | ~8GB | **NEU! Multimodal Unified** |
| Gemma 4 26B A4B | 26B | 2025 | Apache 2.0 | ~17GB | MoE Architektur |
| Gemma 4 31B | 31B | 2025 | Apache 2.0 | ~20GB | Dense, hoechste Leistung |

**Gemma 4 12B-it Details (NEU!):**
- **Any-to-Any Multimodal:** Text, Audio, Image, Video Input → Text Output
- Encoder-free — kein separater Vision/Audio Encoder notwendig
- 256K Kontextfenster
- 140+ Sprachen
- Apache 2.0 Lizenz
- HF: `google/gemma-4-12B-it`
- **Perfekt fuer lokale Multimodal-Anwendungen**

---

### Llama Familie (Meta)

| Model | Parameter | Release | Lizenz | VRAM (Q6) | Besonderheiten |
|-------|-----------|---------|--------|-----------|----------------|
| Llama 3.1 8B | 8B | Sep 2024 | Llama 3 Community | ~7GB | Bewaehrt, grosser Support |
| Llama 3.1 70B | 70B | Sep 2024 | Llama 3 Community | ~45GB | Hochleistung |
| **Llama 4 Scout 17B** | 17B | 2025 | Llama 4 Community | ~12GB | **10M Token Kontext!** Multimodal |

**Llama 4 Scout 17B Details:**
- **10 Millionen Token Kontextfenster** — enorm!
- Multimodal: Image + Text Input
- Sehr effizient fuer seine Groesse
- Llama 4 Lizenz (Genehmigung bei >700M MAU)
- HF: `meta-llama/Llama-4-Scout-17B-16E-Instruct`

---

### Granite Familie (IBM)

| Model | Parameter | Release | Lizenz | VRAM (Q6) | Besonderheiten |
|-------|-----------|---------|--------|-----------|----------------|
| **Granite 3.3 8B** | 8B | 2025 | Apache 2.0 | ~7GB | **Extrem schnell: 633 tok/s** |

**Granite 3.3 8B Details:**
- Bis zu 633 tokens/sec gemessen (Artificial Analysis)
- Laeuft auf ALLEM — sogar CPU-only
- Apache 2.0 — voll kommerziell nutzbar
- Ueberraschend gut fuer die kleine Groesse
- Eher fuer einfache Tasks und schnelle Antworten

---

## Quellen & Verifikation

### HuggingFace (direkt besucht)
- `https://huggingface.co/models?sort=trending&author=Qwen` — Qwen3 Modelle
- `https://huggingface.co/models?sort=trending&search=gemma-4` — Gemma 4 Familie
- `https://huggingface.co/google/gemma-4-12B-it` — Gemma 4 12B Details
- `https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct` — Llama 4 Scout

### Artificial Analysis (Benchmark-Daten)
- Granite 3.3 8B: 633 tok/s Speed-Champion
- Intelligence Index: Claude Fable 5 > GPT-5.5 > GLM-5.2 > Gemini 3.1 Pro

---

## Was noch fehlt (benoetigt YouTube/Community Input)

1. **Echte Inference-Tests auf Consumer-Hardware** — VRAM, Latenz, tok/s
2. **Deutsch-Sprach-Tests** — welche Modelle sprechen am natuerlichsten Deutsch?
3. **Kreativschreiben-Vergleich** — Benchmarks messen das nicht
4. **Langzeit-Stabilitaet** — welche Modelle halten Kontext am besten ueber lange Sessions?

---

*Erstellt: 2026-06-17 | Naechste Aktualisierung: nach YouTube-Recherche von Bob*