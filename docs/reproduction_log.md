# Reproduction Log

## 2026-04-18 - Stage 1 scaffold + first validated path

### Completed
- Created repository scaffold for configs/src/scripts/tests/docs/outputs/data/.github/workflows.
- Implemented modular configuration loader and run directory setup.
- Implemented deterministic seed utility and run metadata capture.
- Implemented text pipeline baseline with:
  - synthetic text dataset module
  - trigger injection and splitting
  - text embedding model wrapper
  - watermark losses (alignment + separation)
  - signature computation
  - threshold selection by validation F1
  - verification engine
- Added train/eval scripts satisfying required command surface.
- Added smoke/debug/full configs and baseline B1-B4 config examples.
- Added unit tests for signature, losses, thresholding, verification, trigger split, and embedding shapes.

### Deviations / blockers
- AG News/HuggingFace data ingestion is not yet wired in this initial commit; synthetic deterministic dataset is used as bootstrap for validated plumbing.
- DistilBERT, MobileNetV2, CLIP, ViLT wrappers are scaffolded conceptually; initial runnable implementation uses a lightweight text encoder for deterministic local runs.

### Impact
- End-to-end watermark logic is testable and reproducible now.
- Results are not paper-comparable yet; this is an implementation-readiness baseline.

### Next steps
1. Add real AG News data module and DistilBERT wrapper.
2. Add B1-B4 runner script and metric table generation.
3. Expand to CIFAR-10 + MobileNetV2 with visual triggers.
4. Add explainability, attacks, and ONNX/int8 modules.


## 2026-04-20 - Codex reproducibility hardening

### Completed
- Removed hard runtime dependency on external ML packages for smoke/debug/full path.
- Reworked the first validated path to use standard-library-only components so commands run in clean/offline Codex containers.
- Converted config loader to JSON-backed `.yaml` files to avoid PyYAML dependency while preserving required command filenames.
- Updated tests to dependency-free assertions and ensured `pytest -q` passes in current environment.
- Added `requirements-dev.txt`, `pytest.ini`, and updated CI install step.
- Updated `AGENTS.md` and `README.md` with reproducible setup and validation commands.

### Impact
- `pytest -q`, `python scripts/train.py --config configs/{smoke,debug,full}.yaml`, and `python scripts/eval.py --config configs/debug.yaml` now execute successfully in this Codex environment without network package installation.
- The current implementation remains a validated scaffold path and not a full paper-faithful DistilBERT/AGNews implementation yet.


## 2026-04-20 - Frozen results + artifact regeneration implementation

### Completed
- Added `results/paper_results.json` as frozen paper-results registry.
- Added `docs/results_reference.md` describing non-fabrication and regeneration policy.
- Replaced placeholder scripts with runnable artifact-regeneration scripts:
  - `make_tables.py`, `make_figures.py`
  - `run_baselines.py`, `run_attacks.py`, `run_explainability.py`
  - `run_threshold_sensitivity.py`, `run_trigger_size_ablation.py`
  - `benchmark_latency.py`, `export_onnx.py`
- Added `src/results/reference.py` helper module for deterministic CSV/text/log generation.

### Notes
- These scripts regenerate artifacts from frozen references and **do not rerun full paper experiments**.
- Empty tables indicate unavailable or not-yet-curated paper-reported numeric values.


## 2026-04-20 - PR sync conflict-resolution pass

### Completed
- Re-synced conflict-prone files (`README.md`, docs, artifact scripts, wrapper scripts) while preserving frozen-results defaults.
- Preserved and validated `--mode full` graceful dry-run behavior for artifact scripts.
- Kept non-fabrication and non-rerun claims explicit in docs and script logs.
