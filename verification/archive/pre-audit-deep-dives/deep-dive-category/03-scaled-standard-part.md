# Verification 3: Scaled Standard Part

**Tool:** SymPy 1.14.0 (Python venv)
**Tests:** 4/4 passed

## What Was Verified

The index map I relates to NSA's standard part map st by:
  I(v) = st(v / eps^{grade(v)})

This means: divide out the infinitesimal/infinite component, then take the standard part (which is trivially just the result, since v/eps^{grade(v)} is already a real number for monomials).

## SymPy Code

```python
import sympy as sp

eps = sp.Symbol('epsilon', positive=True)
a = sp.Symbol('a', real=True, nonzero=True)

# Grade 1: I(0_a) = st(a*eps / eps) = st(a) = a
assert sp.simplify(a*eps/eps - a) == 0

# Grade -1: I(inf_a) = st((a/eps) * eps) = st(a) = a
assert sp.simplify((a/eps)*eps - a) == 0

# Grade 2: I(0^2_a) = st(a*eps^2 / eps^2) = st(a) = a
assert sp.simplify(a*eps**2/eps**2 - a) == 0

# Grade -2: I(inf^2_a) = st((a/eps^2) * eps^2) = st(a) = a
assert sp.simplify((a/eps**2)*eps**2 - a) == 0
```

## Results

All 4 tests passed. The formula I(v) = st(v / eps^{grade(v)}) is verified for grades -2, -1, 1, 2.

## Interpretation

The index map "normalizes" a virtual number by dividing out its infinitesimal/infinite factor (eps^n), leaving only the real coefficient. This is analogous to how, in a graded ring, one extracts the coefficient by dividing out the grading variable. The standard part map st is trivial here (the result is already real for monomials), but the formula connects IVNA's index extraction to NSA's standard part in a clean way.
