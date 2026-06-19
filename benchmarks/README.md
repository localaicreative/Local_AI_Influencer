# Automatisiertes 2-System LLM Benchmarking

## Konzept

**Zwei Systeme, gegenseitiges Testing:**
- **Lena** (Threadripper PRO + 4x GPU) — Controller / Executor
- **Ava** (i7 + RTX 4060 Ti/2070) — Controller / Executor

**Cross-Testing Mode:**
- System A triggert Tests → System B führt aus → System A observiert & bewertet
- Dann umgekehrt → beide Perspektiven im Ergebnis

## Architektur

```
┌─────────────┐         SSH          ┌─────────────┐
│   LENA      │ ◄──────────────────► │     AVA     │
│ Threadripper│                       │  i7-4790    │
│ 4x GPU      │  trigger/observe      │ RTX 4060 Ti │
│ Controller  │ ──────────────────►   │ Executor    │
└─────────────┘                       └─────────────┘

Results → SQLite DB → Live HTML Table (online)
```

## Test-Kategorien

### 1. Inference Performance
- Tokens/sec pro Modelgröße (7B, 13B, 35B, 70B+)
- Latenz (erste Token)
- VRAM/RAM Verbrauch

### 2. Quality Benchmarks
- GSM8K (Mathematik)
- MMLU (Allgemeinwissen)
- HumanEval (Coding)
- Eigene Prompts (Roleplay, Writing, Translation)

### 3. Real-World Tasks
- "Schreib ein Kinderbuch Kapitel" → Bewertung
- "Debug diesen Python Code" → Korrektheits-Check
- "Fasse diesen Artikel zusammen" → Qualität

## Dateistruktur

```
benchmarks/
├── runner/           ← Benchmark-Runner Skripte
│   ├── run_local.py  ← Tests auf lokalem System
│   └── run_remote.py ← Tests via SSH auf anderem System
├── tests/            ← Standardisierte Test-Suiten
│   ├── inference/    ← Performance-Tests
│   ├── quality/      ← Quality-Benchmarks
│   └── realworld/    ← Real-World Tasks
├── results/          ← Ergebnisse
│   ├── lena/         ← Lena's Ergebnisse
│   │   └── 2026-06-18.json
│   └── ava/          ← Ava's Ergebnisse
├── db/               ← SQLite Datenbank
└── output/           ← Generierte HTML Tabellen
```

## Status
- [ ] Runner-Skripte implementieren
- [ ] Test-Suite definieren
- [ ] SQLite DB Schema erstellen
- [ ] HTML Output Generator bauen
- [ ] Auto-Update Pipeline (cron auf Ava)
