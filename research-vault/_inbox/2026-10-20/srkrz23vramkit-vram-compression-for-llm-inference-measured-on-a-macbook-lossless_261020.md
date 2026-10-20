---
created: 2026-10-20
tags: [research, auto-generated]
status: new
source: GitHub Trending
source-type: Code
attention-score: 12
blog-potential: low
url: https://github.com/SRKRZ23/vramkit
---

# SRKRZ23/vramkit — VRAM compression for LLM inference, measured on a MacBook: lossless weight codec (-33% vs 4-bit on r

## Zusammenfassung

VRAM compression for LLM inference, measured on a MacBook: lossless weight codec (-33% vs 4-bit on real Qwen weights, beats zstd) + drop-in PyTorch KV-cache compression. Key finding: quantize KV keys per-CHANNEL (not per-token) -> int8 KV near-lossless, +0.1% real perplexity at 2x. ROCm/CUDA/MPS/CPU.

## Quelle

- **Feed:** [GitHub Trending](https://github.com/SRKRZ23/vramkit)
- **Typ:** Code
- **Attention Score:** 12pts
- **Blog-Potenzial:** LOW

## Nchste Schritte

- [ ] Deep Dive durchfuhren falls Score >= 30
- [ ] In richtige Kategorie verschieben falls notig
- [ ] Backlinks zu verwandten Notes hinzufugen

## Verwandte Notes

- [[ ]]
