# Phase 3: IVNA and Differential Equations — Deep Dive

*Date: 2026-03-31*
*All claims computationally verified via Python/NumPy/SciPy*
*Verification script: `code/verify-odes.py`*
*Verification output: `research/findings/verify-odes-output.txt`*

---

## Executive Summary

IVNA's treatment of differential equations is its most structurally revealing application. Every ODE becomes a difference equation with infinitesimal step size; linear ODEs solve exactly via A-EXP; systems solve via matrix exponential; second-order ODEs reduce to characteristic equations. The framework breaks down cleanly and honestly for nonlinear ODEs. PDEs become finite difference schemes with infinitesimal mesh.

This deep dive covers four domains: harmonic oscillator (2nd-order linear), systems/matrix exponential, nonlinear ODEs (honest limitations), and the heat equation (PDE sketch). Each finding is rated for paper inclusion.

---

## 1. Harmonic Oscillator: y'' + y = 0 — RATING: HIGH

### 1.1 The IVNA Difference Equation

IVNA's second derivative uses the centered difference:

    y''(x) = [y(x + 0_1) - 2y(x) + y(x - 0_1)] / 0^2_1

Substituting into y'' + y = 0:

    [y(x + 0_1) - 2y(x) + y(x - 0_1)] / 0^2_1 + y(x) = 0

Multiply through by 0^2_1:

    y(x + 0_1) - 2y(x) + y(x - 0_1) + 0^2_1 * y(x) = 0

**This is a difference equation with infinitesimal step size 0_1.** The continuous ODE has become a discrete recurrence — but with a step size that is a virtual zero rather than a finite number.

### 1.2 Characteristic Equation Derivation

Try the ansatz y(x) = lambda^{x/h} where h = 0_1. Substituting:

    lambda - 2 + 1/lambda + h^2 = 0

Multiply by lambda:

    lambda^2 - (2 - h^2)*lambda + 1 = 0

Quadratic formula:

    lambda = [(2 - h^2) +/- sqrt((2 - h^2)^2 - 4)] / 2

For h = 0_1 (infinitesimal):

    discriminant = -4h^2 + h^4 = h^2(-4 + h^2)
    sqrt(discriminant) = h * sqrt(-4 + h^2) =; h * 2i = 2i * 0_1

Therefore:

    lambda = 1 - h^2/2 +/- ih = 1 - 0^2_1/2 +/- i*0_1

**Key properties of lambda:**
- |lambda|^2 = (1 - h^2/2)^2 + h^2 = 1 + h^4/4 =; 1 (unit modulus)
- arg(lambda) = arctan(h / (1 - h^2/2)) =; h = 0_1

So lambda =; e^{i*0_1}, and:

    y(x) = lambda^{x/h} = (e^{i*0_1})^{inf_x} = e^{ix}

**General solution: y = A*cos(x) + B*sin(x).** The standard result, derived entirely from IVNA's difference equation framework.

### 1.3 Verification: 2cos(0_1) - 2 + 0^2_1 = 0

The crucial identity that makes e^{ix} satisfy the IVNA difference equation:

    e^{ix}[e^{i*0_1} + e^{-i*0_1} - 2 + 0^2_1] = e^{ix}[2cos(0_1) - 2 + 0^2_1] = 0

Using the Taylor expansion of cos:

    cos(0_1) = 1 - 0^2_1/2 + 0^4_1/24 - ...
    2cos(0_1) - 2 + 0^2_1 = 0^4_1/12 - ... (a 4th-order virtual zero)

Under =; (collapse): 0^4_1/12 =; 0. So the equation holds to all relevant orders.

**Numerical verification** (see `verify-odes-output.txt`): For epsilon = 10^{-1} through 10^{-3}, the ratio |2cos(eps) - 2 + eps^2| / (eps^4/12) approaches 1.0, confirming the O(eps^4) residual. (Below eps = 10^{-4}, floating-point cancellation dominates, as expected.)

### 1.4 What This Shows

1. **IVNA handles second-order ODEs** via its centered second-derivative formula
2. **The characteristic equation method for difference equations** gives the correct roots lambda = e^{+/-ih}
3. **Euler's formula emerges naturally**: cos(x) and sin(x) are the real and imaginary parts of e^{ix} = (1 + 0_i)^{inf_x}
4. **The discrete-continuous bridge is explicit**: the same characteristic equation works for finite step h (discrete oscillator) and infinitesimal step h = 0_1 (continuous oscillator)

