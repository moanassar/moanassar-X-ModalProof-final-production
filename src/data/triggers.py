"""Trigger helpers."""

from __future__ import annotations

from typing import Dict, List


def split_triggers(triggers: List[str], seed: int) -> Dict[str, List[str]]:
    """Deterministically split triggers into train/val/test sets."""
    import random

    rng = random.Random(seed)
    items = list(triggers)
    rng.shuffle(items)

    n = len(items)
    n_train = max(1, int(0.6 * n))
    n_val = max(1, int(0.2 * n))
    train = items[:n_train]
    val = items[n_train : n_train + n_val]
    test = items[n_train + n_val :]
    if not test:
        test = items[-1:]
    return {"train": train, "val": val, "test": test}
