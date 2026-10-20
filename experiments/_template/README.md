# <your experiment name>

**Owner:** <your name>
**Date:** <YYYY-MM-DD>
**Status:** draft | running | done

## Question

What are you trying to find out, in one sentence?

## Hypothesis

What do you expect to see, and why?

## Method

What are you varying, and what are you measuring? Which model, which data,
which pressures, how many items, how many turns, which seed. If you added
a new pressure or a new dataset, say so and link to the file.

## How to run

```bash
# From the repo root
bash experiments/<this-folder>/run.sh
```

Results go to `results/<name>/<timestamp>/`.

## Results

Numbers from `metrics.json`:

- Initial accuracy:
- Overall caving rate:
- Correction acceptance rate (if applicable):
- Per-pressure caving rate: (paste the table from the CLI)

Attach or link `caving_by_pressure.png`.

## What's next

What should the next experiment do? Any dead ends worth writing down?
