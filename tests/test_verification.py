from src.evaluation.verification import verify_watermark


def test_verification_positive():
    out = verify_watermark([0.8, 0.9, 0.85], threshold=0.5)
    assert out["decision"] is True
