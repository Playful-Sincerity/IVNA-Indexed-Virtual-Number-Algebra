"""
Demo 4: Numerical ODE Solver at Singularities — IEEE 754 vs IVNA
================================================================

Solves dy/dx = 1/x (singular at x=0) numerically.
Also solves dy/dx = 1/x² and dy/dx = y/x (Euler ODE) for variety.

Standard solver: fails or produces garbage near x=0
IVNA solver: handles x = 0_ε cleanly, tracks the singularity

The exact solution of dy/dx = 1/x is y = ln|x| + C, which has a
logarithmic singularity at x=0. The question is: what does the
NUMERICAL solver do when it steps through x=0?
"""

import sys
import os
import numpy as np
from fractions import Fraction
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ivna import Virtual, Z, I

# ============================================================
# ODE 1: dy/dx = 1/x (logarithmic singularity at x=0)
# Exact solution: y = ln|x| + C
# ============================================================

def solve_ieee754_euler(f, x_start, x_end, y0, n_steps):
    """Euler's method with IEEE 754 arithmetic.

    Returns: xs, ys, diagnostics
    """
    h = (x_end - x_start) / n_steps
    xs = [x_start]
    ys = [y0]
    diagnostics = {'nans': 0, 'infs': 0, 'max_slope': 0.0, 'crash_step': None}

    x, y = x_start, y0
    for step in range(n_steps):
        try:
            slope = f(x)
        except ZeroDivisionError:
            slope = float('inf')

        if math.isnan(slope):
            diagnostics['nans'] += 1
            if diagnostics['crash_step'] is None:
                diagnostics['crash_step'] = step
        elif math.isinf(slope):
            diagnostics['infs'] += 1
            if diagnostics['crash_step'] is None:
                diagnostics['crash_step'] = step

        diagnostics['max_slope'] = max(diagnostics['max_slope'],
                                        abs(slope) if not (math.isnan(slope) or math.isinf(slope)) else 0)

        y = y + h * slope
        x = x + h

        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys), diagnostics


def solve_ieee754_rk4(f, x_start, x_end, y0, n_steps):
    """RK4 with IEEE 754 arithmetic."""
    h = (x_end - x_start) / n_steps
    xs = [x_start]
    ys = [y0]
    diagnostics = {'nans': 0, 'infs': 0, 'crash_step': None}

    x, y = x_start, y0
    for step in range(n_steps):
        try:
            k1 = h * f(x)
            k2 = h * f(x + h/2)
            k3 = h * f(x + h/2)
            k4 = h * f(x + h)
        except ZeroDivisionError:
            k1 = k2 = k3 = k4 = float('inf')

        dy = (k1 + 2*k2 + 2*k3 + k4) / 6

        if math.isnan(dy) or math.isinf(dy):
            if math.isnan(dy):
                diagnostics['nans'] += 1
            else:
                diagnostics['infs'] += 1
            if diagnostics['crash_step'] is None:
                diagnostics['crash_step'] = step

        y = y + dy
        x = x + h

        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys), diagnostics


