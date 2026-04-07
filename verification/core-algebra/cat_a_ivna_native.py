"""
IVNA Verification Suite — Category A: IVNA-Native Algebraic Checks
===================================================================

Every check in this file uses the Virtual class (Z(), I()) as the
computational engine. These exercise IVNA's axiom system directly.

Category A is the authoritative measure of IVNA verification.
"""

import sys
import os
import math
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'code'))
from ivna import Virtual, Z, I, virtual_exp, ivna_derivative, virtual_taylor

passed = 0
failed = 0
results = []

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        results.append(("PASS", name))
    else:
        failed += 1
        results.append(("FAIL", name + (f" [{detail}]" if detail else "")))


# ============================================================
# A1: CORE AXIOMS (A1-A11 + D-INDEX-ZERO + Powers)
# ============================================================

# A1: 0_x * 0_y = 0^2_{xy}
for x, y in [(1,1), (2,3), (1,7), (Fraction(1,2),4), (5,5), (-2,3)]:
    r = Z(x) * Z(y)
    check(f"A1: Z({x})*Z({y}) = 0^2_{{{x*y}}}", r == Virtual('zero', x*y, 2))

# A2: inf_x * inf_y = inf^2_{xy}
for x, y in [(1,1), (2,3), (5,7), (-1,4), (Fraction(1,3),9)]:
    r = I(x) * I(y)
    check(f"A2: I({x})*I({y}) = inf^2_{{{x*y}}}", r == Virtual('inf', x*y, 2))

# A3: 0_x * inf_y = xy (the product/exit rule)
for x, y in [(1,1), (2,3), (7,5), (Fraction(1,3),9), (-3,2), (100,100)]:
    r = Z(x) * I(y)
    check(f"A3: Z({x})*I({y}) = {x*y}", r == Fraction(x*y))

# A3 commutativity
for x, y in [(2,3), (7,5), (1,1), (-4,2)]:
    check(f"A3-comm: I({y})*Z({x}) = {x*y}", I(y) * Z(x) == Fraction(x*y))

# A4: n * 0_x = 0_{nx}
for n, x in [(3,2), (5,7), (-2,3), (Fraction(1,2),4), (0,5)]:
    r = n * Z(x)
    check(f"A4: {n}*Z({x}) = Z({n*x})", r == Z(n*x))

# A5: n * inf_x = inf_{nx}
for n, x in [(3,2), (5,7), (-1,3), (Fraction(1,2),6)]:
    r = n * I(x)
    check(f"A5: {n}*I({x}) = I({n*x})", r == I(n*x))

# A6: y / 0_x = inf_{y/x}
for y_val, x in [(6,2), (10,5), (1,1), (7,3), (-3,2)]:
    r = y_val / Z(x)
    check(f"A6: {y_val}/Z({x}) = I({Fraction(y_val,x)})", r == I(Fraction(y_val,x)))

# A7: y / inf_x = 0_{y/x}
for y_val, x in [(6,2), (1,1), (10,5), (7,3)]:
    r = y_val / I(x)
    check(f"A7: {y_val}/I({x}) = Z({Fraction(y_val,x)})", r == Z(Fraction(y_val,x)))

# A8: 0_x / 0_y = x/y
for x, y in [(6,2), (10,5), (7,3), (1,1), (Fraction(1,2), Fraction(1,4))]:
    r = Z(x) / Z(y)
    check(f"A8: Z({x})/Z({y}) = {Fraction(x,y)}", r == Fraction(x, y))

# A9: inf_x / inf_y = x/y
for x, y in [(6,2), (10,5), (7,3), (1,1)]:
    r = I(x) / I(y)
    check(f"A9: I({x})/I({y}) = {Fraction(x,y)}", r == Fraction(x, y))

