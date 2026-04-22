from src.data.triggers import split_triggers


def test_split_triggers_deterministic():
    trig = [f"t{i}" for i in range(10)]
    a = split_triggers(trig, seed=42)
    b = split_triggers(trig, seed=42)
    assert a == b
