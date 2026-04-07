# Verification 6: Jet Space Connection

**Tool:** SymPy 1.14.0 (Python venv)
**Tests:** 4/4 passed

## What Was Verified

When an analytic function is evaluated at eps (i.e., at 0_1 in IVNA), the Taylor expansion produces a formal power series in eps. The coefficient of the leading virtual term equals the corresponding derivative data (the jet).

## SymPy Code

```python
import sympy as sp

eps = sp.Symbol('epsilon', positive=True)
x = sp.Symbol('x')

# sin(eps): Taylor at 0 gives eps - eps^3/6 + ...
sin_eps = sp.series(sp.sin(eps), eps, 0, n=4)
# Leading coefficient of eps is 1 = sin'(0)
assert str(sin_eps) == 'epsilon - epsilon**3/6 + O(epsilon**4)'

# exp(eps): Taylor at 0 gives 1 + eps + eps^2/2 + eps^3/6 + ...
exp_eps = sp.series(sp.exp(eps), eps, 0, n=4)
# Leading virtual (non-constant) coefficient of eps is 1 = exp'(0)
assert str(exp_eps) == '1 + epsilon + epsilon**2/2 + epsilon**3/6 + O(epsilon**4)'

# eps^2: no first-order term, leading term is eps^2
# Coefficient 1 = f''(0)/2! where f(x) = x^2, f''(0) = 2
t2_eps = sp.series(eps**2, eps, 0, n=4)
assert str(t2_eps) == 'epsilon**2'

# cos(eps): 1 - eps^2/2 + ...
cos_eps = sp.series(sp.cos(eps), eps, 0, n=4)
# First virtual term: -eps^2/2, coefficient = -1/2 = cos''(0)/2!
assert str(cos_eps) == '1 - epsilon**2/2 + O(epsilon**4)'
```

## Results

All 4 tests passed.

## Interpretation

The index of the leading non-constant term in f(0_x) is the leading jet data of f at 0, scaled by x. Specifically:

If f(t) = f(0) + a_k * t^k + ... (first nonzero derivative at order k), then:
- f(0_x) = f(0) + 0^k_{a_k * x^k} + ...
- I(leading virtual term) = a_k * x^k = f^(k)(0)/k! * x^k

This is the standard relationship between formal power series and jets. IVNA's notation makes the grading visible (0^k means k-th order), but the mathematical content is classical.

Contrast with SDG: The Kock-Lawvere axiom uses nilpotent infinitesimals (d^2 = 0) to capture only 1-jets. IVNA's eps is not nilpotent (eps^k != 0 for all k), so it captures jets of all orders simultaneously. This is the well-known advantage of NSA-style infinitesimals over SDG-style nilpotent infinitesimals.
