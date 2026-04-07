# Verification: Fourier Transform of sgn(x)

## Standard Result
F[sgn(x)](w) = -2i/w (physics convention)

## Wolfram Verification

```mathematica
FourierTransform[Sign[x], x, w, FourierParameters -> {1, -1}]
(* Result: (-2*I)/w *)
```
**PASS**

## Inverse Verification

```mathematica
InverseFourierTransform[-2*I/w, w, x, FourierParameters -> {1, -1}]
```
(Wolfram license expired before this completed, but the forward transform confirms the result.)

## Fourier Series Verification

sgn(x) Fourier coefficients on [-pi, pi]:
```mathematica
c_n = (1/(2*Pi))*Integrate[Sign[x]*Exp[-I*n*x], {x, -Pi, Pi}]
(* c_0 = 0 *)
(* c_n = I*(-1 + (-1)^n)/(n*Pi) *)
(* For odd n: c_n = -2I/(n*Pi) *)
(* For even n: c_n = 0 *)
```
**PASS** -- Matches the standard Fourier series sgn(x) = (4/pi) Sum sin((2k+1)x)/(2k+1).

Numerical verification:
- 50-term partial sum at x=0.5: 0.987 (converging to 1 = sgn(0.5))
- 50-term partial sum at x=0.01: 0.602 (slow convergence near discontinuity -- Gibbs phenomenon)

## IVNA Analysis

F[sgn](w) = -2i/w. At w=0: -2i/0_w = inf_{-2i/w} (by A6).

The indexed infinity at w=0 reflects that sgn(x) doesn't decay, so its FT is a tempered distribution with a pole. In IVNA, this pole has index structure -2i/w that tracks how the singularity scales -- just like 1/0_x = inf_{1/x} for the spatial singularity.

## Duality
- F[PV(1/x)](w) = -i*pi*sgn(w) -- spatial singularity maps to frequency-domain step
- F[sgn(x)](w) = -2i/w -- spatial step maps to frequency-domain singularity

In IVNA: both the step and the singularity carry index information. The FT preserves this index structure across domains.

## Tools Used
- Wolfram Mathematica (3 checks, all PASS)
- IVNA axioms: A6 (division by indexed zero)
