# IVNA Lean 4 Formalization

Machine-checked formalization of the Indexed Virtual Number Algebra (IVNA) axiom system in Lean 4.

## What This Proves

1. **Consistency**: The 11 IVNA axioms (A1-A11) plus commutativity are mutually consistent. We construct a concrete model over GF(2) where all axioms hold simultaneously.

2. **Key Theorems** (12 theorems derived from axioms alone):
   - T1: Division-by-zero roundtrip: `(y / 0_x) * 0_x = y`
   - T2: Multiplication commutativity
   - T3: Division-by-infinity roundtrip: `(y / inf_x) * inf_x = y`
   - T4-T5: Self-division yields 1: `0_x / 0_x = 1`, `inf_x / inf_x = 1`
   - T6-T7: Associativity of scalar-virtual multiplication
   - T8: Scalar-zero division recovery: `(n * 0_x) / 0_x = n`
   - T9-T12: Commutativity and associativity of virtual addition

## File Structure

| File | Contents |
|------|----------|
| `LeanIvna/Basic.lean` | The `V F` inductive type (real, zero, inf) |
| `LeanIvna/Axioms.lean` | `IVNASystem F` structure with all 11 axioms |
| `LeanIvna/Model.lean` | Consistency proof via GF(2) model construction |
| `LeanIvna/Theorems.lean` | 12 theorems derived from axioms |
| `LeanIvna.lean` | Root module importing everything |

## How to Verify

```bash
# Requires Lean 4.16.0 (installed via elan)
cd lean-ivna
lake build
```

A successful build means every proof has been machine-checked.

## Design Decisions

**No Mathlib dependency.** The formalization is entirely self-contained. Field operations are bundled into the `IVNASystem` structure rather than relying on Mathlib's algebraic hierarchy.

**GF(2) as consistency model.** We use `Bool` (the two-element field) as our concrete model. This is a valid consistency proof because the axioms are universally quantified equalities -- if they hold over any model, the axiom set is satisfiable, hence consistent. The choice of GF(2) makes all proofs decidable by case analysis.

**Order-1 only.** We formalize first-order indexed zeros and infinities (0_x, inf_x) but not higher orders (0^2_x, etc.). The core axioms and all key theorems are fully expressible at order 1.

**Abstract over the field.** The theorems in `Theorems.lean` are parametric over any `IVNASystem F` -- they hold for ANY model, not just GF(2). The model construction merely proves such a model exists.

## Axiom Summary

| ID | Rule | Lean field |
|----|------|------------|
| A1 | 0_x * 0_y = 0_{xy} | `ax_mul_zero_zero` |
| A2 | inf_x * inf_y = inf_{xy} | `ax_mul_inf_inf` |
| A3 | 0_x * inf_y = xy | `ax_mul_zero_inf` |
| A4 | n * 0_x = 0_{nx} | `ax_mul_real_zero` |
| A5 | n * inf_x = inf_{nx} | `ax_mul_real_inf` |
| A6 | y / 0_x = inf_{y/x} | `ax_div_real_zero` |
| A7 | y / inf_x = 0_{y/x} | `ax_div_real_inf` |
| A8 | 0_x / 0_y = x/y | `ax_div_zero_zero` |
| A9 | inf_x / inf_y = x/y | `ax_div_inf_inf` |
| A10 | 0_x + 0_y = 0_{x+y} | `ax_add_zero_zero` |
| A11 | inf_x + inf_y = inf_{x+y} | `ax_add_inf_inf` |

## Lean Version

Lean 4.16.0 (leanprover/lean4:v4.16.0)
