# Category Theory Deep Dive — Verification Files

**Date:** 2026-04-01
**Main findings:** `../deep-dive-category.md`
**Total tests:** 25/25 passed (all SymPy)

## File Index

| File | What It Verifies | Tests |
|---|---|---|
| `01-graded-algebra-structure.md` | Grade additivity under multiplication | 5/5 |
| `02-homomorphism-properties.md` | Index map as ring homomorphism (mult + add) | 5/5 |
| `03-scaled-standard-part.md` | I(v) = st(v / eps^{grade(v)}) | 4/4 |
| `04-valuation-and-division.md` | Grade as discrete valuation + division axioms | 5/5 |
| `05-short-exact-sequence.md` | 1 -> Z -> R*xZ -> R* -> 1 splits | 6/6 |
| `06-jet-space-verification.md` | Taylor coefficients match jet data | 4/4 |

## Tools Used

- SymPy 1.14.0 (Python venv at /tmp/ivna-env)
- SymPy MCP server (for introduce_expression, simplify_expression)
- Wolfram/Mathematica: attempted but license unavailable during this session

## Note

All algebraic identities were verified symbolically (not just numerically). Each test checks that a SymPy expression simplifies to exactly 0, confirming the identity holds for all valid parameter values.
