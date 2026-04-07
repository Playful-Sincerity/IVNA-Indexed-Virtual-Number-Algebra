# IVNA Verification

Independent verification of the Indexed Virtual Number Algebra axiom system.

## Quick Start

```bash
# Set up environment (one time)
python3 -m venv /tmp/ivna-env
source /tmp/ivna-env/bin/activate
pip install sympy z3-solver numpy scipy

# Run everything
python3 verification/run_all.py
```

This runs meta-verification first (checking that tests are sound), then all categories, then Lean4, then any Wolfram scripts present.

## Structure

```
verification/
  run_all.py                          # Single entry point — run this
  README.md                           # You are here

  core-algebra/                       # Category A: IVNA-Native (185 checks)
    cat_a_ivna_native.py              # Uses Z(), I(), Virtual class directly
                                      # Tool: Python + code/ivna.py

  nsa-embedding/                      # Category B: NSA Embedding (70 checks)
    cat_b_nsa_embedding.py            # Maps 0_x→x*ε, ∞_x→x/ε, checks all axioms
                                      # Tool: SymPy

  classical-correspondence/           # Category C: Classical Correspondence (93 checks)
    cat_c_classical_correspondence.py # Confirms notation maps onto known results
                                      # Tool: SymPy (does NOT import ivna.py — honest)

  z3-axioms/                          # Z3 Axiom Encoding (13 checks)
    cat_z3_real.py                    # Satisfiability, roundtrip, independence
                                      # Tool: Z3

  lean4/                              # Formal Proofs
    → See ../lean-ivna/               # 11 axioms, 12 theorems, GF(2) model
                                      # Tool: Lean 4 (lake build)

  wolfram/                            # Wolfram Cross-Verification
    [scripts added here are auto-discovered by run_all.py]
                                      # Tool: Wolfram Engine

  meta-audit/                         # Meta-Verification + Audit
    meta_verify.py                    # Checks that the suite itself is sound
    meta-audit-2026-04-06.md          # The audit that prompted this re-verification

  results/                            # Saved run outputs
    suite-run-2026-04-06.txt

  archive/                            # Historical verification (pre-audit)
    pre-audit-deep-dives/             # Deep-dive files that tested classical math
    legacy-scripts/                   # Old verify-*.py files
    legacy-outputs/                   # Old .txt run outputs
    phase4-reports/                   # Old Phase 4 markdown reports
```

## What Each Category Tests

| Category | What | Tool | Count |
|----------|------|------|-------|
| **A: Core Algebra** | IVNA axioms via the `Virtual` class | Python | 185 |
| **B: NSA Embedding** | Axiom consistency under standard algebra | SymPy | 70 |
| **C: Classical** | Notation maps onto known results (honest framing) | SymPy | 93 |
| **Z3** | Satisfiability + axiom independence | Z3 | 13 |
| **Lean4** | Machine-checked formal proofs | Lean 4 | 11 axioms, 12 theorems |
| **Wolfram** | Independent cross-verification | Wolfram Engine | (in progress) |
| **Meta** | Verifies the suite itself is sound | Python | 18 |

## Meta-Verification

Before trusting any results, `run_all.py` runs `meta_verify.py` which checks:
- Category A files import `ivna.py` (actually test the system)
- Category C files do NOT import `ivna.py` (honest about being classical)
- No tautological assertions (`check(name, True)`)
- No trivial Z3 checks (`x == x`)
- `ivna_derivative()` is not a passthrough (calls `virtual_taylor()` + divides via A8)

## Running Individual Categories

```bash
source /tmp/ivna-env/bin/activate

# Just the IVNA-native checks
python3 verification/core-algebra/cat_a_ivna_native.py

# Just the NSA embedding
python3 verification/nsa-embedding/cat_b_nsa_embedding.py

# Just Z3
python3 verification/z3-axioms/cat_z3_real.py

# Just Lean4
cd lean-ivna && lake build

# Just the core implementation tests (30 built-in tests)
python3 code/ivna.py
```

## Why This Structure

A 2026-04-06 audit found the prior verification suite inflated its count with ~270 classical math checks that didn't test IVNA's axiom system. This reorganized suite:
1. Separates genuine IVNA verification from classical correspondence
2. Includes meta-verification (verifying that verification is sound)
3. Organizes by tool so reviewers can verify with what they have
4. Archives old verification for historical reference
