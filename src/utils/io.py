"""I/O helpers for outputs and metadata."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def prepare_run_dir(base_output: str, experiment_name: str) -> Path:
    """Create experiment output directory if needed and return its path."""
    run_dir = Path(base_output) / experiment_name
    run_dir.mkdir(parents=True, exist_ok=True)
    for sub in ["checkpoints", "signatures", "metrics", "logs", "figures", "tables"]:
        (run_dir / sub).mkdir(parents=True, exist_ok=True)
    return run_dir


def write_json(payload: Dict[str, Any], path: Path) -> None:
    """Write JSON to disk."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)


def append_jsonl(payload: Dict[str, Any], path: Path) -> None:
    """Append one JSON line."""
    payload = dict(payload)
    payload["timestamp_utc"] = datetime.utcnow().isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
