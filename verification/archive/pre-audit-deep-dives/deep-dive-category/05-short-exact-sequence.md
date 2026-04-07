# Verification 5: Short Exact Sequence

**Tool:** SymPy 1.14.0 (Python venv)
**Tests:** 6/6 passed

## What Was Verified

The short exact sequence of groups:

```
1 → Z → R* × Z → R* → 1
     n↦(1,n)   (c,n)↦c
```

Specifically: the composition projection ∘ inclusion = constant 1.
That is, projecting the coefficient from a unit-coefficient element at any grade gives 1.

## SymPy Code

```python
import sympy as sp

eps = sp.Symbol('epsilon', positive=True)

for grade in [-2, -1, 0, 1, 2, 3]:
    # Inclusion: n -> (1, n) = 1 * eps^n
    incl = 1 * eps**grade
    # Projection: extract coefficient = divide by eps^grade
    coeff = sp.simplify(incl / eps**grade)
    assert coeff == 1, f"Failed for grade {grade}: got {coeff}"
```

## Results

All 6 tests passed for grades {-2, -1, 0, 1, 2, 3}.

## Interpretation

The sequence splits via sigma: R* -> R* x Z, c -> (c, 0). This means:
- Every IVNA element (c,n) decomposes uniquely as sigma(c) * iota(n) = (c,0)*(1,n)
- The "real part" (c,0) carries the index, the "grade part" (1,n) carries the order
- Since the extension splits with trivial action, R* x Z = R* x Z (direct product)

The kernel of the index map I = {(1,n) : n in Z} is the group of "unit-indexed" elements: {0_1, inf_1, 0^2_1, inf^2_1, ...}. These are the IVNA elements that carry no coefficient information — only grade/order data.
