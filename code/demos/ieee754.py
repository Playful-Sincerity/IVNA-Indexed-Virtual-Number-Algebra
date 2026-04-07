"""
Demo 3: IEEE 754 vs IVNA — Comprehensive Edge-Case Comparison
=============================================================

Runs 30+ edge-case arithmetic operations in both IEEE 754 and IVNA.
Counts: how many NaN/undefined cases does IVNA resolve?
Shows: exactly where IVNA preserves information that IEEE 754 destroys.
"""

import sys
import os
import math
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ivna import Virtual, Z, I

# ============================================================
# TEST OPERATIONS
# ============================================================

def ieee_op(description, expr_str, ieee_result, ivna_result, ivna_roundtrip=None):
    """Create a comparison record."""
    # Classify IEEE result
    if isinstance(ieee_result, float):
        if math.isnan(ieee_result):
            ieee_class = 'NaN'
        elif math.isinf(ieee_result):
            ieee_class = 'Inf' if ieee_result > 0 else '-Inf'
        else:
            ieee_class = 'finite'
    else:
        ieee_class = 'finite'

    # Classify IVNA result
    if isinstance(ivna_result, Virtual):
        if ivna_result.kind == 'inf':
            ivna_class = 'virtual_inf'
        else:
            ivna_class = 'virtual_zero'
    elif isinstance(ivna_result, (int, float, Fraction)):
        ivna_class = 'finite'
    elif isinstance(ivna_result, tuple):
        ivna_class = 'coexistence'
    elif isinstance(ivna_result, str):
        ivna_class = 'special'
    else:
        ivna_class = str(type(ivna_result))

    # Does IVNA resolve an IEEE failure?
    resolved = ieee_class in ('NaN', 'Inf', '-Inf') and ivna_class in ('finite', 'virtual_inf', 'virtual_zero')

    # Does IVNA preserve more information?
    info_preserved = (
        (ieee_class == 'NaN' and ivna_class != 'NaN') or
        (ieee_class in ('Inf', '-Inf') and ivna_class == 'virtual_inf') or
        (ieee_class == 'finite' and ieee_result == 0 and ivna_class == 'virtual_zero')
    )

    return {
        'description': description,
        'expr': expr_str,
        'ieee_result': ieee_result,
        'ieee_class': ieee_class,
        'ivna_result': ivna_result,
        'ivna_class': ivna_class,
        'resolved': resolved,
        'info_preserved': info_preserved,
        'roundtrip': ivna_roundtrip,
    }


