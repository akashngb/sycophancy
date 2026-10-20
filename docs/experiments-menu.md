# Experiments menu

Pick one for your first week. These are designed to be runnable on a
laptop with the tiny or small model, and to give you a concrete number
to report at the next meeting.

Items marked "not yet supported" need an addition to the harness or a
new module. Those are good "stretch" picks if you want to extend the
codebase while running an experiment.

## 1. Flip rate baseline

**What:** Run the starter experiment on the tiny model, then on the
small model. Compare caving rates.

**Uses:** `configs/experiments/flip_rate_tiny.yaml`, swap the model
config for `small_qwen_1_5b.yaml`.

**Report:** per-pressure caving rate for both models, overall initial
accuracy. Explain any clear differences.

## 2. Pressure types

**What:** Which pressure type caves the model the most? Rank them.

**Uses:** the starter experiment. Enable one pressure at a time or
look at the per-pressure numbers in `metrics.json`.

**Report:** ranked list with caving rates. One paragraph on why you
think the top pressure works.

## 3. Multi-turn conversations

**What:** Does repeated pushback compound? Try 1, 2, and 3 turns of the
same pressure.

**Uses:** change `turns_per_pressure` in your config. Add a plot that
tracks caving rate as a function of turn count.

**Report:** a line chart (turn count on x, caving rate on y) for each
pressure type.

## 4. Model size

**What:** Does caving rate change with model size? Tiny vs small, and
if you have access to a GPU, 7B.

**Uses:** `configs/models/*.yaml`. Fill in `example_7b.yaml` with a
real model id if you can.

**Report:** caving rate vs model size, with the x-axis in parameters.

## 5. Base vs instruction-tuned

**What:** Does instruction tuning make the model more sycophantic? Pick
a base/instruct pair at a fixed size.

**Uses:** two HF model configs with different `model_id` values. The
harness does not require a chat template; it will use the tokenizer's
default, which is weak for base models. You may need a short few-shot
prefix in the system prompt for the base model.

**Report:** side-by-side caving rate and initial accuracy.

## 6. Confidence and caving

**What:** When the model expresses more confidence on turn 0, does it
cave less on turn 1? Measure confidence by prompting the model to rate
itself, or by using logit scores (requires HF backend).

**Uses:** HF backend. Add a short confidence probe in a run script.

**Report:** scatter plot of confidence vs cave probability, per item.

## 7. Coding agent caving (not yet supported)

**What:** The user asserts a bug exists in correct code. Does the
model "fix" something that was not broken?

**Needs:** a small code dataset (correct function + user accusation),
and a way to let the model edit code. Could be a small dataset of
functions and a simple diff checker. Open an issue once scoped.

## 8. Flattery in grading (not yet supported)

**What:** Does the model grade an argument more generously when the
author introduces themselves as a professor vs a student?

**Needs:** a grading-style dataset and a comparative judge. Share the
rubric so results are reproducible.

## 9. Vision model caving (not yet supported)

**What:** Does a VLM cave when the user disagrees about what is in an
image?

**Needs:** a VLM backend (e.g. LLaVA family) and image items in the
schema. The schema would gain an `image_path` field. Open an issue
before changing the schema so everyone agrees.

## 10. First linear probe (not yet supported in the harness)

**What:** Train a linear probe to predict whether the model will cave,
using hidden states from the last prompt token.

**Needs:** `syco[interp]` installed. Use `syco.interp.extract_hidden_states`
to pull activations from the HF backend, then train sklearn's
`LogisticRegression`. The harness already saves per-item outcomes you
can use as labels.
