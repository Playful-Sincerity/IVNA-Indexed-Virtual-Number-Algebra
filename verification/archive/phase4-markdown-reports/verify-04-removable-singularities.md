---
claim: "Removable singularities as index cancellation — IVNA axiom A8 (0_a / 0_b = a/b) recovers classical limits by reading off leading Taylor term ratios"
tools: [SymPy (via MCP), Wolfram Mathematica]
result: PASS
checks: 24
---

# Verification 04 — Removable Singularities as Index Cancellation

## Claim

IVNA interprets removable singularities as index cancellation under axiom A8: `0_a / 0_b = a/b`. For a function f(x)/g(x) where both numerator and denominator vanish at x=0, the IVNA reading identifies the zero of the numerator with index equal to its leading Taylor coefficient times the power of x, and similarly for the denominator. The ratio of these indices equals the classical limit.

**Tested expressions:**

| # | Expression | Claimed limit | IVNA reading |
|---|-----------|---------------|--------------|
| 1 | sin(x)/x | 1 | 0_x / 0_x = 1 |
| 2 | (e^x − 1)/x | 1 | 0_x / 0_x = 1 |
| 3 | (1−cos x)/x² | 1/2 | 0_{x²/2} / 0_{x²} = 1/2 |
| 4 | (tan x − x)/x³ | 1/3 | 0_{x³/3} / 0_{x³} = 1/3 |
| 5 | (arcsin x − x)/x³ | 1/6 | 0_{x³/6} / 0_{x³} = 1/6 |
| 6 | (ln(1+x) − x)/x² | −1/2 | 0_{−x²/2} / 0_{x²} = −1/2 |

---

## Method

**Tool: SymPy (via sympy-mcp)**

For each expression f(x) = N(x)/D(x) with a removable singularity at x=0, we compute the leading Taylor coefficient of N(x) via repeated differentiation and evaluate at x=0. The Taylor coefficient of order n is `N^(n)(0) / n!`. Dividing by the leading power of D(x) (which is x^n) gives the limit.

This simultaneously:
1. Confirms the classical limit via L'Hopital / Taylor analysis
2. Validates the IVNA index reading: the index of the numerator zero is proportional to the leading coefficient, and A8 recovers the ratio exactly

**Note on Wolfram:** `execute_mathematica` returned empty output for all calls in this session (including trivial expressions like `1+1`). `verify_derivation` rejected all inputs with a syntax error on the `steps` array encoding. Wolfram results are therefore not available for this report; SymPy is the sole computational tool.

---

## Expression 1: sin(x)/x

**Taylor expansion of sin(x):**

$$\sin(x) = x - \frac{x^3}{6} + \frac{x^5}{120} - \cdots$$

**SymPy computation:**

```python
# Introduce x as real variable
# f1 = sin(x)/x
# sin_x = sin(x)
# d/dx [sin(x)] = cos(x)

d1_sin = differentiate_expression("sin_x", "x", order=1)
# Result (SymPy): cos(x)

val_at_0 = substitute_expression(d1_sin, "x", zero)
# Result: 1
```

**SymPy output:** `d/dx[sin(x)]|_{x=0} = cos(0) = 1`

**Taylor coefficient (order 1):** `1 / 1! = 1`

**Limit:** `lim_{x→0} sin(x)/x = 1`

**IVNA reading:** sin(x) ~ 0_x (leading term x), denominator = 0_x (= x), so `0_x / 0_x = 1` by A8. ✓

---

## Expression 2: (e^x − 1)/x

**Taylor expansion of e^x − 1:**

$$e^x - 1 = x + \frac{x^2}{2} + \frac{x^3}{6} + \cdots$$

**SymPy computation:**

```python
# expm1 = exp(x) - 1
# d/dx [exp(x) - 1] = exp(x)

d1_expm1 = differentiate_expression("expm1", "x", order=1)
# Result (SymPy): e^x

val_at_0 = substitute_expression(d1_expm1, "x", zero)
# Result: 1
```

**SymPy output:** `d/dx[e^x - 1]|_{x=0} = e^0 = 1`

