# Frozen model revisions

The model-level notebooks use the exact revisions recorded by the original confirmatory runs.

| Model | Revision / checkpoint | License metadata |
|---|---|---|
| `EleutherAI/pythia-70m` | `de3e4e2d6cbb3b1a51f90fe153ea51fcd8c7c852` (checkpoint 143000) | Apache-2.0 |
| `EleutherAI/pythia-70m-seed1` | `a94dc37ad8326640e664560d32a0d4a229253fce` (143000) | Apache-2.0 |
| `EleutherAI/pythia-70m-seed2` | `258e7aedecacc445bdc68229398e49b9e90d59e0` (143000) | Apache-2.0 |
| `EleutherAI/pythia-70m-seed3` | `d6d278fb9b57ed4ce7faf49ad0aae4ee0805936b` (143000) | Apache-2.0 |
| `EleutherAI/pythia-70m-seed4` | `3df7f50e40f6af8ff5828969ecf527eb983b83f1` (143000) | Apache-2.0 |
| `EleutherAI/pythia-70m-seed5` | `3aadf268d91f74f998fbf12509e60a8a29c7c045` (143000) | Apache-2.0 |
| `openai-community/gpt2` | `607a30d783dfa663caf39e06633721c8d4cfcd7e` | MIT |
| `facebook/opt-125m` | `27dcfa74d334bc871f3234de431e71c6eeba5dd6` | OPT-175B License Agreement |
| `Qwen/Qwen2.5-0.5B` | `060db6499f32faf8b98477b0a26969ef7d8b9987` | Apache-2.0 |

No model weights are redistributed in this artifact.


## Fresh multi-billion study

The paper additionally evaluates:

- `Qwen/Qwen3-8B`
- `mistralai/Mistral-7B-v0.3`

These model IDs are recorded exactly as loaded in the frozen Kaggle run on 2026-08-25. The run did not log immutable Hugging Face commit revisions for these two checkpoints, so the artifact does not invent revision hashes post hoc. Model weights are not included.
