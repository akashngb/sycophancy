# Glossary

- **Sycophancy.** The model telling the user what the user seems to
  want to hear, instead of what the model's best guess actually is.
  In our setting this usually looks like switching a correct answer to
  a wrong one under pushback.

- **Caving rate.** Among items where the model first answered correctly,
  the fraction where it changed its final answer to the known wrong
  answer under pushback that contained no new information.

- **Correction acceptance rate.** Among items where the model first
  answered incorrectly, the fraction where it accepted a real correction
  (new, correct information from the user).

- **Probe.** A small classifier (usually linear) trained on model
  activations to predict a target label. If a probe works, that label
  is at least linearly represented in those activations.

- **Activation patching.** Replacing the activations at a chosen
  location in a model's forward pass with activations from a different
  input, then measuring what changes in the output. Used to localize
  which parts of the model are responsible for a behavior.

- **Steering vector.** A direction in activation space you add to the
  model's hidden state at inference time to push behavior one way or
  the other. See Rimsky et al. (2024).

- **Residual stream.** The running sum of activations each transformer
  block reads from and writes to. The main highway through the network.

- **Instruction tuning.** Fine-tuning a base language model on
  (instruction, response) pairs so it follows instructions. Produces
  "Instruct" or "Chat" variants of a base model.

- **RLHF.** Reinforcement learning from human feedback. A later
  training stage that uses human preferences, usually via a learned
  reward model. Often implicated as a source of sycophancy, because
  humans sometimes prefer confident or agreeable answers.
