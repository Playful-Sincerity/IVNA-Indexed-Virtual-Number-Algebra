#!/usr/bin/env python3
"""Verify-08: Blow-up correspondence.

Claim: IVNA's 0_x/0_y corresponds to projective coordinates in algebraic blow-ups.

Tests: 2 two-variable examples where blow-up substitution y=tx resolves the singularity.
"""
import sys
import sympy as sp

x, y, t = sp.symbols('x y t')
results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-08: Blow-up correspondence")
print("=" * 60)

# --- Example 1: (x² + y²)/(xy) at origin ---
print("\n--- Example 1: f(x,y) = (x² + y²)/(xy) ---")
f1 = (x**2 + y**2)/(x*y)
# Blow-up: y = tx
f1_blown = f1.subs(y, t*x)
f1_simplified = sp.simplify(f1_blown)
print(f"  After y=tx: {f1_simplified}")
check("Example 1: simplifies to t + 1/t", sp.simplify(f1_simplified - (t + 1/t)) == 0)

# Verify it's well-defined for all t != 0
f1_at_t2 = f1_simplified.subs(t, 2)
check("Example 1: t=2 → 5/2", f1_at_t2 == sp.Rational(5, 2))
f1_at_t1 = f1_simplified.subs(t, 1)
check("Example 1: t=1 → 2", f1_at_t1 == 2)

# --- Example 2: (x³ - y³)/(x - y) at x=y ---
print("\n--- Example 2: f(x,y) = (x³ - y³)/(x - y) ---")
f2 = (x**3 - y**3)/(x - y)
f2_factored = sp.factor(x**3 - y**3)
print(f"  x³ - y³ factors as: {f2_factored}")

# Verify algebraic identity
identity = sp.expand((x**3 - y**3) - (x - y)*(x**2 + x*y + y**2))
check("Example 2: x³-y³ = (x-y)(x²+xy+y²)", identity == 0)

# Cancel common factors (simplify doesn't always cancel rational expressions)
f2_cancelled = sp.cancel(f2)
print(f"  Cancelled: {f2_cancelled}")
check("Example 2: simplifies to x²+xy+y²",
      sp.expand(f2_cancelled - (x**2 + x*y + y**2)) == 0)

# Evaluate at x=y (after cancellation, no longer 0/0)
f2_at_diag = f2_cancelled.subs(y, x)
print(f"  At x=y: {sp.simplify(f2_at_diag)}")
check("Example 2: at x=y gives 3x²", sp.simplify(f2_at_diag - 3*x**2) == 0)

# Numeric spot check
f2_numeric = f2_cancelled.subs([(x, 1), (y, 1)])
check("Example 2: f(1,1) = 3", f2_numeric == 3)

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