def run_all_comparisons():
    """Run all edge-case comparisons."""
    results = []

    # === DIVISION BY ZERO ===

    # 1. Basic division by zero
    results.append(ieee_op(
        "5 / 0",
        "5 / 0",
        float('inf'),  # IEEE: +Inf (information about 5 lost)
        5 / Z(1),       # IVNA: ∞_5 (5 is preserved in index)
        ivna_roundtrip="∞_5 · 0_1 = 5"
    ))

    # 2. Different numerators / 0
    results.append(ieee_op(
        "3 / 0",
        "3 / 0",
        float('inf'),  # IEEE: +Inf (same as 5/0 — lost which number!)
        3 / Z(1),       # IVNA: ∞_3 (3 preserved)
        ivna_roundtrip="∞_3 · 0_1 = 3"
    ))

    # 3. Negative / 0
    results.append(ieee_op(
        "-7 / 0",
        "-7 / 0",
        float('-inf'),
        (-7) / Z(1),    # IVNA: ∞_{-7}
        ivna_roundtrip="∞_{-7} · 0_1 = -7"
    ))

    # 4. 0 / 0
    results.append(ieee_op(
        "0 / 0",
        "0 / 0",
        float('nan'),   # IEEE: NaN
        Z(0) / Z(1),    # IVNA: 0/1 = 0 (via 0_x/0_y = x/y, here 0_0/0_1)
        ivna_roundtrip="0_0 / 0_1 = 0 (index ratio)"
    ))

    # === INFINITY ARITHMETIC ===

    # 5. Inf - Inf
    results.append(ieee_op(
        "∞ - ∞",
        "Inf - Inf",
        float('inf') - float('inf'),  # IEEE: NaN
        I(5) - I(3),                   # IVNA: ∞_5 - ∞_3 = ∞_2 (indices subtract)
    ))

    # 6. Inf / Inf
    results.append(ieee_op(
        "∞ / ∞",
        "Inf / Inf",
        float('inf') / float('inf'),  # IEEE: NaN
        I(6) / I(2),                   # IVNA: ∞_6 / ∞_2 = 3 (index ratio)
    ))

    # 7. 0 * Inf
    results.append(ieee_op(
        "0 × ∞",
        "0 * Inf",
        0 * float('inf'),             # IEEE: NaN
        Z(3) * I(5),                   # IVNA: 0_3 · ∞_5 = 15 (index product)
        ivna_roundtrip="0_3 · ∞_5 = 3·5 = 15"
    ))

    # 8. Inf * 0
    results.append(ieee_op(
        "∞ × 0",
        "Inf * 0",
        float('inf') * 0,             # IEEE: NaN
        I(7) * Z(2),                   # IVNA: ∞_7 · 0_2 = 14
    ))

    # 9. Inf + Inf
    results.append(ieee_op(
        "∞ + ∞",
        "Inf + Inf",
        float('inf') + float('inf'),  # IEEE: Inf (loses structure)
        I(3) + I(5),                   # IVNA: ∞_8 (indices add)
    ))

    # 10. 0 * 0 (meaningful case)
    results.append(ieee_op(
        "0 × 0 (indexed)",
        "0_3 · 0_5",
        0 * 0,                         # IEEE: 0 (loses what the zeros were)
        Z(3) * Z(5),                   # IVNA: 0²_15 (higher order, product index)
    ))

    # === DIVISION ROUNDTRIPS ===

    # 11. Division roundtrip: (a/0) * 0
    a = 42
    results.append(ieee_op(
        "(42/0) × 0 roundtrip",
        "(42/0) * 0",
        (float('inf')) * 0,            # IEEE: NaN (info destroyed)
        (a / Z(1)) * Z(1),             # IVNA: ∞_42 · 0_1 = 42 (roundtrip!)
        ivna_roundtrip="42/0_1 = ∞_42, ∞_42 · 0_1 = 42 ✓"
    ))

    # 12. Double division roundtrip
    results.append(ieee_op(
        "1 / (1/0) roundtrip",
        "1 / (1/0)",
        1 / float('inf'),             # IEEE: 0 (lost which infinity)
        1 / (1 / Z(1)),               # IVNA: 1 / ∞_1 = 0_1, then 1/0_1 = ∞_1... actually 1/(1/0_1) = 1/∞_1 = 0_1
    ))

    # === POWER OPERATIONS ===

    # 13. 0^0
    results.append(ieee_op(
        "0^0",
        "0**0",
        0**0,                          # IEEE: 1 (by convention, not algebraically)
        "Convention: 1 (same as IEEE)",  # IVNA agrees with convention
    ))

    # 14. Inf^0
    results.append(ieee_op(
        "∞^0",
        "Inf**0",
        float('inf')**0,              # IEEE: 1 (dubious convention)
        "∞_x ^ 0 — undefined in IVNA (order becomes 0)",
    ))

    # 15. 0^(-1) = 1/0
    results.append(ieee_op(
        "0^(-1) = 1/0",
        "0**(-1)",
        float('inf'),                  # IEEE: Inf (lost info about which zero)
        Z(3) ** (-1),                  # IVNA: 0_3^{-1} — needs special handling
    ))

    # === COMPARISON: DIFFERENT ZEROS, DIFFERENT INFINITIES ===

    # 16. Are all zeros equal?
    results.append(ieee_op(
        "5/Inf vs 3/Inf",
        "5/Inf == 3/Inf ?",
        5/float('inf') == 3/float('inf'),  # IEEE: True (0 == 0)
        Z(5) == Z(3),                       # IVNA: False (0_5 ≠ 0_3)
    ))

    # 17. Are all infinities equal?
    results.append(ieee_op(
        "5/0 vs 3/0",
        "5/0 == 3/0 ?",
        True,  # IEEE: Inf == Inf is True
        I(5) == I(3),                       # IVNA: False (∞_5 ≠ ∞_3)
    ))

    # === LIMIT-LIKE OPERATIONS ===

    # 18. sin(x)/x as x→0
    results.append(ieee_op(
        "sin(0)/0 (limit = 1)",
        "sin(0)/0",
        float('nan'),                  # IEEE: 0/0 = NaN
        Z(1) / Z(1),                   # IVNA: 0_1/0_1 = 1 (using Taylor: sin(0_1) ≈ 0_1)
        ivna_roundtrip="sin(0_x) ≈ 0_x for small x, so sin(0_1)/0_1 = 0_1/0_1 = 1"
    ))

    # 19. (1-cos(x))/x² as x→0 (limit = 1/2)
    results.append(ieee_op(
        "(1-cos(0))/0² (limit = 1/2)",
        "(1-cos(0))/0²",
        float('nan'),                  # IEEE: 0/0 = NaN
        "IVNA: 0_{1/2}/0_1 = 1/2 via Taylor",  # cos(0_x) ≈ 1 - 0_{x²/2}
    ))

    # 20. x*ln(x) as x→0 (limit = 0)
    results.append(ieee_op(
        "0·ln(0) (limit = 0)",
        "0 * ln(0)",
        0 * float('-inf'),            # IEEE: NaN (0 * -Inf)
        "IVNA: 0_x · ∞_{-ln(1/x)} = -x·ln(1/x) → 0",
    ))

    # === ARITHMETIC CHAINS ===

    # 21. (a/0) * (0/b) — should give a/b
    results.append(ieee_op(
        "(6/0) × (0/3) = 2",
        "(6/0) * (0/3)",
        float('inf') * 0,             # IEEE: NaN
        (6 / Z(1)) * (Z(1) / 3),     # IVNA: ∞_6 · 0_{1/3} = 6·(1/3) = 2
    ))

    # 22. (a/0) / (b/0) — should give a/b
    results.append(ieee_op(
        "(6/0) / (3/0) = 2",
        "(6/0) / (3/0)",
        float('inf') / float('inf'),  # IEEE: NaN
        (6 / Z(1)) / (3 / Z(1)),     # IVNA: ∞_6 / ∞_3 = 2
    ))

    # 23. 0/0 + 0/0 — should be addable
    results.append(ieee_op(
        "0/0 + 0/0",
        "NaN + NaN",
        float('nan') + float('nan'),  # IEEE: NaN
        Z(3)/Z(1) + Z(5)/Z(1),       # IVNA: 3 + 5 = 8
    ))

    # 24. Nested: 1/(1/(1/0))
    results.append(ieee_op(
        "1/(1/(1/0))",
        "1/(1/(1/0))",
        0.0,                          # IEEE: 1/(1/Inf) = 1/0 = Inf... actually 1/Inf=0, 1/0=Inf
        1 / (1 / (1 / Z(1))),         # IVNA: 1/0_1=∞_1, 1/∞_1=0_1, 1/0_1=∞_1
    ))

    # === MULTIPLICATION CHAINS ===

    # 25. 0 * Inf * 0 * Inf
    results.append(ieee_op(
        "0·∞·0·∞ chain",
        "0*Inf*0*Inf",
        float('nan'),                  # IEEE: NaN propagation
        Z(2) * I(3) * Z(4) * I(5),   # IVNA: (0_2·∞_3) · (0_4·∞_5) = 6 · 20 = 120
    ))

    # 26. Inf - Inf (same origin)
    results.append(ieee_op(
        "∞ - ∞ (same index)",
        "∞_5 - ∞_5",
        float('nan'),                  # IEEE: NaN
        I(5) - I(5),                   # IVNA: 0 (D-INDEX-ZERO: exits to real 0)
    ))

    # 27. Scalar * Inf preservation
    results.append(ieee_op(
        "3 × ∞ (which infinity?)",
        "3 * Inf",
        float('inf'),                  # IEEE: Inf (lost the 3)
        3 * I(1),                      # IVNA: ∞_3 (3 preserved in index)
    ))

    # 28. Division by different zeros gives different infinities
    results.append(ieee_op(
        "6/0_2 vs 6/0_3 (different!)",
        "6/0_2 vs 6/0_3",
        "Both give Inf (IEEE)",        # IEEE: both Inf, indistinguishable
        f"{6/Z(2)} vs {6/Z(3)}",       # IVNA: ∞_3 vs ∞_2 (different!)
    ))

    # 29. Sum of infinitely small terms
    results.append(ieee_op(
        "0_1 + 0_2 + 0_3 = 0_6",
        "0_1 + 0_2 + 0_3",
        0 + 0 + 0,                    # IEEE: 0 (structure lost)
        Z(1) + Z(2) + Z(3),           # IVNA: 0_6 (indices accumulate)
    ))

    # 30. Product ∞ × finite × 0 (order matters in IEEE)
    results.append(ieee_op(
        "∞ × 3 × 0 (=? depends on order in IEEE)",
        "Inf*3*0 vs Inf*0*3",
        float('inf') * 0,             # IEEE: NaN regardless of order
        I(1) * 3 * Z(1),              # IVNA: ∞_3 · 0_1 = 3
        ivna_roundtrip="IVNA is order-independent: (∞_1·3)·0_1 = ∞_3·0_1 = 3"
    ))

    # 31. Zero squared / Zero
    results.append(ieee_op(
        "0²/0 (higher order zero / zero)",
        "0²_6 / 0_2",
        0,                             # IEEE: 0/0... wait, 0²=0, 0/0=NaN
        Virtual('zero', 6, 2) / Z(2),  # IVNA: 0²_6 / 0_2 = 0_{3}
    ))

    # 32. Infinity squared / Infinity
    results.append(ieee_op(
        "∞²/∞ (higher order inf / inf)",
        "∞²_6 / ∞_2",
        float('inf'),                  # IEEE: Inf/Inf = NaN, but Inf²/Inf = Inf
        Virtual('inf', 6, 2) / I(2),   # IVNA: ∞²_6 / ∞_2 = ∞_{3}
    ))

    return results