### 1.5 Paper Inclusion Assessment

**Include as a subsection in the Applications/Calculus section.** This is the strongest single result in this deep dive. It shows IVNA handling a second-order ODE that the earlier work (dy/dx = ky) did not cover, connects to Euler's formula (already identified as HIGH in the e-exploration), and demonstrates the difference equation viewpoint concretely.

**Recommended presentation**: Lead with the difference equation transformation, show the characteristic equation, derive e^{ix}, note that this is the same mechanism that gives e^{kx} for first-order ODEs but now with complex roots.

---

## 2. Systems of ODEs and Matrix Exponential — RATING: HIGH

### 2.1 The IVNA Framework

For dy/dx = Ay where A is an n x n matrix:

    y(x + 0_1) = y(x) + 0_1 * A * y(x) = (I + 0_1 * A) * y(x)

After inf_1 steps (one unit of x):

    y(x + 1) = (I + 0_1 * A)^{inf_1} * y(x)

By the matrix generalization of A-EXP:

    (I + 0_1 * A)^{inf_1} = e^A

**This IS the matrix exponential.** IVNA derives it as "infinitely many infinitesimal steps" — the precise historical motivation from Lie's original work (1888).

### 2.2 Verification: 2x2 Rotation

For A = [[0, -1], [1, 0]] (the generator of SO(2) rotations):

    e^A = [[cos(1), -sin(1)], [sin(1), cos(1)]]

**Verified:**
- `scipy.linalg.expm(A)` matches the rotation matrix to machine precision (error < 10^{-16})
- IVNA simulation (I + A/N)^N converges at rate O(1/N):
  - N = 10: error 4.1e-02
  - N = 100: error 4.2e-03
  - N = 1000: error 4.2e-04
  - N = 100000: error 4.2e-06

The O(1/N) convergence rate is first-order, matching forward Euler.

### 2.3 Verification: e^{At} for Various t

e^{At} with A = [[0,-1],[1,0]] gives rotation by t radians. Verified for t = 0, 0.5, 1.0, pi/2, pi, 2*pi — all match to machine precision (max error < 5e-16).

### 2.4 Verification: Coupled Oscillators (4x4 System)

Two masses connected by springs:
- x1'' = -2*x1 + x2
- x2'' = x1 - 2*x2

Written as y' = Ay with A (4x4 matrix).

**Results:**
- Eigenvalues of A are purely imaginary (+/-i, +/-i*sqrt(3)), confirming undamped oscillation
- IVNA simulation (I + A*dt)^N matches scipy expm to error 1.5e-05 (N=100000)
- Energy is conserved to 10 decimal places over t = 0 to t = 20

### 2.5 The Lie Theory Connection

IVNA's formula e^A = (I + 0_1 * A)^{inf_1} is the **exact definition of the exponential map** from Lie algebra to Lie group:

    exp: g -> G

The Lie algebra element A generates infinitesimal transformations. IVNA makes this concrete:
- **0_1 * A** is the infinitesimal transformation (Lie algebra element scaled to virtual zero)
- **I + 0_1 * A** is the group element "infinitesimally close to the identity"
- **(I + 0_1 * A)^{inf_1}** iterates to a finite transformation

This extends the Euler identity insight from Section 2 (e-exploration):

    e^{i*theta} = (1 + 0_i)^{inf_theta}

is the Lie group/algebra relationship for SO(2), and

    e^A = (I + 0_1 * A)^{inf_1}

is the same relationship for any matrix Lie group. **IVNA notation makes the mechanism visible where e^A hides it.**

### 2.6 Quantum Mechanics Connection (Brief)

Time evolution in quantum mechanics:

    U(t) = e^{-iHt/hbar}

In IVNA:

    U(t) = (I + 0_1 * (-iH/hbar))^{inf_t}

"Infinitely many infinitesimal time steps." This is Feynman's path integral motivation expressed algebraically. **Speculative — mention briefly, do not overclaim.**

### 2.7 Paper Inclusion Assessment

**Include as a separate subsection.** The matrix exponential result deepens the e-exploration findings significantly:
- It generalizes A-EXP from scalars to matrices
- It connects IVNA to Lie theory (established, important mathematics)
- It provides a concrete verification case (rotation matrix)
- The Lie theory angle is genuinely illuminating (notation makes the mechanism visible)

