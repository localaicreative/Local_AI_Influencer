---
created: 2026-06-19
tags: [trend, local-llm, qwen]
status: new
sources:
  - https://huggingface.co/models?sort=trending
---

# Qwen3.5 Distillation Trend — Claude-Style Reasoning Models

## Zusammenfassung

Qwen3.5-27B wurde als "Claude 4.6 Opus Reasoning Distilled" auf HuggingFace hochgeladen und hat innerhalb weniger Tage 2882 Likes erreicht. Dies zeigt einen klaren Trend: Community distilliert proprietäre Reasoning-Fähigkeiten in lokale, offene Models.

## Bedeutung für LocalLLM

- **Demokratisierung von Reasoning:** Bisher nur bei Closed-Source Modellen (Claude, GPT) verfügbar
- **Lokale Inferenz möglich:** 27B Model läuft auf Consumer GPUs mit Q4-Q8 Quantisierung
- **Community-getrieben:** Keine offizielle Freigabe von Anthropic — Community reverse-engineert Fähigkeiten

## Aktueller Stand

| Model | Likes | Parameter | Status |
|-------|-------|-----------|--------|
| Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled | 2882 | 27B | Aktiv, Community-maintained |
| Qwen/QwQ-32B | 2931 | 32B | Offiziell von Qwen Team |
| Qwen/Qwen3.6-35B-A3B | 2166 | 35B | Aktiv, neue Architektur |

## Hardware-Anforderungen (geschätzt)

| Quantisierung | VRAM Minimum | Empfohlene GPU |
|--------------|-------------|----------------|
| Q4_K_M | ~18GB | RTX 3090/4090 |
| Q5_K_M | ~22GB | RTX 4090 + CPU RAM |
| Q6_K | ~26GB | Multi-GPU Setup |

## Quellen & Links

- [HuggingFace Trending Models](https://huggingface.co/models?sort=trending)
- [Qwen3.5 Distilled Model Page](https://huggingface.co/Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled)

## Verwandte Notes

- [[ ]]
- [[ ]]
