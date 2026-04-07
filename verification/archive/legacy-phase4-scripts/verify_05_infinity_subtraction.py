#!/usr/bin/env python3
"""Verify-05: Infinity subtraction ∞_a - ∞_b = ∞_{a-b}.

Claim: A11 makes ∞ - ∞ determinate. NSA embedding: a/ε - b/ε = (a-b)/ε.
D-INDEX-ZERO: ∞_0 → 0.

Tests: symbolic identity, specific values, edge cases, Z3 consistency.
"""
import sys
import sympy as sp

results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-05: Infinity subtraction ∞_a - ∞_b = ∞_{a-b}")
print("=" * 60)

a, b, eps = sp.symbols('a b epsilon', real=True)

# --- Symbolic identity ---
print("\n--- Symbolic identity: a/ε - b/ε = (a-b)/ε ---")
identity = sp.simplify(a/eps - b/eps - (a - b)/eps)
check("a/ε - b/ε - (a-b)/ε = 0", identity == 0)

# --- Specific cases ---
print("\n--- Specific cases ---")
cases = [
    ("a=3, b=1", 3, 1, 2),
    ("a=5, b=5", 5, 5, 0),
    ("a=π, b=-π", sp.pi, -sp.pi, 2*sp.pi),
    ("a=1, b=-1", 1, -1, 2),
]
for name, a_val, b_val, expected_idx in cases:
    result = sp.simplify(a_val/eps - b_val/eps)
    if expected_idx == 0:
        check(f"{name}: ∞_{a_val} - ∞_{b_val} = 0 (D-INDEX-ZERO)", result == 0)
    else:
        expected = expected_idx/eps
        check(f"{name}: ∞_{a_val} - ∞_{b_val} = ∞_{{{expected_idx}}}",
              sp.simplify(result - expected) == 0)

# --- Edge cases ---
print("\n--- Edge cases ---")
check("∞_a - ∞_{-a} = ∞_{2a}", sp.simplify(a/eps - (-a)/eps - 2*a/eps) == 0)
check("∞_a - ∞_a = 0", sp.simplify(a/eps - a/eps) == 0)

# --- Z3 consistency ---
print("\n--- Z3 consistency check ---")
try:
    from z3 import Reals, Solver, sat, unsat, Not, ForAll
    a_z3, b_z3, eps_z3 = Reals('a b eps')
    s = Solver()
    # The negation of the identity should be unsatisfiable
    s.add(eps_z3 != 0)
    s.add(Not(a_z3/eps_z3 - b_z3/eps_z3 == (a_z3 - b_z3)/eps_z3))
    result = s.check()
    check("Z3: negation of identity is UNSAT", result == unsat)
except ImportError:
    print("  [SKIP] Z3 not available")

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
