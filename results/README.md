# results/

Each run writes to `results/<experiment_name>/<timestamp>/` with:

- `config.json` — the fully resolved config, including model and env info.
- `responses.jsonl` — one line per item/pressure, with every turn.
- `metrics.json` — initial accuracy, caving rate (overall and per pressure),
  hedging rate, and correction acceptance rate when applicable.
- `caving_by_pressure.png` — simple bar chart.

Everything inside here except this README is gitignored. Share results
by committing a notebook or writing a short summary in `experiments/.../`.