**Recommended presentation**: State the matrix A-EXP, verify with the rotation example, note the Lie theory connection in one paragraph. Coupled oscillators can go in an appendix or be mentioned briefly.

---

## 3. Nonlinear ODEs: Honest Limitations — RATING: HIGH (for credibility)

### 3.1 Bernoulli Equation: dy/dx = y^2

IVNA step:

    y(x + 0_1) = y(x) + 0_1 * y(x)^2 = y(x) * (1 + 0_1 * y(x))

**The problem**: the factor (1 + 0_1 * y(x)) depends on y(x), which changes at every step. There is no constant base to exponentiate via A-EXP.

For linear ODEs: y(x + 0_1) = (1 + 0_k) * y(x). The factor (1 + 0_k) is **constant**. The product telescopes: y(x) = (1 + 0_k)^{inf_x} * y(0) = e^{kx} * y(0).

For nonlinear ODEs: the product does not telescope. We must iterate step by step.

**Verification** (y(0) = 1, exact solution y = 1/(1-x)):

| N       | y(0.5) IVNA | y(0.5) exact | rel error | y(0.9) IVNA | y(0.9) exact | rel error |
|---------|-------------|--------------|-----------|-------------|--------------|-----------|
| 100     | 1.97336     | 2.00000      | 1.33e-02  | 8.27859     | 10.00000     | 1.72e-01  |
| 1,000   | 1.99724     | 2.00000      | 1.38e-03  | 9.77749     | 10.00000     | 2.23e-02  |
| 10,000  | 1.99972     | 2.00000      | 1.39e-04  | 9.97705     | 10.00000     | 2.29e-03  |
| 100,000 | 1.99997     | 2.00000      | 1.39e-05  | 9.99770     | 10.00000     | 2.30e-04  |

**Convergence is first-order** (O(h)): halving h halves the error. For linear ODEs, IVNA gives the EXACT answer via A-EXP. For nonlinear ODEs, IVNA is forward Euler — no algebraic shortcut.

### 3.2 Logistic Equation: dy/dx = ry(1-y)

IVNA step:

    y(x + 0_1) = y(x) * [1 + 0_r - 0_{r*y(x)}]

Again, the step factor depends on y(x). No algebraic closure.

**Verification** (r=1, y(0)=0.1, exact y(x) = 1/(1 + 9*e^{-x})):

Same pattern as Bernoulli: first-order convergence, no algebraic advantage. Confirmed numerically.

### 3.3 Separation of Variables Still Works

For dy/dx = y^2, separation of variables in IVNA:

    dy / y^2 = dx  =>  sum_{k} 0_1 * y_k^{-2} = x  =>  -1/y(x) + 1/y(0) = x

This gives the correct solution y(x) = y(0)/(1 - x*y(0)). But it requires knowing the antiderivative of y^{-2}, which is a standard calculus fact.

**The key insight**: For linear ODEs, A-EXP provides the universal antiderivative (the exponential function). For nonlinear ODEs, problem-specific antiderivatives are still required. IVNA does not eliminate this need.

### 3.4 The Fundamental Dichotomy

| Property                     | Linear ODEs (dy/dx = ky, dy/dx = Ay) | Nonlinear ODEs (dy/dx = f(y)) |
|------------------------------|---------------------------------------|-------------------------------|
| Step factor                  | Constant: (1 + 0_k) or (I + 0_1*A) | Variable: depends on y(x)    |
| Product telescopes?          | Yes — via A-EXP                      | No                            |
| Closed-form solution?        | Yes: e^{kx}, e^{Ax}                 | Only with antiderivatives     |
| IVNA advantage over standard?| Yes: algebraic, no limits            | No: reduces to Euler method   |

### 3.5 Paper Inclusion Assessment

**Include as a dedicated subsection.** This honest limitation section is essential for credibility. Reviewers will immediately ask "what about nonlinear?" — better to address it head-on than have it raised as an objection.

**Recommended presentation**: State the linear/nonlinear dichotomy clearly. Show one nonlinear example (Bernoulli) with numerical convergence data. Note that IVNA provides the correct formal expression but no algebraic shortcut. Conclude that the linear/matrix case is the framework's strength; nonlinear ODEs are a limitation shared with every other framework.

---

## 4. Heat Equation PDE Sketch — RATING: MEDIUM

### 4.1 IVNA Discretization

The heat equation u_t = k * u_xx in IVNA:

