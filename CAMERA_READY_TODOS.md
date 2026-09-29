# Camera-ready additions reserved in the project page

The public page already contains a hidden, commented-out `#camera-ready-additions` section in `index.html`.
Uncomment it only when the requested analyses are ready.

## Reviewer-requested additions

1. Add a stronger scale baseline: displacement norm relative to the receiver-state norm.
2. Add an attribution-patching / AtP-style baseline.
3. Add a small exact-JVP / FP32 closure experiment to rule out finite-difference error.
4. Reconcile the differing raw correlations reported across sections.
5. Sharpen the contribution statement beyond simply confirming the local second-order KL approximation at full dose.

## Suggested public-page wording after the new results exist

Keep the novelty statement narrow: the contribution is the controlled crossed-receiver intervention in which the exact same natural displacement is physically applied to multiple destinations, together with evidence that receiver-local downstream geometry predicts the resulting destination-specific full-dose ordering. Do not frame the Fisher quadratic form itself as new.
