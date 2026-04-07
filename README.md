# IVNA — Indexed Virtual Number Algebra

**What if `x / 0` gave you `∞ₓ` instead of ERROR — and you could multiply back to get `x`?**

IVNA is a consistent algebraic framework that attaches indices to zeros and infinities, making division by zero and indeterminate forms algebraically operable. Information that standard arithmetic discards as "undefined" is preserved and recoverable.

```
x / 0₁  =  ∞ₓ         (division by zero yields an indexed infinity)
∞ₓ × 0₁ =  x          (multiply back — information preserved)
0ₓ / 0ᵧ  =  x/y        (zero divided by zero is well-defined)
e  =  (1 + 0₁)^{∞₁}   (Euler's number as a direct algebraic expression)
```

IVNA is to nonstandard analysis what `a + bi` is to ℝ² — the notation is the contribution. It doesn't replace existing mathematics; it provides a new interface to it.

> *Paper:* [Indexed Virtual Number Algebra: A Consistent Framework for Division by Zero and Indeterminate Forms](paper/ivna-paper.pdf)

## Verify Everything

All claims are computationally verified. One command runs everything:

```bash
# Set up (one time)
python3 -m venv /tmp/ivna-env
source /tmp/ivna-env/bin/activate
pip install sympy z3-solver numpy scipy

# Run the full verification suite
python3 verification/run_all.py
```

This runs meta-verification (checking the suite itself), then all 403 checks across 6 tools, then Lean 4. Detailed per-tool outputs are auto-saved to `verification/_results/`.

Or verify individual components:

```bash
python3 code/ivna.py                    # 30 core tests (no dependencies)
cd lean-ivna && lake build              # Lean 4 formal proofs (11 axioms, 12 theorems)
```

## What's Here

```
├── verification/               # START HERE — all verification in one place
│   ├── run_all.py              # Single command runs everything
│   ├── README.md               # Verification guide for reviewers
│   ├── core-algebra/           # Category A: IVNA-native (185 checks)
│   ├── nsa-embedding/          # Category B: NSA consistency (70 checks)
│   ├── classical-correspondence/ # Category C: notation checks (93 checks)
│   ├── z3-axioms/              # Z3 axiom encoding (13 checks)
│   ├── wolfram/                # Wolfram cross-verification (42 checks)
│   ├── meta-audit/             # Meta-verification + audit report
│   └── _results/               # Saved run outputs (organized by tool)
│
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
│   ├── ivna.py                 # Core implementation + 30 tests
│   ├── demos/                  # Demo scripts + outputs
│   └── vea-web/                # Interactive VEA calculator demo
│
├── research/                   # Research findings and writing
├── debates/                    # Adversarial analysis transcripts (4 debates)
└── phases/                     # Phase plans (1-5)
```

## Core Idea

Standard arithmetic maps `x / 0` to "undefined" — a black hole that destroys information. IVNA recovers it:

| Standard Math | IVNA |
|--------------|------|
| `x / 0` = undefined | `x / 0₁` = `∞ₓ` |
| `0 / 0` = indeterminate | `0ₓ / 0ᵧ` = `x/y` |
| `∞ × 0` = indeterminate | `∞ₓ × 0ᵧ` = `xy` |
| `∞ / ∞` = indeterminate | `∞ₓ / ∞ᵧ` = `x/y` |
| `(1 + 0)^∞` = indeterminate | `(1 + 0₁)^{∞₁}` = `e` |

The indices carry the contextual information that makes each expression deterministic.

## Verification Summary

**403 checks across 6 tools, 0 failures.** Each check is honestly categorized:

| Category | Tool | Checks | What It Tests |
|----------|------|--------|---------------|
| A: IVNA-native | Python/ivna.py | 185 | Exercises the `Virtual` class directly |
| A: Core tests | Python/ivna.py | 30 | Built-in unit tests |
| B: NSA embedding | SymPy | 70 | Axiom consistency under hyperreal mapping |
| C: Classical | SymPy | 93 | Notation maps onto known results (honest) |
| Z3 encoding | Z3 SMT | 13 | Satisfiability + axiom independence |
| Cross-verification | Wolfram Engine | 42 | Independent symbolic engine |
| Formal proofs | Lean 4.16 | 23 | Machine-checked (0 sorry in core) |
| Meta-verification | Python | 18 | Checks the suite itself is sound |

See `verification/README.md` for details and `verification/_results/` for full per-tool outputs.

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

Open `code/vea-web/index.html` in a browser for a live VEA (Virtual Expression Arithmetic) calculator. Type expressions like `5/0` and see IVNA in action.

## Author

**Wisdom Happy**
[Playful Sincerity Research](https://playfulsincerity.org)
Wisdom@PlayfulSincerity.org

## License

MIT — see [LICENSE](LICENSE).
