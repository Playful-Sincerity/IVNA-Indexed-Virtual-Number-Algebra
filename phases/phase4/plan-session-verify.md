# Session Brief: VERIFY — Rigorous Multi-Tool Verification

## Context
IVNA (Indexed Virtual Number Algebra) is a math framework at `~/Playful Sincerity/PS Research/IVNA/`. A deep dive found that IVNA's product rule (0_x · ∞_y = xy) appears across 9 mathematical domains. These claims need rigorous verification before they go into the paper.

Read these files first:
- `~/Playful Sincerity/PS Research/IVNA/CLAUDE.md` — project context, tools, structure
- `~/Playful Sincerity/PS Research/IVNA/research/findings/deep-dive-unification.md` — the claims to verify
- `~/Playful Sincerity/PS Research/IVNA/research/verification/deep-dive-unification/` — initial Wolfram checks (need deepening)
- `~/Playful Sincerity/PS Research/IVNA/paper/ivna-paper.tex` — the paper (1495 lines)

## Task

Triple-verify every claim in the unification table using at least 2 independent tools per claim. The probability claims (A8 = Bayes, Borel-Kolmogorov) need the deepest scrutiny since they're the newest and boldest.

### Claims to Verify (prioritized)

**HIGH PRIORITY (new, bold):**
1. **A8 = Bayes' theorem for continuous densities** — Verify that 0_{f(x,y)} / 0_{f(x)} = f(y|x) holds formally. Test with bivariate normal, bivariate exponential, and at least one pathological case (e.g., Cauchy distribution). Tools: Wolfram + SymPy.
2. **Borel-Kolmogorov paradox dissolution** — Verify the sphere example (uniform on S², condition on φ=0) with at least 2 different parameterizations. Show that IVNA gives different indices for different parameterizations and both produce correct conditional densities. Tools: Wolfram + SymPy.
3. **Dirac delta as product rule** — Verify normalization (∫δ=1), sifting (∫fδ=f(0)), scaling (δ(ax)=δ(x)/|a|), and convolution (δ*f=f) all follow from 0_x·∞_y=xy. Test with rectangular, Gaussian, and Lorentzian nascent deltas. Tools: Wolfram + SymPy.

**MEDIUM PRIORITY (established, need cross-tool confirmation):**
4. **Removable singularities as index cancellation** — sin(x)/x, (eˣ-1)/x, (1-cos(x))/x², and add 3 more: (tan(x)-x)/x³, (arcsin(x)-x)/x³, (ln(1+x)-x)/x². Verify via Taylor expansion that leading terms cancel to give the correct index. Tools: SymPy + Wolfram.
5. **Infinity subtraction** — ∞_a - ∞_b = ∞_{a-b}. Verify NSA embedding gives (a/ε - b/ε) = (a-b)/ε. Test edge cases: what happens with ∞_a - ∞_{-a}? (Should be ∞_{2a}.) What about ∞_a - ∞_a? (Should be ∞_0 → 0 by D-INDEX-ZERO.) Tools: Z3 + Wolfram.
6. **Residue extraction** — Verify that 0_x · ∞_{c/x} = c matches standard residue computation for 5+ rational functions with simple, double, and triple poles. Include one with complex residues. Tools: SymPy + Wolfram.

**LOWER PRIORITY (well-established):**
7. **Compound growth / e** — Already verified (489 checks). Just add the scaling symmetry verification (1+0_{x/n})^{∞_{ny}} = e^{xy} for n = 1,2,3,0.5,π. Tools: Wolfram.
8. **Blow-up correspondence** — Already verified in blow-up-comparison.md. Add 2 more 2-variable examples. Tools: SymPy.
9. **KL divergence** — Verify 0·ln(0) = 0 and p·ln(p/0) = ∞_p with 3 specific probability distributions. Tools: Wolfram.

### Output Format

For each claim, create a file in `research/verification/phase4/`:
- `verify-01-bayes-theorem.md` — code, output, interpretation
- `verify-02-borel-kolmogorov.md`
- etc.

Each file should have:
```markdown
---
claim: "[one-line claim]"
tools: [list of tools used]
result: PASS / FAIL / PARTIAL
---
```

Create a `README.md` summarizing all results in a table.

### Failure Protocol

If any claim FAILS verification:
- Document exactly what failed and why
- Assess whether the claim can be refined (e.g., "holds for simple poles but not double poles") or must be withdrawn
- Flag in the README with a clear warning
- Do NOT silently drop it — the paper restructuring session needs to know

### Success Criteria
- Every claim has ≥2 independent tool verifications
- The 3 high-priority claims have ≥3 verifications each
- All results are saved with full code and output
- Any failures or edge cases are documented honestly
