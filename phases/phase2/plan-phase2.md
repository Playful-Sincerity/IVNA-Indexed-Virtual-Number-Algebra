# IVNA Phase 2: From Validated Algebra to Published Paper

## Environment Health

**Verdict: CLEAN**

- Git repo initialized, uncommitted work from Phase 1 (to be committed)
- Lean 4.16.0 installed via elan, no Lean files yet
- Python venv at /tmp/ivna-env (SymPy 1.14.0, Z3 4.16.0)
- All Phase 1 artifacts present (28/28 tests, NSA embedding, VEX calc, 6 section plans)
- Research partner system configured (SymPy MCP, Z3, Wolfram, GVR rule)
- CLAUDE.md present and current

---

## Assumptions

1. "Virtual Numbers" kept as term, with explicit justification in the paper
2. Lean4 formalization (axioms + NSA proof) completes BEFORE paper drafting
3. e exploration runs in parallel with Lean4, results feed into paper
4. Paper is the primary deliverable; VEX calculator gets brief treatment inside it
5. Claude credited as co-author (transparent AI collaboration)
6. ArXiv first, then journal (American Mathematical Monthly or Mathematical Intelligencer)
7. Writing voice: Wisdom's natural style adapted for academic rigor (style guide being produced)

---

## Cross-Cutting Concerns

### Core Deliverable
A 20-30 page academic paper with:
- Machine-checked Lean4 consistency proof as supplementary material
- GitHub repo with Python test suite + VEX calculator
- ArXiv preprint establishing priority

### Technology Stack
- **Writing**: LaTeX (standard for math papers)
- **Computation**: Python/SymPy for verification, ivna.py as reference implementation
- **Formal verification**: Lean 4.16.0 with Mathlib
- **Version control**: Git (the IVNA project repo)

### Naming Convention
- "Virtual Numbers" — zeros and infinities with indices
- "Non-Virtual Numbers" — standard reals/complex
- "IVNA" — Indexed Virtual Number Algebra
- "VEX" — Virtual EXtended (calculator/computer arithmetic mode)
- Notation: 0_x, ∞_x, =; (as in the original paper)

### Quality Standard
- Every mathematical claim in the paper must be:
  - Computationally verified (SymPy/Python — GVR rule)
  - Formally verified where possible (Lean4)
  - Honestly scoped (explicit limitations)

### Verification
- Python tests: `source /tmp/ivna-env/bin/activate && python3 ivna.py`
- Lean4: `lake build` in the Lean project directory
- LaTeX: `pdflatex` or `latexmk`

---

## Meta-Plan

### Goal
Produce a publishable academic paper on IVNA with machine-checked proofs, deep exploration of consequences (especially e), and honest positioning — then submit to ArXiv and a target journal. This is Wisdom's first academic publication and a gateway to credibility for other PS Research projects.

### Sections

1. **Deep e Exploration** — Investigate all consequences of e = (1+0₁)^{∞₁}: Euler's identity, scaling symmetry, information theory connection, FTC in IVNA, differential equations as difference equations. Discover new directions.
   - Complexity: L
   - Risk: Medium — some directions may dead-end, but the core result is solid
   - Acceptance criteria:
     - All 5 stated directions explored with computational verification
     - At least 2 genuinely novel insights identified for inclusion in the paper
     - Each finding documented with SymPy/Python verification
     - Integration formalization (FTC) attempted with concrete examples

2. **Lean4 Formalization** — Core axiom typeclass + NSA embedding instance = machine-checked consistency proof.
   - Complexity: L
   - Risk: High — Lean4/Mathlib can be finicky; hyperreal numbers in Mathlib may have gaps
   - Acceptance criteria:
     - IVNA typeclass defined with all core axioms (A1-A7)
     - NSA embedding instance constructed and type-checks
     - `lake build` succeeds with no errors
     - At least the division-by-zero roundtrip theorem proven
     - Supplementary material package ready for paper submission

3. **Writing Style Audit** — Analyze Wisdom's writing across projects to produce a style guide for paper drafting.
   - Complexity: S
   - Risk: Low
   - Acceptance criteria:
     - Style guide produced with concrete drafting rules
     - Voice characteristics identified (sentence patterns, formality, tone)
     - Academic adaptation guidance provided
   - Status: RUNNING (background agent)

4. **Paper Drafting** — Write the 10-section paper using the outline from value-assessment.md, in Wisdom's voice, incorporating e exploration results and Lean4 proofs.
   - Complexity: L
   - Risk: Medium — balancing accessibility with rigor, voice with formality
   - Acceptance criteria:
     - All 10 sections drafted in LaTeX
     - Every equation computationally verified
     - Lean4 proofs referenced as supplementary material
     - e exploration results integrated into Sections 3 and 5
     - Limitations section is honest and specific
     - Paper compiles cleanly with pdflatex
     - 20-30 pages (standard math paper length)

5. **Paper Review & Polish** — Internal review, consistency checks, formatting for submission.
   - Complexity: M
   - Risk: Low
   - Acceptance criteria:
     - All cross-references correct
     - Bibliography complete and properly formatted
     - No unverified claims
     - Abstract captures the key contribution clearly
     - Suitable for blind review (no identifying info beyond author line)

6. **Publication Pipeline** — ArXiv submission, GitHub repo setup, journal targeting.
   - Complexity: S
   - Risk: Medium — ArXiv endorsement needed, journal selection matters
   - Acceptance criteria:
     - GitHub repo public with code, tests, Lean proofs, VEX calculator
     - ArXiv preprint submitted (math.RA or math.GM)
     - Cover letter drafted for journal submission
     - Target journal selected with specific justification

### Dependency Graph

```
Section 1 (e Exploration) → Section 4 (Paper Drafting)
Section 2 (Lean4) → Section 4 (Paper Drafting)
Section 3 (Style Audit) → Section 4 (Paper Drafting)
Section 4 → Section 5 (Review)
Section 5 → Section 6 (Publication)

Parallel batch 1: [Section 1, Section 2, Section 3]
Sequential: Section 4 → Section 5 → Section 6
```

### Acceptance Tests (meta-level)
- The paper compiles, reads well, and every claim is verified
- Lean4 proofs type-check and are included as supplementary
- ArXiv submission is live with a citable preprint ID
- A mathematician reading this paper would find it credible and well-positioned

### Overall Success Criteria
The project is DONE when:
1. A LaTeX paper exists that could be submitted to AMM or Math Intelligencer
2. Lean4 proofs are on GitHub and type-check
3. ArXiv preprint is submitted
4. Wisdom has a clear path to journal submission

---

## Estimated Timeline (Compressed — Claude-paced, not human-paced)

```
Hour 1-2:   Sections 1, 2, 3 in parallel (e exploration, Lean4, style audit ✓)
Hour 2-3:   Section 4 (paper drafting — incorporate results as they land)
Hour 3-4:   Section 5 + 6 (review, GitHub, ArXiv prep)
```

---

*Plan created: 2026-03-31*
*Status: Awaiting approval of meta-plan*
