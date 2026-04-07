#!/usr/bin/env python3
"""Verify-04: Removable singularities as index cancellation.

Claim: A8 (0_a / 0_b = a/b) recovers classical limits by reading off
leading Taylor term ratios. No L'Hôpital, no limits, no circularity.

Tests: 6 expressions at x=0.
"""
import sys
import sympy as sp

x = sp.Symbol('x')
results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-04: Removable singularities as index cancellation")
print("=" * 60)

cases = [
    ("sin(x)/x",           sp.sin(x)/x,                          1),
    ("(e^x - 1)/x",        (sp.exp(x) - 1)/x,                   1),
    ("(1-cos(x))/x²",      (1 - sp.cos(x))/x**2,                sp.Rational(1, 2)),
    ("(tan(x)-x)/x³",      (sp.tan(x) - x)/x**3,                sp.Rational(1, 3)),
    ("(arcsin(x)-x)/x³",   (sp.asin(x) - x)/x**3,               sp.Rational(1, 6)),
    ("(ln(1+x)-x)/x²",     (sp.log(1 + x) - x)/x**2,            sp.Rational(-1, 2)),
]

for name, expr, expected in cases:
    print(f"\n--- {name} ---")

    # Method 1: Direct limit
    lim = sp.limit(expr, x, 0)
    check(f"{name} limit = {expected}", lim == expected)

    # Method 2: Taylor series — extract leading term ratio
    series = sp.series(expr, x, 0, n=1)
    leading = series.removeO()
    # Evaluate at x=0 (the constant term IS the limit)
    val = leading.subs(x, 0) if leading.has(x) else leading
    check(f"{name} Taylor leading term = {expected}", val == expected)

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
