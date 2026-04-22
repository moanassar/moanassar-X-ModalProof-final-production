from src.watermark.threshold import select_threshold


def test_threshold_selection_returns_f1():
    trigger = [0.9, 0.8, 0.85]
    benign = [0.2, 0.1, 0.05]
    out = select_threshold(trigger, benign, step=0.01)
    assert 0.0 <= out["f1"] <= 1.0
    assert min(benign) <= out["threshold"] <= max(trigger)
