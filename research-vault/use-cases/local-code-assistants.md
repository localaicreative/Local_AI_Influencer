---
created: 2026-06-19
tags: [use-case, coding]
status: new
sources:
  - https://github.com/search?q=local+llm&type=repositories
---

# Use-Case: Lokale Code-Assistenten mit LLMs

## Was macht der User?

Entwickler nutzen lokale LLMs als Code-Assistenten — alternativ zu GitHub Copilot/ChatGPT. Vorteile: Privatsphäre (kein Code verlässt die Maschine), keine API-Kosten, funktioniert offline.

## Benötigte Hardware

| Komponente | Minimum | Empfohlen |
|-----------|---------|-----------|
| GPU | RTX 3060 12GB | RTX 4090 24GB |
| RAM | 32GB | 64GB+ |
| Storage | 500GB NVMe | 1TB+ NVMe |

## Genutzte Models/Tools

- **Model:** Qwen2.5-Coder-32B-Instruct (2046 likes auf HuggingFace)
- **Tooling:** Ollama, LM Studio, oder vLLM für Server-Setup
- **Prompting:** System prompt mit Coding-Konventionen + Context aus aktuellen Dateien

## Ergebnisse & Performance

| Model | Tokens/sec (RTX 4090) | Code-Qualität | VRAM |
|-------|----------------------|---------------|------|
| Qwen2.5-Coder-32B (Q4) | ~8-12 | Hoch, gut für Python/JS | ~20GB |
| Mistral-7B-Instruct (Q8) | ~25-35 | Mittel, schnell aber weniger kontextbewusst | ~8GB |

**Community-Feedback:** Qwen-Coder Models werden als "Copilot-Ersatz" empfohlen. 32B Model bietet beste Balance zwischen Qualität und Geschwindigkeit auf Consumer Hardware.

## Quellen & Links

- [GitHub Local LLM Repos](https://github.com/search?q=local+llm&type=repositories)
- [Qwen2.5-Coder on HuggingFace](https://huggingface.co/Qwen/Qwen2.5-Coder-32B-Instruct)

## Verwandte Notes

- [[RTX 4090 Single GPU Workhorse]]
- [[ ]]
