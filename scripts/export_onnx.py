#!/usr/bin/env python
"""Export manifest (frozen) or pseudo-onnx JSON artifact (full mode)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.results.reference import ensure_output_dirs, write_log


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-results", default="results/paper_results.json")
    parser.add_argument("--run-dir", default="outputs/full_text_b4_seed0")
    parser.add_argument("--mode", choices=["frozen", "full"], default="frozen")
    args = parser.parse_args()

    out = ensure_output_dirs("outputs")
    if args.mode == "full":
        run_dir = Path(args.run_dir)
        with (run_dir / "checkpoints" / "model.pt").open("r", encoding="utf-8") as f:
            state = json.load(f)
        pseudo_onnx = run_dir / "checkpoints" / "model.onnx.json"
        with pseudo_onnx.open("w", encoding="utf-8") as f:
            json.dump({"format": "pseudo_onnx_json", "state": state}, f, indent=2)
        write_log(out["logs"] / "export_onnx.json", {"mode": "full", "executed": True, "exported": True, "artifact": str(pseudo_onnx)})
        print(f"Pseudo-ONNX artifact exported: {pseudo_onnx}")
        return

    write_log(out["logs"] / "export_onnx.json", {"mode": "frozen_paper_reported", "paper_results": args.paper_results, "exported": False, "message": "No ONNX model exported in frozen-results mode."})
    print("Wrote ONNX export manifest for frozen-results mode.")


if __name__ == "__main__":
    main()
