from syco.utils.device import pick_device


def test_explicit_override_wins():
    assert pick_device("cpu") == "cpu"


def test_env_override(monkeypatch):
    monkeypatch.setenv("SYCO_DEVICE", "cpu")
    assert pick_device() == "cpu"


def test_auto_returns_valid(monkeypatch):
    monkeypatch.delenv("SYCO_DEVICE", raising=False)
    assert pick_device() in {"cuda", "mps", "cpu"}
