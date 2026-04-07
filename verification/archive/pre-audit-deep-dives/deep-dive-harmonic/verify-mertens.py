"""Verify Mertens' theorem for prime reciprocal sums."""
from sympy import *
from sympy import primerange

print("=== Sum 1/p for p <= n vs ln(ln(n)) + M ===")
print(f"Mertens constant M ~ 0.2614972128...")
print(f"gamma = {float(EulerGamma):.10f}")
print()

for N in [100, 1000, 10000, 100000]:
    s = sum(1.0 / p for p in primerange(2, N + 1))
    lnln = float(log(log(N)))
    M_est = s - lnln
    print(f"N={N:>6}: Sum 1/p = {s:.8f}, ln(ln(N)) = {lnln:.8f}, M_est = {M_est:.8f}")

print()
print("=== Connection: M = gamma + sum_p (ln(1-1/p) + 1/p) ===")
correction = sum(float(log(1 - 1.0 / p) + 1.0 / p) for p in primerange(2, 100001))
print(f"gamma = {float(EulerGamma):.10f}")
print(f"correction sum (primes <= 100000) = {correction:.10f}")
print(f"gamma + correction = {float(EulerGamma) + correction:.10f}")
print(f"M literature value = 0.2614972128")
