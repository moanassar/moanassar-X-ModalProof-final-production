"""Dependency-free synthetic text dataset utilities."""

from __future__ import annotations

import random
from typing import Dict, List, Sequence, Tuple


def _simple_tokenize(text: str, vocab_size: int, max_length: int) -> List[int]:
    ids = [(ord(ch) % vocab_size) for ch in text.lower()]
    if len(ids) < max_length:
        ids += [0] * (max_length - len(ids))
    return ids[:max_length]


def build_synthetic_text_splits(
    n_train: int,
    n_val: int,
    n_test: int,
    num_labels: int,
    trigger_phrases: Sequence[str],
    trigger_ratio: float,
    vocab_size: int,
    max_length: int,
    seed: int,
) -> Dict[str, List[Dict[str, object]]]:
    rng = random.Random(seed)

    def make_split(size: int, split_name: str) -> List[Dict[str, object]]:
        rows: List[Dict[str, object]] = []
        n_trigger = int(size * trigger_ratio)
        flags = [1] * n_trigger + [0] * (size - n_trigger)
        rng.shuffle(flags)
        for i in range(size):
            label = rng.randrange(num_labels)
            base = f"{split_name} sample {i}"
            if flags[i] == 1:
                phrase = trigger_phrases[i % len(trigger_phrases)]
                text = f"{base} {phrase}"
            else:
                text = base
            rows.append(
                {
                    "input_ids": _simple_tokenize(text, vocab_size=vocab_size, max_length=max_length),
                    "labels": label,
                    "is_trigger": flags[i],
                }
            )
        return rows

    return {
        "train": make_split(n_train, "train"),
        "val": make_split(n_val, "val"),
        "test": make_split(n_test, "test"),
    }


def create_text_dataloaders(config: Dict) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    data_cfg = config["dataset"]
    trig_cfg = config["triggers"]
    prep_cfg = config["preprocessing"]

    splits = build_synthetic_text_splits(
        n_train=data_cfg["synthetic"]["n_train"],
        n_val=data_cfg["synthetic"]["n_val"],
        n_test=data_cfg["synthetic"]["n_test"],
        num_labels=config["model"]["num_labels"],
        trigger_phrases=trig_cfg["phrases"],
        trigger_ratio=trig_cfg["trigger_ratio"],
        vocab_size=prep_cfg["vocab_size"],
        max_length=prep_cfg["max_length"],
        seed=config["experiment"]["seed"],
    )
    return splits["train"], splits["val"], splits["test"]
