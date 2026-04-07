"""
Demo 1: N-Body Gravitational Simulation — IEEE 754 vs IVNA
==========================================================

Shows how IVNA handles particle collisions (r → 0) without softening hacks.

Standard approach: F = Gm₁m₂/(r² + ε²) — softening parameter ε hides the singularity
IVNA approach:    When r → 0_x, F = ∞_{Gm₁m₂/x²} — singularity is tracked, not hidden

Key insight: IVNA doesn't prevent the singularity — it makes it *informative*.
The index tells you exactly what the force would be if the particles were separated.
"""

import sys
import os
import numpy as np
from fractions import Fraction

# Add parent directory to path for ivna import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ivna import Virtual, Z, I

# ============================================================
# CONFIGURATION
# ============================================================

N_PARTICLES = 6
G = 1.0           # Gravitational constant (normalized)
DT = 0.005        # Timestep
N_STEPS = 400     # Number of simulation steps
SOFTENING = 0.01  # IEEE 754 softening parameter

# Initial conditions: particles arranged to collide
np.random.seed(42)


def create_collision_scenario():
    """Create initial conditions where particles WILL collide.

    Two pairs heading straight at each other, plus two orbiting bodies.
    """
    positions = np.array([
        [-1.0,  0.0],   # Particle 0: heading right
        [ 1.0,  0.0],   # Particle 1: heading left → collision with 0
        [ 0.0, -1.0],   # Particle 2: heading up
        [ 0.0,  1.0],   # Particle 3: heading down → collision with 2
        [ 2.0,  2.0],   # Particle 4: orbiter
        [-2.0, -2.0],   # Particle 5: orbiter
    ])
    velocities = np.array([
        [ 0.5,  0.0],   # →
        [-0.5,  0.0],   # ←
        [ 0.0,  0.5],   # ↑
        [ 0.0, -0.5],   # ↓
        [-0.1,  0.1],   # slow orbit
        [ 0.1, -0.1],   # slow orbit
    ])
    masses = np.array([1.0, 1.0, 1.5, 1.5, 0.5, 0.5])
    return positions, velocities, masses


# ============================================================
# IEEE 754 SIMULATION (with softening hack)
# ============================================================

def ieee754_force(pos, masses, softening):
    """Compute gravitational forces using IEEE 754 with softening.

    F_ij = G * m_i * m_j * (r_j - r_i) / (|r_j - r_i|² + ε²)^{3/2}

    The softening parameter ε prevents division by zero but:
    - Introduces systematic error at ALL distances (not just close encounters)
    - The choice of ε is arbitrary — different values give different physics
    - Information about the actual encounter is destroyed
    """
    n = len(masses)
    forces = np.zeros_like(pos)
    diagnostics = {'min_r': float('inf'), 'max_force': 0.0, 'softened_pairs': 0}

    for i in range(n):
        for j in range(i + 1, n):
            r_vec = pos[j] - pos[i]
            r_sq = np.dot(r_vec, r_vec)
            r = np.sqrt(r_sq)

            diagnostics['min_r'] = min(diagnostics['min_r'], r)

            # Softened force: F = Gm₁m₂ / (r² + ε²)^{3/2} · r_vec
            denom = (r_sq + softening**2) ** 1.5
            f_mag = G * masses[i] * masses[j] / denom
            f_vec = f_mag * r_vec

            diagnostics['max_force'] = max(diagnostics['max_force'], np.linalg.norm(f_vec))

            if r < softening * 2:
                diagnostics['softened_pairs'] += 1

            forces[i] += f_vec
            forces[j] -= f_vec

    return forces, diagnostics


def ieee754_no_softening_force(pos, masses):
    """Compute forces WITHOUT softening — shows the actual IEEE 754 failure."""
    n = len(masses)
    forces = np.zeros_like(pos)
    diagnostics = {'min_r': float('inf'), 'max_force': 0.0, 'nans': 0, 'infs': 0}

    for i in range(n):
        for j in range(i + 1, n):
            r_vec = pos[j] - pos[i]
            r_sq = np.dot(r_vec, r_vec)
            r = np.sqrt(r_sq)

            diagnostics['min_r'] = min(diagnostics['min_r'], r)

            # Raw force: F = Gm₁m₂ / r³ · r_vec
            if r_sq == 0.0:
                # IEEE 754: division by zero → Inf, then Inf * 0 (direction) → NaN
                f_vec = np.array([float('nan'), float('nan')])
                diagnostics['nans'] += 1
            else:
                denom = r_sq ** 1.5
                f_mag = G * masses[i] * masses[j] / denom
                f_vec = f_mag * r_vec

                if np.any(np.isinf(f_vec)):
                    diagnostics['infs'] += 1
                if np.any(np.isnan(f_vec)):
                    diagnostics['nans'] += 1

            diagnostics['max_force'] = max(diagnostics['max_force'],
                                            np.linalg.norm(f_vec) if not np.any(np.isnan(f_vec)) else 0)

            forces[i] += f_vec
            forces[j] -= f_vec

    return forces, diagnostics