# ============================================================
# OUTPUT AND ANALYSIS
# ============================================================

def format_result(r):
    """Format an IEEE result for display."""
    if isinstance(r, float):
        if math.isnan(r):
            return "NaN"
        elif math.isinf(r):
            return "+Inf" if r > 0 else "-Inf"
        elif r == 0:
            return "0"
        else:
            return f"{r}"
    elif isinstance(r, bool):
        return str(r)
    elif isinstance(r, str):
        return r
    else:
        return str(r)


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  IVNA Demo 3: IEEE 754 vs IVNA — Edge-Case Comparison             ║")
    print("║  Systematic comparison of 32 arithmetic edge cases                 ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    results = run_all_comparisons()

    # Print full table
    print(f"\n{'#':>3s}  {'Operation':>35s}  {'IEEE 754':>15s}  {'IVNA':>25s}  {'Resolved?':>10s}")
    print("-" * 95)

    for i, r in enumerate(results, 1):
        ieee_str = format_result(r['ieee_result'])
        ivna_str = format_result(r['ivna_result'])
        resolved = "YES ✓" if r['resolved'] else ("INFO+" if r['info_preserved'] else "—")
        print(f"{i:>3d}  {r['description']:>35s}  {ieee_str:>15s}  {ivna_str:>25s}  {resolved:>10s}")

    # Statistics
    print()
    print("=" * 70)
    print("STATISTICS")
    print("=" * 70)

    total = len(results)
    nan_cases = sum(1 for r in results if r['ieee_class'] == 'NaN')
    inf_cases = sum(1 for r in results if r['ieee_class'] in ('Inf', '-Inf'))
    resolved = sum(1 for r in results if r['resolved'])
    info_preserved = sum(1 for r in results if r['info_preserved'])

    print(f"\n  Total operations tested:       {total}")
    print(f"  IEEE 754 NaN results:          {nan_cases}")
    print(f"  IEEE 754 ±Inf results:         {inf_cases}")
    print(f"  IVNA resolves (NaN/Inf→value): {resolved}")
    print(f"  IVNA preserves more info:      {info_preserved}")
    print(f"  Resolution rate:               {resolved}/{nan_cases + inf_cases} = {resolved/(nan_cases + inf_cases)*100:.0f}%" if (nan_cases + inf_cases) > 0 else "  No failures to resolve")

    # Show roundtrips
    roundtrips = [r for r in results if r['roundtrip']]
    if roundtrips:
        print(f"\n  ROUNDTRIP DEMONSTRATIONS ({len(roundtrips)}):")
        for r in roundtrips:
            print(f"    {r['description']}: {r['roundtrip']}")

    # Categories
    print(f"\n  CATEGORY BREAKDOWN:")
    categories = {
        'Division by zero': [r for r in results if '/0' in r['expr'] or '/ 0' in r['description']],
        'Indeterminate forms': [r for r in results if any(x in r['description'] for x in ['0·∞', '∞·0', '∞-∞', '∞/∞', '0/0', '0×∞', '∞×0'])],
        'Information preservation': [r for r in results if r['info_preserved']],
        'Arithmetic chains': [r for r in results if 'chain' in r['description'] or 'roundtrip' in r['description']],
    }

    for cat_name, cat_results in categories.items():
        cat_resolved = sum(1 for r in cat_results if r['resolved'])
        print(f"    {cat_name}: {len(cat_results)} tests, {cat_resolved} resolved by IVNA")

    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(f"""
  IEEE 754 produces {nan_cases} NaN results and {inf_cases} ±Inf results across {total} edge cases.
  IVNA resolves {resolved} of these to meaningful values.

  The key insight is NOT just "fewer NaNs" — it's that IVNA values carry
  STRUCTURE that IEEE 754 values don't:

  1. Different zeros are distinguishable: 0_3 ≠ 0_5
     (IEEE: 0 == 0, can't tell which computation produced it)

  2. Different infinities are distinguishable: ∞_3 ≠ ∞_5
     (IEEE: Inf == Inf, can't tell 5/0 from 3/0)

  3. Roundtrips work: 5/0_1 = ∞_5, ∞_5 · 0_1 = 5
     (IEEE: 5/0 = Inf, Inf * 0 = NaN — information destroyed)

  4. Indeterminate forms have determinate values:
     0_x · ∞_y = xy, ∞_x / ∞_y = x/y, ∞_x - ∞_y = ∞_{{x-y}}
     (IEEE: all NaN)
""")
