"""
VEX Calculator — Virtual EXtended Arithmetic
=============================================

A calculator that uses IVNA (Indexed Virtual Number Algebra) instead of
raising division-by-zero errors. Where a standard calculator says "ERROR,"
VEX produces indexed virtual numbers that you can keep computing with.

Standard:  5 / 0  →  ERROR
VEX:       5 / 0  →  ∞_5  (and you can keep going)

This is the tangible demonstration of IVNA's core insight: zeros and
infinities carry information (their index), and preserving that information
eliminates most "undefined" and "indeterminate" results.
"""

import sys
import os
from fractions import Fraction
from typing import Union

# Import the IVNA core classes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ivna import Virtual, Z, I


# ============================================================
# VexCalc — The Calculator
# ============================================================

class VexCalc:
    """A calculator that uses IVNA instead of raising division-by-zero errors.

    Standard mode: 5 / 0  → ERROR
    VEX mode:      5 / 0  → ∞_5 (and you can keep computing with it)

    Usage:
        calc = VexCalc()
        result = calc.div(5, 0)        # → ∞_5
        result = calc.mul(result, Z(1)) # → 5 (roundtrip!)
        calc.collapse(result)           # → ∞ (strip indices)
    """

    def __init__(self):
        self.history = []

    # --- Core operations ---

    def add(self, a, b):
        """Addition with full IVNA support."""
        a, b = self._coerce(a), self._coerce(b)
        result = self._perform(a, '+', b)
        self._record(a, '+', b, result)
        return result

    def sub(self, a, b):
        """Subtraction with full IVNA support."""
        a, b = self._coerce(a), self._coerce(b)
        result = self._perform(a, '-', b)
        self._record(a, '-', b, result)
        return result

    def mul(self, a, b):
        """Multiplication with full IVNA support."""
        a, b = self._coerce(a), self._coerce(b)
        result = self._perform(a, '×', b)
        self._record(a, '×', b, result)
        return result

    def div(self, a, b):
        """Division — the key operation. Division by zero produces indexed infinities."""
        a, b = self._coerce(a), self._coerce(b)
        result = self._perform(a, '÷', b)
        self._record(a, '÷', b, result)
        return result

    def collapse(self, value):
        """The =; operator. Strips virtual indices, returns standard value.

        ∞_5 =; ∞
        0_3 =; 0
        7   =; 7
        """
        if isinstance(value, Virtual):
            return value.collapse()
        elif isinstance(value, tuple):
            # Coexistence expression like (∞_5, '+', 3)
            # Collapse each part
            parts = []
            for item in value:
                if isinstance(item, Virtual):
                    parts.append(item.collapse())
                elif isinstance(item, str):
                    parts.append(item)
                else:
                    parts.append(item)
            # Now evaluate the collapsed expression
            return self._eval_collapsed(parts)
        return value

    # --- Display ---

    def display(self, value):
        """Format a value for clean display."""
        if isinstance(value, Virtual):
            return self._format_virtual(value)
        elif isinstance(value, tuple):
            return self._format_coexistence(value)
        elif isinstance(value, Fraction):
            if value.denominator == 1:
                return str(value.numerator)
            return str(float(value))
        elif isinstance(value, float):
            if value == float('inf'):
                return '∞'
            elif value == float('-inf'):
                return '-∞'
            elif value != value:  # NaN
                return 'NaN'
            return str(value)
        return str(value)

    def _format_virtual(self, v):
        """Format a Virtual number for display."""
        sign = ''
        index = v.index
        if index < 0:
            sign = '-'
            index = -index
        order_str = f"^{v.order}" if v.order != 1 else ""
        # Clean up index display
        if isinstance(index, Fraction):
            if index.denominator == 1:
                idx_str = str(index.numerator)
            else:
                idx_str = str(float(index))
        else:
            idx_str = str(index)
        if v.kind == 'zero':
            return f"{sign}0{order_str}_{idx_str}"
        else:
            return f"{sign}∞{order_str}_{idx_str}"

    def _format_coexistence(self, expr):
        """Format a coexistence tuple like (∞_5, '+', 3)."""
        parts = []
        for item in expr:
            if isinstance(item, Virtual):
                parts.append(self._format_virtual(item))
            elif isinstance(item, str):
                parts.append(f" {item} ")
            elif isinstance(item, Fraction):
                if item.denominator == 1:
                    parts.append(str(item.numerator))
                else:
                    parts.append(str(float(item)))
            else:
                parts.append(str(item))
        return ''.join(parts)

    # --- Internal machinery ---

    def _coerce(self, value):
        """Convert inputs to appropriate types.

        - Plain numbers stay as numbers (int, float, Fraction)
        - Virtual objects pass through
        - Zero (as int/float) is treated as the real number 0, NOT as 0_1
          (To use indexed zeros, explicitly pass Z(x))
        """
        if isinstance(value, Virtual):
            return value
        elif isinstance(value, (int, float)):
            return value
        elif isinstance(value, Fraction):
            return value
        return value

    def _perform(self, a, op, b):
        """Perform an operation, handling all IVNA cases."""
        if op == '+':
            return self._add(a, b)
        elif op == '-':
            return self._sub(a, b)
        elif op == '×':
            return self._mul(a, b)
        elif op == '÷':
            return self._div(a, b)

    def _add(self, a, b):
        """Addition logic."""
        if isinstance(a, Virtual) and isinstance(b, Virtual):
            return a + b
        elif isinstance(a, Virtual):
            return a + b
        elif isinstance(b, Virtual):
            return b + a
        else:
            return a + b

    def _sub(self, a, b):
        """Subtraction logic."""
        if isinstance(a, Virtual) and isinstance(b, Virtual):
            return a - b
        elif isinstance(a, Virtual):
            return a - b
        elif isinstance(b, Virtual):
            return a - b
        else:
            return a - b

    def _mul(self, a, b):
        """Multiplication logic."""
        if isinstance(a, Virtual) and isinstance(b, Virtual):
            return a * b
        elif isinstance(a, Virtual):
            return a * b
        elif isinstance(b, Virtual):
            return b * a
        else:
            return a * b

    def _div(self, a, b):
        """Division logic — the heart of VEX.

        When b is 0 (plain zero), we need to convert it to an indexed zero.
        Convention: plain 0 → 0_1 (the "standard" zero with index 1).
        This gives:  5 / 0 = 5 / 0_1 = ∞_{5/1} = ∞_5
        """
        if isinstance(a, Virtual) and isinstance(b, Virtual):
            return a / b
        elif isinstance(a, Virtual):
            if b == 0:
                # Virtual / plain zero: treat 0 as 0_1
                return a / Z(1)
            return a / b
        elif isinstance(b, Virtual):
            return a / b
        else:
            # Both are plain numbers
            if b == 0:
                if a == 0:
                    # 0 / 0 → 0_1 / 0_1 = 1 (both zeros get index 1)
                    return Z(1) / Z(1)
                # a / 0 → a / 0_1 = ∞_{a/1} = ∞_a
                return a / Z(1)
            return Fraction(a, b) if isinstance(a, int) and isinstance(b, int) else a / b

    def _eval_collapsed(self, parts):
        """Evaluate a collapsed coexistence expression."""
        if len(parts) == 3:
            left, op, right = parts
            if op == '+':
                if left == float('inf') or right == float('inf'):
                    return float('inf')
                if left == float('-inf') or right == float('-inf'):
                    return float('-inf')
                return left + right
            elif op == '-':
                if left == float('inf') and right == float('inf'):
                    return float('nan')  # ∞ - ∞ is indeterminate in standard math
                return left - right
        return parts

    def _record(self, a, op, b, result):
        """Record operation in history."""
        self.history.append({
            'a': a, 'op': op, 'b': b, 'result': result
        })


