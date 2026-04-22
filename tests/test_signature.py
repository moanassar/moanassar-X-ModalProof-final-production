import math

from src.watermark.signature import compute_signature, cosine_scores


def test_signature_unit_norm():
    emb = [[1.0, 2.0], [3.0, 4.0]]
    sig = compute_signature(emb)
    norm = math.sqrt(sum(v * v for v in sig))
    assert abs(norm - 1.0) < 1e-6


def test_cosine_scores_shape():
    emb = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
    sig = compute_signature([[1.0, 0.0]])
    scores = cosine_scores(emb, sig)
    assert len(scores) == 3