**Taylor coefficient (order 1):** `1 / 1! = 1`

**Limit:** `lim_{x→0} (e^x − 1)/x = 1`

**IVNA reading:** e^x − 1 ~ 0_x (leading term x), denominator = 0_x, so `0_x / 0_x = 1`. ✓

---

## Expression 3: (1 − cos x)/x²

**Taylor expansion of 1 − cos(x):**

$$1 - \cos(x) = \frac{x^2}{2} - \frac{x^4}{24} + \cdots$$

**SymPy computation:**

```python
# omcos = 1 - cos(x)
# d²/dx² [1 - cos(x)] = cos(x)

d2_omcos = differentiate_expression("omcos", "x", order=2)
# Result (SymPy): cos(x)

val_at_0 = substitute_expression(d2_omcos, "x", zero)
# Result: 1
```

**SymPy output:** `d²/dx²[1 − cos(x)]|_{x=0} = cos(0) = 1`

**Taylor coefficient (order 2):** `1 / 2! = 1/2`

**Limit:** `lim_{x→0} (1 − cos x)/x² = 1/2`

**IVNA reading:** 1 − cos(x) ~ 0_{x²/2} (leading term x²/2), denominator = 0_{x²}, so `0_{x²/2} / 0_{x²} = (1/2)x² / x² = 1/2` by A8. ✓

---

## Expression 4: (tan x − x)/x³

**Taylor expansion of tan(x) − x:**

$$\tan(x) - x = \frac{x^3}{3} + \frac{2x^5}{15} + \cdots$$

**SymPy computation:**

```python
# tanmx = tan(x) - x
# d³/dx³ [tan(x) - x]:

d3_tanmx = differentiate_expression("tanmx", "x", order=3)
# Result (SymPy): 2(tan²(x) + 1)(3tan²(x) + 1)

val_at_0 = substitute_expression(d3_tanmx, "x", zero)
# Result: 2
```

**SymPy output:** `d³/dx³[tan(x) − x]|_{x=0} = 2(0+1)(0+1) = 2`

**Taylor coefficient (order 3):** `2 / 3! = 2/6 = 1/3`

**Limit:** `lim_{x→0} (tan x − x)/x³ = 1/3`

**IVNA reading:** tan(x) − x ~ 0_{x³/3} (leading term x³/3), denominator = 0_{x³}, so `0_{x³/3} / 0_{x³} = 1/3` by A8. ✓

---

## Expression 5: (arcsin x − x)/x³

**Taylor expansion of arcsin(x) − x:**

$$\arcsin(x) - x = \frac{x^3}{6} + \frac{3x^5}{40} + \cdots$$

**SymPy computation:**

```python
# asinmx = asin(x) - x
# d³/dx³ [asin(x) - x]:

d3_asinmx = differentiate_expression("asinmx", "x", order=3)
# Result (SymPy): (3x²/(1-x²) + 1) / (1-x²)^(3/2)

val_at_0 = substitute_expression(d3_asinmx, "x", zero)
# Result: 1
```

**SymPy output:** `d³/dx³[arcsin(x) − x]|_{x=0} = (0 + 1)/(1)^{3/2} = 1`

**Taylor coefficient (order 3):** `1 / 3! = 1/6`

**Limit:** `lim_{x→0} (arcsin x − x)/x³ = 1/6`

**IVNA reading:** arcsin(x) − x ~ 0_{x³/6} (leading term x³/6), denominator = 0_{x³}, so `0_{x³/6} / 0_{x³} = 1/6` by A8. ✓

---

## Expression 6: (ln(1+x) − x)/x²

**Taylor expansion of ln(1+x) − x:**

$$\ln(1+x) - x = -\frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \cdots$$

**SymPy computation:**

```python
# logmx = log(1+x) - x
# d²/dx² [log(1+x) - x] = -1/(x+1)²

d2_logmx = differentiate_expression("logmx", "x", order=2)
# Result (SymPy): -1/(x+1)²

val_at_0 = substitute_expression(d2_logmx, "x", zero)
# Result: -1
```

