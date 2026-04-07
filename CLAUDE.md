# IVNA — Indexed Virtual Number Algebra

## What This Is
A consistent algebraic framework that attaches indices to zeros and infinities, making division by zero and indeterminate forms algebraically operable. Proven consistent via NSA embedding (37/37 SymPy + 11/11 Z3 checks). Lean4 formalization complete (11 axioms, 12 theorems, consistency proof).

## Status
**Phase 2: Paper drafting.** Re-verification complete (2026-04-06 audit + new suite). Lean4 proofs compile. LaTeX scaffold ready. Next: fill in paper sections, then ArXiv submission.

## Verification Status (post-audit, 2026-04-06)

Run `python3 verification/run_all.py` — single command runs everything.

| Tool | Category | Checks | Failures |
|------|----------|--------|----------|
| Python/ivna.py | A: IVNA-Native | 185 | 0 |
| SymPy | B: NSA Embedding | 70 | 0 |
| SymPy | C: Classical Correspondence | 93 | 0 |
| Z3 | Axiom Encoding | 13 | 0 |
| Wolfram | Cross-Verification | 42 | 0 |
| Lean 4 | Formal Proofs | 11 axioms, 12 theorems | 0 sorry |
| Python | Meta-Verification | 18 | 0 |
| Python/ivna.py | Core Unit Tests | 30 | 0 |
| **Total** | | **403 + Lean4** | **0** |

- See `verification/meta-audit/meta-audit-2026-04-06.md` for the audit that prompted this revision.
- Prior "427 checks" count was inflated with ~270 classical-math checks; corrected suite isolates genuine IVNA-native verification.

## Key Results
- **IVNA is consistent** — NSA embedding provides concrete model, Lean4 machine-checked
- **e = (1 + 0₁)^{∞₁}** — direct algebraic definition, not a limit
- **Derivatives verified via A-VT + A8 pipeline** — polynomial, rational, trig, exponential, logarithmic
- **Division-by-zero roundtrip** — 5/0₁ = ∞₅, ∞₅ · 0₁ = 5 (information preserved)
- **IVNA is to NSA what a+bi is to R²** — the notation is the contribution
- **Unification across 9 domains** — Bayes, Dirac delta, residues, blow-ups, etc. share a common algebraic structure

## Project Structure

```
IVNA/
├── CLAUDE.md                    # This file
├── .gitignore
│
├── paper/                       # The academic paper
│   ├── ivna-paper.tex           # LaTeX source (10-section structure)
│   └── ivna-paper.pdf           # Compiled PDF
│
├── lean-ivna/                   # Lean 4 formalization
│   ├── LeanIvna/
│   │   ├── Basic.lean           # V F inductive type
│   │   ├── Axioms.lean          # 11 IVNA axioms as structure
│   │   ├── Model.lean           # Consistency proof (GF(2) model)
│   │   └── Theorems.lean        # 12 derived theorems
│   ├── lakefile.lean
│   ├── lean-toolchain
│   └── README.md
│
├── code/                        # Python implementation & tools
│   ├── ivna.py                  # Core IVNA implementation (28 tests)
│   ├── vea_calculator.py        # VEA calculator prototype/demo
│   ├── verify/                  # Verification scripts (7 original + 10 phase4)
│   ├── demos/                   # Demo scripts + outputs
│   └── vea-web/                 # Interactive web calculator
│
├── research/                    # Research process & findings
│   ├── findings/                # Research findings (markdown)
│   │   ├── deep-dive-unification.md  # Cross-domain unification (9 domains)
│   │   ├── algebraic-characterization.md  # IVNA ≅ K* × Z
│   │   ├── blow-up-comparison.md     # Blow-up correspondence
│   │   ├── literature-phase4/        # Prior art assessments
│   │   └── abandoned/                # Dead-end explorations
│   ├── verification/            # Verification logs & outputs
│   │   ├── deep-dive-unification/    # Wolfram verification of unification claims
│   │   └── phase4/                   # Phase 4 claim verifications (9 files)
│   ├── agent-outputs/           # Raw agent outputs (traceability)
│   └── writing/                 # Style guide, writing aids
│
├── phases/                      # Phase plans (1-5)
│   └── phase4/plan.md           # CURRENT: Unification thesis pivot
│
├── debates/                     # Adversarial analysis transcripts
├── distribution/                # Outreach & publication
├── sessions/                    # Session logs
├── chronicle/                   # Semantic logging
└── archive/                     # Superseded files
```

## Core Axioms (resolved)
- **A1-A5**: Multiplication rules (zero×zero, inf×inf, zero×inf, scalar×zero, scalar×inf)
- **A6-A9**: Division rules (by zero, by inf, zero/zero, inf/inf)
- **A10-A11**: Addition rules
- **A-EXP**: (1 + 0_x)^{∞_y} = e^{xy} — resolves the e problem
- **A-VT**: Virtual Taylor Axiom — extends analytic functions to virtual arguments
- **D-INDEX-ZERO**: Index 0 exits to real 0 (like i-i=0 exits imaginaries)

## Research Tools (available)
- **sympy-mcp** — symbolic math verification
- **mcp-solver** — Z3 satisfiability checking
- **wolfram / wolfram-verify** — computation + step-by-step verification
- **jupyter-mcp-server** — persistent computation
- **arxiv-latex-mcp** — raw LaTeX from arXiv papers
- **Lean 4** — formal proof verification (`lake build` in lean-ivna/)
- **Python venv** — `/tmp/ivna-env` (SymPy 1.14.0, Z3 4.16.0, NumPy, SciPy)
- Run tests: `source /tmp/ivna-env/bin/activate && python3 code/ivna.py`
- Compile paper: `cd paper && tectonic ivna-paper.tex`
- Build Lean: `cd lean-ivna && lake build`

## GVR Rule (Auto-Applied)
This project falls under `~/Playful Sincerity/PS Research/**`:
1. Generate reasoning from training knowledge
2. Verify with computation tools (SymPy, Wolfram, Z3) before presenting
3. Revise if verification reveals errors

## Future Work: Transfer Principle Generalization
A-VT currently restricts IVNA's function extension to analytic functions (those with convergent Taylor series). The natural next step is an IVNA-native transfer axiom based on NSA's full transfer principle, which would extend virtual arguments to ALL first-order definable functions — removing the analyticity restriction. This is identified in the paper (Section 3 scope remark + Future Work item 5). The challenge: the transfer principle requires model-theoretic machinery (ultrafilters, Łoś's theorem) that could undermine IVNA's accessibility goal. Finding the right balance is the research problem.

## Publication Plan
- **ArXiv first** (math.RA or math.GM) — establishes priority
- **Target journal**: American Mathematical Monthly or Mathematical Intelligencer
- **Supplementary**: GitHub repo with code + Lean proofs + VEA calculator
- **Attribution**: Wisdom as sole author, Playful Sincerity Digital Core in acknowledgments
- **Methodology cites**: Aletheia (arXiv:2602.10177) for GVR loop inspiration

## Connection to Other PS Research
- **Gravitationalism**: IVNA notation for field singularities
- **ULP**: Both seek irreducible formal structures
- **Academic credibility**: First publication → gateway for other PS Research papers
