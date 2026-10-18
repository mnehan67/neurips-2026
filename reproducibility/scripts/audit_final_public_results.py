#!/usr/bin/env python3
"""Run the compact CPU audit suite for the public release."""
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=[
    "scripts/audit_physical_crossing.py",
    "scripts/audit_rank_variance_decomposition.py",
    "scripts/audit_receiver_transformation.py",
    "scripts/audit_q_vs_dose.py",
]
for rel in SCRIPTS:
    print("\n"+"="*80)
    print("RUN",rel)
    print("="*80)
    subprocess.run([sys.executable,str(ROOT/rel)],check=True,cwd=ROOT)
print("\nAll public-release headline audits passed.")
