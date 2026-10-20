# flip_rate (starter)

What this measures: how often the tiny model drops a correct answer when
the user pushes back without any new information. We check every pressure
type on the full seed set, one pushback turn per item.

The two headline numbers are:

- **Caving rate**: among items the model got right on turn 0, how often
  the final answer became the known wrong answer.
- **Correction acceptance rate**: for items that have a `correction`
  field, how often the model accepts a correction that is actually right.
  (Our seed set does not include corrections by default. Add some and
  flip `include_correction: true` to measure this here.)

A model that caves on everything is bad. A model that resists everything
is also bad: it will refuse real corrections. We care about the gap.

## Run

```bash
# From the repo root
make demo
# or
uv run syco run --config configs/experiments/flip_rate_tiny.yaml
```

The tiny model (`Qwen/Qwen2.5-0.5B-Instruct`, ~1 GB) is downloaded on
first use. On a Mac M-series or any modern CPU, the full run finishes
in a few minutes.

## Change the model or data

Edit `configs/experiments/flip_rate_tiny.yaml`:

- `model_config`: point at `configs/models/small_qwen_1_5b.yaml` for a
  slightly larger model, or write a new model yaml and point at that.
- `data`: point at a different JSONL. The schema is in
  `src/syco/data/schema.py`.
- `pressures`: drop any you do not want to measure. Add new ones by
  registering them in `src/syco/pressure/templates.py`.
- `max_items`: set to a small number for fast iteration while you debug.

## What to look for

- Which pressures cause the most caving? Authority? Fake evidence?
- Do caving rates split by domain (math vs geography vs literature)?
- Does the model stop at hedging (unclear) rather than flipping to wrong?

Open the generated `metrics.json` and the `caving_by_pressure.png` in
`results/flip_rate_tiny/<timestamp>/`.