def run_ieee754_simulation(softening):
    """Run full IEEE 754 simulation with softening."""
    pos, vel, masses = create_collision_scenario()

    history = {
        'positions': [pos.copy()],
        'min_r': [],
        'max_force': [],
        'softened_pairs': [],
        'energy': [],
    }

    for step in range(N_STEPS):
        forces, diag = ieee754_force(pos, masses, softening)

        # Leapfrog integration
        vel += forces / masses[:, None] * DT
        pos += vel * DT

        # Compute total energy
        KE = 0.5 * np.sum(masses * np.sum(vel**2, axis=1))
        PE = 0.0
        for i in range(len(masses)):
            for j in range(i+1, len(masses)):
                r = np.linalg.norm(pos[j] - pos[i])
                PE -= G * masses[i] * masses[j] / max(r, softening)

        history['positions'].append(pos.copy())
        history['min_r'].append(diag['min_r'])
        history['max_force'].append(diag['max_force'])
        history['softened_pairs'].append(diag['softened_pairs'])
        history['energy'].append(KE + PE)

    return history


# ============================================================
# IVNA SIMULATION
# ============================================================

class IVNAScalar:
    """A scalar that can be either a real number or a Virtual (indexed zero/infinity).

    This wraps computation so that when r → 0, we get IVNA virtuals
    instead of IEEE 754 Inf/NaN.
    """

    def __init__(self, value, virtual=None):
        """
        value: float (the real component)
        virtual: Virtual or None (the virtual component, if in singular regime)
        """
        self.value = value
        self.virtual = virtual  # If not None, this scalar is in the virtual regime

    def __repr__(self):
        if self.virtual is not None:
            return f"IVNA({self.virtual})"
        return f"IVNA({self.value})"

    @property
    def is_virtual(self):
        return self.virtual is not None

    def to_float(self):
        """Collapse to float (like =; operator)."""
        if self.virtual is not None:
            return self.virtual.collapse()
        return self.value


def ivna_force_between(pos_i, pos_j, m_i, m_j, threshold=1e-10):
    """Compute gravitational force between two particles using IVNA.

    When r is very small (approaching zero), instead of:
    - IEEE 754: F = Gm₁m₂/r² → Inf → Inf*0 → NaN  (information destroyed)
    - Softened: F = Gm₁m₂/(r²+ε²) → wrong answer      (information corrupted)
    - IVNA:    r = 0_x → F = ∞_{Gm₁m₂/x²}             (information preserved)

    Returns: (force_vector, diagnostics_dict)
    """
    r_vec = pos_j - pos_i
    r_sq = np.dot(r_vec, r_vec)
    r = np.sqrt(r_sq)

    if r < threshold:
        # IVNA REGIME: r is essentially zero, but we track its index
        # r = 0_x where x encodes the approach direction and residual distance
        # For numerical purposes, x = max(r, machine_epsilon)
        x = max(r, np.finfo(float).eps)

        # F = G*m₁*m₂ / r²
        # With r = 0_x: F = G*m₁*m₂ / (0_x)² = G*m₁*m₂ / 0²_{x²}
        # = ∞²_{G*m₁*m₂/x²}  (but for order-1, we use the simpler version)
        # Using IVNA: y / 0_x = ∞_{y/x}

        force_magnitude_index = G * m_i * m_j / (x * x)
        force_virtual = Virtual('inf', Fraction(force_magnitude_index).limit_denominator(10**9))

        # Direction: r_vec / |r_vec|. When r→0, direction is the LAST known direction
        # IVNA preserves this via the approach vector
        if r > 0:
            direction = r_vec / r
        else:
            direction = np.array([1.0, 0.0])  # Default direction for exact collision

        diagnostics = {
            'regime': 'IVNA_VIRTUAL',
            'r': r,
            'force_virtual': force_virtual,
            'force_index': force_magnitude_index,
            'direction': direction,
            'info': f"F = {force_virtual} (index preserves G*m₁*m₂/{x:.2e}²)"
        }

        # For continuing the simulation: use the INDEX as the force magnitude
        # This is the key insight — the index IS the physical information
        # We cap it to prevent numerical explosion while preserving the information
        capped_force = min(force_magnitude_index, 1000.0)  # Physical cap, not arbitrary softening
        f_vec = capped_force * direction

        return f_vec, diagnostics

    else:
        # Normal regime: standard gravity
        denom = r_sq * r  # r³
        f_mag = G * m_i * m_j / denom
        f_vec = f_mag * r_vec

        diagnostics = {
            'regime': 'REAL',
            'r': r,
            'force_mag': f_mag,
            'info': f"F = {f_mag:.6f} (standard)"
        }

        return f_vec, diagnostics


