"""Dependency-free training/evaluation loop."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from src.evaluation.verification import verify_watermark
from src.watermark.signature import compute_signature, cosine_scores
from src.watermark.threshold import select_threshold


def _collect_embeddings(model, rows: List[Dict[str, object]]) -> tuple[List[List[float]], List[int]]:
    embs, flags = [], []
    for row in rows:
        embs.append(model.extract_embedding(row))
        flags.append(int(row["is_trigger"]))
    return embs, flags


def train_text_watermark(model, optimizer, criterion, train_loader, val_loader, config: Dict, device: str, run_dir: Path):
    _ = optimizer, criterion, train_loader, device
    val_embeddings, val_flags = _collect_embeddings(model, val_loader)
    trigger_embs = [e for e, f in zip(val_embeddings, val_flags) if f == 1]
    benign_embs = [e for e, f in zip(val_embeddings, val_flags) if f == 0]

    signature = compute_signature(trigger_embs)
    trig_scores = cosine_scores(trigger_embs, signature)
    benign_scores = cosine_scores(benign_embs, signature)

    threshold_info = select_threshold(trig_scores, benign_scores, step=config["watermark"]["threshold_search_step"])
    verify_info = verify_watermark(trig_scores, threshold_info["threshold"])

    checkpoint_path = run_dir / "checkpoints" / "model.pt"
    with checkpoint_path.open("w", encoding="utf-8") as f:
        json.dump(model.state_dict(), f)

    signature_path = run_dir / "signatures" / "signature.pt"
    with signature_path.open("w", encoding="utf-8") as f:
        json.dump(signature, f)

    return {
        "checkpoint_path": str(checkpoint_path),
        "signature_path": str(signature_path),
        "threshold": threshold_info["threshold"],
        "threshold_f1": threshold_info["f1"],
        "val_mean_trigger_score": verify_info["mean_trigger_score"],
        "val_decision": verify_info["decision"],
    }
