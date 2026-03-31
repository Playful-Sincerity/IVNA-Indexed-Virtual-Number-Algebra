import LeanIvna.Axioms

/-!
# IVNA Consistency Proof via Model Construction

We construct a concrete `IVNASystem` using `F = Bool` (GF(2)).
If the axioms hold over GF(2), they are mutually consistent.
-/

namespace IVNA

-- GF(2) field operations on Bool
private def bAdd : Bool → Bool → Bool := xor
private def bMul : Bool → Bool → Bool := (· && ·)
private def bNeg : Bool → Bool := id  -- -x = x in GF(2)
private def bInv : Bool → Bool := id  -- x⁻¹ = x in GF(2) (for x ≠ 0)

/-- IVNA multiplication on `V Bool`. -/
def vmulB : V Bool → V Bool → V Bool
  | V.real a,  V.real b  => V.real (bMul a b)
  | V.real n,  V.zero x  => V.zero (bMul n x)
  | V.real n,  V.inf x   => V.inf  (bMul n x)
  | V.zero x,  V.real n  => V.zero (bMul n x)
  | V.zero x,  V.zero y  => V.zero (bMul x y)
  | V.zero x,  V.inf y   => V.real (bMul x y)
  | V.inf x,   V.real n  => V.inf  (bMul n x)
  | V.inf x,   V.zero y  => V.real (bMul y x)
  | V.inf x,   V.inf y   => V.inf  (bMul x y)

/-- IVNA division on `V Bool`. -/
def vdivB : V Bool → V Bool → V Bool
  | V.real a,  V.real b  => V.real (bMul a b)  -- fdiv = fmul in GF(2)
  | V.real y,  V.zero x  => V.inf  (bMul y x)
  | V.real y,  V.inf x   => V.zero (bMul y x)
  | V.zero x,  V.real n  => V.zero (bMul x n)
  | V.zero x,  V.zero y  => V.real (bMul x y)
  | V.zero x,  V.inf y   => V.zero (bMul x y)
  | V.inf x,   V.real n  => V.inf  (bMul x n)
  | V.inf x,   V.zero y  => V.inf  (bMul x y)
  | V.inf x,   V.inf y   => V.real (bMul x y)

/-- IVNA addition on `V Bool`. -/
def vaddB : V Bool → V Bool → V Bool
  | V.real a,  V.real b  => V.real (bAdd a b)
  | V.real a,  V.zero _  => V.real a     -- unconstrained
  | V.real a,  V.inf _   => V.real a     -- unconstrained
  | V.zero x,  V.real _  => V.zero x     -- unconstrained
  | V.zero x,  V.zero y  => V.zero (bAdd x y)  -- A10
  | V.zero x,  V.inf _   => V.zero x     -- unconstrained
  | V.inf x,   V.real _  => V.inf x      -- unconstrained
  | V.inf x,   V.zero _  => V.inf x      -- unconstrained
  | V.inf x,   V.inf y   => V.inf  (bAdd x y)  -- A11

-- Helper lemmas for Bool/GF(2) field properties
private theorem bMul_comm : ∀ (a b : Bool), bMul a b = bMul b a := by
  intro a b; cases a <;> cases b <;> rfl

private theorem bMul_assoc : ∀ (a b c : Bool), bMul (bMul a b) c = bMul a (bMul b c) := by
  intro a b c; cases a <;> cases b <;> cases c <;> rfl

private theorem bMul_one : ∀ (a : Bool), bMul a true = a := by
  intro a; cases a <;> rfl

private theorem bAdd_comm : ∀ (a b : Bool), bAdd a b = bAdd b a := by
  intro a b; cases a <;> cases b <;> rfl

private theorem bAdd_assoc : ∀ (a b c : Bool), bAdd (bAdd a b) c = bAdd a (bAdd b c) := by
  intro a b c; cases a <;> cases b <;> cases c <;> rfl

private theorem bInv_cancel : ∀ (a : Bool), a ≠ false → bMul a (bInv a) = true := by
  intro a ha; cases a with
  | false => exact absurd rfl ha
  | true  => rfl

/-- **Main Consistency Theorem**: The IVNA axiom set is satisfiable.

    We exhibit a concrete model over GF(2) = Bool. Every axiom holds
    by case analysis on Bool values (decidable in finite time). -/
def ivna_consistent : IVNASystem Bool where
  fzero    := false
  fone     := true
  fadd     := bAdd
  fmul     := bMul
  fneg     := bNeg
  finv     := bInv
  fdiv     := bMul  -- In GF(2), a/b = a * b⁻¹ = a * b (since b⁻¹ = b)

  one_ne_zero := by decide
  mul_comm'   := bMul_comm
  mul_assoc'  := bMul_assoc
  mul_one'    := bMul_one
  add_comm'   := bAdd_comm
  add_assoc'  := bAdd_assoc
  div_def'    := by intro a b; cases a <;> cases b <;> rfl
  inv_cancel' := bInv_cancel

  vmul := vmulB
  vdiv := vdivB
  vadd := vaddB

  ax_mul_real_real := by intro a b; rfl
  ax_mul_zero_zero := by intro x y; rfl
  ax_mul_inf_inf   := by intro x y; rfl
  ax_mul_zero_inf  := by intro x y; rfl
  ax_mul_real_zero := by intro n x; rfl
  ax_mul_real_inf  := by intro n x; rfl

  ax_div_real_zero := by intro y x; rfl
  ax_div_real_inf  := by intro y x; rfl
  ax_div_zero_zero := by intro x y; rfl
  ax_div_inf_inf   := by intro x y; rfl

  ax_add_zero_zero := by intro x y; rfl
  ax_add_inf_inf   := by intro x y; rfl

  ax_vmul_comm := by
    intro a b
    cases a with
    | real a =>
      cases b with
      | real b =>
        show V.real (bMul a b) = V.real (bMul b a)
        rw [bMul_comm]
      | zero x => rfl
      | inf x  => rfl
    | zero x =>
      cases b with
      | real n => rfl
      | zero y =>
        show V.zero (bMul x y) = V.zero (bMul y x)
        rw [bMul_comm]
      | inf y  => rfl  -- both sides reduce to V.real (bMul x y)
    | inf x =>
      cases b with
      | real n => rfl
      | zero y => rfl  -- both sides reduce to V.real (bMul y x)
      | inf y  =>
        show V.inf (bMul x y) = V.inf (bMul y x)
        rw [bMul_comm]

end IVNA
