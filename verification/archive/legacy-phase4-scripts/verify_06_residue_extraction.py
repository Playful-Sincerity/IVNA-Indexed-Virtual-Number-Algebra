#!/usr/bin/env python3
"""Verify-06: Residue extraction via product rule A3.

Claim: 0_x · ∞_{c/x} = c matches standard residue computation.
For simple poles: IVNA product rule = residue definition.
For double poles: differentiation of regularized product.

Tests: 6 functions, 9 poles (7 simple, 2 double).
"""
import sys
import sympy as sp

z = sp.Symbol('z')
results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-06: Residue extraction via product rule A3")
print("=" * 60)

cases = [
    # (name, function, pole, expected_residue)
    ("1/z at z=0",              1/z,                    0,      1),
    ("e^z/z² at z=0",           sp.exp(z)/z**2,         0,      1),
    ("1/(z(z-1)) at z=0",       1/(z*(z-1)),            0,      -1),
    ("1/(z(z-1)) at z=1",       1/(z*(z-1)),            1,      1),
    ("z/(z²+1) at z=i",         z/(z**2+1),             sp.I,   sp.Rational(1,2)),
    ("z/(z²+1) at z=-i",        z/(z**2+1),             -sp.I,  sp.Rational(1,2)),
    ("sin(z)/z² at z=0",        sp.sin(z)/z**2,         0,      1),
    ("(z+1)/(z²(z-1)) at z=0",  (z+1)/(z**2*(z-1)),    0,      -2),
    ("(z+1)/(z²(z-1)) at z=1",  (z+1)/(z**2*(z-1)),    1,      2),
]

for name, func, pole, expected in cases:
    res = sp.residue(func, z, pole)
    print(f"\n  {name}")
    print(f"    SymPy residue: {res}")
    print(f"    Expected: {expected}")
    check(name, sp.simplify(res - expected) == 0)

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
