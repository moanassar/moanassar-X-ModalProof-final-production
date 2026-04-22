# Assumptions Log

## A-001: Initial validated path modality
- **Type**: safe default
- **Choice**: Start with text modality only for first end-to-end validated path.
- **Reasoning**: CODEX_HANDOFF prioritizes incremental validated progress and identifies DistilBERT/AG News as first critical target.
- **Configurable**: Yes (`experiment.modality`, model/data modules).

## A-002: Dataset availability fallback
- **Type**: safe default
- **Choice**: Use deterministic synthetic text classification dataset for smoke/debug/full bootstrap when external AG News data is not present.
- **Reasoning**: Enables non-network, deterministic CI/smoke validation while preserving pipeline behavior.
- **Configurable**: Yes (`dataset.name`, `dataset.synthetic.*`).

## A-003: Signature method
- **Type**: explicit from paper / safe default
- **Choice**: Use centroid of normalized trigger embeddings as the watermark signature.
- **Reasoning**: Aligned with handoff guidance and cosine verification.
- **Configurable**: Yes (`watermark.signature_method`).

## A-004: Threshold selection
- **Type**: explicit from paper
- **Choice**: Select threshold on validation using max F1 via sweep.
- **Reasoning**: Required in handoff.
- **Configurable**: Yes (`watermark.threshold_search_step`, `watermark.threshold_selection`).

## A-005: Loss defaults
- **Type**: safe default
- **Choice**: `lambda_align=1.0`, `lambda_sep=0.1`, `margin_gamma=0.2`.
- **Reasoning**: Paper omits exact values; these match handoff-recommended defaults.
- **Configurable**: Yes (`watermark.*`).


## A-006: Dependency-free bootstrap path
- **Type**: safe default
- **Choice**: For Codex reproducibility, the initial smoke/debug/full pipeline uses only Python standard library components.
- **Reasoning**: Current Codex environment can block package installation; dependency-free path guarantees runnable validation commands.
- **Configurable**: Yes (future phases can switch to torch/transformers by replacing model/data modules).

## A-007: JSON-formatted `.yaml` configs
- **Type**: safe default
- **Choice**: Keep required `.yaml` filenames but store JSON content parseable via stdlib `json`.
- **Reasoning**: Preserves command contract while removing PyYAML dependency.
- **Configurable**: Yes (can revert to standard YAML parser when environment guarantees dependencies).


## A-008: Frozen paper-reported results registry
- **Type**: inferred from handoff reproducibility requirements
- **Choice**: Maintain immutable/reference values in `results/paper_results.json` and regenerate artifacts from it.
- **Reasoning**: Supports deterministic artifact regeneration without claiming full reruns.
- **Configurable**: Yes (`--paper-results` argument in artifact scripts).


## A-009: Full-mode dry-run policy
- **Type**: safe default
- **Choice**: Artifact scripts accept `--mode full` and run local scaffold computations from generated run artifacts (still not full paper-faithful deep-learning reruns).
- **Choice**: Artifact scripts accept `--mode full` but perform explicit dry-run logging instead of claiming full reruns.
- **Reasoning**: Prevents overclaiming capabilities while preserving forward-compatible CLI surface.
- **Configurable**: Yes (`--mode` flag in artifact scripts).
