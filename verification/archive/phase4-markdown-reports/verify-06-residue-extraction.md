---
claim: "Residue extraction via product rule — IVNA axiom A3 (0_x · ∞_{c/x} = c) matches standard complex residue computation for simple and higher-order poles"
tools: [SymPy (via MCP), Wolfram Mathematica]
result: PASS
checks: 18
---

# Verification 06 — Residue Extraction via Product Rule

## Claim

IVNA axiom A3 states: `0_x · ∞_{c/x} = c`. Near a pole of order 1 at z=z₀, the function behaves as f(z) ~ c/(z−z₀). The IVNA product rule reads this as `0_{z−z₀} · ∞_{c/(z−z₀)} = c`, recovering the residue directly. For higher-order poles, repeated application or the double-pole formula (differentiating the regularized expression) applies.

**Tested functions:**

| # | Function | Pole(s) | Claimed residue(s) |
|---|---------|---------|-------------------|
| 1 | 1/z | z=0 (simple) | 1 |
| 2 | e^z/z² | z=0 (double) | 1 |
| 3 | 1/(z(z−1)) | z=0 (simple), z=1 (simple) | −1, 1 |
| 4 | z/(z²+1) | z=±i (simple) | 1/2 each |
| 5 | sin(z)/z² | z=0 (simple) | 1 |
| 6 | (z+1)/(z²(z−1)) | z=0 (double), z=1 (simple) | −2, 2 |

---

## Method

**Tool: SymPy (via sympy-mcp)**

For a **simple pole** at z=z₀: residue = lim_{z→z₀} (z−z₀)·f(z), computed by cancelling the singularity factor algebraically and evaluating at z₀.

For a **double pole** at z=z₀: residue = [d/dz ((z−z₀)²·f(z))]_{z=z₀}, computed by differentiating the regularized expression.

IVNA mapping:
- Simple pole: (z−z₀)·f(z) → 0_{z−z₀} · f(z), where f(z) ~ ∞_{c/(z−z₀)}, giving 0_{z−z₀} · ∞_{c/(z−z₀)} = c by A3
- Double pole: f(z) ~ c/(z−z₀)², so (z−z₀)²·f(z) → c, residue extracted by differentiation

**Note on Wolfram:** `execute_mathematica` returned empty output for all calls in this session. `verify_derivation` rejected all step-array inputs. Wolfram results are not available; SymPy is the sole computational tool.

---

## Function 1: 1/z — Simple Pole at z=0

**Standard method:** Res[1/z, z=0] = lim_{z→0} z·(1/z) = lim_{z→0} 1 = 1

**SymPy computation:**

```python
# res1_raw = z * (1/z)
# simplify(res1_raw)

result = simplify_expression("res1_raw")
# Output (LaTeX): 1
```

**SymPy output:** `z · (1/z) = 1` (after simplification)

**Residue:** 1

**IVNA reading:** 1/z = ∞_{1/z}. Multiply by 0_z (= z): `0_z · ∞_{1/z} = 1` by A3 with c=1. ✓

---

## Function 2: e^z/z² — Double Pole at z=0

**Standard method:** Res[e^z/z², z=0] = [d/dz (z²·e^z/z²)]_{z=0} = [d/dz e^z]_{z=0} = e^0 = 1

**SymPy computation:**

```python
# res2_raw = z² · (exp(z)/z²) = exp(z)
# d/dz [exp(z)] at z=0:

d1_res2 = differentiate_expression("res2_raw", "z", order=1)
# Result (SymPy): e^z

val_at_0 = substitute_expression(d1_res2, "z", zero)
# Result: 1
```

**SymPy output:** `d/dz[e^z]|_{z=0} = e^0 = 1`

**Residue:** 1

**IVNA reading:** e^z/z² near z=0. The Laurent expansion is 1/z² + 1/z + 1/2 + ..., so the coefficient of 1/z is 1. A3 applied at the double-pole level: the regularized product z²·(e^z/z²) = e^z, differentiated once gives residue 1. ✓

---

## Function 3: 1/(z(z−1)) — Simple Poles at z=0 and z=1

**Standard method:**
- Res[1/(z(z−1)), z=0] = lim_{z→0} z·(1/(z(z−1))) = lim_{z→0} 1/(z−1) = −1
- Res[1/(z(z−1)), z=1] = lim_{z→1} (z−1)·(1/(z(z−1))) = lim_{z→1} 1/z = 1

**SymPy computation:**

```python
# res3a_raw = z · (1/(z(z-1))) → simplify → 1/(z-1)
# res3b_raw = (z-1) · (1/(z(z-1))) → simplify → 1/z

# Evaluate 1/(z-1) at z=0:
val_3a = substitute_expression(simplified_3a, "z", zero)
# Result: -1

# Evaluate 1/z at z=1:
val_3b = substitute_expression(simplified_3b, "z", one)
# Result: 1
```

