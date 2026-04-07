# Verification: Convolution with Delta

## Standard Result
f * delta = f, i.e., (f * delta)(x) = int f(x-t) delta(t) dt = f(x)

## Wolfram Verification

```mathematica
Integrate[Exp[-(x-t)^2]*DiracDelta[t], {t, -Infinity, Infinity}]
(* Result: E^(-x^2) *)

Integrate[Sin[x-t]*DiracDelta[t], {t, -Infinity, Infinity}]
(* Result: Sin[x] *)

Integrate[(x-t)^3*DiracDelta[t], {t, -Infinity, Infinity}]
(* Result: x^3 *)

Integrate[((x-t)^2) * DiracDelta[t], {t, -Infinity, Infinity}]
(* Result: x^2 *)
```
**ALL PASS** (4 checks)

## IVNA Derivation

(f * delta)(x) = int f(x-t) delta(t) dt
= Riemann sum over inf_1 subintervals of width 0_1
= Sum_{j} f(x - t_j) * delta(t_j) * 0_1

delta(t_j) = inf_1 when t_j is in the subinterval containing 0 (exactly one such subinterval)
delta(t_j) = 0 for all other subintervals

Sum = f(x - 0) * inf_1 * 0_1 + Sum_{j != 0} f(x - t_j) * 0 * 0_1
    = f(x) * 1 + 0
    = f(x)

**Product rule A3 does all the work:** inf_1 * 0_1 = 1.

## Assessment

This is completely trivial in IVNA -- it's just A3 applied once. The convolution identity is the sifting property, which was already covered in the unification deep dive. No new insight here.

## Tools Used
- Wolfram Mathematica (4 checks, all PASS)
- IVNA axiom: A3 (product rule)
