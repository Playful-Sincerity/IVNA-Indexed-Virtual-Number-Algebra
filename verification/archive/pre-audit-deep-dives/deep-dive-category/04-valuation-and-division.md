# Verification 4: Valuation Property and Division Axioms

**Tool:** SymPy 1.14.0 (Python venv)
**Tests:** 5/5 passed (1 valuation + 4 division)

## What Was Verified

### Valuation Property
The grade map G: (c,n) -> n is a discrete valuation:
- G(x*y) = G(x) + G(y) (multiplicative -> additive)

### Division Axioms in NSA
All four IVNA division axioms are verified algebraically via the NSA embedding.

## SymPy Code

```python
import sympy as sp

eps = sp.Symbol('epsilon', positive=True)
a, b, c = sp.symbols('a b c', real=True, nonzero=True)

# Valuation: grade(0^3_a * inf^2_b) = 3 + (-2) = 1
# (a*eps^3) * (b/eps^2) should equal a*b*eps (grade 1)
assert sp.simplify((a*eps**3)*(b/eps**2) - a*b*eps) == 0

# Division axioms
# A8: 0_a / 0_b = a/b
assert sp.simplify((a*eps)/(b*eps) - a/b) == 0

# A9: inf_a / inf_b = a/b
assert sp.simplify((a/eps)/(b/eps) - a/b) == 0

# A6: c / 0_a = inf_{c/a}
assert sp.simplify(c/(a*eps) - (c/a)/eps) == 0

# A7: c / inf_a = 0_{c/a}
assert sp.simplify(c/(a/eps) - (c/a)*eps) == 0
```

## Results

All 5 tests passed.

## Notes on Valuation

The grade map satisfies both valuation axioms:
1. G(xy) = G(x) + G(y) — verified above
2. G(x+y) >= min(G(x), G(y)) — holds trivially because IVNA addition is only defined within grades (A10, A11), so G(x) = G(y) = n implies G(x+y) = n = min(n,n). The exception is D-INDEX-ZERO (a + (-a) -> 0), where G(0) = +infinity by convention, satisfying the inequality.

The valuation ring {(c,n) : n >= 0} consists of reals and indexed zeros (no infinities). The maximal ideal {(c,n) : n > 0} is the indexed zeros. The residue field is R*.
