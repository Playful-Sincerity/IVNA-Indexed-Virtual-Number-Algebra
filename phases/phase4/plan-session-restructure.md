# Session Brief: RESTRUCTURE — Paper Edit Plan

## Prerequisites
**Do not start this session until VERIFY and SEARCH are complete.** Read their output files first:
- `research/verification/phase4/README.md` — which claims survived verification
- `research/findings/literature-phase4/README.md` — which claims are novel vs. anticipated
- Any new findings from the EXPLORE session

## Context
IVNA paper at `~/Playful Sincerity/PS Research/IVNA/paper/ivna-paper.tex` (~1495 lines). Currently structured as a calculus-first paper. Needs to pivot to a unification thesis.

Read the full paper and:
- `~/Playful Sincerity/PS Research/IVNA/research/findings/deep-dive-unification.md`
- `~/Playful Sincerity/PS Research/IVNA/plan.md`

## Task

Design a detailed section-by-section edit plan for the paper. Do NOT make edits — produce a plan that Wisdom approves before any changes happen.

### Current Structure (what exists)
```
1. Introduction (problem, complex numbers precedent, proposal, summary)
2. Core Algebra (virtual numbers, multiplication, division, addition, powers, collapse, duality, index domain)
3. Extended Axioms (VT, EXP, scope)
4. Consistency (NSA embedding, what IVNA is, why valuable)
5. Applications: Calculus (derivatives, L'Hôpital, integration, e, residues, set sizes)
6. Applications: Physics (singularity classification)
7. Applications: Computer Science (VEAMode)
8. Literature Positioning (related frameworks, comparison, novelty, criticisms)
9. Limitations and Scope
10. Conclusion (summary, future work, vision)
Appendix: Verification Details
```

### Proposed New Structure (to be refined)
```
1. Introduction — REWRITE opener to lead with unification, not calculus
   - The problem: 9 domains, 9 independent resolution mechanisms, one underlying operation
   - The precedent: complex numbers (a+bi unified R² arithmetic)
   - IVNA's proposal: indexed zeros/infinities as a common algebraic language
   - Summary of results: the unification table as the headline

2. Core Algebra — KEEP largely intact
   - Update index domain to C\{0} per recursive-indexing-closure findings
   - Add virtual-index reduction remark

3. Extended Axioms — KEEP

4. Consistency — KEEP, add algebraic characterization (K* × Z) if not already there

5. The Unification Thesis — NEW SECTION (the heart of the paper)
   5.1 The Product Rule Across Domains (the table)
   5.2 Calculus: Derivatives and Integration (condensed from old Section 5)
   5.3 The Exponential Constant (from old Section 5.5)
   5.4 Distributions: The Dirac Delta (NEW)
   5.5 Probability: Conditional Density and Bayes' Theorem (NEW — star section)
   5.6 Complex Analysis: Residues and Partial Fractions (from old Section 5.7)
   5.7 Singularity Resolution: The Blow-Up Correspondence (from research)
   5.8 Removable Singularities as Index Cancellation (NEW)
   5.9 [Any HIGH-rated findings from EXPLORE session]

6. Applications: Physics — KEEP (condensed)
7. Applications: Computer Science — KEEP (condensed)

8. Literature Positioning — UPDATE
   - Add blow-up paragraph (already drafted)
   - Add citations from SEARCH session
   - Update comparison table

9. Limitations and Scope — UPDATE
   - Add honest assessment of what unification claims are restatements vs. new

10. Conclusion — REWRITE
   - Lead with unification thesis
   - Future work: reparametrization invariance, functoriality, measure theory formalization

Appendix: Verification Details — UPDATE with new check counts
```

### Specific Deliverables

1. **Section-by-section edit plan** — for each section:
   - What stays, what moves, what's new, what's cut
   - Specific line numbers in the current paper
   - Draft LaTeX for any new subsections (don't write into the paper — write into the plan)
   - Estimated line count for the new section

2. **The unification table as LaTeX** — draft the table for Section 5.1

3. **The Bayes/probability section as LaTeX** — draft Section 5.5 (this is the boldest new claim and needs the most careful writing)

4. **Abstract rewrite** — draft new abstract emphasizing unification

5. **Risk assessment** — which edits are safe (moving existing content) vs. risky (new claims that need verification backing)?

### Constraints
- Total paper length should stay under 40 pages (currently ~35)
- The core algebra and consistency sections should not change significantly
- Every new claim must have a citation to the verification files
- The paper must still work as a standalone math paper — not assume the reader knows about the deep dive

### Output
Save to `plan-restructure-detailed.md` in the project root. This is the document Wisdom approves before any edits begin.

### Success Criteria
- Every section has a clear "what changes" specification
- New LaTeX is drafted (not just described)
- The unification table is the visual centerpiece
- The probability section is written carefully enough to survive expert scrutiny
- Risk assessment identifies which claims need the strongest verification backing
