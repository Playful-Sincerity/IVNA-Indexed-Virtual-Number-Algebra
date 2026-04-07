#!/usr/bin/env python3
"""Verify-07: Compound growth / e scaling symmetry.

Claim: (1 + 0_{x/n})^{∞_{ny}} = e^{xy} — the index product (x/n)(ny) = xy
cancels n, making the result scale-invariant.

Tests: Limit[(1+x/(nm))^(nmy), m→∞] = e^{xy} for n = 1, 2, 3, 1/2, π.
"""
import sys
import sympy as sp

x, y, m = sp.symbols('x y m', real=True, positive=True)
results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-07: Compound growth / e scaling symmetry")
print("=" * 60)

# --- IVNA index cancellation ---
print("\n--- IVNA index cancellation: (x/n)(ny) = xy ---")
n = sp.Symbol('n', positive=True)
product = sp.simplify((x/n) * (n*y))
check("(x/n)(ny) simplifies to xy", product == x*y)

# --- Limit verification for each n ---
print("\n--- Limit[(1 + x/(nm))^(nmy), m→∞] = e^{xy} ---")
n_values = [
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (sp.Rational(1,2), "1/2"),
    (sp.pi, "π"),
]

for n_val, n_name in n_values:
    expr = (1 + x/(n_val*m))**(n_val*m*y)
    lim = sp.limit(expr, m, sp.oo)
    check(f"n={n_name}: limit = e^{{xy}}", sp.simplify(lim - sp.exp(x*y)) == 0)

# --- Numerical verification ---
print("\n--- Numerical spot check: x=2, y=3 → e^6 ---")
import math
e6 = math.exp(6)
for n_val, n_name in [(1, "1"), (2, "2"), (3, "3"), (0.5, "1/2"), (math.pi, "π")]:
    m_val = 10**8
    approx = (1 + 2/(n_val*m_val))**(n_val*m_val*3)
    err = abs(approx - e6)
    check(f"n={n_name} numeric: |approx - e^6| < 0.01 (err={err:.2e})", err < 0.01)

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
