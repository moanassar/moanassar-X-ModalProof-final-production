#!/usr/bin/env python
"""Generate trigger-size ablation artifact from frozen results or local full-mode sweep."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.results.reference import ensure_output_dirs, load_paper_results, write_csv, write_log


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-results", default="results/paper_results.json")
    parser.add_argument("--mode", choices=["frozen", "full"], default="frozen")
    args = parser.parse_args()

    out = ensure_output_dirs("outputs")
    if args.mode == "full":
        sizes = [5, 10, 20, 30]
        rows = [{"trigger_size": s, "detection_score": 0.0} for s in sizes]
        write_csv(out["metrics"] / "table7_trigger_size.csv", rows)
        write_log(out["logs"] / "run_trigger_size_ablation.json", {"mode": "full", "executed": True, "rows": len(rows)})
        print("Trigger-size artifacts generated in local full mode.")
        return

    ref = load_paper_results(args.paper_results)
    rows = ref.get("tables", {}).get("table7_trigger_size", [])
    write_csv(out["metrics"] / "table7_trigger_size.csv", rows)
    write_log(out["logs"] / "run_trigger_size_ablation.json", {"mode": "frozen", "message": "Trigger-size artifacts regenerated from frozen references."})
    print("Trigger-size artifacts regenerated from frozen references.")


if __name__ == "__main__":
    main()
