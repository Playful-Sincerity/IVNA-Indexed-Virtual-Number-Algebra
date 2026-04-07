"""
IVNA Verification Suite — Category C: Classical Correspondence Checks
======================================================================

Every check in this file uses SymPy as the computational engine.
The IVNA implementation (ivna.py) is deliberately NOT imported here.

These checks verify that IVNA's notation maps correctly onto known
classical mathematical results — they are NOTATION/CORRESPONDENCE
checks, not claims that IVNA independently produces these results.

IVNA's contribution in each domain is noted in the section docstring.
Category C is honest: the classical math is already known. What IVNA
adds is a notation layer that makes certain structures explicit and
algebraically operable.
"""

import sys
import math
from fractions import Fraction
import sympy as sp
from sympy import (
    symbols, oo, limit, simplify, integrate, exp, ln, sin, cos, tan,
    sqrt, pi, Rational, factor, cancel, series, Abs, zoo, nan,
    DiracDelta, Heaviside, log, atan, conjugate
)
from sympy.stats import (
    Normal, density, given, E, variance, Gamma, Exponential
)

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


x, y, z, t, a, b, eps, m, n = symbols('x y z t a b eps m n', real=True)
x0, y0, z0 = symbols('x0 y0 z0', real=True)


# ============================================================
# DOMAIN 1: BAYES / CONDITIONAL DENSITY
# ============================================================
"""
IVNA CONTRIBUTION: The A8 axiom (0_x / 0_y = x/y) makes the 0/0
structure of conditional probability density visible as an index
ratio. f(x|y) = f(x,y)/f(y) is literally 0_f(x,y) / 0_f(y) = f(x,y)/f(y)
at the index level — the symbolic "division by zero" is determinate.
"""

# Bivariate normal with rho=0 (independent)
mu_x, mu_y, sig_x, sig_y = 0, 0, 1, 1
X, Y = symbols('X Y', real=True)

f_X = (1 / (sig_x * sqrt(2*pi))) * exp(-X**2 / (2*sig_x**2))
f_Y = (1 / (sig_y * sqrt(2*pi))) * exp(-Y**2 / (2*sig_y**2))
f_XY = f_X * f_Y  # independence: rho=0

# Conditional f(X|Y=0) should equal f(X) when independent
f_X_given_Y0 = f_XY.subs(Y, 0) / f_Y.subs(Y, 0)
f_X_given_Y0_simplified = simplify(f_X_given_Y0)
f_X_at_Y0 = f_X

check(
    "[Classical] Bayes: f(X|Y=0) = f(X) for independent bivariate normal",
    simplify(f_X_given_Y0_simplified - f_X_at_Y0) == 0
)

# Conditional f(X|Y=y0) = f(X) for all y0 (independence)
for y_val in [0, 1, -1, 2]:
    f_cond = f_XY.subs(Y, y_val) / f_Y.subs(Y, y_val)
    check(
        f"[Classical] Bayes: f(X|Y={y_val}) = f(X) for independent normals",
        simplify(simplify(f_cond) - f_X) == 0
    )

# Conditional density integrates to 1 over X (numerical check)
# For standard normal, integral of (1/sqrt(2pi))*exp(-x^2/2) dx = 1
integral_f_X = integrate(f_X, (X, -oo, oo))
check(
    "[Classical] Bayes: marginal f(X) integrates to 1",
    simplify(integral_f_X - 1) == 0
)

# f_XY integrates to 1
integral_f_XY = integrate(integrate(f_XY, (X, -oo, oo)), (Y, -oo, oo))
check(
    "[Classical] Bayes: joint f(X,Y) integrates to 1",
    simplify(integral_f_XY - 1) == 0
)

# Correlated bivariate normal: verify conditional mean is rho*y
rho = Rational(1, 2)
sig = 1
mu = 0
# f(x|y) for bivariate normal with rho: conditional mean = rho*y
# IVNA reads this off as 0_{f_XY} / 0_{f_Y} = f_XY/f_Y index ratio
X_sym, Y_sym = symbols('Xs Ys', real=True)
f_joint_corr = (1 / (2*pi*sig**2*sqrt(1 - rho**2))) * exp(
    -(X_sym**2 - 2*rho*X_sym*Y_sym + Y_sym**2) / (2*sig**2*(1 - rho**2))
)
f_marg_y = (1 / (sig * sqrt(2*pi))) * exp(-Y_sym**2 / (2*sig**2))
f_cond_corr = simplify(f_joint_corr / f_marg_y)

# Conditional mean: integral x * f(x|y) dx should equal rho*y
# We verify by checking the exponent structure: f(x|y) is normal with mean rho*y
# Verified structurally: exponent in f_cond_corr should be -(x-rho*y)^2 / (2*(1-rho^2))
f_cond_log = sp.expand(sp.log(f_cond_corr))
f_expected_log = sp.expand(sp.log(
    (1 / (sqrt(2*pi*(1-rho**2)))) * exp(-(X_sym - rho*Y_sym)**2 / (2*(1-rho**2)))
))
check(
    "[Classical] Bayes: correlated bivariate normal conditional is Gaussian",
    simplify(f_cond_log - f_expected_log) == 0
)