Time derivative: [u(x, t + 0_t) - u(x, t)] / 0_t
Space 2nd derivative: [u(x + 0_x, t) - 2u(x,t) + u(x - 0_x, t)] / 0^2_x

Substituting:

    u(x, t + 0_t) = u(x,t) + (k * 0_t / 0^2_x) * [u(x+0_x,t) - 2u(x,t) + u(x-0_x,t)]

### 4.2 The Multi-Scale Issue

**Critical observation**: we need DIFFERENT indexed zeros for time and space. Using the same 0_1 for both produces k * 0_1 / 0^2_1 = k / 0_1 = k * inf_1, which diverges.

**Resolution**: Set 0_t = 0^2_{alpha*x^2} (a second-order zero), so that:

    k * 0^2_{alpha*x^2} / 0^2_x = k * alpha (finite)

With alpha = k/2 (stability boundary), this gives the standard FTCS (Forward-Time Central-Space) finite difference scheme.

**The stability condition** (CFL condition: k*dt/dx^2 <= 1/2) emerges naturally from IVNA arithmetic: the ratio of indexed zeros must be a finite number, not a virtual number.

### 4.3 Numerical Verification

For k=1, L=1, sin(pi*x) initial condition:

| t     | u(L/2) IVNA   | u(L/2) exact  | rel error |
|-------|---------------|---------------|-----------|
| 0.01  | 0.906012      | 0.906018      | 6.5e-06   |
| 0.05  | 0.610478      | 0.610498      | 3.3e-05   |
| 0.10  | 0.372684      | 0.372708      | 6.5e-05   |
| 0.20  | 0.138893      | 0.138911      | 1.3e-04   |

IVNA discretization matches exact solution to high accuracy.

### 4.4 Key Insights

1. **IVNA naturally produces finite difference schemes**: derivatives are literal difference quotients with indexed zeros, and the scheme IS the IVNA step equation.

2. **Multiple indexed zeros**: PDEs require different indexed zeros for different dimensions. IVNA naturally accommodates this — each dimension gets its own infinitesimal scale.

3. **Stability from arithmetic**: The CFL condition is not imposed externally; it follows from requiring that ratios of indexed zeros produce finite (not virtual) coefficients.

4. **No computational advantage**: Finite difference methods for PDEs are centuries old. IVNA provides a notational framework that shows WHY they work (they are the natural IVNA discretization), but does not improve upon existing numerical methods.

### 4.5 Paper Inclusion Assessment

**Include as a brief sketch (one paragraph + one equation) in a "Further Directions" or "Discussion" section.** The multi-scale observation (different 0_t and 0_x) and the stability-from-arithmetic insight are worth mentioning but do not merit a full section. The heat equation adds breadth but not depth to the paper's argument.

---

## 5. Literature Positioning

### 5.1 NSA Approach to ODEs

IVNA's ODE treatment is directly parallel to the NSA approach developed by:

- **H. Jerome Keisler, "Elementary Calculus: An Infinitesimal Approach" (1976)**: Defines derivatives and integrals using infinitesimals. The ODE treatment uses the "internal Euler's method" — iterating with infinitesimal step size and taking the standard part. This is exactly what IVNA does with different notation.

- **Abraham Robinson, "Non-Standard Analysis" (1966)**: The foundational text. Robinson proved that NSA is consistent relative to ZFC. His framework provides the rigorous backing for all IVNA constructions.

- **Cutland, "Nonstandard Analysis and its Applications" (1988)**: Extends NSA methods to stochastic differential equations and measure theory.

**IVNA's relationship to Keisler**: IVNA's ODE step y(x + 0_1) = y(x) + 0_1 * f(x, y(x)) IS Keisler's internal Euler method, with 0_1 replacing his infinitesimal epsilon. The collapse operator =; IS the standard part function st(). The mathematical content is identical; the notation differs. **This must be acknowledged in the paper.**

### 5.2 Time Scales Calculus (Hilger, 1988)

Stefan Hilger's time scales calculus (PhD thesis, 1988; published in Results Math., 1990) provides a rigorous unification of continuous and discrete analysis. A "time scale" T is any closed subset of the reals; calculus on T includes both standard calculus (T = R) and difference equations (T = Z) as special cases.

**Comparison with IVNA**: Hilger's framework is more general (arbitrary time scales) and more rigorous (full measure-theoretic foundation). IVNA's contribution is not a new unification framework but rather a specific notational system that makes the discrete-continuous bridge visible at the level of individual equations. The paper should cite Hilger's work and clarify that IVNA is a notational contribution, not a replacement for time scales calculus.