# A10: 0_x + 0_y = 0_{x+y}
for x, y in [(1,1), (2,3), (7,5), (-3,3), (Fraction(1,2), Fraction(1,2))]:
    r = Z(x) + Z(y)
    expected_idx = x + y
    if expected_idx == 0:
        check(f"A10+D-INDEX-ZERO: Z({x})+Z({y}) = 0", r == 0 and not isinstance(r, Virtual))
    else:
        check(f"A10: Z({x})+Z({y}) = Z({expected_idx})", r == Z(expected_idx))

# A11: inf_x + inf_y = inf_{x+y}
for x, y in [(1,1), (2,3), (7,5), (Fraction(1,3), Fraction(2,3))]:
    r = I(x) + I(y)
    check(f"A11: I({x})+I({y}) = I({x+y})", r == I(x+y))

# D-INDEX-ZERO: 0_x - 0_x = real 0
for x in [1, 3, 7, Fraction(1,2), 100]:
    r = Z(x) - Z(x)
    check(f"D-INDEX-ZERO: Z({x})-Z({x}) = 0", r == 0 and not isinstance(r, Virtual))

# Powers: (0_x)^n = 0^n_{x^n}
for x, n in [(2,3), (1,2), (3,2), (1,4), (2,5)]:
    r = Z(x) ** n
    check(f"Power: Z({x})^{n} = 0^{n}_{{{x**n}}}", r == Virtual('zero', x**n, n))

# Powers: (inf_x)^n = inf^n_{x^n}
for x, n in [(2,3), (1,2), (3,2)]:
    r = I(x) ** n
    check(f"Power: I({x})^{n} = inf^{n}_{{{x**n}}}", r == Virtual('inf', x**n, n))


# ============================================================
# A2: STRUCTURAL PROPERTIES
# ============================================================

# Associativity: (0_a * 0_b) * inf_c = 0_a * (0_b * inf_c)
for a, b, c in [(2,3,5), (1,7,3), (4,2,6)]:
    left = (Z(a) * Z(b)) * I(c)
    right = Fraction(b*c) * Z(a)
    check(f"Assoc: (Z({a})*Z({b}))*I({c}) = {a}*(Z({b})*I({c}))", left == right)

# Commutativity: Z(x)*I(y) = I(y)*Z(x)
for x, y in [(2,3), (7,5), (1,1), (10,10)]:
    check(f"Comm: Z({x})*I({y}) = I({y})*Z({x})", Z(x)*I(y) == I(y)*Z(x))

# Distributivity: Z(a)*(I(b)+I(c)) = Z(a)*I(b) + Z(a)*I(c)
for a, b, c in [(2,3,5), (1,4,6), (3,7,2)]:
    left = Z(a) * (I(b) + I(c))
    right = (Z(a) * I(b)) + (Z(a) * I(c))
    check(f"Distrib: Z({a})*(I({b})+I({c})) = Z({a})*I({b})+Z({a})*I({c})", left == right)

# Division-by-zero roundtrip: (y/0_x)*0_x = y
for y_val in [1, 5, 7, -3, Fraction(1,3), 42]:
    for x in [1, 2, 3]:
        step1 = y_val / Z(x)
        step2 = step1 * Z(x)
        check(f"Roundtrip: ({y_val}/Z({x}))*Z({x}) = {y_val}", step2 == Fraction(y_val))

# Double reciprocal: 1/(1/0_x) = 0_x
for x in [1, 2, 3, 7]:
    r = 1 / (1 / Z(x))
    check(f"DoubleRecip: 1/(1/Z({x})) = Z({x})", r == Z(x))


# ============================================================
# A3: HIGHER-ORDER INTERACTIONS
# ============================================================

# 0^2_x * inf_y = 0_{xy} (one order cancels)
for x, y in [(1,1), (2,3), (5,7)]:
    r = Virtual('zero', x, 2) * I(y)
    check(f"HiOrder: 0^2_{x}*I({y}) = Z({x*y})", r == Z(x*y))

# 0^3_x * inf^2_y = 0_{xy} (two orders cancel)
for x, y in [(1,1), (2,3)]:
    r = Virtual('zero', x, 3) * Virtual('inf', y, 2)
    check(f"HiOrder: 0^3_{x}*inf^2_{y} = Z({x*y})", r == Z(x*y))