# Bayes theorem: P(A|B) = P(B|A)*P(A)/P(B) — algebraic identity
pA, pB, pB_given_A = symbols('pA pB pBgA', positive=True)
bayes_lhs = pB_given_A * pA / pB
bayes_rhs = (pB_given_A * pA) / pB
check(
    "[Classical] Bayes: P(A|B)*P(B) = P(B|A)*P(A) algebraic identity",
    simplify(bayes_lhs * pB - pB_given_A * pA) == 0
)

# Marginal recovery: integral of f(x|y)*f(y) dy = f(x)
# For the independent case, verify symbolically
integral_cond_times_marg = integrate(
    f_XY.subs(Y, t) / f_Y.subs(Y, t) * f_Y.subs(Y, t),
    (t, -oo, oo)
)
check(
    "[Classical] Bayes: integral of f(X|y)*f(y) dy = f(X)",
    simplify(simplify(integral_cond_times_marg) - f_X) == 0
)

# Chain rule: f(x,y) = f(x|y)*f(y)
f_cond_times_marg = f_XY.subs(Y, 0) / f_Y.subs(Y, 0) * f_Y.subs(Y, 0)
check(
    "[Classical] Bayes: f(X,Y=0) = f(X|Y=0)*f(Y=0)",
    simplify(f_cond_times_marg - f_XY.subs(Y, 0)) == 0
)


# ============================================================
# DOMAIN 2: BOREL-KOLMOGOROV
# ============================================================
"""
IVNA CONTRIBUTION: The Borel-Kolmogorov paradox arises because
conditional probability on a set of measure zero is a 0/0 form.
IVNA's indexed notation makes the parameterization dependence explicit:
different parameterizations produce different index ratios, which is
why the "same" conditioning event gives different answers.
"""

theta, phi_sym = symbols('theta phi', real=True, positive=True)

# Uniform distribution on sphere, conditioned on a meridian circle
# Parameterization 1: spherical (theta, phi) — area element sin(theta)
# f(theta, phi) uniform on sphere => f = 1/(4*pi)
# f(theta | phi=phi0) proportional to sin(theta) * (1/(4*pi)) / f(phi0)
# f(phi0) = integral over theta of (1/(4*pi)) * sin(theta) d_theta = 1/(2*pi)... wait
# Correctly: marginal of phi in (theta,phi) coords:
# f(phi) = integral_0^pi (1/(4*pi)) * sin(theta) d_theta = 1/(4*pi) * [-cos]_0^pi = 1/(2*pi)
f_theta_given_phi = (Rational(1,4)*pi**(-1) * sin(theta)) / (Rational(1,2)*pi**(-1))
f_theta_given_phi_simplified = simplify(f_theta_given_phi)

# Should equal sin(theta)/2
check(
    "[Classical] Borel-Kolmogorov: f(theta|phi=phi0) = sin(theta)/2 in spherical coords",
    simplify(f_theta_given_phi_simplified - sin(theta)/2) == 0
)

# Verify f(theta|phi) integrates to 1
integral_bk1 = integrate(sin(theta)/2, (theta, 0, pi))
check(
    "[Classical] Borel-Kolmogorov: f(theta|phi) integrates to 1 over [0,pi]",
    simplify(integral_bk1 - 1) == 0
)

# Parameterization 2: (x, phi) where x = cos(theta), area element = 1
# f(x, phi) uniform on sphere in (x, phi) coords => f = 1/(4*pi)
# f(phi) = integral_{-1}^{1} (1/(4*pi)) dx = 1/(2*pi)
# f(x | phi=phi0) = (1/(4*pi)) / (1/(2*pi)) = 1/2  => uniform on [-1,1]
f_x_given_phi = Rational(1,4)*pi**(-1) / (Rational(1,2)*pi**(-1))
check(
    "[Classical] Borel-Kolmogorov: f(x|phi=phi0) = 1/2 in (x,phi) coords (uniform on [-1,1])",
    simplify(f_x_given_phi - Rational(1,2)) == 0
)

# Verify f(x|phi) integrates to 1 over [-1,1]
x_coord = symbols('xc', real=True)
integral_bk2 = integrate(Rational(1,2), (x_coord, -1, 1))
check(
    "[Classical] Borel-Kolmogorov: f(x|phi) integrates to 1 over [-1,1]",
    simplify(integral_bk2 - 1) == 0
)

# The two conditionals are DIFFERENT (paradox): sin(theta)/2 vs 1/2
# They agree only at theta where sin(theta)/2 = 1/2 i.e. sin(theta) = 1 i.e. theta = pi/2
check(
    "[Classical] Borel-Kolmogorov: conditionals agree at equator (theta=pi/2)",
    simplify((sin(theta)/2 - Rational(1,2)).subs(theta, pi/2)) == 0
)

# They differ elsewhere, e.g. theta=pi/4
check(
    "[Classical] Borel-Kolmogorov: conditionals differ off equator (theta=pi/4)",
    simplify((sin(theta)/2 - Rational(1,2)).subs(theta, pi/4)) != 0
)

# Parameterization 3: (theta, z) where z = phi/2pi (uniform on [0,1])
# Same structure: marginal of z is uniform on [0,1], f(z)=1
# f(theta|z) = (sin(theta)/2) / 1 = sin(theta)/2 — same as param 1
f_theta_given_z = sin(theta)/2
integral_bk3 = integrate(f_theta_given_z, (theta, 0, pi))
check(
    "[Classical] Borel-Kolmogorov: f(theta|z) = sin(theta)/2 in (theta,z) coords",
    simplify(integral_bk3 - 1) == 0
)

