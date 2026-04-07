# Session Brief: SEARCH — Literature & Prior Art

## Context
IVNA (Indexed Virtual Number Algebra) is a math framework at `~/Playful Sincerity/PS Research/IVNA/`. A deep dive found that IVNA's product rule unifies how 9 domains resolve indeterminate forms. Before we claim novelty, we need to know if anyone has noticed these connections before.

Read these files first:
- `~/Playful Sincerity/PS Research/IVNA/CLAUDE.md` — project context
- `~/Playful Sincerity/PS Research/IVNA/research/findings/deep-dive-unification.md` — the claims
- `~/Playful Sincerity/PS Research/IVNA/research/findings/algebraic-characterization.md` — IVNA ≅ K* × Z
- `~/Playful Sincerity/PS Research/IVNA/research/findings/blow-up-comparison.md` — blow-up correspondence
- `~/Playful Sincerity/PS Research/IVNA/paper/ivna-paper.tex` — current literature section starts ~line 983

## Task

Search for prior art on each of the unification claims. Use Semantic Scholar MCP, paper-search MCP, and web search. For each claim, answer: **novel, partially anticipated, or already known?**

### Search Queries (by claim)

**1. Probability / Bayes connection**
- "indexed zeros probability" OR "infinitesimal probability conditional density"
- "Borel-Kolmogorov paradox resolution algebraic"
- "nonstandard analysis conditional probability" — NSA people may have noticed this
- "division by zero probability" OR "zero probability conditional"
- Check: Keisler's probability work, Nelson's radically elementary probability, Benci-Di Nasso probability applications
- Key question: Has anyone in the NSA community noticed that the infinitesimal ratio ε₁/ε₂ computes conditional densities?

**2. Dirac delta / product rule connection**
- "infinitesimal Dirac delta" OR "nonstandard analysis delta function"
- "delta function algebraic" OR "delta function without distributions"
- Check: Todorov & Vernaeve's work on nonstandard delta functions, Robinson's original treatment
- Key question: NSA already represents delta as (1/ε)·1_{[-ε/2,ε/2]}. Has anyone connected this to a product rule on indexed objects?

**3. Renormalization / infinity subtraction**
- "nonstandard analysis renormalization" OR "infinitesimal regularization QFT"
- "indexed infinities subtraction" OR "labeled infinities physics"
- Check: Albeverio et al., "Nonstandard Methods in Stochastic Analysis and Mathematical Physics"
- Key question: Has the NSA community formalized ∞_a - ∞_b = ∞_{a-b} or equivalent?

**4. Blow-up / index correspondence**
- "blow-up division by zero" OR "exceptional divisor algebraic division"
- "blow-up arithmetic" OR "blow-up without scheme theory"
- This was already searched in blow-up-comparison.md — update if new results found
- Key question: Has anyone in algebraic geometry noticed the connection to division-by-zero algebras?

**5. Cross-domain unification**
- "indeterminate forms unified framework" OR "resolving singularities algebraic"
- "0/0 infinity minus infinity common structure"
- "division by zero applications across mathematics"
- Check Bergstra's 2019 survey for any cross-domain framing

**6. Laurent monomial / graded monoid interpretation**
- "Laurent polynomial division by zero" OR "graded ring singularity"
- "monomial arithmetic infinity"
- Does the algebraic characterization (K* × Z) appear in any division-by-zero context?

### Output Format

Save to `research/findings/literature-phase4/`:
- `prior-art-probability.md` — what was found, assessment
- `prior-art-dirac-delta.md`
- `prior-art-renormalization.md`
- `prior-art-blow-up.md`
- `prior-art-unification.md`
- `prior-art-algebraic.md`
- `README.md` — summary table

Each file should include:
- Search queries used
- Papers/sources found (with DOIs or URLs)
- Assessment: NOVEL / PARTIALLY ANTICIPATED / ALREADY KNOWN
- If partially anticipated: what's new in IVNA's version vs. what was known
- Any papers we should cite that we're not currently citing

### Key Sources to Check
These are the most likely places someone might have anticipated IVNA's unification:
1. **Keisler's probability via infinitesimals** — he may have the Bayes connection
2. **Todorov & Vernaeve** — nonstandard delta functions
3. **Albeverio et al.** — NSA in physics/QFT
4. **Bergstra's 2019 survey** — most comprehensive review of division-by-zero frameworks
5. **Carlström's wheel theory papers** — any cross-domain applications?

### Success Criteria
- Every claim has a prior art assessment
- Any "partially anticipated" or "already known" findings include the specific paper and what it covers
- The paper's literature section can be updated with proper citations
- Honest assessment — if someone already did this, we cite them and explain what IVNA adds