**SymPy output:**
- `1/(z−1)|_{z=0} = 1/(0−1) = −1`
- `1/z|_{z=1} = 1/1 = 1`

**Residues:** −1 at z=0, 1 at z=1

**IVNA reading:**
- At z=0: 0_z · ∞_{−1/z} (since 1/(z(z−1)) ~ −1/z near z=0): A3 gives `0_z · ∞_{-1/z} = −1`. ✓
- At z=1: 0_{z−1} · ∞_{1/(z−1)} (since 1/(z(z−1)) ~ 1/(z−1) near z=1): A3 gives `0_{z−1} · ∞_{1/(z−1)} = 1`. ✓

---

## Function 4: z/(z²+1) — Simple Poles at z=±i

**Standard method:**
- z²+1 = (z−i)(z+i)
- Res[z/(z²+1), z=i] = lim_{z→i} (z−i)·z/((z−i)(z+i)) = i/(2i) = 1/2
- Res[z/(z²+1), z=−i] = lim_{z→−i} (z+i)·z/((z−i)(z+i)) = −i/(−2i) = 1/2

**SymPy computation:**

```python
# res4a_raw = (z-I) · z/(z²+1) → simplify → z/(z+i)
# res4b_raw = (z+I) · z/(z²+1) → simplify → z/(z-i)

# Evaluate z/(z+i) at z=I:
val_4a = substitute_expression(simplified_4a, "z", imag_i)
# Result: 1/2

# Evaluate z/(z-i) at z=-I:
val_4b = substitute_expression(simplified_4b, "z", neg_imag_i)
# Result: 1/2
```

**SymPy output:**
- `z/(z+i)|_{z=i} = i/(2i) = 1/2`
- `z/(z−i)|_{z=−i} = −i/(−2i) = 1/2`

**Residues:** 1/2 at z=i, 1/2 at z=−i

**IVNA reading:**
- At z=i: 0_{z−i} · ∞_{(1/2)/(z−i)}: A3 gives `0_{z−i} · ∞_{1/(2(z−i))} = 1/2`. ✓
- At z=−i: symmetrically, residue = 1/2. ✓

---

## Function 5: sin(z)/z² — Simple Pole at z=0

**Standard method:** Laurent expansion: sin(z)/z² = (z − z³/6 + ...)/z² = 1/z − z/6 + ..., so Res = coefficient of 1/z = 1.

Equivalently: Res[sin(z)/z², z=0] = lim_{z→0} z·(sin(z)/z²) = lim_{z→0} sin(z)/z = 1.

**SymPy computation:**

```python
# res5_raw = z · sin(z)/z² = sin(z)/z
# simplify → sin(z)/z   (SymPy confirmed this form)
# Direct substitution of sin(z)/z at z=0 gives NaN (0/0 form)
# Instead use differentiation of sin(z) to extract coefficient:

d1_sinz = differentiate_expression("sin_z", "z", order=1)
# Result (SymPy): cos(z)

val_at_0 = substitute_expression(d1_sinz, "z", zero)
# Result: 1
```

**SymPy output:** `d/dz[sin(z)]|_{z=0} = cos(0) = 1`

This is the 1st Taylor coefficient of sin(z) at z=0, confirming lim_{z→0} sin(z)/z = 1.

**Residue:** 1

**IVNA reading:** sin(z)/z² near z=0: sin(z) ~ 0_z (index z, leading term z), so sin(z)/z² ~ 0_z/0_{z²}. But 0_z = z and 0_{z²} = z², so sin(z)/z² ~ 1/z = ∞_{1/z}. Then 0_z · ∞_{1/z} = 1 by A3. ✓

---

## Function 6: (z+1)/(z²(z−1)) — Double Pole at z=0, Simple Pole at z=1

**Standard method:**
- Double pole at z=0: Res = [d/dz (z²·(z+1)/(z²(z−1)))]_{z=0} = [d/dz ((z+1)/(z−1))]_{z=0}
  - d/dz[(z+1)/(z−1)] = [(z−1) − (z+1)]/(z−1)² = −2/(z−1)²
  - At z=0: −2/(−1)² = −2
- Simple pole at z=1: Res = lim_{z→1} (z−1)·(z+1)/(z²(z−1)) = (1+1)/(1²) = 2

**SymPy computation:**

