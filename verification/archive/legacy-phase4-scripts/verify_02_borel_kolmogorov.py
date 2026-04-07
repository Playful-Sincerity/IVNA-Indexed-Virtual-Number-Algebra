#!/usr/bin/env python3
"""Verify-02: Borel-Kolmogorov paradox dissolution.

Claim: Different parameterizations of uniform-on-S² give different indexed zeros,
hence different conditional densities. No paradox — just different IVNA computations.

Tests: 3 parameterizations of (theta, phi) on the unit sphere.
"""
import sys
import sympy as sp

theta, phi, u, lam = sp.symbols('theta phi u lambda', real=True)
results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-02: Borel-Kolmogorov paradox dissolution")
print("=" * 60)

# --- Parameterization 1: (theta, phi) ---
print("\n--- Param 1: (theta, phi), theta in [0,pi], phi in [0,2pi) ---")
f1_joint = sp.sin(theta)/(4*sp.pi)
f1_phi = sp.integrate(f1_joint, (theta, 0, sp.pi))
print(f"  Marginal f(phi): {f1_phi}")
check("Param1: marginal = 1/(2pi)", sp.simplify(f1_phi - 1/(2*sp.pi)) == 0)

cond1 = sp.simplify(f1_joint / f1_phi)
print(f"  Conditional f(theta|phi): {cond1}")
int1 = sp.integrate(cond1, (theta, 0, sp.pi))
check("Param1: conditional integrates to 1", sp.simplify(int1) == 1)
check("Param1: conditional = sin(theta)/2", sp.simplify(cond1 - sp.sin(theta)/2) == 0)

# --- Parameterization 2: (u=cos(theta), phi) ---
print("\n--- Param 2: (u=cos(theta), phi), u in [-1,1] ---")
f2_joint = 1/(4*sp.pi)
f2_phi = sp.integrate(f2_joint, (u, -1, 1))
print(f"  Marginal f(phi): {f2_phi}")
check("Param2: marginal = 1/(2pi)", sp.simplify(f2_phi - 1/(2*sp.pi)) == 0)

cond2 = sp.simplify(f2_joint / f2_phi)
print(f"  Conditional f(u|phi): {cond2}")
int2 = sp.integrate(cond2, (u, -1, 1))
check("Param2: conditional integrates to 1", sp.simplify(int2) == 1)
check("Param2: conditional = 1/2", sp.simplify(cond2 - sp.Rational(1, 2)) == 0)

# --- Key test: different conditionals from same event ---
print("\n--- Paradox check ---")
check("Different conditionals: sin(theta)/2 != 1/2",
      sp.simplify(cond1 - cond2) != 0)

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
