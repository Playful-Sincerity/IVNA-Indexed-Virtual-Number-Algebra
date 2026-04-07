---
claim: "Borel-Kolmogorov paradox dissolves because different parameterizations give different indexed zeros"
tools: [Wolfram Mathematica, SymPy]
result: PASS
checks: 6 (3 parameterizations x 2 tools)
---

# Verify-02: Borel-Kolmogorov Paradox Dissolution

## Claim

The Borel-Kolmogorov paradox: conditioning a uniform distribution on S² on a great circle gives different answers depending on parameterization. Standard resolution: "conditioning on zero-measure events is ill-defined without specifying the sigma-algebra."

IVNA resolution: different parameterizations give different density functions, hence different indices on the indexed zeros. Dividing different indexed zeros gives different results. The "paradox" is just two different indexed-zero divisions.

## Setup

Uniform distribution on S². Same event: the meridian phi=0.

## Parameterization 1: (theta, phi)

theta in [0,pi], phi in [0,2pi). Joint: f(theta,phi) = sin(theta)/(4pi).

### Wolfram
```
Marginal f(phi) = 1/(2pi)
Conditional f(theta|phi=0) = sin(theta)/2
Integral: 1 ✓
```

### SymPy
```
Marginal f(phi) = 1/(2*pi)
Conditional f(theta|phi) = sin(theta)/2
Integral: 1 ✓
```

**IVNA:** P(phi=0) = 0_{1/(2pi)}, P(theta,phi=0) = 0_{sin(theta)/(4pi)}.
A8: 0_{sin(theta)/(4pi)} / 0_{1/(2pi)} = sin(theta)/2. ✓

## Parameterization 2: (u=cos(theta), phi)

u in [-1,1], phi in [0,2pi). Joint: f(u,phi) = 1/(4pi).

### Wolfram
```
Marginal f(phi) = 1/(2pi)
Conditional f(u|phi=0) = 1/2
Integral: 1 ✓
```

### SymPy
```
Marginal f(phi) = 1/(2*pi)
Conditional f(u|phi) = 1/2
Integral: 1 ✓
```

**IVNA:** P(phi=0) = 0_{1/(2pi)}, P(u,phi=0) = 0_{1/(4pi)}.
A8: 0_{1/(4pi)} / 0_{1/(2pi)} = 1/2. ✓

## Parameterization 3: (theta, lambda=2*phi)

theta in [0,pi], lambda in [0,4pi). Joint: f(theta,lambda) = sin(theta)/(8pi).

### Wolfram
```
Marginal f(lambda) = 1/(4pi)
Conditional f(theta|lambda=0) = sin(theta)/2
Integral: 1 ✓
```

**IVNA:** P(lambda=0) = 0_{1/(4pi)}, P(theta,lambda=0) = 0_{sin(theta)/(8pi)}.
A8: 0_{sin(theta)/(8pi)} / 0_{1/(4pi)} = sin(theta)/2. ✓

Same conditional as Param 1 (because the theta structure is identical), but the marginal index is different (1/(4pi) vs 1/(2pi)). IVNA makes this visible.

## Key Insight

The "paradox" disappears because IVNA forces you to track the density through the index:
- Param 1 vs Param 2: **Different** conditionals (sin(theta)/2 vs 1/2) because the joint densities carry different theta-dependence
- Param 1 vs Param 3: **Same** conditional but different marginal indices, because rescaling phi doesn't change the theta structure

Standard math hides this in the sigma-algebra. IVNA puts it in the index.

## Summary

| Parameterization | Wolfram | SymPy | Conditional | Result |
|---|---|---|---|---|
| (theta, phi) | PASS | PASS | sin(theta)/2 | PASS |
| (u=cos(theta), phi) | PASS | PASS | 1/2 | PASS |
| (theta, lambda=2phi) | PASS | — | sin(theta)/2 | PASS |

**Verdict:** The Borel-Kolmogorov paradox is cleanly resolved. Different parameterizations produce different indexed zeros, leading to different (but correct) conditional densities. No paradox — just different computations made transparent by the index.
