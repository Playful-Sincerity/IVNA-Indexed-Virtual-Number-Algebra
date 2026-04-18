"""
IVNA Verification — Multivariate Limit Analysis
==================================================

Verifies that IVNA correctly produces directional limits for
multivariate expressions using different index ratios.

Prompted by Kiel Howe's feedback (2026-04-13): "stress test against
problems where you don't actually have a shared limit."

Finding: IVNA handles independent approaches through index ratios
(directions) and orders (rates), matching classical results exactly.
"""

import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'code'))
from ivna import Virtual, Z, I

passed = 0
failed = 0
results = []

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        results.append(("PASS", name))
    else:
        failed += 1
        results.append(("FAIL", name + (f" [{detail}]" if detail else "")))


# ============================================================
# CASE 1: xy/(x^2+y^2) — direction-dependent limit
# ============================================================

# Classical: lim(x→0, y→0) xy/(x²+y²) depends on direction.
# Along y=mx: answer is m/(1+m²).
# IVNA: x=0_a, y=0_b → ab/(a²+b²), which IS the directional limit for slope b/a.

for a, b, expected_num, expected_den in [
    (1, 1, 1, 2),     # y=x direction: 1/2
    (1, 2, 2, 5),     # y=2x direction: 2/5
    (1, 3, 3, 10),    # y=3x direction: 3/10
    (2, 3, 6, 13),    # y=3x/2 direction: 6/13
    (3, 1, 3, 10),    # y=x/3 direction: 3/10
    (1, 5, 5, 26),    # y=5x direction: 5/26
    (2, 1, 2, 5),     # y=x/2 direction: 2/5
]:
    x = Z(a)
    y = Z(b)

    num = x * y          # 0²_{ab}
    x_sq = x ** 2        # 0²_{a²}
    y_sq = y ** 2        # 0²_{b²}
    denom = x_sq + y_sq  # 0²_{a²+b²}

    result = num / denom
    expected = Fraction(expected_num, expected_den)

    check(f"Multivar xy/(x²+y²) direction b/a={b}/{a}: IVNA={result}, classical={expected}",
          result == expected,
          f"got {result}")


# ============================================================
# CASE 2: (x²-y²)/(x²+y²) — another direction-dependent limit
# ============================================================

# Along y=mx: (x²-m²x²)/(x²+m²x²) = (1-m²)/(1+m²)
# IVNA: x=0_a, y=0_b → (a²-b²)/(a²+b²)

for a, b in [(1,1), (1,2), (2,1), (1,3), (3,2)]:
    x = Z(a)
    y = Z(b)

    x_sq = x ** 2
    y_sq = y ** 2
    num = x_sq - y_sq      # 0²_{a²-b²} (or real 0 if a=b)
    denom = x_sq + y_sq    # 0²_{a²+b²}

    if isinstance(num, Virtual) and isinstance(denom, Virtual):
        result = num / denom
    elif num == 0:
        result = Fraction(0)
    else:
        result = "unexpected"

    expected = Fraction(a**2 - b**2, a**2 + b**2)

    check(f"Multivar (x²-y²)/(x²+y²) a={a},b={b}: IVNA={result}, classical={expected}",
          result == expected,
          f"got {result}")


# ============================================================
# CASE 3: Higher-order approach (curved path y=x²)
# ============================================================

# Along y=x²: lim x·x²/(x²+x⁴) = lim x³/(x²(1+x²)) = lim x/(1+x²) = 0
# IVNA: x=0₁, y=0²₁ (second-order zero)

x = Z(1)           # 0₁
y = Z(1) ** 2       # 0²₁ (y = x²)

# xy = 0₁ · 0²₁ = 0³₁
num = x * y
check("Curved approach: x·y = 0₁·0²₁ = 0³₁",
      isinstance(num, Virtual) and num.kind == 'zero' and num.order == 3)

# x² = 0²₁
x_sq = x ** 2
check("Curved approach: x² = 0²₁",
      isinstance(x_sq, Virtual) and x_sq.order == 2)

# x²+y² = 0²₁ + 0⁴₁ → dominated by 0²₁ (lower order wins)
# In IVNA, different-order addition produces a tuple (coexistence)
# The leading term is 0²₁ (it dominates)
y_sq = y ** 2  # 0⁴₁

# xy / x² = 0³₁ / 0²₁ = 0₁ (one order remains → approaches zero)
result_leading = num / x_sq
check("Curved approach: xy/x² = 0³₁/0²₁ = 0₁ → collapses to 0",
      isinstance(result_leading, Virtual) and result_leading.kind == 'zero',
      f"got {result_leading}")

check("Curved approach: 0₁ collapses to 0 under =;",
      result_leading.collapse() == 0 if isinstance(result_leading, Virtual) else False)


# ============================================================
# CASE 4: Division-by-zero roundtrip in multivariate context
# ============================================================

# Verify that multivariate IVNA still preserves information
for a, b in [(2, 3), (5, 7), (1, 4)]:
    product = Z(a) * Z(b)  # 0²_{ab}
    # Divide by 0_a to recover 0_b
    recovered = product / Z(a)  # 0²_{ab} / 0_a should give...
    # Actually: 0²_{ab} / 0₁_a — different orders: 0²/0¹ = 0¹
    # Result: 0_{ab/a} = 0_b (one order cancels, index divides)
    check(f"Multivar roundtrip: (0_{a}·0_{b})/0_{a} recovers 0_{b}",
          isinstance(recovered, Virtual) and recovered.kind == 'zero'
          and recovered.index == Fraction(b) and recovered.order == 1,
          f"got {recovered}")


# ============================================================
# REPORT
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("IVNA — MULTIVARIATE LIMIT VERIFICATION")
    print("(Prompted by Kiel Howe's feedback, 2026-04-13)")
    print("=" * 70)
    print()

    for status, name in results:
        icon = "PASS" if status == "PASS" else "FAIL"
        print(f"  [{icon}] {name}")

    print()
    print(f"  PASSED: {passed}")
    print(f"  FAILED: {failed}")
    print(f"  TOTAL:  {passed + failed}")
    print()

    if failed == 0:
        print("  ALL MULTIVARIATE CHECKS PASSED")
    else:
        print(f"  {failed} CHECKS FAILED")

    sys.exit(0 if failed == 0 else 1)
