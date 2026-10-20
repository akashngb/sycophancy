# Project overview

## The problem

When a user pushes back on a model's answer, the model often changes
its answer even though the user has given no new information. This is
sycophancy. It is bad because it means the model's second answer is
determined more by social pressure than by what the model actually knows.

The usual fix (train the model to resist pushback) has an obvious
failure mode. Users are sometimes right. A model that resists all
pushback will also refuse real corrections, which is just as bad.

## Why it is hard

Separating "the user is applying pressure" from "the user has new
information" is subtle. Both look similar on the surface: a short
disagreement from the user. A good system has to be able to update
when there is new information, and only then.

## What we measure

Every result we report has two numbers.

- **Caving rate**: among items where the model first gave the correct
  answer, how often did it change its final answer to the known wrong
  answer under pushback that contained no new information?
- **Correction acceptance rate**: among items where the model first
  gave the wrong answer, how often did it accept a real correction?

An intervention that cuts caving rate while keeping correction
acceptance roughly stable is a real improvement. An intervention that
drops caving rate by also dropping correction acceptance is not.

## The year's structure

**Phase 1 (shared groundwork, first few weeks).** Everyone builds and
uses the same benchmark and evaluation harness. We expand the seed data,
add new pressure types, calibrate against a few baseline models, and
read the core papers in `docs/reading-list.md`.

**Phase 2 (directions).** Individuals or pairs pick a direction.
Direction folders live under `directions/`. Current candidate
directions include:

- Interpretability. Probes and activation patching to find where in the
  model caving decisions are made.
- Interventions. Fine-tuning vs activation steering vs prompting.
- Multi-turn conversations. Does pressure compound over several turns?
- Coding agents. Caving when a human says "that function has a bug"
  without actually pointing at one.
- Agent-to-agent sycophancy. Does one agent cave to another?
- Vision-language models. Does caving look different with images?
- Feedback and flattery sycophancy. Grading, review, and compliment
  responses as a different flavor of sycophancy.

Directions are not fixed. Pick one, scope a first experiment, and refine.

## How this becomes TMI's

In April we merge this repo into TMI's main repo. To keep that cheap:

- No absolute paths. All paths resolve relative to a config or `cwd`.
- Nothing assumes this is the root of a larger project.
- All dependencies are declared in `pyproject.toml`.
- Secrets live in `.env`, never in code or configs.
