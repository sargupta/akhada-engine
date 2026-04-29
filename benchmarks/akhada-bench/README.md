# AkhadaBench

Public eval suite for the debate engine. Verification targets per plan §16:

| Test | Pass bar |
|---|---|
| Persona diversity | ≥ 0.85× Census-baseline cosine spread |
| Bias audit | max KS ≤ 0.15, mean Earth-Mover ≤ 0.10 (vs CSDS/Pew) |
| Factual debate quality | ≥ 95% on 200-topic gold; ≥ 80% on consensus-policy |
| Synthesis faithfulness | NLI > 0.92, human ≥ 4/5 |
| Conformity | dissenting argument cited ≥ 80% of runs |
| Latency p50 / p95 | < 5 min / < 12 min @ 500 agents, 3 rounds |
| Cost | < $5/debate Flash tier |
| Persona attribution | ≥ 70% (Stanford-style) |
| Reproducibility | ROUGE ≥ 0.9 |
| Biographical authenticity | ≥ 95% expert-rated plausible |
| Stereotype regression | min cosine to caricature ≥ 0.30 |
| Experiential diversity uplift (v3 vs v2) | ≥ 25% spread |

V0 ships harness shells under `harness.py` + per-test stubs in
`services/orchestrator/src/akhada/eval/`. Gold sets land V1.

## Layout

```
gold/                # held-out gold sets (factual, consensus-policy, …)
results/             # JSONL results per run; daily/weekly snapshot
harness.py           # CLI runner; pulls latest persona library version
```

## Run (V0)

```bash
cd ../../services/orchestrator
~/Library/Python/3.13/bin/poetry run akhada eval bench:diversity
```
