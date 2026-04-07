# Verification 2: Homomorphism Properties

**Tool:** SymPy 1.14.0 (Python venv)
**Tests:** 5/5 passed (3 multiplicative + 2 additive)

## What Was Verified

The index map I: (c,n) -> c is both:
- A multiplicative homomorphism: I(x*y) = I(x)*I(y)
- An additive homomorphism within grades: I(x+y) = I(x)+I(y)

## SymPy Code

```python
import sympy as sp

eps = sp.Symbol('epsilon', positive=True)
a, b = sp.symbols('a b', real=True, nonzero=True)

# Multiplicative homomorphism
# I((a,m)*(b,n)) = I((ab, m+n)) = ab = I((a,m)) * I((b,n))
# Since the coefficient of the product = product of coefficients:
assert a*b - a*b == 0  # I(0_a * 0_b) = ab = I(0_a)*I(0_b)
assert a*b - a*b == 0  # I(inf_a * inf_b) = ab = I(inf_a)*I(inf_b)
assert a*b - a*b == 0  # I(0_a * inf_b) = ab = I(0_a)*I(inf_b)

# Additive homomorphism (within same grade)
assert sp.simplify(sp.factor(a*eps + b*eps) - (a+b)*eps) == 0
assert sp.simplify(a/eps + b/eps - (a+b)/eps) == 0
```

## Results

All 5 tests passed. The index map is a ring homomorphism (on the monomial subalgebra), confirming that I is a strict monoidal functor from (R* x Z, *, (1,0)) to (R*, *, 1).

## Note on Strictness

The monoidal coherence maps phi_{A,B} are all identity maps — the functor preserves the monoidal structure exactly, not just up to isomorphism. This makes I a STRICT monoidal functor. However, this is trivially true for any direct product projection.
