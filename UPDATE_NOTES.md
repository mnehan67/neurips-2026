# Public repository update — 2026-10-24

Prepared from the user-supplied **FINAL NEURIPS NEHAN MADE.zip**, using the Website/ files as the project-page source and its nested GitHub_Repository archive as the reproducibility source. The live GitHub repository was read for comparison only; it was not modified during packaging.

## Changes relative to the previous live repository

- Replaced the root website with the final, longer-spaced version: new camera-ready abstract, interactive Magnitude/Direction/Stress Tests visualizer, unchanged accepted-workshop hero and MusIML-only BibTeX.
- Included `static/js/explorer.js`, absent from the old live repository; included updated CSS and the clean Figure 1 image.
- Added the camera-ready paper's **Figure 5** as a website illustration of individual within-displacement receiver rankings, with a data-regeneration function in the figure script.
- Added final `reproducibility/results/crossed_stress_tests_v1/` data, including corrected fragility summaries and the exact downstream-suffix stress-test rows.
- Added `notebooks/kaggle_2xT4_crossed_reviewer_stress_tests.ipynb`, `scripts/audit_crossed_stress_tests.py`, and that audit to the main CPU verification suite.
- Updated reproducibility documentation, root README, and preferred citation metadata for consistency with the website; restored the source-scoped MIT license text.
- Added an offline website-relative-asset check and `.nojekyll` marker for branch-based GitHub Pages.

## Deliberately excluded

- NeurIPS camera-ready PDF submissions and Overleaf source ZIPs: paper deliverables, not website or reproducibility artifacts.
- The outer combined archives, local build previews, and private audit logs.
- The superseded cache-collided held-out fragility summary and unverified manuscript edits.

## Local verification

The four-part CPU audit, independent numerical JVP verification, static website asset check, and complete figure regeneration were run against the packaged frozen data. The updated Figure 5 Spearman results match the published 0/1/2 panels. These checks verify *internal consistency of released outputs*, not a full GPU re-execution of the experiments.
