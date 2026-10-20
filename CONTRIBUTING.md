# Contributing

Small changes, often. Please follow these rules so we can merge cleanly
into the TMI monorepo at the end of the year.

## Workflow

1. Pull `main`.
2. Create a branch named `yourname/short-description`, for example
   `akash/add-authority-pressure` or `catherine/confidence-probe-wip`.
3. Make your change. Keep PRs under about 400 lines when you can.
4. Run `make check` before pushing. It runs ruff and the test suite.
5. Open a pull request. Fill in the template. Link an issue if one exists.
6. One reviewer approves, then you merge. Squash merges are fine.

Never push directly to `main`.

## What to install

```bash
make setup           # uv sync --extra dev + pre-commit install
```

Optional extras:

```bash
uv sync --extra interp   # transformer-lens, nnsight, scikit-learn
uv sync --extra api      # openai, anthropic
# serve (vllm) is Linux + CUDA only; see docs/setup-guide.md
```

## What not to commit

- `.env` or any file with API keys or tokens.
- Anything under `data/raw/` or `data/processed/`.
- Model weights (`*.safetensors`, `*.bin`, `*.pt`, `*.ckpt`, `*.gguf`).
- Anything under `results/` except the README.
- Full experiment outputs. Share them as a short summary in your
  `experiments/<name>/README.md` instead.

The `.gitignore` already excludes these, but double-check `git status`
before committing.

## Adding an experiment

```bash
cp -r experiments/_template experiments/yourname_short_question
```

Fill in `README.md`, `config.yaml`, and `run.sh`. Point `config.yaml` at
the data and model you want. Commit the folder with the final summary
in the README so a teammate can reproduce you.

See `docs/experiments-menu.md` for options.

## Adding a pressure type

Edit `src/syco/pressure/templates.py`. Call `register_pressure(...)` at
the bottom of the file. Add a short unit test in `tests/test_pressure.py`.

## Adding a dataset

Write JSONL that matches `syco.data.schema.Item`. Put committed sets
under `data/seed/`. Keep them small and only include facts you are
certain of. Larger or auto-generated sets go under `data/processed/`
and are not committed.

## Code style

- `ruff` enforces style and basic bugs. Run `make format` to autofix.
- Prefer small, well-named functions over clever one-liners.
- Avoid absolute paths. Use `pathlib.Path` and resolve relative to the
  config or `cwd`.
- Keep heavy imports (torch, transformers) inside functions when they
  are only used in one place, so unrelated modules import fast.

## Where we talk

Project discussion happens in the TMI Discord channel. For anything
that needs to persist beyond a chat, open an issue.
