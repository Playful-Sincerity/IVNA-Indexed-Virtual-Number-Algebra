"""
IVNA Verification Suite — Category B: NSA Embedding Consistency
===============================================================

This file tests IVNA axioms via the Non-Standard Analysis embedding:

    0_x  ->  x * epsilon^order      (indexed zero = infinitesimal multiple)
    inf_x -> x * epsilon^(-order)   (indexed infinity = infinite multiple)

Under standard algebra with symbolic epsilon > 0, all IVNA axioms must hold.
This provides the concrete model that guarantees IVNA's consistency.

Category B is intentionally standalone — no ivna.py import. The embedding
is tested against standard SymPy algebra, not against IVNA's own Python
class. This is a model-theoretic check, not a software test.
"""

import sys
from sympy import symbols, Symbol, simplify, series, ln, exp, oo

# --- symbolic setup ---------------------------------------------------------

eps = Symbol('epsilon_0', positive=True)
x, y, z = symbols('x y z', real=True, nonzero=True)
r = Symbol('r', real=True, nonzero=True)

# --- embedding functions ----------------------------------------------------

def embed_zero(index, order=1):
    """Map 0_index (order) -> index * eps^order."""
    return index * eps**order

def embed_inf(index, order=1):
    """Map inf_index (order) -> index * eps^(-order)."""
    return index * eps**(-order)

# --- check harness ----------------------------------------------------------

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

def sym_eq(expr):
    """Return True if a SymPy expression simplifies to zero."""
    return simplify(expr) == 0


# ============================================================
# A1: 0_x * 0_y = 0^2_{xy}
# ============================================================

# embed_zero(x) * embed_zero(y) = x*eps * y*eps = xy*eps^2 = embed_zero(xy, order=2)
lhs = embed_zero(x) * embed_zero(y)
rhs = embed_zero(x * y, order=2)
check("A1: embed_zero(x)*embed_zero(y) = embed_zero(xy, 2)", sym_eq(lhs - rhs))

# Concrete cases
for a, b in [(2, 3), (5, 7), (1, 1)]:
    lhs = embed_zero(a) * embed_zero(b)
    rhs = embed_zero(a * b, order=2)
    check(f"A1-concrete: embed_zero({a})*embed_zero({b}) = embed_zero({a*b}, 2)",
          sym_eq(lhs - rhs))


# ============================================================
# A2: inf_x * inf_y = inf^2_{xy}
# ============================================================

lhs = embed_inf(x) * embed_inf(y)
rhs = embed_inf(x * y, order=2)
check("A2: embed_inf(x)*embed_inf(y) = embed_inf(xy, 2)", sym_eq(lhs - rhs))

for a, b in [(2, 3), (5, 7), (1, 1)]:
    lhs = embed_inf(a) * embed_inf(b)
    rhs = embed_inf(a * b, order=2)
    check(f"A2-concrete: embed_inf({a})*embed_inf({b}) = embed_inf({a*b}, 2)",
          sym_eq(lhs - rhs))


# ============================================================
# A3: 0_x * inf_y = xy  (product / exit rule)
# ============================================================

# x*eps * y*eps^(-1) = xy (eps cancels)
lhs = embed_zero(x) * embed_inf(y)
rhs = x * y
check("A3: embed_zero(x)*embed_inf(y) = xy", sym_eq(lhs - rhs))

# Commutativity
check("A3-comm: embed_inf(y)*embed_zero(x) = xy",
      sym_eq(embed_inf(y) * embed_zero(x) - x * y))

for a, b in [(2, 3), (7, 5), (1, 1)]:
    lhs = embed_zero(a) * embed_inf(b)
    check(f"A3-concrete: embed_zero({a})*embed_inf({b}) = {a*b}",
          sym_eq(lhs - a * b))


# ============================================================
# A4: n * 0_x = 0_{nx}
# ============================================================

# r * (x*eps) = (rx)*eps = embed_zero(rx)
lhs = r * embed_zero(x)
rhs = embed_zero(r * x)
check("A4: r*embed_zero(x) = embed_zero(rx)", sym_eq(lhs - rhs))

for n, a in [(3, 2), (5, 7), (-2, 3)]:
    check(f"A4-concrete: {n}*embed_zero({a}) = embed_zero({n*a})",
          sym_eq(n * embed_zero(a) - embed_zero(n * a)))


# ============================================================
# A5: n * inf_x = inf_{nx}
# ============================================================

lhs = r * embed_inf(x)
rhs = embed_inf(r * x)
check("A5: r*embed_inf(x) = embed_inf(rx)", sym_eq(lhs - rhs))

for n, a in [(3, 2), (5, 7), (-1, 3)]:
    check(f"A5-concrete: {n}*embed_inf({a}) = embed_inf({n*a})",
          sym_eq(n * embed_inf(a) - embed_inf(n * a)))