# 0^n_1 * inf^n_1 = 1 (all orders cancel — key for integration)
for n in range(1, 6):
    r = Z(1)**n * I(1)**n
    check(f"OrderCancel: Z(1)^{n}*I(1)^{n} = 1", r == Fraction(1))


# ============================================================
# A4: DERIVATIVES VIA A-VT + A8 PIPELINE
# ============================================================

# Polynomial derivatives: d/dx(x^n) = n*x^(n-1)
for n in range(2, 7):
    x_val = 5
    from math import comb
    derivs = [comb(n, k) * math.factorial(k) * x_val**(n-k) / math.factorial(k)
              if k <= n else 0 for k in range(n+1)]
    # Simpler: derivatives of x^n at x_val
    derivs = []
    f_val = x_val ** n
    derivs.append(f_val)
    d = n * x_val**(n-1)
    derivs.append(d)
    d2 = n*(n-1) * x_val**(n-2) if n >= 2 else 0
    derivs.append(d2)
    d3 = n*(n-1)*(n-2) * x_val**(n-3) if n >= 3 else 0
    derivs.append(d3)

    result, residuals = ivna_derivative(derivs)
    expected = n * x_val**(n-1)
    check(f"Deriv: d/dx(x^{n}) at x={x_val} = {expected}",
          abs(float(result) - expected) < 1e-10,
          f"got {result}")

# Transcendental derivatives via A-VT + A8
test_fns = [
    ("sin", lambda a: [math.sin(a), math.cos(a), -math.sin(a), -math.cos(a)],
     lambda a: math.cos(a)),
    ("cos", lambda a: [math.cos(a), -math.sin(a), -math.cos(a), math.sin(a)],
     lambda a: -math.sin(a)),
    ("exp", lambda a: [math.exp(a)]*4,
     lambda a: math.exp(a)),
    ("ln", lambda a: [math.log(a), 1/a, -1/a**2, 2/a**3],
     lambda a: 1/a),
    ("1/x", lambda a: [1/a, -1/a**2, 2/a**3, -6/a**4],
     lambda a: -1/a**2),
]

for fname, deriv_fn, expected_fn in test_fns:
    test_points = [1.0, 2.0] if fname == "ln" or fname == "1/x" else [0.5, 1.0]
    for a in test_points:
        derivs = deriv_fn(a)
        result, residuals = ivna_derivative(derivs)
        expected = expected_fn(a)
        check(f"Deriv-AVT: d/dx({fname}) at x={a} = {expected:.6f}",
              abs(float(result) - expected) < 1e-10,
              f"got {float(result):.6f}")
        # Verify residuals are Virtual zeros
        for r in residuals:
            if isinstance(r, Virtual):
                check(f"Deriv-residual: {fname} at {a} residual is zero-kind",
                      r.kind == 'zero')


# ============================================================
# A5: EXPONENTIAL AXIOM (A-EXP)
# ============================================================

# e = (1 + 0_1)^{inf_1}
check("A-EXP: e = virtual_exp(1,1)", abs(virtual_exp(1,1) - math.e) < 1e-10)

# Scaling: (1+0_x)^{inf_y} = e^{xy}
for x, y in [(1,2), (2,1), (2,3), (0.5,2), (1,-1), (3,0.5)]:
    result = virtual_exp(x, y)
    expected = math.e ** (x*y)
    check(f"A-EXP: virtual_exp({x},{y}) = e^{{{x*y}}}",
          abs(result - expected) < 1e-8)

# Consistency: [e^{xy}]^2 = e^{2xy}
for x, y in [(1,1), (2,3)]:
    left = virtual_exp(x, y) ** 2
    right = virtual_exp(x, 2*y)
    check(f"A-EXP-consist: [e^{{{x*y}}}]^2 = e^{{{2*x*y}}}",
          abs(left - right) < 1e-8)


