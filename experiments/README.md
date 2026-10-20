# experiments/

Each experiment lives in its own folder. The folder is your lab notebook:
a README that explains what you did, a config that reproduces it, and a
run script that invokes the CLI.

## Add a new experiment

```bash
cp -r experiments/_template experiments/your_name_short_question
```

Then edit:

- `README.md`: question, hypothesis, method, results, what's next.
- `config.yaml`: the experiment config (which model, which pressures, data).
- `run.sh`: the exact command you ran.

Commit the folder, including the final `README.md` with results summarized.
Do not commit anything from `results/` (it is gitignored). Link to a run
by path or by committing a small summary notebook if you want to share plots.

## Working starter

`flip_rate/` is the reference experiment. If you are not sure where to
start, run that end to end and read every line of its config.