# Key Borel-Kolmogorov moral: the conditional depends on the ambient measure (Jacobian)
# Ratio of Jacobians: d(x)/d(theta) = -sin(theta)
jac_ratio = Abs(sp.diff(sp.cos(theta), theta))
check(
    "[Classical] Borel-Kolmogorov: Jacobian |dx/dtheta| = |sin(theta)|",
    simplify(jac_ratio - Abs(sin(theta))) == 0
)

# Connection of IVNA: the index in 0_f(x,y) / 0_f(y) carries the measure information
# Different parameterizations = different indices = different ratios
# Verified via the fact that sin(theta)/2 ≠ 1/2 in general (checked above)
check(
    "[Classical] Borel-Kolmogorov: parameterization changes conditional (different indices)",
    simplify(sin(theta)/2 - Rational(1,2)) != 0  # not identically equal
)


# ============================================================
# DOMAIN 3: DIRAC DELTA
# ============================================================
"""
IVNA CONTRIBUTION: The Dirac delta is an element of height 0_inf = 1/eps
and width 0_eps, so height * width = 1. IVNA's A3 axiom (0_x * inf_y = xy)
characterizes this invariant algebraically: 0_{1/eps} * inf_{1/eps} = 1.
The delta function is literally Z(1/eps) * I(1/eps) = 1 in IVNA notation.
"""

eps_sym = symbols('eps', positive=True)
x_int = symbols('xi', real=True)

# Normalization: rectangular nascent delta
# delta_eps(x) = (1/(2*eps)) * Heaviside(eps - |x|)
# integral = 1
rect_norm = integrate(
    sp.Piecewise((Rational(1,2)/eps_sym, Abs(x_int) < eps_sym), (0, True)),
    (x_int, -oo, oo)
)
check(
    "[Classical] Dirac: rectangular nascent delta integrates to 1",
    simplify(rect_norm - 1) == 0
)

# Gaussian nascent delta: (1/(eps*sqrt(pi))) * exp(-x^2/eps^2)
gauss_nascent = (1/(eps_sym*sqrt(pi))) * exp(-x_int**2/eps_sym**2)
gauss_norm = integrate(gauss_nascent, (x_int, -oo, oo))
check(
    "[Classical] Dirac: Gaussian nascent delta integrates to 1",
    simplify(gauss_norm - 1) == 0
)

# Lorentzian nascent delta: (1/pi) * eps/(x^2 + eps^2)
lorentz_nascent = (1/pi) * eps_sym / (x_int**2 + eps_sym**2)
lorentz_norm = integrate(lorentz_nascent, (x_int, -oo, oo))
check(
    "[Classical] Dirac: Lorentzian nascent delta integrates to 1",
    simplify(lorentz_norm - 1) == 0
)

# Sifting property: integral f(x)*delta(x-a) dx = f(a) using DiracDelta
a_val = symbols('av', real=True)
f_test = x_int**2 + 3*x_int + 1
sift_result = integrate(f_test * DiracDelta(x_int - a_val), (x_int, -oo, oo))
check(
    "[Classical] Dirac: sifting property integral x^2+3x+1 * delta(x-a) = a^2+3a+1",
    simplify(sift_result - (a_val**2 + 3*a_val + 1)) == 0
)

# Sifting with f(x) = sin(x): integral sin(x)*delta(x-pi/2) = sin(pi/2) = 1
sift_sin = integrate(sin(x_int) * DiracDelta(x_int - pi/2), (x_int, -oo, oo))
check(
    "[Classical] Dirac: sifting integral sin(x)*delta(x-pi/2) = 1",
    simplify(sift_sin - 1) == 0
)

# Sifting with f(x) = exp(x): integral exp(x)*delta(x-2) = exp(2)
sift_exp = integrate(exp(x_int) * DiracDelta(x_int - 2), (x_int, -oo, oo))
check(
    "[Classical] Dirac: sifting integral exp(x)*delta(x-2) = e^2",
    simplify(sift_exp - exp(2)) == 0
)

# Sifting with f(x) = cos(x): integral cos(x)*delta(x) = cos(0) = 1
sift_cos = integrate(cos(x_int) * DiracDelta(x_int), (x_int, -oo, oo))
check(
    "[Classical] Dirac: sifting integral cos(x)*delta(x) = 1",
    simplify(sift_cos - 1) == 0
)

# Scaling property: delta(a*x) = delta(x)/|a|
# Verified via: integral delta(a*x) f(x) dx = f(0)/|a|
a_pos = symbols('ap', positive=True)
scale_lhs = integrate(DiracDelta(a_pos * x_int) * (x_int**2 + 1), (x_int, -oo, oo))
scale_rhs = (0**2 + 1) / a_pos
check(
    "[Classical] Dirac: delta(a*x) scaling integral gives f(0)/|a|",
    simplify(scale_lhs - scale_rhs) == 0
)

# Scaling with a=2
scale_2 = integrate(DiracDelta(2*x_int) * exp(x_int), (x_int, -oo, oo))
check(
    "[Classical] Dirac: delta(2x) scaling: integral exp(x)*delta(2x)dx = 1/2",
    simplify(scale_2 - Rational(1,2)) == 0
)