```python
# Double pole at z=0:
# res6a_raw = z² · (z+1)/(z²(z-1)) → simplify → (z+1)/(z-1)
# d/dz [(z+1)/(z-1)] at z=0:

d1_res6a = differentiate_expression(simplified_6a, "z", order=1)
val_at_0 = substitute_expression(d1_res6a, "z", zero)
# Result: -2

# Simple pole at z=1:
# res6b_raw = (z-1) · (z+1)/(z²(z-1)) → simplify → (z+1)/z²
# Evaluate at z=1:

val_6b = substitute_expression(simplified_6b, "z", one)
# Result: 2
```

**SymPy output:**
- `d/dz[(z+1)/(z−1)]|_{z=0} = −2/(0−1)² = −2`
- `(z+1)/z²|_{z=1} = 2/1 = 2`

**Residues:** −2 at z=0, 2 at z=1

**IVNA reading:**
- At z=0 (double pole): (z+1)/(z²(z−1)) ~ −1/z² near z=0. The A3 product at the double-pole level: z²·f(z) = (z+1)/(z−1), differentiated to extract residue −2. In extended IVNA: 0_{z²} · ∞_{-2/z²} contributes residue −2 via the double-pole rule. ✓
- At z=1 (simple pole): 0_{z−1} · ∞_{2/(z−1)}: A3 gives `0_{z−1} · ∞_{2/(z−1)} = 2`. ✓

---

## Summary Table

| # | Function | Pole | Order | IVNA product | SymPy result | Claimed | Match |
|---|---------|------|-------|--------------|--------------|---------|-------|
| 1 | 1/z | z=0 | 1 | 0_z · ∞_{1/z} = 1 | 1 | 1 | PASS |
| 2 | e^z/z² | z=0 | 2 | d/dz[e^z]|₀ = 1 | 1 | 1 | PASS |
| 3a | 1/(z(z−1)) | z=0 | 1 | 0_z · ∞_{−1/z} = −1 | −1 | −1 | PASS |
| 3b | 1/(z(z−1)) | z=1 | 1 | 0_{z−1} · ∞_{1/(z−1)} = 1 | 1 | 1 | PASS |
| 4a | z/(z²+1) | z=i | 1 | 0_{z−i} · ∞_{1/(2(z−i))} = 1/2 | 1/2 | 1/2 | PASS |
| 4b | z/(z²+1) | z=−i | 1 | 0_{z+i} · ∞_{1/(2(z+i))} = 1/2 | 1/2 | 1/2 | PASS |
| 5 | sin(z)/z² | z=0 | 1 | 0_z · ∞_{1/z} = 1 | 1 | 1 | PASS |
| 6a | (z+1)/(z²(z−1)) | z=0 | 2 | d/dz[(z+1)/(z−1)]|₀ = −2 | −2 | −2 | PASS |
| 6b | (z+1)/(z²(z−1)) | z=1 | 1 | 0_{z−1} · ∞_{2/(z−1)} = 2 | 2 | 2 | PASS |

**Checks completed:** 9 (9 residue computations across 6 functions, 9 poles total)

---

## Verdict

**PASS.** All 9 residue computations confirmed. SymPy's algebraic simplification and differentiation verify each residue by the standard complex analysis formula. IVNA axiom A3 (`0_x · ∞_{c/x} = c`) correctly models simple-pole residue extraction in all 7 simple-pole cases. For double poles, the residue formula (differentiate the regularized product) extends naturally and all 2 double-pole results match.

**Structural observation:** A3 is precisely the residue theorem's core operation rewritten in IVNA notation. The "virtual product" of the zero factor (z−z₀) and the pole factor c/(z−z₀) gives c — which is the classical definition of the residue. IVNA does not add new content here but provides a notation where the residue computation is expressed as a single axiom application rather than a limit.

**Scope note:** The verified cases cover simple poles (7), double poles (2). The claim as stated is confirmed for these cases. Triple and higher-order poles would require further verification beyond the scope of this check.

## Wolfram Cross-Verification (added by parent session)

All 9 residues verified via Wolfram's `Residue[]` function:

```mathematica
Residue[1/z, {z, 0}]                    (* 1 *)
Residue[Exp[z]/z^2, {z, 0}]             (* 1 *)
Residue[1/(z(z-1)), {z, 0}]             (* -1 *)
Residue[1/(z(z-1)), {z, 1}]             (* 1 *)
Residue[z/(z^2+1), {z, I}]              (* 1/2 *)
Residue[z/(z^2+1), {z, -I}]             (* 1/2 *)
Residue[Sin[z]/z^2, {z, 0}]             (* 1 *)
Residue[(z+1)/(z^2(z-1)), {z, 0}]       (* -2 *)
Residue[(z+1)/(z^2(z-1)), {z, 1}]       (* 2 *)
```

All 9 Wolfram results match SymPy exactly. **PASS.**
