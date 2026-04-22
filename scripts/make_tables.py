#!/usr/bin/env python
"""Regenerate paper tables from frozen reference values or local full-mode artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.results.full_pipeline import build_table5_from_runs
from src.results.reference import ensure_output_dirs, load_paper_results, write_csv, write_log

TABLE_FILES = {
    "table3_detection_accuracy": "table3_detection_accuracy.csv",
    "table4_attribution_alignment": "table4_attribution_alignment.csv",
    "table5_internal_baselines": "table5_internal_baselines.csv",
    "table6_threshold_sensitivity": "table6_threshold_sensitivity.csv",
    "table7_trigger_size": "table7_trigger_size.csv",
    "table8_repeatability": "table8_repeatability.csv",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-results", default="results/paper_results.json")
    parser.add_argument("--mode", choices=["frozen", "full"], default="frozen")
    args = parser.parse_args()

    out = ensure_output_dirs("outputs")
    if args.mode == "full":
        # Prefer any locally generated metrics; fall back to run discovery for table5.
        table5_rows = build_table5_from_runs("outputs")
        write_csv(out["metrics"] / "table5_internal_baselines.csv", table5_rows)

        for key, filename in TABLE_FILES.items():
            path = out["metrics"] / filename
            if not path.exists():
                write_csv(path, [])

        write_log(out["logs"] / "make_tables.json", {"mode": "full", "executed": True, "table5_rows": len(table5_rows)})
        print("Tables generated from local full-mode artifacts.")
        return

    ref = load_paper_results(args.paper_results)
    for key, filename in TABLE_FILES.items():
        rows = ref.get("tables", {}).get(key, [])
        write_csv(out["metrics"] / filename, rows)

    write_log(out["logs"] / "make_tables.json", {"mode": ref.get("metadata", {}).get("mode", "unknown"), "paper_results": args.paper_results, "message": "Tables regenerated from frozen references only."})
    print("Regenerated table artifacts from frozen paper results.")


if __name__ == "__main__":
    main()
