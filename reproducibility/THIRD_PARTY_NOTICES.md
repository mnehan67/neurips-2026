# Third-party notices and use restrictions

This public reproducibility repository does **not** redistribute pretrained model weights and does **not** redistribute full raw C4 or WikiText documents. Model-level notebooks download public checkpoints directly from their canonical repositories at frozen revisions. The artifact includes only author-created code, derived experimental outputs, and small frozen token-ID inputs needed to make the intervention protocol exactly reproducible.

## Models

- **Pythia-70M and PolyPythias Pythia-70M seeds** (`EleutherAI/...`): model cards identify the license as **Apache-2.0**. No weights are included.
- **GPT-2 124M** (`openai-community/gpt2`): model card identifies the license as **MIT**. No weights are included.
- **Qwen2.5-0.5B** (`Qwen/Qwen2.5-0.5B`): model card identifies the license as **Apache-2.0**. No weights are included.
- **OPT-125M** (`facebook/opt-125m`): governed by the **OPT-175B License Agreement**. No weights are included. The model is used only for non-commercial research evaluation. The exact license text is included at `third_party_licenses/OPT-175B_LICENSE.md`. Required attribution from that license: “OPT-175B is licensed under the OPT-175B license, Copyright (c) Meta Platforms, Inc. All Rights Reserved.” The OPT license also restricts commercial/production, military/nuclear, surveillance, biometric, unlawful, and other prohibited uses, including certain uses of data produced by the software.

## Text sources used to create frozen token IDs

- **C4 (`allenai/c4`)**: the current dataset card identifies **ODC-BY 1.0** and states that use is additionally subject to Common Crawl terms of use. Attribution/provenance: C4 was introduced with Raffel et al., *Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer* (arXiv:1910.10683 / JMLR 2020); this artifact used the `allenai/c4` distribution. License: https://opendatacommons.org/licenses/by/1-0/ . Common Crawl terms: https://commoncrawl.org/terms-of-use . Apart from the short C4 excerpts printed in Figure 2 and its figure-source CSV, the artifact includes no raw C4 text. `inputs/pythia_confirmatory_c4_token_ids.zip` and `inputs/external_scope/c4/` contain transformed token IDs used only for reproducibility; to the extent upstream dataset/content terms apply to these transformations, those terms remain applicable.
- **WikiText (`Salesforce/wikitext`)**: attribution/provenance: Stephen Merity, Caiming Xiong, James Bradbury, and Richard Socher, *Pointer Sentinel Mixture Models* (arXiv:1609.07843). The current Hugging Face repository presents inconsistent license metadata: its top-level tags show **CC BY-SA 3.0** and **GFDL**, while the dataset-card licensing paragraph states **CC BY-SA 4.0**. Rather than silently choose one, this artifact preserves the upstream attribution, imposes no author-code license on the WikiText-derived files, and treats all applicable upstream terms as controlling. Canonical license references: https://creativecommons.org/licenses/by-sa/3.0/ , https://creativecommons.org/licenses/by-sa/4.0/ , and https://www.gnu.org/licenses/fdl-1.3.html . The artifact includes no raw WikiText text; `inputs/external_scope/wikitext/` contains transformed token IDs only.

Canonical model repository identifiers and exact model revisions are listed in `MODEL_REVISIONS.md`; input provenance is detailed in `DATA_PROVENANCE.md`. The author-code MIT license does not override any third-party term.


## Additional checkpoints in the public workshop manuscript

- Qwen3-8B: Qwen open-weight checkpoint distributed under Apache-2.0.
- Mistral-7B-v0.3: Mistral open-weight checkpoint distributed under Apache-2.0.

The artifact contains only derived numerical outputs and model identifiers; it does not redistribute these model weights.