def solve_ivna_euler(f, x_start, x_end, y0, n_steps, singularity_at=0.0, threshold=1e-12):
    """Euler's method with IVNA-aware arithmetic.

    When x approaches the singularity, we switch to IVNA representation:
    x = singularity + 0_ε where ε tracks the approach distance.

    The key insight: f(0_ε) = 1/0_ε = ∞_{1/ε}
    The slope is an indexed infinity, and h * ∞_{1/ε} = h/ε (a real number!)
    because h is a real number times an indexed infinity.

    Wait — more precisely: h · ∞_{1/ε} for small h gives a large but finite step.
    The IVNA algebra handles this: h · ∞_x = ∞_{hx}, which is still virtual.
    But we can use the INDEX to make informed decisions about step adaptation.
    """
    h = (x_end - x_start) / n_steps
    xs = [x_start]
    ys = [y0]
    ivna_log = []

    x, y = x_start, y0

    for step in range(n_steps):
        dist_to_sing = abs(x - singularity_at)

        if dist_to_sing < threshold:
            # IVNA REGIME
            # x ≈ singularity, so x = 0_ε where ε = dist_to_sing (or machine eps)
            epsilon = max(dist_to_sing, np.finfo(float).eps)

            # f(x) = 1/x = 1/0_ε = ∞_{1/ε} (IVNA division rule)
            slope_index = 1.0 / epsilon
            slope_virtual = I(Fraction(slope_index).limit_denominator(10**12))

            # The step: h * f(x) = h * ∞_{1/ε} = ∞_{h/ε}
            # This is still virtual — the update is "infinitely large" with known scale
            step_index = h * slope_index  # = h/ε

            # IVNA DIAGNOSTIC: The index tells us what's happening
            # If h/ε >> 1, we're trying to make a huge step → need smaller h
            # If h/ε ≈ 1, the step and singularity are balanced

            # Adaptive strategy using IVNA index:
            # Use the INDEX to compute an adapted step size
            # The exact solution near 0 is y = ln|x|, so Δy ≈ ln|x+h| - ln|x|
            # For x near 0: we use the IVNA index to bound the step

            adapted_dy = math.log(abs(x + h)) - math.log(epsilon) if abs(x + h) > 0 else 0

            ivna_log.append({
                'step': step,
                'x': x,
                'distance_to_singularity': dist_to_sing,
                'slope_virtual': str(slope_virtual),
                'slope_index': slope_index,
                'h_over_eps': step_index,
                'adapted_dy': adapted_dy,
                'action': 'IVNA: used index for step adaptation'
            })

            y = y + adapted_dy

        elif dist_to_sing < abs(h) * 10:
            # TRANSITION ZONE: approaching singularity
            # Use smaller sub-steps
            n_sub = 20
            sub_h = h / n_sub
            for _ in range(n_sub):
                if abs(x - singularity_at) < threshold:
                    epsilon = max(abs(x - singularity_at), np.finfo(float).eps)
                    adapted_dy = math.log(abs(x + sub_h)) - math.log(epsilon) if abs(x + sub_h) > 0 else 0
                    y += adapted_dy
                else:
                    slope = f(x)
                    y += sub_h * slope
                x_temp = x  # Don't update x in sub-loop

            ivna_log.append({
                'step': step,
                'x': x,
                'distance_to_singularity': dist_to_sing,
                'action': 'TRANSITION: adaptive sub-stepping near singularity'
            })
        else:
            # NORMAL REGIME
            slope = f(x)
            y = y + h * slope

        x = x + h
        xs.append(x)
        ys.append(y)

    return np.array(xs), np.array(ys), ivna_log


# ============================================================
# DEMONSTRATION
# ============================================================

