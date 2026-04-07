# Session Brief: DEBATE — Adversarial Stress-Test

## Prerequisites
**Do not start until RESTRUCTURE is complete.** The debate must argue against the actual restructured paper, not the old version. Read:
- `plan-restructure-detailed.md` — the approved edit plan
- The updated `paper/ivna-paper.tex` (if edits have been applied)
- `research/verification/phase4/README.md` — verification results
- `research/findings/literature-phase4/README.md` — prior art results

## Context
The IVNA paper has been restructured around a unification thesis: the product rule 0_x · ∞_y = xy appears across 9 domains. The strongest new claim is that A8 = Bayes' theorem for continuous densities. This needs adversarial stress-testing.

## Task

Run `/debate --opus` with full source material loaded. The debate skill (at `~/.claude/skills/debate/skill.md`) now includes Phase 1.5 (source material loading), so agents will read the actual paper before arguing.

### Proposition
"IVNA's cross-domain unification thesis — that the product rule 0_x · ∞_y = xy is the common algebraic mechanism underlying derivatives, the Dirac delta, conditional densities, residue extraction, renormalization, compound growth, blow-up resolution, and removable singularities — represents a significant and novel mathematical contribution."

### Configuration
```
/debate "IVNA's cross-domain unification thesis represents a significant mathematical contribution" --opus --context "~/Playful Sincerity/PS Research/IVNA/paper/ivna-paper.tex"
```

Use `--opus` because this is a research/theory topic where reasoning depth matters.

### What We're Testing
1. **Does the unification thesis survive scrutiny?** Or are these just restatements in new notation?
2. **Is the probability claim (A8 = Bayes) genuinely novel?** Or did NSA people already know this?
3. **Does the blow-up correspondence add value?** Or is it just restating algebraic geometry?
4. **Is the "9 domains, one rule" framing honest?** Or does it cherry-pick while ignoring cases where IVNA doesn't help?
5. **What's the strongest remaining attack?** This is what we fix before submission.

### Post-Debate
After the synthesis:
1. Compare with the Phase 3 debate (at `debates/2026-03-31-mathematical-contribution/`). Did the unification pivot address CON's original demands?
2. List any new gaps the debate found
3. For each gap: assess whether it's fixable (paper edit) or fundamental (thesis change)
4. Save debate outputs per the skill (automatic now — `debates/YYYY-MM-DD-unification-thesis/`)

### Success Criteria
- Debate completes with no escalation issues
- Synthesis identifies no FATAL flaws (gaps are fine, fatal flaws are not)
- The unification thesis is rated stronger than the original "calculus tool" thesis
- Any gaps found have clear remediation paths
- Comparison with Phase 3 debate shows measurable improvement
