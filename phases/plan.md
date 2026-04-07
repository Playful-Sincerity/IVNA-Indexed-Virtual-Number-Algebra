# IVNA Phase 4 — Paper Restructuring & Completion Plan

## Environment Health
**WARNINGS** — This is not a git repo at this path level (the IVNA project may have its own git). Session results from VERIFY, SEARCH, EXPLORE, and initial DEBATE are all in place. No blockers.

## Assumptions
- The three parallel sessions (VERIFY, SEARCH, EXPLORE) are fully complete and their outputs are final
- The existing debate (2026-04-01-unification-thesis) is the "Phase 3 debate" — a new debate will run on the restructured paper
- Filesystem restructure uses `git mv` — requires clean working tree
- Paper stays under 40 pages
- Wisdom is sole author

---

## Cross-Cutting Concerns

- **Verification standard**: Every claim in the paper must trace to a verification file in `research/verification/`
- **Citation completeness**: All "must cite" papers from SEARCH must be added before arXiv submission
- **Framing**: Per debate synthesis — avoid "unification" in title/abstract; lead with concrete results (blow-up correspondence, VEA, consistency proof); frame cross-domain observation as "structural remark"
- **Methodology documentation**: The debate function, GVR loop, and multi-session decomposition are novel research methodologies worth documenting — but in a math paper, this goes in the appendix/acknowledgments, not a main section
- **Three risky papers**: Fereydoni (2025), Valamontes (2026), Bloom (2025) must be obtained before arXiv submission — this is a separate workstream, not blocking restructuring

---

## Ordering Decision — Recommended Sequence

### Why this order:

1. **RESTRUCTURE first** (paper edit plan) — This is the critical path. Everything else depends on knowing what the paper will look like.
2. **Methodology additions** — Folded INTO the restructure plan as specific sections, not a separate step.
3. **DEBATE second** — Stress-test the restructure plan before committing to edits.
4. **Apply paper edits third** — Only after plan is approved + debate-refined.
5. **Filesystem restructure LAST** — It references paths that exist now. Doing it first would break path references in all session briefs and outputs. Doing it last means we update CLAUDE.md once at the end, not repeatedly.

### Why NOT restructure filesystem first:
- The restructure session brief (`plan-session-restructure.md`) references current paths
- All verification files reference current paths in their links
- The debate session brief references current paths
- Moving files now means updating 20+ path references before we can work
- Moving files last means one clean pass of path updates

### Dependency graph:
```
RESTRUCTURE (edit plan) ──→ DEBATE (stress-test) ──→ APPLY EDITS ──→ FILESYSTEM RESTRUCTURE
     ↑                           ↑
     │                           │
  Methodology additions      Debate feedback
  folded in here             refines the plan
```

---

## Meta-Plan

### Goal
Produce an approved, debate-tested paper edit plan that pivots IVNA from "calculus tool" to a concrete-results-first paper with cross-domain structural observations, then execute the edits and clean up the filesystem.

### Sections

1. **RESTRUCTURE — Paper Edit Plan** — Synthesize VERIFY/SEARCH/EXPLORE results into a section-by-section edit plan with draft LaTeX
   - Complexity: L
   - Risk: Medium — must balance ambition (new claims) with honesty (debate findings)
   - Acceptance criteria:
     - Every section has "what stays / moves / is new / is cut" with line numbers
     - Unification table drafted as LaTeX
     - Bayes/probability section drafted carefully
     - Abstract rewrite drafted
     - Methodology additions specified
     - Risk assessment for each new claim

2. **DEBATE — Adversarial Stress-Test** — Run `/debate --opus` on the restructure plan
   - Complexity: M
   - Risk: Low — debate is well-practiced; worst case is it finds issues we fix
   - Acceptance criteria:
     - No FATAL flaws identified
     - Restructured thesis rated stronger than original "calculus tool" thesis
     - Any gaps have clear remediation paths
     - Comparison with Phase 3 debate shows improvement

3. **APPLY — Execute Paper Edits** — Apply the approved edit plan to `ivna-paper.tex`
   - Complexity: L
   - Risk: Medium — large edit to a working paper; must not break compilation
   - Acceptance criteria:
     - Paper compiles with `tectonic`
     - All new claims cite verification files
     - All "must cite" papers from SEARCH are in bibliography
     - Paper stays under 40 pages
     - Methodology/acknowledgments updated