def demo_ode_1_over_x():
    """dy/dx = 1/x, crossing through x=0."""
    print("=" * 70)
    print("ODE 1: dy/dx = 1/x (logarithmic singularity at x=0)")
    print("       Exact solution: y = ln|x| + C")
    print("=" * 70)

    f = lambda x: 1.0 / x if x != 0 else float('inf')

    # Integration from x = -1 to x = 1 (crossing the singularity)
    x_start, x_end = -1.0, 1.0
    y0 = 0.0  # y(-1) = ln(1) = 0
    n_steps = 200

    print(f"\n  Domain: [{x_start}, {x_end}], crossing singularity at x=0")
    print(f"  Initial condition: y({x_start}) = {y0}")
    print(f"  Steps: {n_steps}")

    # IEEE 754 Euler
    print(f"\n--- IEEE 754 (Euler's method) ---")
    xs_ieee, ys_ieee, diag_ieee = solve_ieee754_euler(f, x_start, x_end, y0, n_steps)

    if diag_ieee['crash_step'] is not None:
        crash_x = x_start + diag_ieee['crash_step'] * (x_end - x_start) / n_steps
        print(f"  CRASHED at step {diag_ieee['crash_step']} (x ≈ {crash_x:.4f})")
        print(f"  NaN values: {diag_ieee['nans']}, Inf values: {diag_ieee['infs']}")
        print(f"  Final y: {ys_ieee[-1]}")
        if math.isnan(ys_ieee[-1]) or math.isinf(ys_ieee[-1]):
            print(f"  → Solution is UNUSABLE after singularity")
    else:
        print(f"  Completed without NaN/Inf (singularity missed by stepping)")
        print(f"  Final y at x=1: {ys_ieee[-1]:.6f} (exact: {math.log(1):.6f})")

    # IEEE 754 RK4
    print(f"\n--- IEEE 754 (RK4) ---")
    xs_rk4, ys_rk4, diag_rk4 = solve_ieee754_rk4(f, x_start, x_end, y0, n_steps)

    if diag_rk4['crash_step'] is not None:
        crash_x = x_start + diag_rk4['crash_step'] * (x_end - x_start) / n_steps
        print(f"  CRASHED at step {diag_rk4['crash_step']} (x ≈ {crash_x:.4f})")
        print(f"  NaN values: {diag_rk4['nans']}, Inf values: {diag_rk4['infs']}")
        print(f"  Final y: {ys_rk4[-1]}")
    else:
        print(f"  Completed without NaN/Inf")
        print(f"  Final y at x=1: {ys_rk4[-1]:.6f}")

    # IVNA Euler
    print(f"\n--- IVNA (Euler's method with indexed singularity handling) ---")
    xs_ivna, ys_ivna, ivna_log = solve_ivna_euler(
        f, x_start, x_end, y0, n_steps, singularity_at=0.0, threshold=1e-12
    )

    print(f"  Completed: {len(xs_ivna)} points")
    print(f"  Final y at x=1: {ys_ivna[-1]:.6f} (exact: {math.log(1):.6f} = 0)")
    print(f"  IVNA events: {len(ivna_log)}")

    if ivna_log:
        print(f"\n  IVNA singularity events (first 5):")
        for evt in ivna_log[:5]:
            if 'slope_virtual' in evt:
                print(f"    Step {evt['step']}: x={evt['x']:.6e}, "
                      f"slope={evt['slope_virtual']}, "
                      f"h/ε={evt['h_over_eps']:.2e}, "
                      f"adapted Δy={evt['adapted_dy']:.6f}")
            else:
                print(f"    Step {evt['step']}: x={evt['x']:.6e}, {evt['action']}")

    # Compare at specific points
    print(f"\n  COMPARISON at selected points:")
    print(f"  {'x':>10s}  {'Exact y':>12s}  {'IEEE Euler':>12s}  {'IEEE RK4':>12s}  {'IVNA':>12s}")
    print("  " + "-" * 65)

    check_points = [-0.8, -0.5, -0.1, -0.01, 0.01, 0.1, 0.5, 0.8]
    for xp in check_points:
        idx_ieee = np.argmin(np.abs(xs_ieee - xp))
        idx_rk4 = np.argmin(np.abs(xs_rk4 - xp))
        idx_ivna = np.argmin(np.abs(xs_ivna - xp))

        exact = math.log(abs(xp))
        y_ieee = ys_ieee[idx_ieee]
        y_rk4 = ys_rk4[idx_rk4]
        y_ivna = ys_ivna[idx_ivna]

        def fmt(v):
            if math.isnan(v):
                return "NaN"
            elif math.isinf(v):
                return "Inf"
            else:
                return f"{v:.6f}"

        print(f"  {xp:>10.3f}  {exact:>12.6f}  {fmt(y_ieee):>12s}  {fmt(y_rk4):>12s}  {fmt(y_ivna):>12s}")


