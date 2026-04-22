#!/usr/bin/env python
"""Regenerate figure placeholders from frozen metadata or local full-mode tables."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.results.reference import ensure_output_dirs, load_paper_results, write_log, write_text_figure

FIG_FILES = {
    "figure2_accuracy": "figure2_accuracy.txt",
    "figure3_robustness_drop": "figure3_robustness_drop.txt",
    "figure4_alignment": "figure4_alignment.txt",
    "figure7_latency": "figure7_latency.txt",
    "figure8_radar": "figure8_radar.txt",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-results", default="results/paper_results.json")
    parser.add_argument("--mode", choices=["frozen", "full"], default="frozen")
    args = parser.parse_args()

    out = ensure_output_dirs("outputs")
    if args.mode == "full":
        for key, filename in FIG_FILES.items():
            write_text_figure(out["figures"] / filename, title=key, source="local_full_mode_tables")
        write_log(out["logs"] / "make_figures.json", {"mode": "full", "executed": True, "figures": len(FIG_FILES)})
        print("Figures generated from local full-mode artifacts.")
        return

    ref = load_paper_results(args.paper_results)
    for key, filename in FIG_FILES.items():
        fig_meta = ref.get("figures", {}).get(key, {})
        source = fig_meta.get("source_table", "unknown")
        write_text_figure(out["figures"] / filename, title=key, source=source)

    write_log(out["logs"] / "make_figures.json", {"mode": ref.get("metadata", {}).get("mode", "unknown"), "paper_results": args.paper_results, "message": "Figures regenerated from frozen references only."})
    print("Regenerated figure artifacts from frozen paper results.")


if __name__ == "__main__":
    main()
