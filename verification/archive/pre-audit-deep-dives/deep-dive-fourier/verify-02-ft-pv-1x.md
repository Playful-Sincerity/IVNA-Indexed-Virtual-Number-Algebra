# Verification: Fourier Transform of PV(1/x)

## Standard Result
F[PV(1/x)](w) = -i*pi*sgn(w) (physics convention: F[f](w) = int f(x) e^{-iwx} dx)

## Wolfram Verification

```mathematica
FourierTransform[1/x, x, w, FourierParameters -> {1, -1}]
(* Result: -I*Pi*Sign[w] *)
```
**PASS**

Also verified with {0, -2pi} convention:
```mathematica
FourierTransform[1/x, x, w, FourierParameters -> {0, -2*Pi}]
(* Result: -I*Pi*Sign[w] *)
```
**PASS** (same result -- convention-independent for this function)

## Key sub-verification: sin(wx)/x integral

```mathematica
Assuming[w > 0, Integrate[Sin[w*x]/x, {x, -Infinity, Infinity}]]
(* Result: Pi *)
```
**PASS** -- This is the Dirichlet integral, the real core of the PV(1/x) transform.

## Hilbert Transform Connection

```mathematica
(1/Pi)*Integrate[DiracDelta[t]/(x - t), {t, -Infinity, Infinity}]
(* Result: 1/(Pi*x) *)
```
**PASS** -- H[delta](x) = 1/(pi*x), confirming the Hilbert transform relationship.

## IVNA Analysis

The decomposition e^{-iwx} = cos(wx) - i*sin(wx) gives:
- PV int (1/x)*cos(wx) dx = 0 (odd integrand)
- PV int (1/x)*sin(wx) dx = pi*sgn(w) (Dirichlet integral)

In IVNA: sin(wx)/x at x = 0 is sin(w*0_h)/0_h. By A-VT (Taylor):
sin(w*0_h) = w*0_h - (w*0_h)^3/6 + ... = 0_{w} (index = w, first-order)
So sin(w*0_h)/0_h = 0_w / 0_h = w/h (by A8).

When h = 1 (the standard grid): sin(w*0_1)/0_1 = w. **No singularity in IVNA.**
The sinc function is regular at x=0 because A8 (index cancellation) resolves the 0/0 form.

## Tools Used
- Wolfram Mathematica (4 checks, all PASS)
- IVNA axioms: A6 (1/0_x = inf_{1/x}), A8 (0/0 cancellation), A-VT (Taylor extension)