### 5.3 Matrix Exponential and Lie Theory

The connection between IVNA's matrix A-EXP and Lie theory is well-established:

- **Sophus Lie (1888)**: Introduced the exponential map from Lie algebra to Lie group. The formula exp(A) = lim_{n->inf} (I + A/n)^n is the classical definition.

- **Hermann Weyl (1934)**: Coined the term "Lie algebra" for what had been called "the algebra of infinitesimal transformations."

- **Modern treatment**: The exponential map exp: g -> G sends Lie algebra elements to group elements. IVNA notation (I + 0_1*A)^{inf_1} = e^A makes the mechanism explicit.

**IVNA's contribution here is purely pedagogical**: the notation reveals the infinitesimal-step interpretation that is implicit in the classical definition. This is valuable for teaching but is not new mathematics.

### 5.4 Peano's Existence Theorem

The Peano existence theorem guarantees that dy/dx = f(x,y) with continuous f has a local solution. The classical proof constructs approximate solutions via Euler polygons and uses Ascoli's theorem to extract a convergent subsequence.

**IVNA connection**: The IVNA step y(x + 0_1) = y(x) + 0_1 * f(x,y(x)) IS the Euler polygon with infinitesimal step. The collapse operator =; extracts the solution. In NSA, this is formalized as: the internal Euler polygon with infinitesimal step, followed by standard part, gives a solution to the ODE. IVNA inherits this rigor through its NSA embedding.

---

## 6. Summary: Paper Inclusion Ratings

| Finding | Rating | Include? | Section | Words |
|---------|--------|----------|---------|-------|
| **Harmonic oscillator via difference equation** | HIGH | Yes | Applications/Calculus | ~400 |
| - Characteristic equation derivation | HIGH | Yes | Same subsection | ~200 |
| - cos/sin emerge from e^{+/-ix} | HIGH | Yes | Same (connects to Euler identity) | ~100 |
| - Numerical convergence data | MEDIUM | Appendix/supplementary | | ~100 |
| **Matrix exponential = (I + 0_1*A)^{inf_1}** | HIGH | Yes | New subsection or extend e section | ~300 |
| - 2x2 rotation verification | HIGH | Yes | Same subsection | ~100 |
| - Lie theory connection | HIGH | Yes | One paragraph | ~150 |
| - Coupled oscillators | MEDIUM | Brief mention or appendix | | ~50 |
| - Quantum mechanics connection | MEDIUM | One sentence | | ~30 |
| **Nonlinear ODEs: honest limitations** | HIGH | Yes | Dedicated subsection | ~300 |
| - Bernoulli example with data | HIGH | Yes | Same subsection | ~150 |
| - Linear/nonlinear dichotomy table | HIGH | Yes | Same subsection | ~100 |
| - Separation of variables remark | MEDIUM | One sentence | | ~30 |
| **Heat equation PDE sketch** | MEDIUM | Brief sketch in Discussion | | ~150 |
| - Multi-scale indexed zeros | MEDIUM | Worth a remark | | ~50 |
| - Stability from arithmetic | MEDIUM | Worth a remark | | ~50 |
| **NSA/Keisler parallel** | HIGH | Literature review | Must acknowledge | ~100 |
| **Time scales calculus (Hilger)** | MEDIUM | Literature review | Brief citation | ~50 |

**Estimated total contribution to paper**: ~1,500-2,000 words (about 3-4 pages of a math paper), forming a substantial new section on ODEs/dynamics.

---

## 7. Deeper Mathematical Analysis

### 7.1 Why Linear ODEs Are Special for IVNA

The fundamental reason IVNA works beautifully for linear ODEs is the **semigroup property**:

For y' = ky: the solution operator S(t) = e^{kt} satisfies S(s+t) = S(s)*S(t).

In IVNA: S(0_1) = 1 + 0_k. Then S(n*0_1) = (1 + 0_k)^n. The semigroup property holds because the step factor is constant.

For matrix ODEs: S(0_1) = I + 0_1*A. Then S(n*0_1) = (I + 0_1*A)^n. Same story.

For nonlinear ODEs: there is no semigroup. The "step operator" at time t depends on y(t), which is unknown. This is why the product does not telescope.

**This semigroup analysis explains exactly where IVNA's algebraic power comes from and where it runs out.** It should be mentioned in the paper (one paragraph).

