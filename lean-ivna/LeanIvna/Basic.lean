/-!
# IVNA Basic Types

The fundamental type for Indexed Virtual Number Algebra.

An IVNA value is one of:
- `real a` : a scalar value a
- `zero x` : an indexed zero 0_x
- `inf x`  : an indexed infinity ∞_x
-/

namespace IVNA

/-- The IVNA value type, parameterized by an index/scalar type `F`. -/
inductive V (F : Type) where
  | real : F → V F
  | zero : F → V F
  | inf  : F → V F

end IVNA
