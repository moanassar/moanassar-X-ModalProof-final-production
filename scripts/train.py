#!/usr/bin/env python
"""Train watermarked model (dependency-free smoke/debug/full path)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.text_dataset import create_text_dataloaders
from src.models.text_model import SimpleTextWatermarkModel
from src.training.trainer import train_text_watermark
from src.utils.config import load_config, save_config_snapshot
from src.utils.io import append_jsonl, prepare_run_dir, write_json
from src.utils.seed import set_global_seed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=str)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    set_global_seed(config["experiment"]["seed"], config["reproducibility"]["deterministic"])

    run_dir = prepare_run_dir(config["experiment"]["output_dir"], config["experiment"]["name"])
    save_config_snapshot(config, run_dir / "config_snapshot.json")

    train_loader, val_loader, _ = create_text_dataloaders(config)

    model = SimpleTextWatermarkModel(
        vocab_size=config["preprocessing"]["vocab_size"],
        embedding_dim=config["model"]["embedding_dim"],
        num_labels=config["model"]["num_labels"],
    )

    results = train_text_watermark(
        model=model,
        optimizer=None,
        criterion=None,
        train_loader=train_loader,
        val_loader=val_loader,
        config=config,
        device="cpu",
        run_dir=Path(run_dir),
    )

    write_json(results, Path(run_dir) / "metrics" / "train_metrics.json")
    append_jsonl(results, Path(run_dir) / "logs" / "events.jsonl")
    print(f"Run complete. Outputs: {run_dir}")


if __name__ == "__main__":
    main()