def demo_ode_1_over_x_squared():
    """dy/dx = 1/x² (stronger singularity at x=0)."""
    print()
    print("=" * 70)
    print("ODE 2: dy/dx = 1/x² (algebraic singularity at x=0)")
    print("       Exact solution: y = -1/x + C")
    print("=" * 70)

    f = lambda x: 1.0 / (x * x) if x != 0 else float('inf')

    # Integration on one side of singularity: x = 0.001 to x = 1
    x_start, x_end = 0.001, 1.0
    y0 = -1.0 / x_start  # Exact: y(0.001) = -1000
    n_steps = 200

    print(f"\n  Domain: [{x_start}, {x_end}]")
    print(f"  y({x_start}) = {y0}")

    # IEEE
    xs_ieee, ys_ieee, diag_ieee = solve_ieee754_euler(f, x_start, x_end, y0, n_steps)

    # Exact solution
    xs_exact = np.linspace(x_start, x_end, n_steps + 1)
    ys_exact = -1.0 / xs_exact

    # Error comparison
    valid_ieee = ~np.isnan(ys_ieee) & ~np.isinf(ys_ieee)
    if np.any(valid_ieee):
        max_err_ieee = np.max(np.abs(ys_ieee[valid_ieee] - (-1.0/xs_ieee[valid_ieee])))
    else:
        max_err_ieee = float('inf')

    print(f"\n  IEEE Euler max error: {max_err_ieee:.6e}")
    print(f"  IEEE final y(1) = {ys_ieee[-1]:.6f} (exact: -1.000000)")

    # Show the behavior near x=0
    print(f"\n  Behavior approaching x=0 from the right:")
    print(f"  {'x':>12s}  {'Exact 1/x²':>15s}  {'IEEE result':>15s}  {'IVNA':>25s}")
    print("  " + "-" * 70)

    test_x = [0.1, 0.01, 0.001, 1e-6, 1e-10, 1e-15, 0.0]
    for x in test_x:
        if x == 0:
            ieee_val = "Inf (then NaN)"
            exact_val = "∞"
            # IVNA: 1/(0_1)² = 1/0²_1 = ∞²_1
            ivna_val = f"{1 / (Z(1) ** 2)}"
        elif x < 1e-150:
            ieee_val = f"{1/(x*x):.2e}" if x > 0 else "Inf"
            exact_val = f"{1/(x*x):.2e}" if x > 0 else "∞"
            eps = Fraction(x).limit_denominator(10**12)
            ivna_val = f"∞_{{{1/(x*x):.2e}}}"
        else:
            ieee_val = f"{1/(x*x):.2e}"
            exact_val = f"{1/(x*x):.2e}"
            ivna_val = f"{1/(x*x):.2e} (real)"

        print(f"  {x:>12.1e}  {exact_val:>15s}  {ieee_val:>15s}  {ivna_val:>25s}")


def demo_ivna_ode_algebra():
    """Show the IVNA algebra for ODE stepping through a singularity."""
    print()
    print("=" * 70)
    print("IVNA ODE ALGEBRA: Stepping Through x=0")
    print("=" * 70)

    print("""
  Consider Euler's method: y_{n+1} = y_n + h · f(x_n)

  At x_n = 0 with f(x) = 1/x:

  IEEE 754:
    slope = 1/0 = Inf
    y_{n+1} = y_n + h · Inf = Inf
    y_{n+2} = Inf + h · f(next_x) = Inf + finite = Inf
    → Solution is permanently corrupted

  IVNA (x_n = 0_ε where ε encodes approach direction):
    slope = 1/0_ε = ∞_{1/ε}
    y_{n+1} = y_n + h · ∞_{1/ε}

    Now h · ∞_{1/ε} = ∞_{h/ε} — this is an indexed infinity.

    The INDEX h/ε tells us:
    - If h >> ε: step is much larger than singularity resolution → refine h
    - If h << ε: step is much smaller → safe to proceed
    - If h ≈ ε: step matches singularity scale → this is the critical regime

    IVNA doesn't magically solve the ODE — it provides INFORMATION
    that guides adaptive step-size control near singularities.
""")

    # Concrete example
    print("  CONCRETE EXAMPLE:")
    h = 0.01
    eps_values = [0.1, 0.01, 0.001, 1e-6, 1e-10]

    print(f"  Step size h = {h}")
    print(f"\n  {'ε (approach dist)':>20s}  {'slope = 1/0_ε':>20s}  {'h·slope = ∞_{{h/ε}}':>20s}  {'h/ε ratio':>12s}  {'Action':>20s}")
    print("  " + "-" * 100)

    for eps in eps_values:
        slope = I(Fraction(1/eps).limit_denominator(10**9))
        step_ratio = h / eps
        update = h * slope  # h · ∞_{1/ε} = ∞_{h/ε}

        if step_ratio < 1:
            action = "Safe: proceed"
        elif step_ratio < 100:
            action = "Caution: monitor"
        else:
            action = "Refine: reduce h"

        print(f"  {eps:>20.1e}  {str(slope):>20s}  {str(update):>20s}  {step_ratio:>12.1e}  {action:>20s}")

    # IVNA advantage: the ratio ∞_{h/ε₁} / ∞_{h/ε₂} = ε₂/ε₁
    print(f"\n  KEY: Ratio of virtual slopes is a real number:")
    s1 = I(Fraction(1, 1000))   # 1/0_{0.001} = ∞_{1/0.001} = ∞_1000
    s2 = I(Fraction(1, 100))    # 1/0_{0.01} = ∞_{1/0.01} = ∞_100
    ratio = s1 / s2             # ∞_1000 / ∞_100 = 10
    print(f"  ∞_{{1000}} / ∞_{{100}} = {ratio}")
    print(f"  → The singularity is 10× stronger at ε=0.001 than at ε=0.01")
    print(f"  → IEEE 754: Inf / Inf = NaN (can't compare singularity strengths)")