# ============================================================
# IEEE 754 comparison helper
# ============================================================

def ieee754_result(a, b, op):
    """Get the IEEE 754 floating-point result of an operation."""
    try:
        a, b = float(a), float(b)
        if op == '/':
            if b == 0.0:
                if a == 0.0:
                    return 'NaN'
                elif a > 0:
                    return '+Inf'
                else:
                    return '-Inf'
            result = a / b
        elif op == '*':
            result = a * b
        elif op == '-':
            result = a - b
        elif op == '+':
            result = a + b
        else:
            return 'ERROR'
        # Normalize the display
        if result != result:  # NaN
            return 'NaN'
        elif result == float('inf'):
            return '+Inf'
        elif result == float('-inf'):
            return '-Inf'
        return str(result)
    except Exception:
        return 'ERROR'


# ============================================================
# DEMONSTRATION
# ============================================================

if __name__ == '__main__':

    calc = VexCalc()

    print("=" * 68)
    print("  VEX Calculator — Virtual EXtended Arithmetic")
    print("  Powered by IVNA (Indexed Virtual Number Algebra)")
    print("=" * 68)
    print()
    print("  What if dividing by zero didn't break your calculator?")
    print("  What if 5 / 0 gave you a usable answer instead of ERROR?")
    print()
    print("  IVNA attaches indices to zeros and infinities, tracking the")
    print("  information that standard math throws away. The result:")
    print("  a calculator that never crashes on division by zero.")
    print()

    # ----------------------------------------------------------
    # Demo 1: The Basic Pitch
    # ----------------------------------------------------------
    print("-" * 68)
    print("  1. THE BASIC PITCH: Division by zero, solved")
    print("-" * 68)
    print()

    result = calc.div(5, 0)
    print(f"  Standard calculator:   5 / 0 = ERROR")
    print(f"  VEX calculator:        5 / 0 = {calc.display(result)}")
    print()
    print(f"  The ∞_5 means: \"infinity that remembers it came from 5.\"")
    print(f"  The subscript 5 is the index — it tracks the numerator.")
    print()

    result2 = calc.div(-3, 0)
    print(f"  Standard calculator:  -3 / 0 = ERROR")
    print(f"  VEX calculator:       -3 / 0 = {calc.display(result2)}")
    print()
    print(f"  Different numerator, different index. The infinity knows its origin.")
    print()

    # ----------------------------------------------------------
    # Demo 2: Roundtrip — Information Preserved
    # ----------------------------------------------------------
    print("-" * 68)
    print("  2. ROUNDTRIP: Multiply back by zero and recover the original")
    print("-" * 68)
    print()

    step1 = calc.div(5, 0)
    print(f"  Step 1:  5 / 0     = {calc.display(step1)}")

    step2 = calc.mul(step1, Z(1))
    print(f"  Step 2:  ∞_5 × 0_1 = {calc.display(step2)}")
    print()
    print(f"  The original value 5 is recovered! Standard math loses this")
    print(f"  information — IEEE 754 says Inf * 0 = NaN. IVNA says ∞_5 × 0_1 = 5.")
    print()

    # ----------------------------------------------------------
    # Demo 3: Chained Virtual Arithmetic
    # ----------------------------------------------------------
    print("-" * 68)
    print("  3. CHAINED OPERATIONS: Virtual numbers obey algebra")
    print("-" * 68)
    print()

    a = calc.div(10, 0)
    b = calc.div(6, 0)
    print(f"  10 / 0 = {calc.display(a)}")
    print(f"   6 / 0 = {calc.display(b)}")

    c = calc.add(a, b)
    print(f"  ∞_10 + ∞_6 = {calc.display(c)}")
    print()
    print(f"  Virtual infinities add by combining indices: ∞_x + ∞_y = ∞_(x+y)")
    print()

    d = calc.mul(a, b)
    print(f"  ∞_10 × ∞_6 = {calc.display(d)}")
    print()
    print(f"  Multiplying infinities: ∞_x × ∞_y = ∞²_(x×y).")
    print(f"  The superscript ² means \"second-order infinity\" — a higher tier.")
    print()

    # ----------------------------------------------------------
    # Demo 4: L'Hôpital Elimination — 0/0 Resolved
    # ----------------------------------------------------------
    print("-" * 68)
    print("  4. INDETERMINATE FORMS RESOLVED: 0/0 gives a real answer")
    print("-" * 68)
    print()

    z1 = Z(6)
    z2 = Z(3)
    result_0over0 = calc.div(z1, z2)
    print(f"  Standard math:  0 / 0  = INDETERMINATE")
    print(f"  VEX calculator: 0_6 / 0_3 = {calc.display(result_0over0)}")
    print()
    print(f"  When both zeros carry indices, 0_x / 0_y = x/y.")
    print(f"  The \"indeterminate\" form 0/0 is only indeterminate because")
    print(f"  standard math stripped the indices. IVNA keeps them.")
    print()

    # Also show ∞/∞
    i1 = I(10)
    i2 = I(5)
    result_infoverinf = calc.div(i1, i2)
    print(f"  Standard math:  ∞ / ∞  = INDETERMINATE")
    print(f"  VEX calculator: ∞_10 / ∞_5 = {calc.display(result_infoverinf)}")
    print()
    print(f"  Same principle: ∞_x / ∞_y = x/y. Indices resolve the ambiguity.")
    print()

    # ----------------------------------------------------------
    # Demo 5: Mixed Arithmetic — Virtual + Real Coexistence
    # ----------------------------------------------------------
    print("-" * 68)
    print("  5. MIXED ARITHMETIC: Virtual and real numbers coexist")
    print("-" * 68)
    print()

    inf5 = I(5)
    mixed = calc.add(inf5, 3)
    print(f"  ∞_5 + 3 = {calc.display(mixed)}")
    print()
    print(f"  When a virtual number and a real number combine in addition,")
    print(f"  they coexist — like how real + imaginary gives a complex number.")
    print(f"  The expression is fully defined, just not reducible further.")
    print()

    # ----------------------------------------------------------
    # Demo 6: The Collapse Operator (=;)
    # ----------------------------------------------------------
    print("-" * 68)
    print("  6. COLLAPSE: Strip indices to get standard values")
    print("-" * 68)
    print()

    inf5 = I(5)
    collapsed_inf = calc.collapse(inf5)
    print(f"  =; ∞_5 = {calc.display(collapsed_inf)}")
    print()

    z3 = Z(3)
    collapsed_z = calc.collapse(z3)
    print(f"  =; 0_3 = {collapsed_z}")
    print()

    print(f"  The =; operator (\"collapse\") strips virtual indices.")
    print(f"  ∞_5 collapses to plain ∞. 0_3 collapses to plain 0.")
    print(f"  It's the bridge back to standard math when you're done computing.")
    print()

    # ----------------------------------------------------------
    # Demo 7: Real-World Example — Computing a Limit
    # ----------------------------------------------------------
    print("-" * 68)
    print("  7. REAL-WORLD: Computing lim(x→0) sin(x)/x via IVNA")
    print("-" * 68)
    print()

    print(f"  In calculus, lim(x→0) sin(x)/x is a famous limit.")
    print(f"  Standard math: direct substitution gives 0/0 — indeterminate.")
    print(f"  You need L'Hôpital's rule or a Taylor series to get 1.")
    print()
    print(f"  With IVNA, we model x→0 as x = 0_1 (an indexed zero).")
    print(f"  For small x, sin(x) ≈ x, so sin(0_1) ≈ 0_1.")
    print(f"  Therefore:")
    print()

    sin_of_zero = Z(1)  # sin(0_1) ≈ 0_1 for the leading term
    x_zero = Z(1)
    limit_result = calc.div(sin_of_zero, x_zero)
    print(f"  sin(0_1) / 0_1 = 0_1 / 0_1 = {calc.display(limit_result)}")
    print()
    print(f"  IVNA gives the answer directly: the limit is 1.")
    print(f"  No L'Hôpital, no epsilon-delta. The indices carry the information.")
    print()

    # More interesting example: lim(x→0) sin(3x)/x
    print(f"  Better yet: lim(x→0) sin(3x)/x")
    print(f"  sin(3 × 0_1) ≈ 3 × 0_1 = 0_3")
    print()
    sin_3x = Z(3)
    limit_3x = calc.div(sin_3x, x_zero)
    print(f"  0_3 / 0_1 = {calc.display(limit_3x)}")
    print()
    print(f"  The index ratio gives you the answer: 3. Correct.")
    print()

    # ============================================================
    # IEEE 754 Comparison
    # ============================================================
    print("=" * 68)
    print("  IEEE 754 vs VEX: How VEX eliminates NaN")
    print("=" * 68)
    print()
    print("  IEEE 754 is the standard for floating-point arithmetic in every")
    print("  computer. It introduced +Inf, -Inf, and NaN. But NaN is a black")
    print("  hole — once you have NaN, it infects every subsequent calculation.")
    print()
    print("  VEX (IVNA) eliminates most NaN cases by preserving index information.")
    print()

    # Build comparison table
    comparisons = [
        ("5 / 0",      "5", "0",     "/",  lambda: calc.div(5, 0)),
        ("-3 / 0",     "-3", "0",    "/",  lambda: calc.div(-3, 0)),
        ("0 / 0",      "0", "0",     "/",  lambda: calc.div(0, 0)),
        ("∞_5 × 0_1",  "inf", "0",   "*",  lambda: calc.mul(I(5), Z(1))),
        ("∞_5 - ∞_3",  "inf", "inf", "-",  lambda: calc.sub(I(5), I(3))),
        ("∞_5 + ∞_3",  "inf", "inf", "+",  lambda: calc.add(I(5), I(3))),
        ("0_6 / 0_3",  "0", "0",     "/",  lambda: calc.div(Z(6), Z(3))),
        ("∞_10 / ∞_5", "inf", "inf", "/",  lambda: calc.div(I(10), I(5))),
    ]

    # Header
    print(f"  {'Expression':<18} {'IEEE 754':<12} {'VEX (IVNA)':<18} {'Verdict'}")
    print(f"  {'─' * 18} {'─' * 12} {'─' * 18} {'─' * 18}")

    nan_count_ieee = 0
    nan_count_vex = 0

    for label, a_str, b_str, op, vex_fn in comparisons:
        ieee = ieee754_result(a_str, b_str, op)
        vex_result = vex_fn()
        vex_str = calc.display(vex_result)

        if ieee == 'NaN':
            nan_count_ieee += 1

        # Check if VEX result is meaningful (not NaN-equivalent)
        vex_is_nan = isinstance(vex_result, float) and vex_result != vex_result

        if vex_is_nan:
            nan_count_vex += 1
            verdict = "both undefined"
        elif ieee == 'NaN':
            verdict = "VEX resolves!"
        elif ieee in ('+Inf', '-Inf'):
            verdict = "VEX adds index"
        else:
            verdict = ""

        print(f"  {label:<18} {ieee:<12} {vex_str:<18} {verdict}")

    print()
    print(f"  IEEE 754 NaN results:  {nan_count_ieee}")
    print(f"  VEX NaN results:       {nan_count_vex}")
    nan_eliminated = nan_count_ieee - nan_count_vex
    if nan_count_ieee > 0:
        pct = (nan_eliminated / nan_count_ieee) * 100
        print(f"  NaN cases eliminated:  {nan_eliminated}/{nan_count_ieee} ({pct:.0f}%)")
    print()

    # ----------------------------------------------------------
    # Summary
    # ----------------------------------------------------------
    print("=" * 68)
    print("  Summary: What VEX (IVNA) Does Differently")
    print("=" * 68)
    print()
    print("  1. DIVISION BY ZERO produces a usable indexed infinity (∞_x)")
    print("     instead of ERROR or bare +Inf.")
    print()
    print("  2. INFORMATION IS PRESERVED. You can multiply back by zero")
    print("     and recover the original number. Try that with IEEE 754.")
    print()
    print("  3. INDETERMINATE FORMS (0/0, ∞/∞, 0×∞, ∞-∞) are resolved")
    print("     by their indices. No more NaN black holes.")
    print()
    print("  4. THE =; OPERATOR bridges back to standard math when needed,")
    print("     stripping indices to get conventional 0, ∞, or real values.")
    print()
    print("  5. BACKWARD COMPATIBLE. Every standard arithmetic result is")
    print("     unchanged. VEX only kicks in where standard math breaks.")
    print()
    print("  IVNA doesn't replace mathematics. It extends it — the same way")
    print("  complex numbers extended the reals to handle √(-1).")
    print()
    print("=" * 68)