# ============================================================
# A6: INTEGRATION (Faulhaber Algebraic)
# ============================================================

# Z(1)^{k+1} * I(1)^{k+1} = 1 for k=0..5
for k in range(6):
    zero_power = Z(1) ** (k + 1)
    inf_power = I(1) ** (k + 1)
    product = zero_power * inf_power
    check(f"Integral-alg: Z(1)^{k+1}*I(1)^{k+1} = 1", product == Fraction(1))

# Higher-order terms remain virtual: Z(1)^{k+1} * I(1)^j with j<k+1
for k in [2, 3, 4]:
    zero_power = Z(1) ** (k + 1)
    inf_power = I(1) ** k  # one less than needed -> virtual zero remains
    product = zero_power * inf_power
    check(f"Integral-hiterm: Z(1)^{k+1}*I(1)^{k} is Virtual zero",
          isinstance(product, Virtual) and product.kind == 'zero')


# ============================================================
# A7: UNIFICATION — IVNA-NATIVE CHECKS
# ============================================================

# Bayes (A8): index ratio = density ratio
for joint, marginal in [(0.1, 0.3), (0.05, 0.5), (0.2, 0.8)]:
    r = Z(joint) / Z(marginal)
    check(f"Unif-Bayes: Z({joint})/Z({marginal}) = {Fraction(joint/marginal).limit_denominator(100)}",
          abs(float(r) - joint/marginal) < 1e-10)

# Dirac delta (A3): height*width = 1 via indexed product
for eps_num, eps_den in [(1,100), (1,1000), (1,10000)]:
    eps = Fraction(eps_num, eps_den)
    height = Fraction(eps_den, eps_num)
    r = Z(eps) * I(height)
    check(f"Unif-Dirac: Z({eps})*I({height}) = 1", r == Fraction(1))

# Residue extraction (A3): zero * pole = residue
for residue_val in [1, 2, 5]:
    r = Z(1) * I(residue_val)
    check(f"Unif-Residue: Z(1)*I({residue_val}) = {residue_val}", r == Fraction(residue_val))

# Infinity subtraction (D-INDEX-ZERO)
for a in [3, 7, 100]:
    r = I(a) - I(a)
    check(f"Unif-InfSub: I({a})-I({a}) = 0", r == 0 and not isinstance(r, Virtual))

# Compound growth (A-EXP scaling)
for n in [1, 2, 10]:
    r1 = virtual_exp(1, 1)
    r2 = virtual_exp(1/n, n)
    check(f"Unif-Growth: exp(1/{n},  {n}) = e", abs(r1 - r2) < 1e-8)

# KL boundary: Z(eps) * I(1/eps) for the 0*log(0) limit
for eps_num, eps_den in [(1,100), (1,1000)]:
    eps = Fraction(eps_num, eps_den)
    inv_eps = Fraction(eps_den, eps_num)
    r = Z(eps) * I(inv_eps)
    check(f"Unif-KL: Z({eps})*I({inv_eps}) = 1", r == Fraction(1))

# Blow-up (A6): real / Z(x) gives indexed infinity
for y, x in [(1,1), (3,2), (5,1)]:
    r = y / Z(x)
    check(f"Unif-Blowup: {y}/Z({x}) = I({Fraction(y,x)})", r == I(Fraction(y,x)))


# ============================================================
# REPORT
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("IVNA VERIFICATION — CATEGORY A: IVNA-NATIVE ALGEBRAIC")
    print("=" * 70)
    print()

    for status, name in results:
        icon = "PASS" if status == "PASS" else "FAIL"
        print(f"  [{icon}] {name}")

    print()
    print(f"  PASSED: {passed}")
    print(f"  FAILED: {failed}")
    print(f"  TOTAL:  {passed + failed}")
    print()

    if failed == 0:
        print("  ALL CATEGORY A CHECKS PASSED")
    else:
        print(f"  {failed} CHECKS FAILED")

    sys.exit(0 if failed == 0 else 1)
