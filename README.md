# IVNA — Indexed Virtual Number Algebra

**What if `5 / 0` gave you `∞₅` instead of ERROR — and you could multiply back to get `5`?**

IVNA is a consistent algebraic framework that attaches indices to zeros and infinities, making division by zero and indeterminate forms algebraically operable. Information that standard arithmetic discards as "undefined" is preserved and recoverable.

```
5 / 0₁  =  ∞₅         (division by zero yields an indexed infinity)
∞₅ × 0₁ =  5          (multiply back — information preserved)
0₃ / 0₅  =  3/5        (zero divided by zero is well-defined)
e  =  (1 + 0₁)^{∞₁}   (Euler's number as a direct algebraic expression)
```

IVNA is to nonstandard analysis what `a + bi` is to ℝ² — the notation is the contribution. It doesn't replace existing mathematics; it provides a new interface to it.

> *Paper:* [Indexed Virtual Number Algebra: A Consistent Framework for Division by Zero and Indeterminate Forms](paper/ivna-paper.pdf)

## Verify Everything in 30 Seconds

All claims in the paper are computationally verified. You can reproduce them:

```bash
# Python tests — 28 algebraic checks (no dependencies beyond Python 3)
python3 code/ivna.py

# Lean 4 proofs — 11 axioms, 12 theorems, consistency proof (requires Lean 4.16.0)
cd lean-ivna && lake build
```

For the full 489-check verification suite (requires SymPy, Z3, and Wolfram access):

```bash
# SymPy symbolic verification — NSA embedding (37 checks) + comprehensive (69 checks)
pip install sympy && python3 code/verify_nsa_embedding.py
python3 code/verify-ivna-sympy-comprehensive.py

# Z3 satisfiability — axiom consistency (31 checks)
pip install z3-solver && python3 code/verify_z3_comprehensive.py

# Calculus suite — derivatives, integrals, FTC (115 checks)
python3 code/verify-calculus.py

# Comprehensive — extended algebraic checks (148 checks)
python3 code/verify-comprehensive.py
```

A successful `lake build` means every proof has been machine-checked. A successful `python3 code/ivna.py` runs the core algebraic test suite. The additional verification scripts reproduce the full 489-check result reported in the paper.

## What's Here

```
├── paper/
│   ├── ivna-paper.tex          # LaTeX source
│   └── ivna-paper.pdf          # Compiled paper
│
├── lean-ivna/                  # Lean 4 formalization
│   ├── LeanIvna/Basic.lean     # V F inductive type (real, zero, inf)
│   ├── LeanIvna/Axioms.lean    # 11 IVNA axioms as a structure
│   ├── LeanIvna/Model.lean     # Consistency proof (GF(2) model)
│   └── LeanIvna/Theorems.lean  # 12 derived theorems
│
├── code/
│   ├── ivna.py                 # Core implementation + 28 tests
│   ├── verify_nsa_embedding.py # NSA embedding verification (37 SymPy + 11 Z3)
│   ├── verify-comprehensive.py # Extended verification suite
│   └── ...                     # Additional verification scripts and demos
│
├── vex-web/
│   └── index.html              # Interactive VEA calculator demo
│
└── research/
    └── findings/               # Verification logs and exploration results
```

## Core Idea

Standard arithmetic maps `5 / 0` to "undefined" — a black hole that destroys information. IVNA recovers it:

| Standard Math | IVNA |
|--------------|------|
| `5 / 0` = undefined | `5 / 0₁` = `∞₅` |
| `0 / 0` = indeterminate | `0₃ / 0₅` = `3/5` |
| `∞ × 0` = indeterminate | `∞₃ × 0₅` = `15` |
| `∞ / ∞` = indeterminate | `∞₆ / ∞₂` = `3` |
| `(1 + 0)^∞` = indeterminate | `(1 + 0₁)^{∞₁}` = `e` |

The indices carry the contextual information that makes each expression deterministic.

## Verification Summary

The paper's claims are verified across five independent tool chains totaling **489 checks with 0 failures**:

| Layer | Tool | Checks | Result |
|-------|------|--------|--------|
| Core axiom tests | Python (ivna.py) | 28 | 28/28 pass |
| NSA embedding | SymPy symbolic | 37 | 37/37 pass |
| Axiom satisfiability | Z3 SMT solver | 11 | 11/11 pass |
| Formal proofs | Lean 4.16 | 23 | Compiles |
| Calculus suite | SymPy | 115 | 115/115 pass |
| Comprehensive | SymPy + Z3 | 148 | 145/0/3* |
| SymPy MCP | sympy-mcp | 69 | 69/69 pass |
| Z3 MCP | mcp-solver | 31 | 31/31 pass |
| Wolfram MCP | Wolfram Language | 27 | 27/27 pass |

*3 warnings are framing recommendations (divergent series, residues, nonlinear ODEs), not mathematical errors.

## The 11 Axioms

| # | Rule | What it means |
|---|------|---------------|
| A1 | `0ₓ × 0ᵧ = 0ₓᵧ` | Zero times zero: indices multiply |
| A2 | `∞ₓ × ∞ᵧ = ∞ₓᵧ` | Infinity times infinity: indices multiply |
| A3 | `0ₓ × ∞ᵧ = xy` | Zero times infinity: exits to real number |
| A4 | `n × 0ₓ = 0ₙₓ` | Scalar times zero: scalar enters index |
| A5 | `n × ∞ₓ = ∞ₙₓ` | Scalar times infinity: scalar enters index |
| A6 | `y / 0ₓ = ∞ᵧ/ₓ` | Division by zero: yields indexed infinity |
| A7 | `y / ∞ₓ = 0ᵧ/ₓ` | Division by infinity: yields indexed zero |
| A8 | `0ₓ / 0ᵧ = x/y` | Zero over zero: exits to ratio |
| A9 | `∞ₓ / ∞ᵧ = x/y` | Infinity over infinity: exits to ratio |
| A10 | `0ₓ + 0ᵧ = 0ₓ₊ᵧ` | Zero plus zero: indices add |
| A11 | `∞ₓ + ∞ᵧ = ∞ₓ₊ᵧ` | Infinity plus infinity: indices add |

## Interactive Demo

Open `vex-web/index.html` in a browser for a live VEA (Virtual Expression Arithmetic) calculator. Type expressions like `5/0` and see IVNA in action.

## Author

**Wisdom Patience Happy**
[Playful Sincerity Research](https://playfulsincerity.org)
Wisdom@PlayfulSincerity.org

## License

MIT — see [LICENSE](LICENSE).
