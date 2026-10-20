# Reading list

Core papers for the project. Each person below has a primary paper to
present and lead discussion on. Everyone reads Sharma et al. first.

- Sharma et al. (2023), Towards Understanding Sycophancy in Language
  Models. (everyone) [link]
  The paper that put sycophancy on the map, with the first systematic
  measurements and a clean statement of the problem.

- Rimsky et al. (2024), Steering Llama 2 via Contrastive Activation
  Addition. (Divy) [link]
  How to steer model behavior at inference time with simple linear
  additions to activations, with recipes for picking the vectors.

- Hewitt & Liang (2019), Designing and Interpreting Probes with Control
  Tasks. (Heng) [link]
  Classic paper on how to tell whether a probe is finding something
  real vs memorizing. Required reading before any probing work.

- Wei et al. (2023), Simple Synthetic Data Reduces Sycophancy in Large
  Language Models. (Raeed) [link]
  Fine-tuning on cheap synthetic data cuts sycophancy. Useful baseline
  for the interventions direction.

- Perez et al. (2022), Discovering Language Model Behaviors with
  Model-Written Evaluations. (Aneya) [link]
  How to generate large behavioral evals cheaply. Relevant for scaling
  our benchmark past the hand-curated seed set.

- Laban et al. (2023), Are You Sure? Challenging LLMs Leads to
  Performance Drops in the FlipFlop Experiment. (Jehanzeb) [link]
  Early systematic look at the "flip" behavior that caving rate
  measures. Directly comparable to what we are building.

- Kadavath et al. (2022), Language Models (Mostly) Know What They Know.
  (Catherine) [link]
  Calibration and self-reported confidence. Useful for the confidence
  and caving experiment and for correction acceptance analysis.

- Zou et al. (2023), Representation Engineering: A Top-Down Approach to
  AI Transparency. (Kian) [link]
  Reading model internals as structured features. Framework for the
  interpretability direction.

Add more as we go. If you present on a paper, write a one-page summary
and link it from your `directions/<you>/` folder.
