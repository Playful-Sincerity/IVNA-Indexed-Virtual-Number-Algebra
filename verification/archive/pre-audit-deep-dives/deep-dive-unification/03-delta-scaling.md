# Verification: Dirac Delta Scaling and Gaussian Nascent Delta

**Tool:** Wolfram Mathematica (via MCP)
**Date:** 2026-04-01

## Code

```mathematica
(* δ(ax) scaling: rect of height 1/ε, width ε/a *)
scaling = Integrate[1/eps, {x, -eps/(2a), eps/(2a)}, Assumptions -> {eps > 0, a > 0}];
Print["∫δ(ax)dx = ", scaling]

(* Gaussian nascent delta integral *)
gaussIntegral = Integrate[1/(eps*Sqrt[2*Pi]) * Exp[-x^2/(2*eps^2)], 
  {x, -Infinity, Infinity}, Assumptions -> eps > 0];
Print["Gaussian nascent delta integral: ", gaussIntegral]

(* IVNA index product for Gaussian *)
Print["∞_{1/√(2π)} · 0_{√(2π)} = ", Simplify[(1/Sqrt[2Pi])*Sqrt[2Pi]]]
```

## Output

```
∫δ(ax)dx = 1/a
Gaussian nascent delta integral: 1
∞_{1/√(2π)} · 0_{√(2π)} = 1
```

## Interpretation

- δ(ax) scaling: IVNA gives width 0_{1/a}, height ∞₁, area = (1/a)·1 = 1/a. Matches standard identity δ(ax) = (1/|a|)δ(x).
- Gaussian nascent delta: height ∞_{1/√(2π)}, effective width 0_{√(2π)}, index product = 1.
- **Every nascent delta sequence has index product = 1.** That's the invariant — height_index × width_index = 1.