# ============================================================
# A6: y / 0_x = inf_{y/x}
# ============================================================

# y / (x*eps) = (y/x) * eps^(-1) = embed_inf(y/x)
lhs = y / embed_zero(x)
rhs = embed_inf(y / x)
check("A6: y/embed_zero(x) = embed_inf(y/x)", sym_eq(lhs - rhs))

for yv, xv in [(6, 2), (10, 5), (1, 1)]:
    check(f"A6-concrete: {yv}/embed_zero({xv}) = embed_inf({yv}/{xv})",
          sym_eq(yv / embed_zero(xv) - embed_inf(yv / xv)))


# ============================================================
# A7: y / inf_x = 0_{y/x}
# ============================================================

# y / (x*eps^(-1)) = (y/x)*eps = embed_zero(y/x)
lhs = y / embed_inf(x)
rhs = embed_zero(y / x)
check("A7: y/embed_inf(x) = embed_zero(y/x)", sym_eq(lhs - rhs))

for yv, xv in [(6, 2), (10, 5), (1, 1)]:
    check(f"A7-concrete: {yv}/embed_inf({xv}) = embed_zero({yv}/{xv})",
          sym_eq(yv / embed_inf(xv) - embed_zero(yv / xv)))


# ============================================================
# A8: 0_x / 0_y = x/y  (ratio exits to real)
# ============================================================

# (x*eps) / (y*eps) = x/y
lhs = embed_zero(x) / embed_zero(y)
rhs = x / y
check("A8: embed_zero(x)/embed_zero(y) = x/y", sym_eq(lhs - rhs))

for xv, yv in [(6, 2), (10, 5), (7, 3)]:
    check(f"A8-concrete: embed_zero({xv})/embed_zero({yv}) = {xv}/{yv}",
          sym_eq(embed_zero(xv) / embed_zero(yv) - xv / yv))


# ============================================================
# A9: inf_x / inf_y = x/y
# ============================================================

# (x*eps^(-1)) / (y*eps^(-1)) = x/y
lhs = embed_inf(x) / embed_inf(y)
rhs = x / y
check("A9: embed_inf(x)/embed_inf(y) = x/y", sym_eq(lhs - rhs))

for xv, yv in [(6, 2), (10, 5), (7, 3)]:
    check(f"A9-concrete: embed_inf({xv})/embed_inf({yv}) = {xv}/{yv}",
          sym_eq(embed_inf(xv) / embed_inf(yv) - xv / yv))


# ============================================================
# A10: 0_x + 0_y = 0_{x+y}
# ============================================================

lhs = embed_zero(x) + embed_zero(y)
rhs = embed_zero(x + y)
check("A10: embed_zero(x)+embed_zero(y) = embed_zero(x+y)", sym_eq(lhs - rhs))

for xv, yv in [(2, 3), (7, 5), (1, 1)]:
    check(f"A10-concrete: embed_zero({xv})+embed_zero({yv}) = embed_zero({xv+yv})",
          sym_eq(embed_zero(xv) + embed_zero(yv) - embed_zero(xv + yv)))


# ============================================================
# A11: inf_x + inf_y = inf_{x+y}
# ============================================================

lhs = embed_inf(x) + embed_inf(y)
rhs = embed_inf(x + y)
check("A11: embed_inf(x)+embed_inf(y) = embed_inf(x+y)", sym_eq(lhs - rhs))

for xv, yv in [(2, 3), (7, 5), (1, 1)]:
    check(f"A11-concrete: embed_inf({xv})+embed_inf({yv}) = embed_inf({xv+yv})",
          sym_eq(embed_inf(xv) + embed_inf(yv) - embed_inf(xv + yv)))


# ============================================================
# D-INDEX-ZERO: 0_x - 0_x = real 0
# ============================================================

# x*eps - x*eps = 0 (standard)
lhs = embed_zero(x) - embed_zero(x)
check("D-INDEX-ZERO: embed_zero(x)-embed_zero(x) = 0", sym_eq(lhs))

for xv in [1, 3, 7]:
    check(f"D-INDEX-ZERO-concrete: embed_zero({xv})-embed_zero({xv}) = 0",
          sym_eq(embed_zero(xv) - embed_zero(xv)))


# ============================================================
# A-EXP leading term: (y/eps)*ln(1 + x*eps) has constant term xy
# ============================================================

# Expand ln(1 + x*eps) = x*eps - (x*eps)^2/2 + ... so (y/eps)*(...) = xy + O(eps)
# Constant term (coefficient of eps^0) should be x*y.
expr = (y / eps) * ln(1 + x * eps)
s = series(expr, eps, 0, 2)          # expand to eps^1
const_term = s.coeff(eps, 0)         # coefficient of eps^0
check("A-EXP leading term: (y/eps)*ln(1+x*eps) constant = xy",
      sym_eq(const_term - x * y))