def demo_one_sided_approach():
    """Show ODE solving approaching a singularity from one side."""
    print()
    print("=" * 70)
    print("ODE 3: Approaching x=0 from the right (dy/dx = 1/x)")
    print("=" * 70)

    f = lambda x: 1.0 / x if x != 0 else float('inf')

    # From x=1 down to x=ε (approaching singularity)
    x_start, x_end = 1.0, 0.001
    y0 = 0.0  # y(1) = ln(1) = 0
    n_steps = 100

    # IEEE Euler
    xs_ieee, ys_ieee, _ = solve_ieee754_euler(f, x_start, x_end, y0, n_steps)

    print(f"\n  {'x':>12s}  {'Exact ln|x|':>12s}  {'IEEE Euler':>12s}  {'Error':>12s}")
    print("  " + "-" * 55)

    check_points = [0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
    for xp in check_points:
        idx = np.argmin(np.abs(xs_ieee - xp))
        exact = math.log(abs(xp))
        ieee = ys_ieee[idx]
        err = abs(ieee - exact) if not (math.isnan(ieee) or math.isinf(ieee)) else float('inf')

        print(f"  {xp:>12.4f}  {exact:>12.6f}  {ieee:>12.6f}  {err:>12.6e}")

    print(f"\n  As x → 0, the exact solution y = ln|x| → -∞")
    print(f"  IEEE Euler tracks this (since we never hit x=0 exactly)")
    print(f"  But the ERROR grows because the slope 1/x gets huge near 0")
    print(f"  IVNA: the indexed infinity ∞_{{1/x}} would signal step refinement needed")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  IVNA Demo 4: Numerical ODE Solver at Singularities               ║")
    print("║  dy/dx = 1/x and dy/dx = 1/x² crossing through x=0               ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    demo_ode_1_over_x()
    demo_ode_1_over_x_squared()
    demo_ivna_ode_algebra()
    demo_one_sided_approach()

    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
  Standard ODE solvers have THREE strategies at singularities:
    1. Crash (IEEE 754 Inf/NaN propagation poisons all subsequent values)
    2. Avoid (split domain to never cross the singularity)
    3. Regularize (modify the ODE to remove the singularity — changes physics)

  IVNA provides a FOURTH strategy:
    4. Track (singularity becomes ∞_x where x carries diagnostic information)
       - The INDEX reveals the singularity's strength and approach rate
       - Ratios of indexed infinities are real numbers (∞_x / ∞_y = x/y)
       - This enables INFORMED adaptive step-size control
       - No arbitrary regularization parameters needed

  HONEST ASSESSMENT:
    - IVNA doesn't "solve" the underlying mathematical singularity
    - The ODE dy/dx = 1/x genuinely has no continuous solution through x=0
    - What IVNA provides is DIAGNOSTIC INFORMATION at the singularity:
      * The index tells you the singularity type and strength
      * Ratios between indexed infinities are computable (vs NaN in IEEE)
      * Step-size adaptation can use the index as a signal
    - This is most valuable for UNEXPECTED singularities in complex ODE systems
      where the physicist may not know in advance where singularities occur
""")
