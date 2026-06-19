---
created: 2026-06-19
tags: [trend, local-llm, chinese-models]
status: new
sources:
  - https://huggingface.co/models?sort=trending
---

# GLM-5.2 — Chinas Antwort auf lokale LLMs

## Zusammenfassung

Zai Org hat GLM-5.2 (753B Parameter) auf HuggingFace veröffentlicht — eines der größten offenen Models überhaupt. Innerhalb von Stunden 4.31k Downloads und 1.42k Likes. Zeigt den Trend: Chinesische Tech-Firmen pushen massive offene Models für lokale Inferenz.

## Bedeutung für LocalLLM

- **Größtes offenes Model:** 753B Parameter — bisher war 70B-120B der Standard
- **Multi-GPU erforderlich:** Läuft NICHT auf Consumer Hardware ohne extreme Setup
- **Open Source Push:** China will unabhängige LLM-Infrastruktur aufbauen

## Aktueller Stand

| Model | Parameter | Downloads | Likes | Status |
|-------|-----------|-----------|-------|--------|
| zai-org/GLM-5.2 | 753B | 4.31k | 1.42k | Neu, <24h alt |
| Qwen/QwQ-32B | 32B | - | 2931 | Etabliert |

## Hardware-Anforderungen (geschätzt)

| Quantisierung | VRAM Minimum | Empfohlene GPU |
|--------------|-------------|----------------|
| Q4_K_M | ~450GB+ | Multi-GPU Cluster (8x A100/H100) |
| Q2_K | ~300GB+ | 4-6x RTX 4090 mit CPU Offloading |

**Realistisch für Consumer?** Nein. Nur für Server/Cluster relevant. Aber interessant als Benchmark und für Distillation kleinerer Models.

## Quellen & Links

- [HuggingFace Trending](https://huggingface.co/models?sort=trending)
- [GLM-5.2 Model Page](https://huggingface.co/zai-org/GLM-5.2)

## Verwandte Notes

- [[Qwen3.5 Distillation Trend]]
- [[ ]]