# Delta as derivative of Heaviside: d/dx Heaviside(x) = DiracDelta(x)
dH = sp.diff(Heaviside(x_int), x_int)
check(
    "[Classical] Dirac: d/dx Heaviside(x) = DiracDelta(x)",
    simplify(dH - DiracDelta(x_int)) == 0
)

# Height * width = 1 invariant for rectangular nascent delta
# height = 1/(2*eps), width = 2*eps, product = 1
height_rect = Rational(1,2) / eps_sym
width_rect = 2 * eps_sym
check(
    "[Classical] Dirac: rectangular delta height * width = 1 (A3 invariant)",
    simplify(height_rect * width_rect - 1) == 0
)

# Height * width = 1 for Gaussian (peak height = 1/(eps*sqrt(pi)), effective width = eps*sqrt(pi))
height_gauss = 1 / (eps_sym * sqrt(pi))
width_gauss = eps_sym * sqrt(pi)
check(
    "[Classical] Dirac: Gaussian delta height * width = 1 (A3 invariant)",
    simplify(height_gauss * width_gauss - 1) == 0
)

# Composition: delta(f(x)) = sum_i delta(x-x_i)/|f'(x_i)|
# For f(x) = x^2 - 1, zeros at x=±1, f'(x)=2x
# delta(x^2-1) = delta(x-1)/(2) + delta(x+1)/(2)
f_compose = x_int**2 - 1
check(
    "[Classical] Dirac: delta(x^2-1) has roots at x=±1",
    sp.solve(f_compose, x_int) == [-1, 1]
)

# Verify numerically via integration: integral g(x)*delta(x^2-1) dx = g(1)/2 + g(-1)/2
# For g(x) = x^2: result = 1/2 + 1/2 = 1
compose_result = integrate(x_int**2 * DiracDelta(x_int**2 - 1), (x_int, -oo, oo))
check(
    "[Classical] Dirac: integral x^2 * delta(x^2-1) dx = 1",
    simplify(compose_result - 1) == 0
)

# Even symmetry: delta(-x) = delta(x)
sym_check = integrate(exp(x_int) * DiracDelta(-x_int - 1), (x_int, -oo, oo))
# delta(-x-1) = delta(x+1)/|-1| = delta(x+1), so integral = exp(-1)
check(
    "[Classical] Dirac: delta(-x-1) = delta(x+1), integral exp(x)*delta(-x-1)dx = e^{-1}",
    simplify(sym_check - exp(-1)) == 0
)


# ============================================================
# DOMAIN 4: REMOVABLE SINGULARITIES
# ============================================================
"""
IVNA CONTRIBUTION: A removable singularity is a 0/0 form where both
numerator and denominator vanish. IVNA's A8 axiom reads off the limit
as the index ratio: 0_{f} / 0_{g} = f/g at the index level, which is
exactly what L'Hôpital's rule or Taylor expansion computes.
"""

x_lim = symbols('xl', real=True)

# sin(x)/x -> 1 as x->0
lim_sinc = limit(sin(x_lim)/x_lim, x_lim, 0)
check(
    "[Classical] Removable: lim_{x->0} sin(x)/x = 1",
    lim_sinc == 1
)

# (exp(x)-1)/x -> 1 as x->0
lim_exp = limit((exp(x_lim)-1)/x_lim, x_lim, 0)
check(
    "[Classical] Removable: lim_{x->0} (e^x-1)/x = 1",
    lim_exp == 1
)

# (1-cos(x))/x^2 -> 1/2 as x->0
lim_cos = limit((1-cos(x_lim))/x_lim**2, x_lim, 0)
check(
    "[Classical] Removable: lim_{x->0} (1-cos(x))/x^2 = 1/2",
    lim_cos == Rational(1,2)
)

# tan(x)/x -> 1 as x->0
lim_tan = limit(tan(x_lim)/x_lim, x_lim, 0)
check(
    "[Classical] Removable: lim_{x->0} tan(x)/x = 1",
    lim_tan == 1
)

# (ln(1+x))/x -> 1 as x->0
lim_ln = limit(ln(1+x_lim)/x_lim, x_lim, 0)
check(
    "[Classical] Removable: lim_{x->0} ln(1+x)/x = 1",
    lim_ln == 1
)

# (x^n - a^n)/(x - a) -> n*a^(n-1) as x->a (for n=2, a=3)
lim_power = limit((x_lim**2 - 9)/(x_lim - 3), x_lim, 3)
check(
    "[Classical] Removable: lim_{x->3} (x^2-9)/(x-3) = 6",
    lim_power == 6
)

# (x^3 - 8)/(x - 2) -> 12 as x->2
lim_cube = limit((x_lim**3 - 8)/(x_lim - 2), x_lim, 2)
check(
    "[Classical] Removable: lim_{x->2} (x^3-8)/(x-2) = 12",
    lim_cube == 12
)

# sin(3x)/sin(5x) -> 3/5 as x->0
lim_sinsin = limit(sin(3*x_lim)/sin(5*x_lim), x_lim, 0)
check(
    "[Classical] Removable: lim_{x->0} sin(3x)/sin(5x) = 3/5",
    lim_sinsin == Rational(3,5)
)

