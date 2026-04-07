"""Verify H_n asymptotics and convergence to gamma."""
from sympy import *

print("=== H_n - ln(n) convergence to gamma ===")
for val in [10, 100, 1000, 10000, 100000]:
    Hn = sum(Rational(1, k) for k in range(1, val + 1))
    diff = float(Hn - log(val))
    err = abs(diff - float(EulerGamma))
    asymp = float(Rational(1, 2 * val))
    print(f"H_{val} - ln({val}) = {diff:.12f}")
    print(f"  error from gamma = {err:.2e}, expected ~1/(2n) = {asymp:.2e}")

print(f"\ngamma = {N(EulerGamma, 30)}")

# Euler-Maclaurin asymptotic terms
print("\n=== Euler-Maclaurin corrections ===")
n_val = 10000
Hn = sum(Rational(1, k) for k in range(1, n_val + 1))
remainder = float(Hn - log(n_val))
cumulative = float(EulerGamma)
print(f"H_{n_val} - ln({n_val}) = {remainder:.15f}")
print(f"gamma                  = {cumulative:.15f}")
print(f"gamma + 1/(2n)         = {cumulative + 1/(2*n_val):.15f}")
print(f"gamma + 1/(2n) - 1/(12n^2) = {cumulative + 1/(2*n_val) - 1/(12*n_val**2):.15f}")
