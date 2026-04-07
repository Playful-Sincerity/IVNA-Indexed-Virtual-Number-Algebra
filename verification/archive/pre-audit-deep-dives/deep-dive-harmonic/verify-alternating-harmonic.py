"""Verify alternating harmonic series = ln(2) and paired form."""
from sympy import *

k = Symbol('k')

# Exact symbolic result
alt_sum = Sum((-1)**(k+1)/k, (k, 1, oo)).doit()
print(f"Sum(-1)^(k+1)/k = {alt_sum} = {N(alt_sum, 20)}")
print(f"ln(2)            = {N(log(2), 20)}")
print(f"Match: {simplify(alt_sum - log(2)) == 0}")

# Paired form: 1/((2j-1)(2j)) = 1/(2j-1) - 1/(2j)
print("\n=== Paired form verification ===")
for N_val in [100, 1000, 10000]:
    paired = sum(Rational(1, (2*j-1)*(2*j)) for j in range(1, N_val+1))
    direct = sum(Rational((-1)**(j+1), j) for j in range(1, 2*N_val+1))
    print(f"N={N_val}: paired = {float(paired):.12f}, direct(2N terms) = {float(direct):.12f}, match: {paired == direct}")

# Partial fraction decomposition
print(f"\n1/((2k-1)(2k)) = {apart(1/((2*k-1)*(2*k)), k)}")

# Bound: paired terms decay like 1/k^2
print("\n=== Decay rate comparison ===")
for j in [10, 100, 1000]:
    exact = 1.0 / ((2*j-1)*(2*j))
    bound = 1.0 / (4*j**2)
    print(f"j={j}: 1/((2j-1)(2j)) = {exact:.6e}, 1/(4j^2) = {bound:.6e}, ratio = {exact/bound:.6f}")