4. **FILESYSTEM — Reorganize Project Structure** — Execute `plan-restructure-filesystem.md`
   - Complexity: S
   - Risk: Low — plan already written, all moves are `git mv`
   - Acceptance criteria:
     - All files moved per plan
     - CLAUDE.md updated with new structure
     - No broken internal links
     - Clean git commit

### Dependency Graph
```
Section 1 (RESTRUCTURE) → Section 2 (DEBATE) → Section 3 (APPLY) → Section 4 (FILESYSTEM)
```
All sequential. No parallelism at the section level — each depends on the previous.

### Overall Success Criteria
- Paper is restructured around concrete results with cross-domain structural observations
- Debate finds no fatal flaws in the new structure
- Paper compiles, all claims verified, all citations present
- Filesystem is clean and well-organized
- Methodology (debate, GVR, multi-session) documented in paper

---

## Methodology Additions — What Goes Where

Wisdom asked about documenting the new research methodologies. Here's the assessment:

### In the Paper (Appendix A — Verification Details, expanded)

The paper already has an appendix on verification. Expand it to cover the full methodology:

1. **GVR Loop** (Generate → Verify → Revise): Every mathematical claim was first generated from theoretical reasoning, then verified with ≥2 independent computational tools (SymPy, Wolfram Mathematica, Z3, Lean 4), then revised if verification failed. 427 total checks, 0 failures across 4 phases.

2. **Multi-Tool Cross-Verification**: Each claim tested with ≥2 independent tools. High-priority claims (Bayes, Borel-Kolmogorov, Dirac delta) tested with 3 tools. Tool disagreement triggers investigation, not averaging.

3. **Adversarial Debate Protocol**: Key thesis claims stress-tested via structured adversarial analysis — independent agents assigned PRO and CON positions, arguing from the source artifact, with neutral synthesis. This caught the framing overreach (Section 8.1 self-limitation vs. "unification" language) and identified that the blow-up correspondence and VEA mode are the strongest novel results.

4. **Multi-Session Decomposition**: Research parallelized across independent workstreams (verification, literature search, exploration) with explicit dependency graphs, enabling simultaneous progress while maintaining traceability.

### In the Acknowledgments

Brief mention: "Research methodology assisted by the Playful Sincerity Digital Core, including computational verification (GVR loop), adversarial debate protocol, and multi-session decomposition."

Cite Aletheia (arXiv:2602.10177) for GVR loop inspiration (already planned).

### NOT in the Paper (separate companion document)

The full case study of AI-assisted research methodology — `research/writing/case-study-ai-assisted-research.md` already exists. This could become a companion paper or blog post, but doesn't belong in a math paper.

---

## Session Inputs Summary

### From VERIFY (155 checks, 0 failures)
- All 9 unification claims verified with ≥2 tools
- Notable: Cauchy distribution works with A8 (no moment existence needed)
- Notable: D-INDEX-ZERO is automatic in NSA embedding
- Notable: Index product invariant (h(ε)·w(ε)=1 for all ε, not just limit)
- Cumulative: 427 checks across 4 phases, 0 failures

### From SEARCH (2 novel, 4 partially anticipated)
- **NOVEL**: Blow-up correspondence, 9-domain unification table
- **PARTIALLY ANTICIPATED**: Probability/Bayes (Jacobs 2021), Dirac delta (Todorov/Vernaeve), Renormalization (Albeverio), Algebraic K*×Z (Santangelo 2016)
- **MUST CITE**: 10 papers not currently in bibliography
- **RISK**: 3 recent papers (Fereydoni 2025, Valamontes 2026, Bloom 2025) — must obtain before arXiv

### From EXPLORE (3 deep dives completed)
- **Category/Functoriality** — MEDIUM: clean restatement, no novel theorem. "Universal receiver" framing worth one remark.
- **Fourier** — MEDIUM: two interesting findings (sin(x)/x non-singular, convolution as index product), no HIGH novelty
- **Harmonic/Euler-Mascheroni** — MEDIUM with HIGH sub-finding: IVNA's indexed infinities are first-order only; harmonic series reveals sub-first-order infinities outside current notation. This is an honest scope limitation worth stating.

### From DEBATE (CON wins on framing)
- "Unification" benchmarks against complex numbers — a comparison IVNA can't win
- Blow-up correspondence is the strongest novel result
- VEA mode NaN elimination is a concrete capability with no prior equivalent
- Borel-Kolmogorov and Bayes/A8 are not yet in the paper — must be integrated or dropped
- Recommendation: lead with concrete results, frame cross-domain as "structural observation"