### 7.2 Second-Order vs. First-Order: The Centered Difference

The centered second derivative formula:

    y''(x) = [y(x+h) - 2y(x) + y(x-h)] / h^2

has error O(h^2), while the forward first derivative:

    y'(x) = [y(x+h) - y(x)] / h

has error O(h). This means the IVNA second derivative is actually MORE accurate than the first derivative for the same step size.

In IVNA terms: the centered formula produces a residual of order 0^2_1 (second-order virtual zero), while the forward formula produces order 0_1 (first-order virtual zero). The centered formula "uses up" the first-order term by symmetry.

### 7.3 The General Linear ODE: y'' + py' + qy = 0

Any second-order linear ODE with constant coefficients becomes:

    y(x+0_1) - 2y(x) + y(x-0_1) + 0^2_1*[p*(y(x+0_1) - y(x))/0_1 + q*y(x)] = 0

Simplifying:

    (1 + p*0_1)*y(x+0_1) - (2 + p*0_1 - q*0^2_1)*y(x) + y(x-0_1) = 0

This is a linear recurrence with constant coefficients (the coefficients involve indexed zeros but are constant with respect to x). It has a characteristic equation:

    (1 + p*0_1)*lambda^2 - (2 + p*0_1 - q*0^2_1)*lambda + 1 = 0

For infinitesimal 0_1, this reduces to the standard characteristic equation r^2 + pr + q = 0. IVNA handles the ENTIRE class of constant-coefficient linear ODEs through this mechanism.

---

## 8. Open Questions for Future Work

1. **Higher-order linear ODEs**: The pattern clearly extends to y^{(n)} + ... = 0 via higher-order difference operators. This should be verified and stated in general.

2. **Variable-coefficient linear ODEs**: y'' + p(x)y' + q(x)y = 0. The IVNA step factors now depend on x (but not on y). This is intermediate between the constant-coefficient case (which IVNA handles perfectly) and the nonlinear case (which IVNA cannot simplify). Does IVNA add value here?

3. **IVNA and numerical analysis**: The connection between IVNA step equations and numerical methods (Euler, midpoint, Runge-Kutta) could be developed. IVNA naturally gives forward Euler; can higher-order methods be expressed in IVNA notation?

4. **Stochastic differential equations**: dy = f(y)dt + g(y)dW. IVNA step: y(t + 0_1) = y(t) + 0_1*f(y) + sqrt(0_1)*g(y)*Z where Z is standard normal. The sqrt(0_1) = 0^{1/2}_1 term reflects the Brownian motion scaling. This connects to Keisler's work on stochastic analysis via NSA.

5. **Wave equation and other PDEs**: u_tt = c^2 * u_xx would require a centered difference in time as well. Multiple indexed zeros (0_t, 0_x) with different orderings would be needed.

---

## References

### Foundational

1. Robinson, A. (1966). *Non-Standard Analysis*. North-Holland.
2. Keisler, H.J. (1976/2012). *Elementary Calculus: An Infinitesimal Approach*. Dover. [Free online edition](https://www.math.wisc.edu/~keisler/calc.html)
3. Hilger, S. (1990). Analysis on measure chains — a unified approach to continuous and discrete calculus. *Results in Mathematics*, 18, 18-56.
4. Cutland, N. (1988). *Nonstandard Analysis and its Applications*. Cambridge University Press.

### Lie Theory and Matrix Exponential

5. Hall, B.C. (2015). *Lie Groups, Lie Algebras, and Representations* (2nd ed.). Springer.
6. Moler, C. & Van Loan, C. (2003). Nineteen dubious ways to compute the matrix exponential, twenty-five years later. *SIAM Review*, 45(1), 3-49.

### Difference Equations

7. Elaydi, S. (2005). *An Introduction to Difference Equations* (3rd ed.). Springer.
8. Bohner, M. & Peterson, A. (2001). *Dynamic Equations on Time Scales*. Birkhauser.

### Peano Existence Theorem

9. Coddington, E.A. & Levinson, N. (1955). *Theory of Ordinary Differential Equations*. McGraw-Hill.

---

*Prepared: 2026-03-31*
*Verification: All numerical results from `code/verify-odes.py` (run date: 2026-03-31)*
*Input sources: e-exploration.md (Section 5: ODEs as difference equations, Section 6b: matrix exponential), value-assessment.md (paper outline), CLAUDE.md (axiom reference)*
