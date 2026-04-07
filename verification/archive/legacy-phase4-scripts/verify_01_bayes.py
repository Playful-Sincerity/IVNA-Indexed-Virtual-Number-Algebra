#!/usr/bin/env python3
"""Verify-01: A8 = Bayes' theorem for continuous densities.

Claim: 0_{f(x,y)} / 0_{f(x)} = f(y|x) — IVNA's zero-division rule (A8)
directly produces the conditional density formula.

Tests: bivariate normal (general rho), Gumbel bivariate exponential, bivariate Cauchy.
"""
import sys
import sympy as sp

x, y, rho = sp.symbols('x y rho', real=True)
results = []

def check(name, condition):
    status = "PASS" if condition else "FAIL"
    results.append((name, status))
    print(f"  [{status}] {name}")
    return condition

print("=" * 60)
print("VERIFY-01: A8 = Bayes' theorem for continuous densities")
print("=" * 60)

# --- Test 1: Bivariate Normal (general rho) ---
print("\n--- Test 1: Bivariate Normal (general rho) ---")
fXY = 1/(2*sp.pi*sp.sqrt(1 - rho**2)) * sp.exp(-(x**2 - 2*rho*x*y + y**2)/(2*(1 - rho**2)))
fX = 1/sp.sqrt(2*sp.pi) * sp.exp(-x**2/2)
known_cond = 1/sp.sqrt(2*sp.pi*(1 - rho**2)) * sp.exp(-(y - rho*x)**2/(2*(1 - rho**2)))

ivna_cond = sp.simplify(fXY / fX)
diff = sp.simplify(ivna_cond - known_cond)
print(f"  IVNA conditional: {ivna_cond}")
print(f"  Known conditional: {known_cond}")
print(f"  Difference: {diff}")
check("Normal (general rho): IVNA matches known conditional", diff == 0)

# Specific rho=1/2
diff_half = sp.simplify(ivna_cond.subs(rho, sp.Rational(1,2)) - known_cond.subs(rho, sp.Rational(1,2)))
check("Normal (rho=1/2): IVNA matches known conditional", diff_half == 0)

# --- Test 2: Gumbel Bivariate Exponential (theta=1/2) ---
print("\n--- Test 2: Gumbel Bivariate Exponential (theta=1/2) ---")
theta = sp.Rational(1, 2)
fXY_exp = (1 + theta*(2*sp.exp(-x) - 1)*(2*sp.exp(-y) - 1)) * sp.exp(-x - y)
fX_exp = sp.integrate(fXY_exp, (y, 0, sp.oo))
print(f"  Marginal f_X: {sp.simplify(fX_exp)}")
check("Exponential: marginal is exp(-x)", sp.simplify(fX_exp - sp.exp(-x)) == 0)

cond_exp = sp.simplify(fXY_exp / fX_exp)
int_check = sp.integrate(cond_exp, (y, 0, sp.oo))
print(f"  Conditional integrates to: {sp.simplify(int_check)}")
check("Exponential: conditional integrates to 1", sp.simplify(int_check) == 1)

# --- Test 3: Bivariate Cauchy (pathological) ---
print("\n--- Test 3: Bivariate Cauchy (pathological) ---")
fXY_cauchy = 1/(2*sp.pi*(1 + x**2 + y**2)**sp.Rational(3,2))
fX_cauchy = sp.integrate(fXY_cauchy, (y, -sp.oo, sp.oo))
print(f"  Marginal f_X: {sp.simplify(fX_cauchy)}")
check("Cauchy: marginal is standard Cauchy", sp.simplify(fX_cauchy - 1/(sp.pi*(1 + x**2))) == 0)

cond_cauchy = sp.simplify(fXY_cauchy / fX_cauchy)
int_cauchy = sp.integrate(cond_cauchy, (y, -sp.oo, sp.oo))
print(f"  Conditional integrates to: {sp.simplify(int_cauchy)}")
check("Cauchy: conditional integrates to 1", sp.simplify(int_cauchy) == 1)

# --- Summary ---
print("\n" + "=" * 60)
passed = sum(1 for _, s in results if s == "PASS")
total = len(results)
print(f"RESULT: {passed}/{total} checks passed")
print("VERDICT:", "PASS" if passed == total else "FAIL")
sys.exit(0 if passed == total else 1)