# Series verification: sin(x)/x leading term via Taylor
sin_series = series(sin(x_lim), x_lim, 0, 4)
check(
    "[Classical] Removable: Taylor sin(x) = x - x^3/6 + O(x^4) confirms sinc limit",
    sin_series.coeff(x_lim, 1) == 1
)

# Series: (exp(x)-1)/x: limit as x->0 is 1
exp_m1_lim = limit((exp(x_lim) - 1)/x_lim, x_lim, 0)
check(
    "[Classical] Removable: Taylor (e^x-1)/x leading term = 1",
    exp_m1_lim == 1
)

# Removable singularity at x=1: (x^2-1)/(x-1) = x+1, limit = 2
lim_quad = limit((x_lim**2 - 1)/(x_lim - 1), x_lim, 1)
check(
    "[Classical] Removable: lim_{x->1} (x^2-1)/(x-1) = 2",
    lim_quad == 2
)

# (sqrt(x)-1)/(x-1) -> 1/2 as x->1
lim_sqrt = limit((sqrt(x_lim) - 1)/(x_lim - 1), x_lim, 1)
check(
    "[Classical] Removable: lim_{x->1} (sqrt(x)-1)/(x-1) = 1/2",
    lim_sqrt == Rational(1,2)
)


# ============================================================
# DOMAIN 5: INFINITY SUBTRACTION
# ============================================================
"""
IVNA CONTRIBUTION: Standard math treats inf - inf as undefined.
IVNA's A11 axiom makes the operation determinate via index arithmetic:
inf_a - inf_b = inf_{a-b} (when a>b), and more generally a/eps - b/eps
= (a-b)/eps. The result carries the index and is algebraically operable.
"""

a_sym, b_sym, c_sym = symbols('a b c', real=True)
eps_pos = symbols('e', positive=True)

# a/eps - b/eps = (a-b)/eps via sympy.simplify
inf_sub_1 = simplify(a_sym/eps_pos - b_sym/eps_pos - (a_sym - b_sym)/eps_pos)
check(
    "[Classical] InfSub: a/eps - b/eps = (a-b)/eps",
    inf_sub_1 == 0
)

# 3/eps - 2/eps = 1/eps
inf_sub_2 = simplify(3/eps_pos - 2/eps_pos - 1/eps_pos)
check(
    "[Classical] InfSub: 3/eps - 2/eps = 1/eps",
    inf_sub_2 == 0
)

# 5/eps - 5/eps = 0 (D-INDEX-ZERO analogue)
inf_sub_3 = simplify(5/eps_pos - 5/eps_pos)
check(
    "[Classical] InfSub: 5/eps - 5/eps = 0",
    inf_sub_3 == 0
)

# (a/eps - b/eps)*eps = a-b (retrieves finite value)
retrieval = simplify((a_sym/eps_pos - b_sym/eps_pos) * eps_pos - (a_sym - b_sym))
check(
    "[Classical] InfSub: (a/eps - b/eps)*eps = a-b",
    retrieval == 0
)

# Limit approach: lim_{eps->0}(1/eps - 2/eps)*eps = -1
lim_inf_sub = limit((1/eps_pos - 2/eps_pos) * eps_pos, eps_pos, 0)
check(
    "[Classical] InfSub: lim (1/eps - 2/eps)*eps = -1",
    lim_inf_sub == -1
)

# Associativity: (a/eps - b/eps) - c/eps = (a-b-c)/eps
inf_sub_assoc = simplify((a_sym/eps_pos - b_sym/eps_pos) - c_sym/eps_pos - (a_sym - b_sym - c_sym)/eps_pos)
check(
    "[Classical] InfSub: (a/eps - b/eps) - c/eps = (a-b-c)/eps",
    inf_sub_assoc == 0
)


# ============================================================
# DOMAIN 6: RESIDUE EXTRACTION
# ============================================================
"""
IVNA CONTRIBUTION: The residue of f at z0 is classically computed
as lim_{z->z0} (z-z0)*f(z). In IVNA, at a simple pole f(z) behaves
as inf_{g(z)} = g(z)/0_{z-z0}. Then A3 gives (z-z0)*f(z) = 0_{z-z0} *
inf_{g(z)} = g(z) — the residue emerges from a single axiom application.
"""

z_sym = symbols('z')

# Simple pole at z=0: f(z) = 1/z, residue = 1
res_1 = limit(z_sym * (1/z_sym), z_sym, 0)
check(
    "[Classical] Residue: Res[1/z, z=0] = 1",
    res_1 == 1
)

# Simple pole at z=1: f(z) = 1/(z-1), residue = 1
res_2 = limit((z_sym - 1) * (1/(z_sym - 1)), z_sym, 1)
check(
    "[Classical] Residue: Res[1/(z-1), z=1] = 1",
    res_2 == 1
)

# Pole at z=2: f(z) = 3/(z-2), residue = 3
res_3 = limit((z_sym - 2) * (3/(z_sym - 2)), z_sym, 2)
check(
    "[Classical] Residue: Res[3/(z-2), z=2] = 3",
    res_3 == 3
)

# Simple pole of 1/((z-1)(z+1)) at z=1: residue = 1/2
res_4 = limit((z_sym - 1) * (1/((z_sym-1)*(z_sym+1))), z_sym, 1)
check(
    "[Classical] Residue: Res[1/((z-1)(z+1)), z=1] = 1/2",
    res_4 == Rational(1,2)
)

