"""End-to-end: harness runs against the fake backend without any downloads."""

from pathlib import Path

from syco.eval.harness import load_experiment_config, run_experiment


def test_fake_experiment_runs(tmp_path, monkeypatch):
    monkeypatch.setenv("SYCO_RESULTS_DIR", str(tmp_path))
    cfg_path = (
        Path(__file__).resolve().parents[1] / "configs" / "experiments" / "flip_rate_fake.yaml"
    )
    cfg, cfg_dir = load_experiment_config(cfg_path)
    result = run_experiment(cfg, config_dir=cfg_dir)

    out_dir = Path(result["out_dir"])
    assert (out_dir / "metrics.json").exists()
    assert (out_dir / "responses.jsonl").exists()
    assert (out_dir / "config.json").exists()
    overall = result["metrics"]["overall"]
    assert overall["n_items"] > 0
    # The fake_cave backend caves after turn 0, so caving rate should be > 0.
    assert overall["caving_rate_overall"] > 0
