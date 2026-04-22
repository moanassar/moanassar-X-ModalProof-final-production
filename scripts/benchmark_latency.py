#!/usr/bin/env python
"""Generate latency artifacts from frozen results or local benchmark."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.results.full_pipeline import benchmark_latency
from src.results.reference import ensure_output_dirs, load_paper_results, write_csv, write_log, write_text_figure
from src.utils.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-results", default="results/paper_results.json")
    parser.add_argument("--config", default="configs/full.yaml")
    parser.add_argument("--mode", choices=["frozen", "full"], default="frozen")
    args = parser.parse_args()

    out = ensure_output_dirs("outputs")
    if args.mode == "full":
        cfg = load_config(args.config)
        lat = benchmark_latency(cfg, repeats=100)
        write_csv(out["metrics"] / "latency_local_full.csv", [lat])
        write_text_figure(out["figures"] / "figure7_latency.txt", "figure7_latency", "latency_local_full.csv")
        write_log(out["logs"] / "benchmark_latency.json", {"mode": "full", "executed": True, **lat})
        print("Latency artifacts generated from local full-mode benchmark.")
        return

    ref = load_paper_results(args.paper_results)
    rows = ref.get("tables", {}).get("table5_internal_baselines", [])
    write_csv(out["metrics"] / "table5_internal_baselines.csv", rows)
    write_text_figure(out["figures"] / "figure7_latency.txt", "figure7_latency", "table5_internal_baselines")
    write_log(out["logs"] / "benchmark_latency.json", {"mode": "frozen", "message": "Latency artifacts regenerated from frozen references."})
    print("Latency artifacts regenerated from frozen references.")


if __name__ == "__main__":
    main()
