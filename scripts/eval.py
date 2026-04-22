#!/usr/bin/env python
"""Evaluate watermark decision on synthetic test split (dependency-free)."""

from __future__ import annotations

import argparse
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.text_dataset import create_text_dataloaders
from src.evaluation.verification import verify_watermark
from src.models.text_model import SimpleTextWatermarkModel
from src.utils.config import load_config
from src.utils.io import write_json
from src.watermark.signature import cosine_scores


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=str)
    parser.add_argument("--run-dir", required=False, type=str)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    run_dir = Path(args.run_dir or (Path(config["experiment"]["output_dir"]) / config["experiment"]["name"]))

    _, _, test_rows = create_text_dataloaders(config)
    model = SimpleTextWatermarkModel(
        vocab_size=config["preprocessing"]["vocab_size"],
        embedding_dim=config["model"]["embedding_dim"],
        num_labels=config["model"]["num_labels"],
    )

    with (run_dir / "checkpoints" / "model.pt").open("r", encoding="utf-8") as f:
        model.load_state_dict(json.load(f))
    with (run_dir / "signatures" / "signature.pt").open("r", encoding="utf-8") as f:
        signature = json.load(f)

    train_metrics = load_config(run_dir / "metrics" / "train_metrics.json")
    threshold = float(train_metrics["threshold"])

    trigger_scores, benign_scores = [], []
    for row in test_rows:
        emb = model.extract_embedding(row)
        score = cosine_scores([emb], signature)[0]
        if int(row["is_trigger"]) == 1:
            trigger_scores.append(score)
        else:
            benign_scores.append(score)

    verification = verify_watermark(trigger_scores, threshold)
    verification["mean_benign_score"] = sum(benign_scores) / max(1, len(benign_scores))
    verification["num_test_samples"] = len(test_rows)

    write_json(verification, run_dir / "metrics" / "eval_metrics.json")
    print(f"Evaluation complete. Outputs: {run_dir / 'metrics' / 'eval_metrics.json'}")


if __name__ == "__main__":
    main()
