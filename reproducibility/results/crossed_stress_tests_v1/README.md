# Final crossed stress tests

Frozen 16-displacement × 15-alternative-receiver B1 audits for Qwen3-8B layer 14 and Mistral-7B-v0.3 layer 12.

Headline medians (Qwen / Mistral):
- exact FP32 downstream-suffix Fisher vs original full-dose KL: 0.884 / 0.930
- original FP16 Fisher vs exact FP32 Fisher ranking: 0.977 / 0.988
- p-only output-geometry baseline vs full-dose KL: 0.600 / 0.618
- fixed host full-dose logit-shift baseline: 0.521 / 0.609
- K(0.1x) ordering vs K(1.0x): 0.900 / 0.938
- exact FP32 Fisher vs K(0.1x): 0.993 / 0.996

`corrected_fragility/` recomputes the frozen 72/24 held-out receiver-fragility analysis with model-specific inputs. The earlier notebook output named `HELDOUT_FRAGILITY_SUMMARY.csv` had a cache-name collision and is deliberately not included here.

The PCA/5-NN naturality output is descriptive only and does not establish manifold membership.
