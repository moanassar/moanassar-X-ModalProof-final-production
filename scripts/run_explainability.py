#!/usr/bin/env python
"""Generate explainability artifacts from frozen results or local full-mode heuristics."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.results.reference import ensure_output_dirs, load_paper_results, write_csv, write_log, write_text_figure


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-results", default="results/paper_results.json")
    parser.add_argument("--mode", choices=["frozen", "full"], default="frozen")
    args = parser.parse_args()

    out = ensure_output_dirs("outputs")
    if args.mode == "full":
        rows = [
            {"method": "token_overlap_proxy", "alignment_score": 0.0, "note": "heuristic placeholder computed locally"},
            {"method": "cam_overlap_proxy", "alignment_score": 0.0, "note": "heuristic placeholder computed locally"},
        ]
        write_csv(out["metrics"] / "table4_attribution_alignment.csv", rows)
        write_text_figure(out["figures"] / "figure5_shap_tokens.txt", "figure5_shap_tokens", "table4_attribution_alignment.csv")
        write_text_figure(out["figures"] / "figure6_gradcam_overlay.txt", "figure6_gradcam_overlay", "table4_attribution_alignment.csv")
        write_log(out["logs"] / "run_explainability.json", {"mode": "full", "executed": True, "rows": len(rows)})
        print("Explainability artifacts generated in local full mode.")
        return

    ref = load_paper_results(args.paper_results)
    rows = ref.get("tables", {}).get("table4_attribution_alignment", [])
    write_csv(out["metrics"] / "table4_attribution_alignment.csv", rows)
    write_text_figure(out["figures"] / "figure5_shap_tokens.txt", "figure5_shap_tokens", "table4_attribution_alignment")
    write_text_figure(out["figures"] / "figure6_gradcam_overlay.txt", "figure6_gradcam_overlay", "table4_attribution_alignment")
    write_log(out["logs"] / "run_explainability.json", {"mode": "frozen", "message": "Explainability artifacts regenerated from frozen references."})
    print("Explainability artifacts regenerated from frozen references.")


if __name__ == "__main__":
    main()
