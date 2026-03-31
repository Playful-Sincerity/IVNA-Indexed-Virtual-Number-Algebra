import LeanIvna.Basic

/-!
# IVNA Axiom System

The IVNA axioms as a Lean structure. Any type satisfying this structure
is a valid model of IVNA, proving the axioms are mutually consistent.
-/

namespace IVNA

/-- The IVNA axiom system, bundling a "field" F with virtual operations.

    We include the field operations (fadd, fmul, fdiv, etc.) as part of
    the structure rather than requiring a Mathlib Field instance.
    This keeps the formalization self-contained. -/
structure IVNASystem (F : Type) where
  /-- Field operations on F -/
  fzero : F
  fone  : F
  fadd  : F → F → F
  fmul  : F → F → F
  fneg  : F → F
  finv  : F → F
  fdiv  : F → F → F

  /-- Nontriviality -/
  one_ne_zero : fone ≠ fzero

  /-- Required field properties -/
  mul_comm'  : ∀ (a b : F), fmul a b = fmul b a
  mul_assoc' : ∀ (a b c : F), fmul (fmul a b) c = fmul a (fmul b c)
  mul_one'   : ∀ (a : F), fmul a fone = a
  add_comm'  : ∀ (a b : F), fadd a b = fadd b a
  add_assoc' : ∀ (a b c : F), fadd (fadd a b) c = fadd a (fadd b c)
  div_def'   : ∀ (a b : F), fdiv a b = fmul a (finv b)
  inv_cancel': ∀ (a : F), a ≠ fzero → fmul a (finv a) = fone

  /-- IVNA operations -/
  vmul : V F → V F → V F
  vdiv : V F → V F → V F
  vadd : V F → V F → V F

  /-- MULTIPLICATION AXIOMS -/
  ax_mul_real_real : ∀ (a b : F), vmul (V.real a) (V.real b) = V.real (fmul a b)
  ax_mul_zero_zero : ∀ (x y : F), vmul (V.zero x) (V.zero y) = V.zero (fmul x y)
  ax_mul_inf_inf   : ∀ (x y : F), vmul (V.inf x) (V.inf y) = V.inf (fmul x y)
  ax_mul_zero_inf  : ∀ (x y : F), vmul (V.zero x) (V.inf y) = V.real (fmul x y)
  ax_mul_real_zero : ∀ (n x : F), vmul (V.real n) (V.zero x) = V.zero (fmul n x)
  ax_mul_real_inf  : ∀ (n x : F), vmul (V.real n) (V.inf x) = V.inf (fmul n x)

  /-- DIVISION AXIOMS -/
  ax_div_real_zero : ∀ (y x : F), vdiv (V.real y) (V.zero x) = V.inf (fdiv y x)
  ax_div_real_inf  : ∀ (y x : F), vdiv (V.real y) (V.inf x) = V.zero (fdiv y x)
  ax_div_zero_zero : ∀ (x y : F), vdiv (V.zero x) (V.zero y) = V.real (fdiv x y)
  ax_div_inf_inf   : ∀ (x y : F), vdiv (V.inf x) (V.inf y) = V.real (fdiv x y)

  /-- ADDITION AXIOMS -/
  ax_add_zero_zero : ∀ (x y : F), vadd (V.zero x) (V.zero y) = V.zero (fadd x y)
  ax_add_inf_inf   : ∀ (x y : F), vadd (V.inf x) (V.inf y) = V.inf (fadd x y)

  /-- COMMUTATIVITY -/
  ax_vmul_comm : ∀ (a b : V F), vmul a b = vmul b a

end IVNA
