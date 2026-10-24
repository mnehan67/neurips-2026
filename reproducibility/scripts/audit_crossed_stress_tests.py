from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parents[1]/'results'/'crossed_stress_tests_v1'
expect={'qwen3_8b':{'exact_Q32_vs_frozen_paper_K':0.8839285714,'frozen_Q16_vs_exact_Q32':0.9767857143,'K_0.10_vs_K1':0.9},'mistral_7b':{'exact_Q32_vs_frozen_paper_K':0.9303571429,'frozen_Q16_vs_exact_Q32':0.9875,'K_0.10_vs_K1':0.9375}}
for m,e in expect.items():
    d=pd.read_csv(R/m/f'{m}_STRESS_SUMMARY.csv').set_index('metric')
    for k,v in e.items():
        got=float(d.loc[k,'median_rho']); assert abs(got-v)<1e-9,(m,k,got,v)
f=pd.read_csv(R/'corrected_fragility'/'HELDOUT_FRAGILITY_CORRECTED_SUMMARY.csv').set_index('model')
assert abs(f.loc['qwen3_8b','pooled_heldout_residual_rho']-0.3793060813)<1e-9
assert abs(f.loc['mistral_7b','pooled_heldout_residual_rho']-0.4891085994)<1e-9
print('crossed stress-test audit: PASS')