# Concrete case
expr_c = (3 / eps) * ln(1 + 2 * eps)
s_c = series(expr_c, eps, 0, 2)
check("A-EXP leading term concrete: (3/eps)*ln(1+2*eps) constant = 6",
      sym_eq(s_c.coeff(eps, 0) - 6))


# ============================================================
# Negation: -embed_zero(x) = embed_zero(-x)
# ============================================================

check("Negation: -embed_zero(x) = embed_zero(-x)",
      sym_eq(-embed_zero(x) - embed_zero(-x)))

check("Negation-inf: -embed_inf(x) = embed_inf(-x)",
      sym_eq(-embed_inf(x) - embed_inf(-x)))

for xv in [2, 5, -3]:
    check(f"Negation-concrete: -embed_zero({xv}) = embed_zero({-xv})",
          sym_eq(-embed_zero(xv) - embed_zero(-xv)))


# ============================================================
# HIGHER-ORDER embedding checks
# ============================================================

# embed_zero(x, 2) * embed_inf(y, 2) = xy  (orders cancel exactly)
# x*eps^2 * y*eps^(-2) = xy
lhs = embed_zero(x, 2) * embed_inf(y, 2)
check("HO: embed_zero(x,2)*embed_inf(y,2) = xy", sym_eq(lhs - x * y))

for xv, yv in [(2, 3), (5, 7)]:
    check(f"HO-concrete(2,2): embed_zero({xv},2)*embed_inf({yv},2) = {xv*yv}",
          sym_eq(embed_zero(xv, 2) * embed_inf(yv, 2) - xv * yv))

# embed_zero(x, 3) * embed_inf(y, 2) = xy*eps  (one zero remains)
# x*eps^3 * y*eps^(-2) = xy*eps = embed_zero(xy, 1)
lhs = embed_zero(x, 3) * embed_inf(y, 2)
rhs = embed_zero(x * y, 1)
check("HO: embed_zero(x,3)*embed_inf(y,2) = embed_zero(xy,1) = xy*eps",
      sym_eq(lhs - rhs))

for xv, yv in [(2, 3), (1, 1)]:
    check(f"HO-concrete(3,2): embed_zero({xv},3)*embed_inf({yv},2) = embed_zero({xv*yv},1)",
          sym_eq(embed_zero(xv, 3) * embed_inf(yv, 2) - embed_zero(xv * yv, 1)))

# embed_zero(x, 3) * embed_inf(y, 1) = xy*eps^2  (two zeros remain)
# x*eps^3 * y*eps^(-1) = xy*eps^2 = embed_zero(xy, 2)
lhs = embed_zero(x, 3) * embed_inf(y, 1)
rhs = embed_zero(x * y, 2)
check("HO: embed_zero(x,3)*embed_inf(y,1) = embed_zero(xy,2) = xy*eps^2",
      sym_eq(lhs - rhs))

for xv, yv in [(2, 3), (1, 1)]:
    check(f"HO-concrete(3,1): embed_zero({xv},3)*embed_inf({yv},1) = embed_zero({xv*yv},2)",
          sym_eq(embed_zero(xv, 3) * embed_inf(yv, 1) - embed_zero(xv * yv, 2)))

# Mixed order: (order n, order n) always cancels to a real scalar
for n in [1, 2, 3, 4]:
    lhs = embed_zero(x, n) * embed_inf(y, n)
    check(f"HO-order-cancel(n={n}): embed_zero(x,{n})*embed_inf(y,{n}) = xy",
          sym_eq(lhs - x * y))

# Symmetric: embed_zero(x, m) * embed_inf(y, n) leaves order |m-n|
# m > n -> virtual zero of order m-n; m < n -> virtual inf of order n-m
lhs = embed_zero(x, 2) * embed_inf(y, 3)   # eps^2 * eps^(-3) = eps^(-1) -> inf
rhs = embed_inf(x * y, 1)
check("HO-asymm(2,3): embed_zero(x,2)*embed_inf(y,3) = embed_inf(xy,1)",
      sym_eq(lhs - rhs))


# ============================================================
# REPORT
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("IVNA VERIFICATION — CATEGORY B: NSA EMBEDDING CONSISTENCY")
    print("=" * 70)
    print()
    print("  Embedding: 0_x -> x*eps^order,  inf_x -> x*eps^(-order)")
    print("  Engine:    SymPy symbolic algebra (no ivna.py)")
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
        print("  ALL CATEGORY B CHECKS PASSED")
    else:
        print(f"  {failed} CHECKS FAILED")

    sys.exit(0 if failed == 0 else 1)
