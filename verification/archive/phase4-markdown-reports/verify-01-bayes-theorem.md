---
claim: "A8 (0_a/0_b = a/b) IS Bayes' theorem for continuous densities: 0_{f(x,y)}/0_{f(x)} = f(y|x)"
tools: [Wolfram Mathematica, SymPy]
result: PASS
checks: 6 (3 distributions x 2 tools)
---

# Verify-01: A8 = Bayes' Theorem for Continuous Densities

## Claim

For continuous random variables with joint density f_XY(x,y) and marginal f_X(x):
- P(X=x) = 0_{f_X(x)} (zero with density as index)
- P(Y=y, X=x) = 0_{f_{XY}(x,y)} (zero with joint density as index)
- By A8: 0_{f_{XY}(x,y)} / 0_{f_X(x)} = f_{XY}(x,y) / f_X(x) = f_{Y|X}(y|x)

The IVNA division rule for indexed zeros directly produces the conditional density formula.

## Test 1: Bivariate Normal (general rho)

**Joint density:**
f_{XY}(x,y) = 1/(2pi sqrt(1-rho^2)) exp(-(x^2 - 2rho*xy + y^2)/(2(1-rho^2)))

**Marginal:**
f_X(x) = 1/sqrt(2pi) exp(-x^2/2)

**Expected conditional:**
f_{Y|X}(y|x) = N(rho*x, 1-rho^2) = 1/sqrt(2pi(1-rho^2)) exp(-(y-rho*x)^2/(2(1-rho^2)))

### Wolfram (rho=1/2)
```mathematica
rho = 1/2;
fXY[x_, y_] := 1/(2 Pi Sqrt[1 - rho^2]) Exp[-(x^2 - 2 rho x y + y^2)/(2 (1 - rho^2))]
fX[x_] := 1/Sqrt[2 Pi] Exp[-x^2/2]
conditional = Simplify[fXY[x, y] / fX[x]]
(* Result: Sqrt[2/(3*Pi)]/E^((x - 2*y)^2/6) *)
diff = FullSimplify[conditional - 1/Sqrt[2 Pi (1-rho^2)] Exp[-(y-rho x)^2/(2(1-rho^2))]]
(* Result: 0 *)
```
**PASS** — difference is exactly 0.

### SymPy (general rho)
```python
fXY = 1/(2*pi*sqrt(1-rho**2)) * exp(-(x**2 - 2*rho*x*y + y**2)/(2*(1-rho**2)))
fX = 1/sqrt(2*pi) * exp(-x**2/2)
known_cond = 1/sqrt(2*pi*(1-rho**2)) * exp(-(y-rho*x)**2/(2*(1-rho**2)))
diff = simplify(fXY/fX - known_cond)
# Result: 0
```
**PASS** — holds for all rho, not just rho=1/2.

## Test 2: Gumbel Bivariate Exponential (theta=1/2)

**Joint density:**
f_{XY}(x,y) = (1 + theta*(2e^{-x}-1)*(2e^{-y}-1)) * e^{-x-y}, x,y > 0

### Wolfram
```mathematica
theta = 1/2;
fXY2[x_, y_] := (1 + theta*(2 Exp[-x]-1)*(2 Exp[-y]-1)) * Exp[-x-y]
fX2 = Integrate[fXY2[x, y], {y, 0, Infinity}, Assumptions -> x > 0]
(* Marginal: e^{-x} *)
cond2 = Simplify[fXY2[x, y] / fX2]
intCheck = Integrate[cond2, {y, 0, Infinity}, Assumptions -> x > 0]
(* Result: 1 *)
```
**PASS** — conditional integrates to 1.

### SymPy
```python
fXY_exp = (1 + Rational(1,2)*(2*exp(-x)-1)*(2*exp(-y)-1)) * exp(-x-y)
fX_exp = integrate(fXY_exp, (y, 0, oo))
# Marginal: exp(-x)
int_check = integrate(simplify(fXY_exp / fX_exp), (y, 0, oo))
# Result: 1
```
**PASS** — conditional integrates to 1.

## Test 3: Bivariate Cauchy (pathological case)

**Joint density:**
f_{XY}(x,y) = 1/(2pi(1+x^2+y^2)^{3/2})

This is pathological because the Cauchy distribution has no finite mean or variance, and the conditional distribution changes form (it's NOT Cauchy).

### Wolfram
```mathematica
fXYc = 1/(2 Pi (1 + x^2 + y^2)^(3/2));
fXc = Integrate[fXYc, {y, -Infinity, Infinity}]
(* Marginal: 1/(pi*(1+x^2)) — standard Cauchy *)
condc = Simplify[fXYc / fXc]
(* Conditional: (1+x^2)/(2*(1+x^2+y^2)^(3/2)) *)
intCheck = Integrate[condc, {y, -Infinity, Infinity}]
(* Result: 1 *)
```
**PASS** — even for pathological distributions, A8 produces a valid conditional density.

### SymPy
```python
fXY_cauchy = 1/(2*pi*(1+x**2+y**2)**Rational(3,2))
fX_cauchy = integrate(fXY_cauchy, (y, -oo, oo))
# Marginal: 1/(pi*(x^2+1)) — standard Cauchy
cond_cauchy = simplify(fXY_cauchy / fX_cauchy)
# Conditional: (x^2+1)/(2*(x^2+y^2+1)^(3/2))
int_check = integrate(cond_cauchy, (y, -oo, oo))
# Result: 1
```
**PASS** — matches Wolfram exactly.

## Summary

| Distribution | Wolfram | SymPy | Result |
|---|---|---|---|
| Bivariate Normal (general rho) | PASS | PASS | PASS |
| Gumbel Bivariate Exponential (theta=0.5) | PASS | PASS | PASS |
| Bivariate Cauchy (pathological) | PASS | PASS | PASS |

**Verdict:** A8 correctly produces conditional densities for all tested distributions, including a pathological case with no finite moments. The claim that "A8 IS Bayes' theorem for continuous densities" is verified.

**Note:** This verifies the *formal computation*, i.e., that f_{XY}/f_X gives the correct conditional density. The IVNA interpretation (that P(X=x) = 0_{f(x)} and division of indexed zeros produces the ratio of indices) is a notational claim that maps correctly onto this standard computation.
