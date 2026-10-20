# sycophancy

LLM Sycophancy Mitigation, a project of Trustworthy Machine Intelligence
(TMI) at the University of Toronto, running October 2026 to April 2027.
Language models often drop a correct answer when a user pushes back
without giving new information. Fixing that is harder than it sounds,
because sometimes the user is actually right. This repo is the shared
benchmark and evaluation harness we use to measure both failure modes.

## The two metrics

- **Caving rate**: how often the model changes a correct answer under
  pushback with no new information.
- **Correction acceptance rate**: how often the model accepts a real
  correction when it was actually wrong.

A good intervention lowers caving rate without lowering correction
acceptance. Report both together, always.

## Quickstart (about 15 minutes)

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Clone and enter the repo.

   ```bash
   git clone https://github.com/akashngb/sycophancy.git
   cd sycophancy
   ```

3. Install dependencies.

   ```bash
   uv sync --extra dev
   ```

4. Copy the env file. You can leave the values empty for the starter run.

   ```bash
   cp .env.example .env
   ```

5. Run the starter experiment on the tiny model. This downloads about
   1 GB of weights on the first run, then takes a few minutes on CPU.

   ```bash
   make demo
   ```

Results land in `results/flip_rate_tiny/<timestamp>/`. Open `metrics.json`
and `caving_by_pressure.png`.

If you want to try everything without downloading a model, run the fake
backend first:

```bash
uv run syco run --config configs/experiments/flip_rate_fake.yaml
```

## Repo map

```
configs/        model and experiment YAMLs
data/           seed data (committed), raw and processed (gitignored)
docs/           project overview, setup guide, reading list, menu, glossary
experiments/    one folder per experiment (lab notebook + config + script)
directions/     where each person's year-long direction lives
notebooks/      exploratory analysis
results/        where runs are written (gitignored except README)
scripts/        small utilities
src/syco/       the package: models, data, pressure, eval, interp, utils, cli
tests/          unit tests, no model downloads
```

See `docs/project-overview.md` for the full picture and
`docs/experiments-menu.md` for first-week experiment ideas.

## Documentation

- `docs/project-overview.md`: the problem, the metrics, the year's shape
- `docs/setup-guide.md`: per-OS setup and common errors
- `docs/experiments-menu.md`: directions you can start on today
- `docs/reading-list.md`: key papers with per-person assignments
- `docs/glossary.md`: terms we use
- `CONTRIBUTING.md`: branch naming, PR flow, what not to commit

## Team

- Akash (lead)
- Divy
- Aneya
- Raeed
- Catherine
- Kian
- Heng
- Jehanzeb

## Where this lives

This repo is self-contained so that at the end of the year it can be
merged into TMI's main monorepo without rewrites. Nothing here assumes
it is the root of a larger project, and there are no absolute paths.

Project discussion happens in the TMI Discord channel.
