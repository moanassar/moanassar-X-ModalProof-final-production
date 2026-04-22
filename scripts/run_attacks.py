#!/usr/bin/env python
"""Generate attack/robustness artifacts from frozen results or local full-mode run."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.results.full_pipeline import run_attack_eval
from src.results.reference import ensure_output_dirs, load_paper_results, write_csv, write_log
from src.utils.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-results", default="results/paper_results.json")
    parser.add_argument("--config", default="configs/full.yaml")
    parser.add_argument("--run-dir", default="outputs/full_text_b4_seed0")
    parser.add_argument("--mode", choices=["frozen", "full"], default="frozen")
    args = parser.parse_args()

    out = ensure_output_dirs("outputs")
    if args.mode == "full":
        cfg = load_config(args.config)
        rows = run_attack_eval(cfg, Path(args.run_dir))
        write_csv(out["metrics"] / "table3_detection_accuracy.csv", rows)
        write_log(out["logs"] / "run_attacks.json", {"mode": "full", "executed": True, "rows": len(rows)})
        print("Attack artifacts generated from local full-mode run.")
        return

    ref = load_paper_results(args.paper_results)
    rows = ref.get("tables", {}).get("table3_detection_accuracy", [])
    write_csv(out["metrics"] / "table3_detection_accuracy.csv", rows)
    write_log(out["logs"] / "run_attacks.json", {"mode": "frozen", "message": "Attack results regenerated from frozen references."})
    print("Attack artifacts regenerated from frozen references.")


if __name__ == "__main__":
    main()
