---
created: 2026-06-19
tags: [hardware, config]
status: new
price-range: mid
sources:
  - https://huggingface.co/models?sort=trending
---

# RTX 4090 Single GPU — LocalLLM Workhorse 2026

## Systemuebersicht

| Komponente | Modell | Preis (ca.) |
|-----------|--------|-------------|
| CPU | AMD Ryzen 7 7800X3D oder Intel i7-14700K | €350-450 |
| GPU(s) | NVIDIA RTX 4090 24GB | €1.800-2.200 |
| RAM | 64GB DDR5 | €150-200 |
| Storage | 2TB NVMe SSD | €100-150 |
| PSU | 1000W 80+ Gold | €150-200 |
| **Gesamt** | | **€2.550-3.200** |

## Was laeuft darauf?

| Model | Groesse | Quantisierung | Performance (geschätzt) | VRAM-Verbrauch |
|-------|---------|--------------|------------------------|----------------|
| Qwen/QwQ-32B | 32B | Q4_K_M | ~8-12 tokens/sec | ~20GB |
| Qwen/Qwen3.6-35B-A3B | 35B | Q4_K_M | ~7-10 tokens/sec | ~22GB |
| Mistral-7B-Instruct-v0.3 | 7B | Q8_0 | ~25-35 tokens/sec | ~8GB |
| Gemma-4-12B-coder | 12B | Q6_K | ~15-20 tokens/sec | ~10GB |

## Quellen & Links

- [HuggingFace Trending Models](https://huggingface.co/models?sort=trending)
- [RTX 4090 Specs](https://www.nvidia.com/de-de/geforce/graphics-cards/40-series/geforce-rtx-4090/)

## Verwandte Notes

- [[Qwen3.5 Distillation Trend]]
- [[ ]]