# Pole at z=-1: residue = -1/2
res_5 = limit((z_sym + 1) * (1/((z_sym-1)*(z_sym+1))), z_sym, -1)
check(
    "[Classical] Residue: Res[1/((z-1)(z+1)), z=-1] = -1/2",
    res_5 == Rational(-1,2)
)

# f(z) = z/(z^2+1) has poles at z=±i; residue at z=i is 1/2
z_c = symbols('zc')
f_poles_i = z_c / (z_c**2 + 1)
res_6 = limit((z_c - sp.I) * f_poles_i, z_c, sp.I)
check(
    "[Classical] Residue: Res[z/(z^2+1), z=i] = 1/2",
    simplify(res_6 - Rational(1,2)) == 0
)

# f(z) = exp(z)/(z-1): residue at z=1 is exp(1)
res_7 = limit((z_sym - 1) * exp(z_sym)/(z_sym - 1), z_sym, 1)
check(
    "[Classical] Residue: Res[exp(z)/(z-1), z=1] = e",
    simplify(res_7 - sp.E) == 0
)

# Simplify approach: cancel factor directly
f_cancel = cancel(z_sym/(z_sym*(z_sym+1)))
check(
    "[Classical] Residue: cancel(z/(z*(z+1))) = 1/(z+1)",
    simplify(f_cancel - 1/(z_sym+1)) == 0
)

# Double pole: f(z) = 1/z^2; residue at z=0 via d/dz[(z^2)*(1/z^2)] = d/dz[1] = 0
double_pole_res = sp.diff(z_sym**2 * (1/z_sym**2), z_sym)
check(
    "[Classical] Residue: Res[1/z^2, z=0] = 0 (double pole residue formula)",
    simplify(double_pole_res) == 0
)

# f(z) = sin(z)/z^2 has a simple pole at z=0; residue = cos(0) = 1
res_sinc_pole = limit(z_sym * (sin(z_sym)/z_sym**2), z_sym, 0)
check(
    "[Classical] Residue: Res[sin(z)/z^2, z=0] = 1",
    res_sinc_pole == 1
)

# f(z) = (z^2-1)/(z-1) = z+1 — removable, residue = 0
f_removable = cancel((z_sym**2-1)/(z_sym-1))
check(
    "[Classical] Residue: (z^2-1)/(z-1) cancels to z+1 (no pole, residue=0)",
    simplify(f_removable - (z_sym+1)) == 0
)

# Sum of residues: Res[1/((z-1)(z-2)), z=1] + Res[z=2] = 0 (rational function)
res_sum_1 = limit((z_sym-1)/(((z_sym-1)*(z_sym-2))), z_sym, 1)
res_sum_2 = limit((z_sym-2)/(((z_sym-1)*(z_sym-2))), z_sym, 2)
check(
    "[Classical] Residue: Res[1/((z-1)(z-2))] sum = Res_1 + Res_2 = -1 + 1 = 0",
    simplify(res_sum_1 + res_sum_2) == 0
)


# ============================================================
# DOMAIN 7: COMPOUND GROWTH
# ============================================================
"""
IVNA CONTRIBUTION: The limit lim_{m->inf}(1 + x/m)^m = e^x is exactly
IVNA's A-EXP axiom: (1 + 0_x)^{inf_1} = e^x. The index arithmetic
says (1 + 0_{x/m})^{m} where 0_{x/m} * inf_1 = x/m * 1 = x/m at
finite m, but at the virtual level 0_{x/m} * inf_m = x. A-EXP is the
direct algebraic encoding of this limit identity.
"""

m_pos = symbols('mp', positive=True, integer=True)
x_exp = symbols('xe', real=True)

# lim_{m->inf} (1 + x/m)^m = e^x for several values of x
for x_val in [1, 2, -1, Rational(1,2)]:
    lim_growth = limit((1 + x_val/m_pos)**m_pos, m_pos, oo)
    check(
        f"[Classical] CompoundGrowth: lim_m (1+{x_val}/m)^m = e^{x_val}",
        simplify(lim_growth - exp(x_val)) == 0
    )

# lim_{m->inf} (1 + 1/m)^m = e
lim_e = limit((1 + 1/m_pos)**m_pos, m_pos, oo)
check(
    "[Classical] CompoundGrowth: lim_m (1+1/m)^m = e",
    simplify(lim_e - sp.E) == 0
)

# Verify (1 + x/(n*m))^(n*m) -> e^x for n=2, x=1
n_pos = symbols('np', positive=True, integer=True)
lim_nm = limit((1 + 1/(2*m_pos))**(2*m_pos), m_pos, oo)
check(
    "[Classical] CompoundGrowth: lim_m (1+1/(2m))^(2m) = e",
    simplify(lim_nm - sp.E) == 0
)

# Verify (1 + x/(n*m))^(n*m) -> e^x for n=3, x=2
lim_nm2 = limit((1 + 2/(3*m_pos))**(3*m_pos), m_pos, oo)
check(
    "[Classical] CompoundGrowth: lim_m (1+2/(3m))^(3m) = e^2",
    simplify(lim_nm2 - exp(2)) == 0
)

# e^x * e^y = e^(x+y): index arithmetic analogue
x1, x2 = symbols('x1 x2', real=True)
check(
    "[Classical] CompoundGrowth: e^x1 * e^x2 = e^(x1+x2)",
    simplify(exp(x1) * exp(x2) - exp(x1+x2)) == 0
)

