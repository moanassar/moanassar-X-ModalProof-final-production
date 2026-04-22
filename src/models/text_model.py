"""Dependency-free text model wrapper."""

from __future__ import annotations

import random
from typing import Dict, List, Tuple


class SimpleTextWatermarkModel:
    """Deterministic embedding and linear-logit stub model."""

    def __init__(self, vocab_size: int, embedding_dim: int, num_labels: int):
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.num_labels = num_labels
        rng = random.Random(0)
        self.classifier = [[rng.uniform(-0.1, 0.1) for _ in range(embedding_dim)] for _ in range(num_labels)]

    def extract_embedding(self, batch: Dict[str, object]) -> List[float]:
        ids = batch["input_ids"]
        vec = [0.0 for _ in range(self.embedding_dim)]
        for token in ids:
            vec[token % self.embedding_dim] += 1.0
        denom = float(max(1, len(ids)))
        return [v / denom for v in vec]

    def forward_task(self, batch: Dict[str, object]) -> List[float]:
        emb = self.extract_embedding(batch)
        return [sum(w * e for w, e in zip(row, emb)) for row in self.classifier]

    def forward_with_embedding(self, batch: Dict[str, object]) -> Tuple[List[float], List[float]]:
        emb = self.extract_embedding(batch)
        logits = [sum(w * e for w, e in zip(row, emb)) for row in self.classifier]
        return logits, emb

    def state_dict(self) -> Dict[str, object]:
        return {"classifier": self.classifier}

    def load_state_dict(self, state: Dict[str, object]) -> None:
        self.classifier = state["classifier"]
