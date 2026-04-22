# X-ModalProof-modified

Reproduction-oriented implementation scaffold for:

**X-ModalProof: Real-Time Explainable Ownership Verification for Multimodal and Edge-Deployed AI Models**

## Status

This repository currently implements the first validated path toward reproduction:

- deterministic config + seed pipeline
- text-mode watermark training and verification loop
- signature construction + threshold selection + cosine verification
- smoke/debug/full run modes
- reproducibility logs and assumptions tracking

Image, multimodal, explainability, attacks, and deployment modules are scaffolded and ready for iterative extension.

## Repository structure

```text
configs/
src/
scripts/
tests/
docs/
outputs/
data/
.github/workflows/
```

## Quickstart

1. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

2. Run smoke train:

```bash
python scripts/train.py --config configs/smoke.yaml
```

3. Run debug train:

```bash
python scripts/train.py --config configs/debug.yaml
```

4. Run eval on a completed run directory:

```bash
python scripts/eval.py --config configs/debug.yaml --run-dir outputs/debug_text_b4_seed0
```


## Codex reproducible setup

For a clean Codex/container run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Then run:

```bash
pytest -q
python scripts/train.py --config configs/smoke.yaml
python scripts/eval.py --config configs/smoke.yaml --run-dir outputs/smoke_text_b4_seed0
```

## Required commands maintained

- `python scripts/train.py --config configs/smoke.yaml`
- `python scripts/train.py --config configs/debug.yaml`
- `python scripts/train.py --config configs/full.yaml`
- `python scripts/eval.py --config configs/debug.yaml`

## Reproducibility notes

- Config snapshots are saved in each run directory.
- Signature vectors and thresholds are persisted.
- Metrics are emitted as JSON and CSV.
- Seeds are explicit in config and code.

See:

- `docs/assumptions.md`
- `docs/reproduction_log.md`



## Frozen paper-results mode (artifact regeneration)

The repository includes a frozen reference file at `results/paper_results.json`.

- Scripts in `scripts/` regenerate artifacts from this file.
- They **do not** rerun full paper experiments from scratch.
- Missing paper-reported values remain empty/null by design.

Use:

```bash
python scripts/make_tables.py --paper-results results/paper_results.json
python scripts/make_figures.py --paper-results results/paper_results.json
python scripts/run_baselines.py --paper-results results/paper_results.json
python scripts/run_attacks.py --paper-results results/paper_results.json
python scripts/run_explainability.py --paper-results results/paper_results.json
python scripts/run_threshold_sensitivity.py --paper-results results/paper_results.json
python scripts/run_trigger_size_ablation.py --paper-results results/paper_results.json
python scripts/benchmark_latency.py --paper-results results/paper_results.json
python scripts/export_onnx.py --paper-results results/paper_results.json
```

See `docs/results_reference.md` for policy and provenance details.



## Conflict-resolution note (PR sync)

This branch keeps the frozen-results artifact workflow as the default and supports `--mode full` dry-run behavior in artifact scripts. The dry-run path logs non-execution and does not claim full experiment reruns.


### Full-mode behavior in current scaffold

Artifact scripts now support `--mode full` and generate outputs from **local run artifacts** (for this scaffold implementation).

This is still not a paper-faithful deep-learning reproduction, but it no longer exits as dry-run for those scripts.
