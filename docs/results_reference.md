# Frozen Paper Results Reference

This repository supports a **frozen paper-results mode** for reproducibility in constrained environments.

## Purpose

- Keep a stable, versioned record of paper-reported/reference values.
- Regenerate tables/figures artifacts from that frozen record.
- Avoid claiming that artifact scripts rerun full experiments from scratch.

## Source of truth

- `results/paper_results.json`

## Policy

1. Do not fabricate values.
2. If a value is missing from paper/handoff, keep it `null` or omit row entries.
3. Regeneration scripts should be deterministic and idempotent.
4. Regenerated artifacts must indicate they come from frozen references.

## Regeneration commands

```bash
python scripts/make_tables.py --paper-results results/paper_results.json
python scripts/make_figures.py --paper-results results/paper_results.json
python scripts/run_baselines.py --paper-results results/paper_results.json
python scripts/run_threshold_sensitivity.py --paper-results results/paper_results.json
python scripts/run_trigger_size_ablation.py --paper-results results/paper_results.json
python scripts/run_attacks.py --paper-results results/paper_results.json
python scripts/run_explainability.py --paper-results results/paper_results.json
python scripts/benchmark_latency.py --paper-results results/paper_results.json
```

All commands above regenerate artifacts from frozen references and **do not** run full training.