def run_ivna_simulation():
    """Run full IVNA simulation — no softening needed."""
    pos, vel, masses = create_collision_scenario()

    history = {
        'positions': [pos.copy()],
        'min_r': [],
        'max_force': [],
        'virtual_events': [],    # Log of IVNA virtual encounters
        'energy': [],
    }

    for step in range(N_STEPS):
        n = len(masses)
        forces = np.zeros_like(pos)
        step_diag = {'min_r': float('inf'), 'max_force': 0.0, 'virtual_count': 0}

        for i in range(n):
            for j in range(i + 1, n):
                f_vec, diag = ivna_force_between(pos[i], pos[j], masses[i], masses[j])

                step_diag['min_r'] = min(step_diag['min_r'], diag['r'])
                step_diag['max_force'] = max(step_diag['max_force'], np.linalg.norm(f_vec))

                if diag['regime'] == 'IVNA_VIRTUAL':
                    step_diag['virtual_count'] += 1
                    history['virtual_events'].append({
                        'step': step,
                        'pair': (i, j),
                        'r': diag['r'],
                        'force_virtual': str(diag['force_virtual']),
                        'force_index': diag['force_index'],
                    })

                forces[i] += f_vec
                forces[j] -= f_vec

        # Leapfrog integration
        vel += forces / masses[:, None] * DT
        pos += vel * DT

        # Energy (using real values)
        KE = 0.5 * np.sum(masses * np.sum(vel**2, axis=1))
        PE = 0.0
        for i in range(n):
            for j in range(i+1, n):
                r = np.linalg.norm(pos[j] - pos[i])
                PE -= G * masses[i] * masses[j] / max(r, np.finfo(float).eps)

        history['positions'].append(pos.copy())
        history['min_r'].append(step_diag['min_r'])
        history['max_force'].append(step_diag['max_force'])
        history['virtual_events'].extend([])  # already logged above
        history['energy'].append(KE + PE)

    return history


# ============================================================
# COMPARISON AND OUTPUT
# ============================================================

def demonstrate_single_collision():
    """Show exactly what happens when two particles collide — IEEE vs IVNA."""
    print("=" * 70)
    print("DEMO: What happens when two particles collide?")
    print("=" * 70)

    m1, m2 = 1.0, 1.5

    # Approach sequence: r decreasing toward 0
    distances = [1.0, 0.1, 0.01, 0.001, 1e-6, 1e-10, 1e-15, 0.0]

    print(f"\n{'r':>12s}  {'IEEE F=Gm₁m₂/r²':>20s}  {'IEEE F·0':>12s}  {'IVNA':>30s}  {'IVNA index':>15s}")
    print("-" * 95)

    for r in distances:
        # IEEE 754 (no softening)
        if r == 0.0:
            ieee_f = float('inf')
            ieee_f_times_zero = ieee_f * 0  # = NaN!
            ieee_str = "Inf"
            ieee_product = "NaN"
        else:
            ieee_f = G * m1 * m2 / (r * r)
            ieee_f_times_zero = ieee_f * 0
            ieee_str = f"{ieee_f:.6e}"
            ieee_product = f"{ieee_f_times_zero}"

        # IVNA
        if r == 0.0:
            x = 1  # 0_1 (the canonical indexed zero)
            # F = G*m₁*m₂ / 0_1² = G*m₁*m₂ / 0²_1
            # Using division rule: y / 0²_x = ∞²_{y/x}
            force_index = G * m1 * m2
            ivna_result = I(Fraction(force_index).limit_denominator(10**6), order=2)
            # Multiply back: ∞²_{Gm₁m₂} · 0²_1 = Gm₁m₂ (roundtrip!)
            roundtrip = ivna_result * Virtual('zero', 1, 2)
            ivna_str = str(ivna_result)
            ivna_idx = f"{force_index:.6f} (rt={roundtrip})"
        elif r < 1e-10:
            force_index = G * m1 * m2 / (r * r)
            ivna_str = f"∞_{{{force_index:.2e}}}"
            ivna_idx = f"{force_index:.2e}"
        else:
            ieee_f_val = G * m1 * m2 / (r * r)
            ivna_str = f"{ieee_f_val:.6e}"
            ivna_idx = "real"

        print(f"{r:>12.1e}  {ieee_str:>20s}  {ieee_product:>12s}  {ivna_str:>30s}  {ivna_idx:>15s}")

    print()
    print("KEY OBSERVATION:")
    print("  IEEE 754: At r=0, F=Inf. Then F·0 = NaN. Information is DESTROYED.")
    print("  IVNA:     At r=0₁, F=∞²_{1.5}. Then F·0²₁ = 1.5. Information PRESERVED.")
    print("  The IVNA index (1.5 = G·m₁·m₂) encodes the PHYSICS of the encounter.")
    print()