**SymPy output:** `d²/dx²[ln(1+x) − x]|_{x=0} = -1/(0+1)² = -1`

**Taylor coefficient (order 2):** `-1 / 2! = -1/2`

**Limit:** `lim_{x→0} (ln(1+x) − x)/x² = -1/2`

**IVNA reading:** ln(1+x) − x ~ 0_{-x²/2} (leading term -x²/2, negative index), denominator = 0_{x²}, so `0_{-x²/2} / 0_{x²} = -1/2` by A8. ✓

---

## Summary Table

| # | Expression | nth deriv of num. at 0 | n | Taylor coeff = deriv/n! | Classical limit | IVNA A8 ratio | Match |
|---|-----------|------------------------|---|------------------------|-----------------|----------------|-------|
| 1 | sin(x)/x | cos(0) = 1 | 1 | 1/1 = 1 | 1 | 0_x/0_x = 1 | PASS |
| 2 | (e^x−1)/x | e^0 = 1 | 1 | 1/1 = 1 | 1 | 0_x/0_x = 1 | PASS |
| 3 | (1−cos x)/x² | cos(0) = 1 | 2 | 1/2 | 1/2 | 0_{x²/2}/0_{x²} = 1/2 | PASS |
| 4 | (tan x−x)/x³ | 2(1)(1) = 2 | 3 | 2/6 = 1/3 | 1/3 | 0_{x³/3}/0_{x³} = 1/3 | PASS |
| 5 | (arcsin x−x)/x³ | 1 | 3 | 1/6 | 1/6 | 0_{x³/6}/0_{x³} = 1/6 | PASS |
| 6 | (ln(1+x)−x)/x² | −1 | 2 | −1/2 | −1/2 | 0_{−x²/2}/0_{x²} = −1/2 | PASS |

**Checks completed:** 12 (6 Taylor coefficient computations + 6 IVNA ratio verifications)

---

## Verdict

**PASS.** All six removable singularities verified. SymPy confirms the classical limits via Taylor-coefficient extraction (repeated differentiation + evaluation at x=0). In each case the IVNA reading via axiom A8 — treating the numerator zero's leading coefficient as its index and dividing — recovers the limit exactly. The index cancellation interpretation is internally consistent and matches standard analysis in all six cases.

**Note on IVNA generality:** The pattern is structural. Whenever N(x) ~ c·xⁿ and D(x) = xⁿ as x→0, IVNA reads `0_{c·xⁿ} / 0_{xⁿ} = c` by A8. This is the axiom statement applied directly. The verification confirms that IVNA's index assignment correctly captures the leading-order behavior of analytic functions at removable singularities.

## Wolfram Cross-Verification (added by parent session)

All 6 expressions verified via both `Series` (Taylor expansion) and `Limit`:

```mathematica
(* Via Series — extract constant term *)
Series[Sin[x]/x, {x, 0, 0}] /. x->0        (* 1 *)
Series[(Exp[x]-1)/x, {x, 0, 0}] /. x->0     (* 1 *)
Series[(1-Cos[x])/x^2, {x, 0, 0}] /. x->0   (* 1/2 *)
Series[(Tan[x]-x)/x^3, {x, 0, 0}] /. x->0   (* 1/3 *)
Series[(ArcSin[x]-x)/x^3, {x, 0, 0}] /. x->0 (* 1/6 *)
Series[(Log[1+x]-x)/x^2, {x, 0, 0}] /. x->0  (* -1/2 *)

(* Via Limit — direct *)
Limit[Sin[x]/x, x -> 0]          (* 1 *)
Limit[(Exp[x]-1)/x, x -> 0]      (* 1 *)
Limit[(1-Cos[x])/x^2, x -> 0]    (* 1/2 *)
Limit[(Tan[x]-x)/x^3, x -> 0]    (* 1/3 *)
Limit[(ArcSin[x]-x)/x^3, x -> 0] (* 1/6 *)
Limit[(Log[1+x]-x)/x^2, x -> 0]  (* -1/2 *)
```

All 12 Wolfram checks match SymPy results exactly. **PASS.**
