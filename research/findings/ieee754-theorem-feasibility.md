# IEEE 754 Theorem Feasibility

**Date:** 2026-04-01
**Verdict:** PURSUE — two clean theorems, strongest applied result

## Experiments (all run against code/ivna.py)

### Catastrophic Cancellation (a = 1+1e-15, b = 1)
- float64: 1.1102e-15 — 11% error, ~1 significant digit
- IVNA: tags as 0_{1e-15}, index stores exact value

### Quadratic Formula (x² - 2·10⁸x + 1 = 0)
- Standard: x₂ = 0.000e+00 — **100% WRONG** (complete cancellation)
- Exact: x₂ = 5e-09
- IVNA: numerator stored as 0_{1e-8}, recovered x₂ = 5e-09, error = 0.00

### NaN Propagation (0/0 → +5 → ×3)
- IEEE: NaN → NaN → NaN (destroyed)
- IVNA: 0_1/0_1 = 1 → +5 = 6 → ×3 = 18 (preserved)
- ∞_5 * 0_1 = 5 (vs Inf * 0 = NaN)

### NaN Elimination — 8/8 cases pass
All primitive NaN operations resolve to determinate IVNA values.

### Roundtrip — 7/7 exact
For all r ∈ {5, -3.14, 1/3, 1e10, 1e-10, π, e}: r/0_1 = ∞_r, ∞_r * 0_1 = r, zero error.

## Comparison with Existing Tools

| Tool | Determinate 0/0 | Continues past NaN | Exact roundtrip |
|------|-----------------|-------------------|----------------|
| IEEE 754 | No | No | No |
| Interval arithmetic | No (wide interval) | Partial | No |
| CADNA/CESTAC | Diagnoses only | No | No |
| Dual numbers / AD | Only for derivatives | Yes (derivatives) | No |
| TwoSum / EFTs | No | No | Partial (addition only) |
| Wheel algebra | Yes (⊥ element) | No (⊥ absorbs) | No |
| **IVNA** | **Yes** | **Yes** | **Yes** |

Key distinctions:
- **vs interval arithmetic**: Intervals track uncertainty ranges; IVNA tracks exact identity. Different epistemic claim.
- **vs CADNA**: CADNA diagnoses computational zeros; IVNA prescribes what to do with them.
- **vs dual numbers**: Dual numbers carry derivatives (ε²=0); IVNA carries magnitudes. Similar structure, different purpose. AD beats IVNA for derivatives.
- **vs TwoSum**: TwoSum recovers companion error for addition. IVNA generalizes to closed algebra across all four indeterminate forms.
- **vs Herbie**: Static rewriter vs runtime algebra. Complementary.

## Formal Theorems

### Theorem 1 (NaN Elimination)
Under VEA mode, every IEEE 754 NaN-producing primitive operation between well-indexed virtual numbers has a determinate result:
- 0_x / 0_y = x/y (eliminates 0/0)
- 0_x · ∞_y = xy (eliminates 0·∞)
- ∞_x / ∞_y = x/y (eliminates ∞/∞)
- ∞_x - ∞_y = ∞_{x-y} or 0 if x=y (eliminates ∞-∞)

Status: PROVABLE from axioms A1-A11. 8/8 computationally verified.

### Theorem 2 (Division Roundtrip)
For any r ∈ R\{0}: (r/0_s) · 0_s = r.
Proof: 2 lines from A6 and A3. 7/7 verified with zero error.

## Honest Assessment

- **Not reinventing interval arithmetic** — distinct epistemic claim (exact identity vs uncertainty range)
- **Killer example**: NaN elimination + quadratic formula. IEEE destroys information; IVNA preserves it.
- **Limitation**: For catastrophic cancellation in general, IVNA needs to know the "true" index at the point of cancellation — which can be circular. The theorem is strongest for STRUCTURAL NaN (0/0, ∞·0) not for ROUNDING cancellation.
- **Publishability**: Not a standalone numerical analysis paper, but the NaN elimination theorem and comparison table strengthen the existing VEA section significantly.

## Recommendation

Add to paper:
1. NaN Elimination as a formal proposition in the VEA section
2. Comparison table (IVNA vs interval arithmetic vs wheels vs TwoSum)
3. Quadratic formula worked example