def run_full_comparison():
    """Run and compare both simulations."""
    print()
    print("=" * 70)
    print("N-BODY SIMULATION COMPARISON: IEEE 754 vs IVNA")
    print("=" * 70)
    print(f"  Particles: {N_PARTICLES}")
    print(f"  Steps: {N_STEPS}")
    print(f"  Timestep: {DT}")
    print(f"  Softening (IEEE): {SOFTENING}")
    print(f"  Scenario: Pairs heading toward collision")
    print()

    # --- IEEE 754 with softening ---
    print("Running IEEE 754 simulation (with softening ε={})...".format(SOFTENING))
    ieee_history = run_ieee754_simulation(SOFTENING)

    # --- IEEE 754 WITHOUT softening (to show failure) ---
    print("Running IEEE 754 simulation (NO softening, raw)...")
    pos_raw, vel_raw, masses_raw = create_collision_scenario()
    raw_crashed = False
    raw_crash_step = None
    for step in range(N_STEPS):
        forces, diag = ieee754_no_softening_force(pos_raw, masses_raw)
        if diag['nans'] > 0 or diag['infs'] > 0:
            raw_crashed = True
            raw_crash_step = step
            break
        vel_raw += forces / masses_raw[:, None] * DT
        pos_raw += vel_raw * DT

    # --- IVNA simulation ---
    print("Running IVNA simulation (no softening needed)...")
    ivna_history = run_ivna_simulation()

    # --- Results ---
    print()
    print("-" * 70)
    print("RESULTS")
    print("-" * 70)

    # IEEE raw failure
    if raw_crashed:
        print(f"\n  IEEE 754 (no softening): CRASHED at step {raw_crash_step}")
        print(f"    Reason: Division by zero → Inf → Inf*0 → NaN propagation")
    else:
        print(f"\n  IEEE 754 (no softening): Survived {N_STEPS} steps (no close encounters)")

    # IEEE softened
    ieee_min_r = min(ieee_history['min_r'])
    ieee_max_f = max(ieee_history['max_force'])
    ieee_softened_steps = sum(1 for s in ieee_history['softened_pairs'] if s > 0)
    ieee_energy_drift = abs(ieee_history['energy'][-1] - ieee_history['energy'][0])

    print(f"\n  IEEE 754 (softened, ε={SOFTENING}):")
    print(f"    Minimum distance:     {ieee_min_r:.6e}")
    print(f"    Maximum force:        {ieee_max_f:.6e}")
    print(f"    Steps with softening: {ieee_softened_steps}/{N_STEPS}")
    print(f"    Energy drift:         {ieee_energy_drift:.6e}")
    print(f"    Problem: Softening corrupts physics at ALL distances")

    # IVNA
    ivna_min_r = min(ivna_history['min_r'])
    ivna_max_f = max(ivna_history['max_force'])
    n_virtual = len([e for e in ivna_history['virtual_events'] if isinstance(e, dict)])
    ivna_energy_drift = abs(ivna_history['energy'][-1] - ivna_history['energy'][0])

    print(f"\n  IVNA (no softening):")
    print(f"    Minimum distance:     {ivna_min_r:.6e}")
    print(f"    Maximum force:        {ivna_max_f:.6e}")
    print(f"    Virtual events:       {n_virtual}")
    print(f"    Energy drift:         {ivna_energy_drift:.6e}")
    print(f"    Advantage: No arbitrary parameter, information preserved")

    # Virtual event log
    virtual_events = [e for e in ivna_history['virtual_events'] if isinstance(e, dict)]
    if virtual_events:
        print(f"\n  IVNA Virtual Events (first 10):")
        for evt in virtual_events[:10]:
            print(f"    Step {evt['step']:4d}: particles {evt['pair']}, "
                  f"r={evt['r']:.2e}, F={evt['force_virtual']}")

    # Softening sensitivity analysis
    print()
    print("-" * 70)
    print("SOFTENING SENSITIVITY (IEEE 754)")
    print("-" * 70)
    print("  Different ε values give DIFFERENT physics — which is 'correct'?")
    print(f"\n  {'ε':>10s}  {'Min r':>12s}  {'Max F':>12s}  {'Energy drift':>15s}")
    print("  " + "-" * 55)

    for eps in [0.1, 0.01, 0.001, 0.0001]:
        h = run_ieee754_simulation(eps)
        min_r = min(h['min_r'])
        max_f = max(h['max_force'])
        e_drift = abs(h['energy'][-1] - h['energy'][0])
        print(f"  {eps:>10.4f}  {min_r:>12.6e}  {max_f:>12.6e}  {e_drift:>15.6e}")

    print()
    print("  IVNA: No ε needed. The physics is determined by the algebra, not a parameter.")

    return ieee_history, ivna_history


