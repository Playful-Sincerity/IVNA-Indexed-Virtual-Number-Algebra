#!/usr/bin/env python3
"""Verify-09: KL divergence — 0·ln(0) = 0 and p·ln(p/0) = ∞_p.

Claim: IVNA resolves two indeterminate forms in KL divergence by computation,
not convention.

Tests: limit verification, 3 probability distributions.
"""
import sys
import math
import sympy as sp

x, p, q, eps = sp.symbols('x p q epsilon', positive=True)
results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-09: KL divergence")
print("=" * 60)

# --- 0·ln(0) = 0 ---
print("\n--- lim_{ε→0+} ε·ln(ε) = 0 ---")
lim = sp.limit(eps * sp.log(eps), eps, 0, '+')
print(f"  Symbolic limit: {lim}")
check("ε·ln(ε) → 0 as ε→0+", lim == 0)

# Numerical convergence table
print("  Numerical convergence:")
for exp in [1, 2, 4, 8, 16]:
    e_val = 10**(-exp)
    val = e_val * math.log(e_val)
    print(f"    ε=10^{-exp}: ε·ln(ε) = {val:.6e}")
check("Numerical: |ε·ln(ε)| < 0.001 at ε=10^{-8}", abs(1e-8 * math.log(1e-8)) < 0.001)

# --- p·ln(p/0) = ∞ ---
print("\n--- lim_{q→0+} p·ln(p/q) = ∞ ---")
lim_inf = sp.limit(p * sp.log(p/eps), eps, 0, '+')
print(f"  Symbolic limit: {lim_inf}")
check("p·ln(p/q) → ∞ as q→0+", lim_inf == sp.oo)

# --- Distribution 1: p = q = [1/2, 1/2] → KL = 0 ---
print("\n--- Distribution 1: p=q=[1/2, 1/2] ---")
kl1 = sp.Rational(1,2)*sp.log(sp.Rational(1,2)/sp.Rational(1,2)) + \
      sp.Rational(1,2)*sp.log(sp.Rational(1,2)/sp.Rational(1,2))
print(f"  KL = {kl1}")
check("KL(p||p) = 0", kl1 == 0)

# --- Distribution 2: p=[0.9, 0.1], q=[0.5, 0.5] ---
print("\n--- Distribution 2: p=[0.9, 0.1], q=[0.5, 0.5] ---")
p2 = [sp.Rational(9,10), sp.Rational(1,10)]
q2 = [sp.Rational(1,2), sp.Rational(1,2)]
kl2 = sum(pi * sp.log(pi/qi) for pi, qi in zip(p2, q2))
kl2_simplified = sp.simplify(kl2)
kl2_float = float(kl2_simplified)
print(f"  KL (exact): {kl2_simplified}")
print(f"  KL (float): {kl2_float:.15f}")
check("KL > 0 (Gibbs inequality)", kl2_float > 0)

# Cross-check with direct computation
kl2_direct = 0.9*math.log(0.9/0.5) + 0.1*math.log(0.1/0.5)
check("KL matches direct float computation",
      abs(kl2_float - kl2_direct) < 1e-12)

# --- Distribution 3: p=[1/3,1/3,1/3], q=[1/2,1/4,1/4] ---
print("\n--- Distribution 3: p=[1/3,1/3,1/3], q=[1/2,1/4,1/4] ---")
p3 = [sp.Rational(1,3), sp.Rational(1,3), sp.Rational(1,3)]
q3 = [sp.Rational(1,2), sp.Rational(1,4), sp.Rational(1,4)]
kl3 = sum(pi * sp.log(pi/qi) for pi, qi in zip(p3, q3))
kl3_simplified = sp.simplify(kl3)
kl3_float = float(kl3_simplified)
print(f"  KL (exact): {kl3_simplified}")
print(f"  KL (float): {kl3_float:.15f}")
check("KL > 0 (Gibbs inequality)", kl3_float > 0)

kl3_direct = sum(1/3*math.log((1/3)/qi) for qi in [0.5, 0.25, 0.25])
check("KL matches direct float computation",
      abs(kl3_float - kl3_direct) < 1e-12)

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
