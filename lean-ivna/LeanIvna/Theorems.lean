import LeanIvna.Axioms

/-!
# IVNA Theorems — derived from axioms, hold in ANY model
-/

namespace IVNA

variable {F : Type} (S : IVNASystem F)

/-- **Theorem 1 (Division-by-Zero Roundtrip).**

    `(real(y) / 0_x) · 0_x = real(y)`

    The signature result: dividing by an indexed zero and multiplying
    back recovers the original value, because the index tracks weight.

    Proof:
    1. A6:   real(y) / 0_x = ∞_{y/x}
    2. Comm: ∞_{y/x} · 0_x = 0_x · ∞_{y/x}
    3. A3:   0_x · ∞_{y/x} = real(x · (y/x))
    4. Algebra: x · (y/x) = x · y · x⁻¹ = y   (using inv_cancel)
-/
theorem div_zero_roundtrip (y x : F) (hx : x ≠ S.fzero) :
    S.vmul (S.vdiv (V.real y) (V.zero x)) (V.zero x) = V.real y := by
  rw [S.ax_div_real_zero]       -- ∞_{fdiv y x}
  rw [S.ax_vmul_comm]           -- 0_x · ∞_{fdiv y x}
  rw [S.ax_mul_zero_inf]        -- real(fmul x (fdiv y x))
  congr 1                       -- suffices: fmul x (fdiv y x) = y
  rw [S.div_def']               -- fmul x (fmul y (finv x))
  rw [← S.mul_assoc']           -- fmul (fmul x y) (finv x)
  rw [S.mul_comm' x y]          -- fmul (fmul y x) (finv x)
  rw [S.mul_assoc']             -- fmul y (fmul x (finv x))
  rw [S.inv_cancel' x hx]       -- fmul y fone
  exact S.mul_one' y

/-- **Theorem 2 (Commutativity).** Restated from axiom for emphasis. -/
theorem vmul_comm (a b : V F) : S.vmul a b = S.vmul b a :=
  S.ax_vmul_comm a b

/-- **Theorem 3 (Division-by-Infinity Roundtrip).**

    `(real(y) / ∞_x) · ∞_x = real(y)`

    The infinity dual of Theorem 1.
-/
theorem div_inf_roundtrip (y x : F) (hx : x ≠ S.fzero) :
    S.vmul (S.vdiv (V.real y) (V.inf x)) (V.inf x) = V.real y := by
  rw [S.ax_div_real_inf]        -- 0_{fdiv y x}
  rw [S.ax_mul_zero_inf]        -- real(fmul (fdiv y x) x)
  congr 1
  rw [S.div_def']               -- fmul (fmul y (finv x)) x
  rw [S.mul_assoc']             -- fmul y (fmul (finv x) x)
  rw [S.mul_comm' (S.finv x) x] -- fmul y (fmul x (finv x))
  rw [S.inv_cancel' x hx]
  exact S.mul_one' y

/-- **Theorem 4 (Zero Self-Division).**

    `0_x / 0_x = real(1)`
-/
theorem zero_div_self (x : F) (hx : x ≠ S.fzero) :
    S.vdiv (V.zero x) (V.zero x) = V.real S.fone := by
  rw [S.ax_div_zero_zero]
  congr 1
  rw [S.div_def', S.inv_cancel' x hx]

/-- **Theorem 5 (Infinity Self-Division).**

    `∞_x / ∞_x = real(1)`
-/
theorem inf_div_self (x : F) (hx : x ≠ S.fzero) :
    S.vdiv (V.inf x) (V.inf x) = V.real S.fone := by
  rw [S.ax_div_inf_inf]
  congr 1
  rw [S.div_def', S.inv_cancel' x hx]

/-- **Theorem 6 (Associativity: real × real × zero).**

    `real(a) · (real(b) · 0_x) = (real(a) · real(b)) · 0_x`
-/
theorem mul_assoc_real_real_zero (a b x : F) :
    S.vmul (V.real a) (S.vmul (V.real b) (V.zero x))
    = S.vmul (S.vmul (V.real a) (V.real b)) (V.zero x) := by
  rw [S.ax_mul_real_zero b x]         -- vmul (real a) (zero (fmul b x))
  rw [S.ax_mul_real_zero a]            -- zero (fmul a (fmul b x))
  rw [S.ax_mul_real_real a b]          -- vmul (real (fmul a b)) (zero x)
  rw [S.ax_mul_real_zero]              -- zero (fmul (fmul a b) x)
  congr 1
  exact (S.mul_assoc' a b x).symm

/-- **Theorem 7 (Associativity: real × real × inf).**

    `real(a) · (real(b) · ∞_x) = (real(a) · real(b)) · ∞_x`
-/
theorem mul_assoc_real_real_inf (a b x : F) :
    S.vmul (V.real a) (S.vmul (V.real b) (V.inf x))
    = S.vmul (S.vmul (V.real a) (V.real b)) (V.inf x) := by
  rw [S.ax_mul_real_inf b x]
  rw [S.ax_mul_real_inf a]
  rw [S.ax_mul_real_real a b]
  rw [S.ax_mul_real_inf]
  congr 1
  exact (S.mul_assoc' a b x).symm

/-- **Theorem 8 (Scalar-Zero Division Recovery).**

    `(real(n) · 0_x) / 0_x = real(n)`

    Multiplying a zero by a scalar, then dividing by that zero, recovers n.
-/
theorem scalar_zero_div_zero (n x : F) (hx : x ≠ S.fzero) :
    S.vdiv (S.vmul (V.real n) (V.zero x)) (V.zero x) = V.real n := by
  rw [S.ax_mul_real_zero]       -- vdiv (zero (fmul n x)) (zero x)
  rw [S.ax_div_zero_zero]       -- real (fdiv (fmul n x) x)
  congr 1
  rw [S.div_def']               -- fmul (fmul n x) (finv x)
  rw [S.mul_assoc']             -- fmul n (fmul x (finv x))
  rw [S.inv_cancel' x hx]
  exact S.mul_one' n

/-- **Theorem 9 (Zero Addition Commutativity).**

    `0_x + 0_y = 0_y + 0_x`
-/
theorem add_zero_comm (x y : F) :
    S.vadd (V.zero x) (V.zero y) = S.vadd (V.zero y) (V.zero x) := by
  rw [S.ax_add_zero_zero, S.ax_add_zero_zero]
  congr 1
  exact S.add_comm' x y

/-- **Theorem 10 (Zero Addition Associativity).**

    `(0_x + 0_y) + 0_z = 0_x + (0_y + 0_z)`
-/
theorem add_zero_assoc (x y z : F) :
    S.vadd (S.vadd (V.zero x) (V.zero y)) (V.zero z)
    = S.vadd (V.zero x) (S.vadd (V.zero y) (V.zero z)) := by
  rw [S.ax_add_zero_zero x y, S.ax_add_zero_zero, S.ax_add_zero_zero y z,
      S.ax_add_zero_zero]
  congr 1
  exact S.add_assoc' x y z

/-- **Theorem 11 (Infinity Addition Commutativity).**

    `∞_x + ∞_y = ∞_y + ∞_x`
-/
theorem add_inf_comm (x y : F) :
    S.vadd (V.inf x) (V.inf y) = S.vadd (V.inf y) (V.inf x) := by
  rw [S.ax_add_inf_inf, S.ax_add_inf_inf]
  congr 1
  exact S.add_comm' x y

/-- **Theorem 12 (Infinity Addition Associativity).**

    `(∞_x + ∞_y) + ∞_z = ∞_x + (∞_y + ∞_z)`
-/
theorem add_inf_assoc (x y z : F) :
    S.vadd (S.vadd (V.inf x) (V.inf y)) (V.inf z)
    = S.vadd (V.inf x) (S.vadd (V.inf y) (V.inf z)) := by
  rw [S.ax_add_inf_inf x y, S.ax_add_inf_inf, S.ax_add_inf_inf y z,
      S.ax_add_inf_inf]
  congr 1
  exact S.add_assoc' x y z

end IVNA
