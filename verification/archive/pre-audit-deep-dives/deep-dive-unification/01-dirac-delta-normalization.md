# Verification: Dirac Delta Normalization

**Tool:** Wolfram Mathematica (via MCP)
**Date:** 2026-04-01

## Code

```mathematica
(* Nascent delta: rectangle of height 1/ε and width ε *)
result1 = Integrate[1/eps, {x, -eps/2, eps/2}, Assumptions -> eps > 0];
Print["Integral of rect_ε: ", result1]

(* Sifting property: ∫ f(x)·rect_ε(x) dx → f(0) *)
f[x_] := x^2 + 3x + 7;
sifting = Limit[Integrate[f[x]/eps, {x, -eps/2, eps/2}, Assumptions -> eps > 0], eps -> 0];
Print["Sifting of x²+3x+7: ", sifting, " (should be f(0) = ", f[0], ")"]
```

## Output

```
Integral of rect_ε: 1
Sifting of x²+3x+7: 7 (should be f(0) = 7)
```

## Interpretation

- Rectangle of height ∞₁ = 1/ε and width 0₁ = ε always has area 1, regardless of ε
- Sifting property verified: ∫f(x)δ(x)dx = f(0) = 7
- IVNA product rule 0₁·∞₁ = 1 IS the normalization condition