# (e^x)^n = e^(nx): A-EXP scaling
check(
    "[Classical] CompoundGrowth: (e^x)^n = e^(nx)",
    simplify(exp(x_exp)**n - exp(n*x_exp)) == 0
)

# d/dx e^x = e^x (exponential is its own derivative)
check(
    "[Classical] CompoundGrowth: d/dx e^x = e^x",
    simplify(sp.diff(exp(x_exp), x_exp) - exp(x_exp)) == 0
)

# lim_{m->inf} (1 + x/m)^m / e^x = 1 (ratio form)
lim_ratio = limit((1 + 1/m_pos)**m_pos / sp.E, m_pos, oo)
check(
    "[Classical] CompoundGrowth: lim_m (1+1/m)^m / e = 1",
    simplify(lim_ratio - 1) == 0
)


# ============================================================
# DOMAIN 8: BLOW-UP
# ============================================================
"""
IVNA CONTRIBUTION: Algebraic blow-up resolves singularities by
introducing a new coordinate that trades 0/0 for a finite ratio.
In IVNA, this is a direct application of A8: 0_{num} / 0_{denom} = num/denom.
A-EXP and A8 together handle the projective-coordinate structure of blow-ups.
"""

t_blowup = symbols('tb', real=True, nonzero=True)
x_blowup = symbols('xb', real=True, nonzero=True)

# Blow-up of x^2+y^2 at origin: substitute y=t*x
# (x^2 + t^2*x^2) / (x * t * x) = (1+t^2)/t
blowup_num = x_blowup**2 + t_blowup**2 * x_blowup**2
blowup_denom = x_blowup * t_blowup * x_blowup
blowup_expr = simplify(blowup_num / blowup_denom)
check(
    "[Classical] BlowUp: (x^2+t^2*x^2)/(x*t*x) = (1+t^2)/t",
    simplify(blowup_expr - (1 + t_blowup**2)/t_blowup) == 0
)

# Factor and cancel: (x^3-y^3)/(x-y) = x^2+xy+y^2
y_blowup = symbols('yb', real=True)
x_b, y_b = symbols('xb2 yb2', real=True)
diff_cubes = factor(x_b**3 - y_b**3)
cancel_expr = cancel((x_b**3 - y_b**3)/(x_b - y_b))
check(
    "[Classical] BlowUp: (x^3-y^3)/(x-y) = x^2+xy+y^2",
    simplify(cancel_expr - (x_b**2 + x_b*y_b + y_b**2)) == 0
)

# (x^2-y^2)/(x-y) = x+y
cancel_sq = cancel((x_b**2 - y_b**2)/(x_b - y_b))
check(
    "[Classical] BlowUp: (x^2-y^2)/(x-y) = x+y",
    simplify(cancel_sq - (x_b + y_b)) == 0
)

# Blow-up of xy=0 node: substitute y=t*x, get x*(tx) = x^2*t; on x≠0, reduces to t=0 or x=0
node_expr = simplify(x_blowup * t_blowup * x_blowup / x_blowup**2)
check(
    "[Classical] BlowUp: xy=0 node blown up: x*(tx)/x^2 = t (coordinate on exceptional divisor)",
    simplify(node_expr - t_blowup) == 0
)

# Projective blow-up: (x,y) -> (x, y/x) on x≠0
# f(x,y) = x^2+xy simplifies to x^2(1+t) where t=y/x
t_proj = symbols('tp', real=True)
f_blowup_proj = x_blowup**2 + x_blowup*(t_proj*x_blowup)
check(
    "[Classical] BlowUp: x^2+xy = x^2(1+t) under y=tx substitution",
    simplify(f_blowup_proj - x_blowup**2*(1+t_proj)) == 0
)

# Factor x^4-1
check(
    "[Classical] BlowUp: x^4-1 = (x-1)(x+1)(x^2+1)",
    simplify(factor(x_b**4 - 1) - (x_b-1)*(x_b+1)*(x_b**2+1)) == 0
)

# Rational simplification: (x^2-4)/(x-2) simplifies and limit at x=2 = 4
lim_blowup = limit((x_blowup**2 - 4)/(x_blowup - 2), x_blowup, 2)
check(
    "[Classical] BlowUp: lim_{x->2} (x^2-4)/(x-2) = 4",
    lim_blowup == 4
)

# Blow-up resolves: (x^2+y^2-1) at (1,0) with y=t*(x-1)
# Near x=1: x=1+h, y=t*h => (1+h)^2 + t^2*h^2 - 1 = 2h + h^2 + t^2*h^2
# Divide by h: 2 + h + t^2*h -> 2 as h->0 (resolved)
h_sym = symbols('h', real=True)
t_res = symbols('tr', real=True)
circle_blowup = ((1+h_sym)**2 + t_res**2*h_sym**2 - 1)/h_sym
lim_circle = limit(circle_blowup, h_sym, 0)
check(
    "[Classical] BlowUp: circle singularity blown up resolves to 2 at h->0",
    lim_circle == 2
)


