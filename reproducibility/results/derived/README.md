# Derived descriptive statistics

`crossed_receiver_effect_spread.csv` — for each crossed bucket, the median over 512 displacements of
log10(max_k K / min_k K) over the alternative receivers of one frozen displacement, and the fraction of
displacements with ratio >= 100 (paper Section 5.2 and Table 7). Regenerate with
`python analysis/derived_stats.py --out results/derived/crossed_receiver_effect_spread.csv`.
