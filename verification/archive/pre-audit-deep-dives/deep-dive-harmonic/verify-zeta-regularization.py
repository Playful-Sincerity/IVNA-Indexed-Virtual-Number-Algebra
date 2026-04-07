"""Verify zeta regularization vs IVNA partial sums."""
from sympy import *

# Partial sum formula
print("=== Sum 1+2+...+n = n(n+1)/2 ===")
for val in [10, 100, 1000]:
    formula = val * (val + 1) // 2
    direct = sum(range(1, val + 1))
    print(f"S_{val} = {formula}, direct = {direct}, match: {formula == direct}")

# Zeta at negative integers
print("\n=== Zeta at negative integers ===")
for n in range(0, 8):
    zv = zeta(-n)
    bn1 = bernoulli(n + 1)
    formula_val = (-1)**n * bn1 / (n + 1)
    print(f"zeta(-{n}) = {zv}, (-1)^{n} * B_{n+1}/{n+1} = {formula_val}")

# Bernoulli numbers
print("\n=== Bernoulli numbers ===")
for n in range(0, 14):
    print(f"B_{n} = {bernoulli(n)}")

# Ramanujan summation check
print("\n=== Ramanujan sum of 1+2+3+... ===")
print("For f(k) = k: Ramanujan sum = -B_2/2 * f'(0)")
print(f"= -(1/6)/2 * 1 = {Rational(-1, 12)}")
print(f"zeta(-1) = {zeta(-1)}")
print(f"Match: {zeta(-1) == Rational(-1, 12)}")
