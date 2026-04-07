"""Verify digamma function properties relevant to IVNA."""
from sympy import *

x = Symbol('x', positive=True)

# psi(1) = -gamma
print("=== psi(1) = -gamma ===")
print(f"psi(1) = {N(digamma(1), 20)}")
print(f"-gamma = {N(-EulerGamma, 20)}")
print(f"Match: {simplify(digamma(1) + EulerGamma) == 0}")

# psi(n) = -gamma + H_{n-1}
print("\n=== psi(n) = -gamma + H_{n-1} ===")
for nn in range(1, 8):
    Hn_minus_1 = sum(Rational(1, k) for k in range(1, nn)) if nn > 1 else 0
    psi_val = float(N(digamma(nn), 15))
    expected = float(Hn_minus_1 - EulerGamma)
    err = abs(psi_val - expected)
    print(f"psi({nn}) = {psi_val:.12f}, -gamma + H_{nn-1} = {expected:.12f}, err = {err:.2e}")

# psi(1/2) = -gamma - 2*ln(2)
print(f"\n=== psi(1/2) ===")
print(f"psi(1/2) = {N(digamma(Rational(1, 2)), 20)}")
print(f"-gamma - 2*ln(2) = {N(-EulerGamma - 2*log(2), 20)}")

# gamma integral representation
print("\n=== gamma = -integral e^{-x} ln(x) dx ===")
val = -integrate(exp(-x) * log(x), (x, 0, oo))
print(f"Result: {val}")
print(f"= EulerGamma: {val == EulerGamma}")

# Laurent expansion showing pole cancellation
print("\n=== 1/h + 1/ln(1-h) Laurent expansion ===")
h = Symbol('h')
s = series(1/h + 1/log(1-h), h, 0, 6)
print(f"1/h + 1/ln(1-h) = {s}")
print("(The 1/h poles cancel, leaving constant 1/2)")