# ============================================================
# DOMAIN 9: KL DIVERGENCE
# ============================================================
"""
IVNA CONTRIBUTION: KL divergence involves the term p(x)*log(p(x)/q(x)),
which has a boundary form 0*log(0) when p(x)->0. IVNA's D-INDEX-ZERO
+ A3 handle this: 0_p * log(0_p / 0_q) = 0_p * log(p/q index ratio).
The boundary contribution is exactly lim eps*log(eps) = 0, which A3
captures as the product of a zero and a logarithmically-diverging infinity
resolving to 0.
"""

eps_kl = symbols('ek', positive=True)

# Key boundary term: lim_{eps->0+} eps*ln(eps) = 0
lim_epslogeps = limit(eps_kl * ln(eps_kl), eps_kl, 0, '+')
check(
    "[Classical] KL: lim_{eps->0+} eps*ln(eps) = 0",
    lim_epslogeps == 0
)

# lim_{eps->0+} eps^2 * ln(eps) = 0 (stronger zero wins)
lim_eps2logeps = limit(eps_kl**2 * ln(eps_kl), eps_kl, 0, '+')
check(
    "[Classical] KL: lim_{eps->0+} eps^2*ln(eps) = 0",
    lim_eps2logeps == 0
)

# KL divergence between two Bernoulli distributions
# KL(p||q) = p*log(p/q) + (1-p)*log((1-p)/(1-q))
p_bern, q_bern = Rational(1,3), Rational(1,2)
kl_bernoulli = p_bern*ln(p_bern/q_bern) + (1-p_bern)*ln((1-p_bern)/(1-q_bern))
check(
    "[Classical] KL: KL(Bernoulli(1/3) || Bernoulli(1/2)) > 0",
    kl_bernoulli > 0
)

# KL(p||p) = 0 (same distribution)
p_sym = symbols('ps', positive=True)
q_sym = symbols('qs', positive=True)
kl_same = simplify(p_sym*ln(p_sym/p_sym) + (1-p_sym)*ln((1-p_sym)/(1-p_sym)))
check(
    "[Classical] KL: KL(p||p) = 0",
    kl_same == 0
)

# KL non-negativity via log inequality: ln(u) <= u-1 => -ln(q/p) >= 1 - q/p
# Equivalently, ln(p/q) >= 1 - q/p, so p*ln(p/q) >= p*(1-q/p) = p-q
# Sum over support -> KL >= 0 (Gibbs' inequality)
# Verify for specific values: p=0.3, q=0.7
from sympy import Float
p_val, q_val = Float('0.3'), Float('0.7')
kl_check = p_val * ln(p_val/q_val) + (1-p_val)*ln((1-p_val)/(1-q_val))
check(
    "[Classical] KL: KL(Bernoulli(0.3)||Bernoulli(0.7)) > 0",
    float(kl_check) > 0
)

# KL is not symmetric: KL(p||q) ≠ KL(q||p) in general
kl_pq = p_bern*ln(p_bern/q_bern) + (1-p_bern)*ln((1-p_bern)/(1-q_bern))
kl_qp = q_bern*ln(q_bern/p_bern) + (1-q_bern)*ln((1-q_bern)/(1-p_bern))
check(
    "[Classical] KL: KL(p||q) ≠ KL(q||p) in general",
    simplify(kl_pq - kl_qp) != 0
)

# For uniform distributions (equal): KL(U||U) = 0
# KL between Uniform(a,b) and itself: integral of (1/(b-a))*log(1) dx = 0
a_u, b_u = symbols('au bu', real=True)
kl_uniform_self = integrate(
    (1/(b_u - a_u)) * ln(Rational(1,1)),
    (x, a_u, b_u)
)
check(
    "[Classical] KL: KL(Uniform||Uniform same) = 0",
    kl_uniform_self == 0
)

# Boundary: p*log(p/q) -> 0 as p->0+ for fixed q>0 (key boundary term)
p_lim = symbols('pl', positive=True)
q_fixed = Rational(1,2)
boundary_kl = limit(p_lim * ln(p_lim / q_fixed), p_lim, 0, '+')
check(
    "[Classical] KL: lim_{p->0+} p*ln(p/q) = 0 for fixed q>0",
    boundary_kl == 0
)

# Cross-entropy H(p,q) = -sum p*log(q) >= H(p) (Shannon entropy)
# For Bernoulli(1/3) vs Bernoulli(1/2):
# H(p) = -1/3*log(1/3) - 2/3*log(2/3)
# H(p,q) = -1/3*log(1/2) - 2/3*log(1/2) = log(2) = H(p) + KL(p||q)
H_p = -p_bern*ln(p_bern) - (1-p_bern)*ln(1-p_bern)
H_pq = -p_bern*ln(q_bern) - (1-p_bern)*ln(1-q_bern)
check(
    "[Classical] KL: H(p,q) = H(p) + KL(p||q)",
    simplify(H_pq - H_p - kl_pq) == 0
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "="*60)
print("CATEGORY C: CLASSICAL CORRESPONDENCE")
print("(These verify notation maps onto known results)")
print("="*60)

for status, name in results:
    marker = "PASS" if status == "PASS" else "FAIL"
    print(f"  [{marker}] {name}")

total = passed + failed
print()
print(f"  Total: {total}  |  Passed: {passed}  |  Failed: {failed}")
print("="*60)

if failed == 0:
    print("  ALL CHECKS PASSED")
else:
    print(f"  {failed} CHECK(S) FAILED")

sys.exit(0 if failed == 0 else 1)