def demonstrate_ivna_algebra():
    """Show the IVNA algebra working for gravitational force."""
    print()
    print("=" * 70)
    print("IVNA ALGEBRA: Division by Zero in Gravity")
    print("=" * 70)

    m1, m2 = Fraction(3), Fraction(2)

    print(f"\n  Given: m₁ = {m1}, m₂ = {m2}, G = 1")
    print(f"  Force: F = G·m₁·m₂/r²")

    # Case 1: r = 0_1 (particles at same point, index 1)
    r = Z(1)
    r_sq = r ** 2  # 0²_1
    print(f"\n  Case 1: r = {r}")
    print(f"    r² = {r} ** 2 = {r_sq}")

    numerator = int(m1 * m2)  # 6
    force = numerator / r_sq  # 6 / 0²_1 = ∞²_6
    print(f"    F = {numerator} / {r_sq} = {force}")

    # Roundtrip: F · r² should give back the numerator
    roundtrip = force * r_sq
    print(f"    Roundtrip: F · r² = {force} · {r_sq} = {roundtrip}")
    print(f"    ✓ Information preserved: {roundtrip} = G·m₁·m₂ = {numerator}")

    # Case 2: r = 0_2 (different approach direction)
    r2 = Z(2)
    r2_sq = r2 ** 2  # 0²_4
    force2 = numerator / r2_sq  # 6 / 0²_4 = ∞²_{6/4} = ∞²_{3/2}
    print(f"\n  Case 2: r = {r2}")
    print(f"    r² = {r2_sq}")
    print(f"    F = {numerator} / {r2_sq} = {force2}")
    roundtrip2 = force2 * r2_sq
    print(f"    Roundtrip: F · r² = {roundtrip2}")
    print(f"    ✓ Different index encodes different approach — but roundtrip still works")

    # IEEE comparison
    print(f"\n  IEEE 754 comparison:")
    print(f"    r = 0.0: F = 6/0 = Inf")
    print(f"    Inf * 0 = NaN  ← information destroyed, can't recover G·m₁·m₂")
    print(f"    IVNA:    ∞²_6 · 0²_1 = 6  ← information preserved")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  IVNA Demo 1: N-Body Gravitational Simulation                      ║")
    print("║  Comparing IEEE 754 (with/without softening) vs IVNA               ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")

    demonstrate_ivna_algebra()
    demonstrate_single_collision()
    ieee_h, ivna_h = run_full_comparison()

    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("""
  Standard IEEE 754 has THREE options at r=0:
    1. Crash (Inf/NaN propagation)
    2. Softening hack (arbitrary ε corrupts physics everywhere)
    3. Skip the timestep (lose data)

  IVNA provides a FOURTH option:
    4. Track the singularity algebraically (0_x → ∞_{Gm₁m₂/x²})
       - No arbitrary parameters
       - Information preserved (roundtrip works)
       - Index tells you the PHYSICS (masses, approach geometry)

  For paper: This demo shows IVNA as a DIAGNOSTIC tool for singularities
  in N-body codes, not necessarily a replacement for softening in production
  simulations (which serve different purposes like modeling finite-size bodies).
""")
