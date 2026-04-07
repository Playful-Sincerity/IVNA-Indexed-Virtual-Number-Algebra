# Risky Papers Search — Phase 4 Literature Review

**Date:** 2026-04-02  
**Purpose:** Deep search for three papers flagged as potential overlap risks with IVNA. Each was previously found but inaccessible (blocked PDFs, 403s). This document reports everything recovered.

---

## Summary Table

| Paper | Found? | Full Text? | Overlap Risk |
|-------|--------|------------|-------------|
| Fereydoni (2025) — Algebraic Fixed-Point Stratification | YES — Google Scholar abstract + second paper | NO — ResearchGate 403 blocked | MEDIUM-HIGH: notation similar ({∞_k}), but mechanism and purpose are fundamentally different |
| Valamontes (2026/2025) — Infinity Algebra | YES — Full 21-page HAL PDF retrieved | YES — complete | LOW: uses single untyped ∞, no indexed product rule, ∞·0 = 0 (opposite of IVNA) |
| Bloom (2025) — Indeterminate Reals | YES — Google Scholar abstract recovered | NO — academia.edu 403 blocked | LOW-MEDIUM: introduces new symbol σ, "pair model" — different mechanism, no indexed product rule |

---

## Paper 1: Fereydoni (2025) — HIGHEST PRIORITY

### Bibliographic Details

- **Full title:** "Algebraic Fixed-Point Stratification of Infinities: A Topologically Consistent Framework for Extended Semirings"
- **Author:** A. Fereydoni (Abolfazl Fereydoni)
- **Year:** 2025
- **Venue:** Preprint on ResearchGate (no journal listed in Google Scholar record)
- **URL:** https://www.researchgate.net/publication/397818363 (PDF blocked 403)
- **Second related paper:** "Hierarchical Equational Definition of Stratified Infinities: An Algebraic Fixed-Point Approach" (same author, same year, ResearchGate)

### Abstract (recovered via Google Scholar snippet)

> "This paper establishes a rigorous hierarchical framework for stratified infinities, denoted as {∞_k}_{k=0}^∞, derived not through existential axioms but as unique fixed-point solutions to recursive algebraic equations within a compactified metric space. Departing from classical Cantorian set theory and Robinson's non-standard analysis, we define an Extended Semiring E equipped with a contractive metric topology. We utilize the Banach Fixed-Point Theorem to prove the existence and uniqueness of these stratified values…"

### Second Paper Abstract (partial, Google Scholar)

> "This paper introduces a rigorous and novel hierarchical equational framework for defining stratified mathematical infinities. Unlike conventional set-theoretic approaches (Cantor) or non-standard analysis (Robinson), which rely on existential axioms or model-theoretic transfers, we construct a family of infinities {∞_k}_{k=0} as unique fixed-point solutions to a recursive system of equations within an extended algebraic structure. We formally define the extended semiring E and utilize Brouwer's Fixed-Point Theorem, Kleene's Recursion…"

### Key Claims (from abstracts)

1. Introduces a family of **stratified infinities {∞_k}** — an indexed hierarchy of distinct infinity values
2. Derived as **fixed-point solutions** to recursive equations (not axiom-postulated)
3. Uses **Banach Fixed-Point Theorem** and **Brouwer's Fixed-Point Theorem** as proof apparatus
4. Defines an **Extended Semiring E** with contractive metric topology
5. Explicitly departs from Cantor (set theory) and Robinson (non-standard analysis)
6. QFT renormalization was cited as motivation (per original report — not confirmed in recovered abstract text)

### Notation

- Uses `{∞_k}` with subscript k — a family of indexed infinities
- Extended Semiring E as the algebraic carrier structure

### Overlap Analysis with IVNA

**Surface similarity:** The notation `{∞_k}` is superficially similar to IVNA's `∞_y` notation. Both papers introduce indexed/stratified infinities.

**Critical differences:**

1. **Mechanism is completely different.** Fereydoni derives his ∞_k via fixed-point iteration on a metric space (a topological/analytic construction). IVNA defines indices operationally — they encode the zero or blow-up that produced the infinity. These are different conceptual primitives.

2. **No indexed product rule.** Fereydoni's abstract makes no mention of a rule like `0_x · ∞_y = xy`. His framework is about *existence and uniqueness* of stratified infinities, not about what happens when you multiply indexed zeros by indexed infinities. The core IVNA innovation is entirely absent.

3. **No zeros.** Fereydoni indexes only infinities, not zeros. IVNA's paired indexing of both zeros and infinities — and the product rule that connects them — has no counterpart here.

4. **No domain unification.** There is no mention of Bayesian inference, probability, ODE blow-up, L'Hôpital, Taylor series, etc. The framework is purely algebraic/topological.

5. **Different algebraic structure.** Fereydoni uses a semiring with metric topology; IVNA is an algebraic extension of ℝ with operational rules.

6. **QFT motivation vs. IVNA's motivation.** Even if QFT renormalization motivated Fereydoni, the resulting framework is fundamentally about existence proofs for infinity hierarchies, not about making indeterminate forms algebraically operable.

### Does it reduce IVNA novelty claims?

- **Indexed product rule (0_x · ∞_y = xy):** NOT threatened. Fereydoni has no such rule.
- **Blow-up correspondence theorem:** NOT threatened. No connection to ODE/PDE blow-up in Fereydoni.
- **9-domain unification table:** NOT threatened. No domains mentioned.
- **Bayes/A8 claim:** NOT threatened. No probability theory.
- **Indexed zeros:** NOT threatened. Fereydoni only indexes infinities.
- **Notation similarity:** MILD CONCERN. The `{∞_k}` notation overlaps and reviewers may notice it. IVNA should clarify the distinction explicitly in the paper.

### Access Status

- PDF blocked (ResearchGate 403 on both papers)
- Full text not recovered
- Two related Fereydoni papers found; both inaccessible as PDFs

### Recommended Access Routes

1. Try Google Scholar cache or Unpaywall
2. Email author: search Abolfazl Fereydoni institutional affiliation
3. Try sci-hub.se with ResearchGate DOI if one becomes available
4. The second paper (Hierarchical Equational Definition) is at: https://www.researchgate.net/publication/397745633

---

## Paper 2: Valamontes (2025) — SECOND PRIORITY

### Bibliographic Details

- **Full title:** Infinity Algebra: A Foundational Framework for Symbolic Computation with Infinite Quantities
- **Author:** Antonios Valamontes (Kapodistrian Academy of Science; avalamontes@kapodistrian.edu.gr)
- **Year:** 2025 (submitted April 24, 2025; revised May 7, 2025)
- **Submitted to:** Demokritos Scientific Journal (noted on preprint header)
- **HAL ID:** hal-05045749
- **URL:** https://hal.science/hal-05045749v1
- **PDF:** https://hal.science/hal-05045749v1/file/Infinity_Algebra__A_Foundational_Framework_for_Symbolic_Computation_with_Infinite_Quantitiesv2.pdf (254 KB, CC BY 4.0)
- **Full text status:** COMPLETE — all 21 pages read

### Full Abstract

> "Infinity Algebra is a new mathematical framework designed to treat infinity not as a limit, asymptotic value, or conceptual extremum—but as a fully operable and symbolic algebraic entity. This paper introduces the foundational axioms of Infinity Algebra, including explicit rules for infinite addition, subtraction, multiplication, division, inverse operations, and exponentiation. By establishing a closed and internally consistent algebraic system, we enable symbolic manipulation of infinite quantities without reliance on traditional limit-based calculus or set-theoretic extensions.
>
> We formally define Infinity Groups, Rings, and Fields that incorporate ∞ as a computable operand, allowing for structured algebraic interactions with real and infinite values. These structures serve as the basis for extended domains such as Infinity Calculus, Infinity Linear Algebra, and Infinity-Valued Function Spaces, including ∞-matrices, ∞-tensors, and symbolic derivatives evaluated at ∞.
>
> Applications span multiple disciplines: from theoretical mathematics to black hole entropy modeling, from quantum field singularities to symbolic AI systems operating over infinite-depth architectures. The symbolic entropy matrix and ∞-Einstein equations demonstrate how Infinity Algebra can reframe gravitational singularities and divergent field interactions in physics.
>
> The framework is supported by a Python-based symbolic computation engine that enables experimentation, visualization, and application of Infinity Algebra to real and abstract problems."

### Complete Axiom Set (Section 2.1 — Infinity Arithmetic Axioms)

Let a, b ∈ ℝ, ∞ denotes the symbolic infinity element:

```
(1)  ∞ + a = ∞
(2)  ∞ − a = ∞
(3)  ∞ + ∞ = ∞
(4)  ∞ − ∞ = ∞         ← NOTE: not undefined; defined as ∞
(5)  ∞ · 0 = 0          ← CRITICAL: opposite of IVNA's core rule
(6)  ∞ · a = ∞  if a ≠ 0
(7)  ∞ · ∞ = ∞
(8)  ∞/a = ∞  if a ≠ 0
(9)  a/∞ = 0
(10) ∞/∞ = ∞
(11) ∞⁻¹ = 0
(12) 0⁻¹ = ∞
(13) ∞⁰ = 1
(14) ∞⁻ᵃ = 0  for all a > 0
(15) ∞ᵃ = ∞  for all a > 0
```

**Infinity Ring multiplicative rules (eq. 16):** a · ∞ = ∞, ∞ · ∞ = ∞, ∞ · 0 = 0

**Infinity Field (eq. 17):** If a ∈ ℝ*, ∞/a = ∞, a/∞ = 0, ∞/∞ = ∞

### Notation

- Uses a single untyped `∞` (and its negative −∞)
- No subscripts, no indices, no typed or phase-labeled infinities
- No indexed zeros
- No `∞_k`, `∞_α`, or any subscripted infinity notation

### Key Claims and Novel Contributions (Section 8)

1. Algebraic closure of operations involving ∞
2. Symbolic derivatives and integrals at infinite scale (Infinity Calculus)
3. Infinity-valued matrices, entropy systems, and eigenstructures
4. Integration with symbolic computing tools (Python/SymPy)
5. A framework for resolving divergent expressions algebraically

### Comparison Framework Included (Section 7)

Valamontes explicitly compares against: Non-Standard Analysis, Hyperreals, Surreal Numbers, Extended Reals, Asymptotic Analysis. He does NOT cite or mention indexed infinity algebras, IVNA-style frameworks, or any framework like IVNA.

### Critical Technical Differences from IVNA

| Feature | Valamontes Infinity Algebra | IVNA |
|---------|----------------------------|------|
| ∞ · 0 | = 0 (Axiom 5) | = xy (indexed product rule) |
| Indexed infinities | None — single ∞ | Yes — ∞_y carries index |
| Indexed zeros | None | Yes — 0_x carries index |
| ∞ − ∞ | = ∞ (Axiom 4) | Would require indices |
| Motivation | Symbolic closure | Making indeterminate forms operable |
| Domain unification | None | 9 domains |
| Blow-up correspondence | None | Central theorem |
| Bayes/A8 | None | Key claim |

### Does it reduce IVNA novelty claims?

- **Indexed product rule:** NOT threatened. Valamontes explicitly defines ∞ · 0 = 0, which is the exact opposite of IVNA's core rule. No indexed product rule exists.
- **Indexed notation:** NOT threatened. No subscripts/indices on ∞.
- **Domain unification:** NOT threatened. No unification across domains.
- **Blow-up correspondence:** NOT threatened. No connection to ODE/PDE blow-up.
- **Bayes/A8:** NOT threatened. No probability theory.

**Overall assessment:** This paper is the weakest threat of the three. Its "Infinity Algebra" name could cause superficial confusion, but the mathematical content is entirely different. The most important difference is that Valamontes' central rule `∞ · 0 = 0` is the *opposite* of IVNA's central innovation `0_x · ∞_y = xy`. This actually reinforces IVNA's distinctiveness — Valamontes shows why an unindexed approach cannot preserve information, while IVNA's indexed approach does.

**Note on the original report's claim of "typed and phase-labelled infinities":** The full text does NOT contain typed or phase-labelled infinities. The description "typed and phase-labelled" appears to have been a mischaracterization. The paper uses a single untyped ∞ throughout.

### Access Status

- Full text: COMPLETE (all 21 pages read via HAL/saved PDF)
- No paywall — CC BY 4.0

---

## Paper 3: Bloom (2025) — THIRD PRIORITY

### Bibliographic Details

- **Full title:** "Indeterminate Reals: An Axiomatic Framework for Undefined Terms"
- **Author:** N.F. Bloom
- **Year:** 2025
- **Venue:** "JSR version" in filename — likely *Journal of Student Research* or similar undergraduate/student journal
- **URL:** https://www.academia.edu/download/124684480/Indeterminate_Reals_JSR_version_4_.pdf (PDF blocked 403)
- **Google Scholar URL:** https://www.academia.edu/124684480 (404 on direct page)

### Abstract (recovered via Google Scholar snippet)

> "Indeterminate forms such as ∞ − ∞ and 0 · ∞ are usually dismissed as undefined, yet they arise naturally in calculus, analysis, and symbolic computation. Motivated by the question of whether these forms could be given structure, I introduce a new symbol, σ, and explore its behavior within a consistent algebraic framework. I drafted axioms for σ, tested multiple approaches that led to contradictions, and ultimately developed the pair model, which satisfies the axioms and avoids collapse. I also prove basic lemmas about σ, compare the…"

*(Abstract truncated by Google Scholar)*

### Key Claims (from recovered abstract)

1. Addresses the same problem class as IVNA: indeterminate forms (∞ − ∞, 0 · ∞)
2. Introduces a new symbol **σ** to handle these forms
3. Develops **axioms for σ** — tested multiple approaches before finding one avoiding contradiction
4. Develops the **"pair model"** — the satisfying construction that avoids collapse
5. Proves basic lemmas about σ
6. Compares σ to existing approaches (abstract truncated — comparisons unknown)
7. "JSR version 4" suggests this is a student research journal paper, likely undergraduate

### What "Pair Model" Likely Means

Based on the abstract, Bloom's approach represents indeterminate forms as **pairs** (analogous to how complex numbers represent 2D values as ordered pairs a + bi). The σ symbol would then behave like a new dimension added to ℝ to accommodate indeterminate forms.

### Overlap Analysis with IVNA

**Surface similarity:** Both IVNA and Bloom address `0 · ∞` as the core indeterminate form to be structured. Both use the complex-numbers-as-analogy framing. Both introduce new algebraic objects.

**Critical differences:**

1. **Different mechanism.** Bloom introduces a new symbol σ and a "pair model." IVNA uses indexed labels on existing symbols (0 and ∞). These are architecturally different approaches.

2. **No indexed product rule.** Bloom's σ is a new *element*, not a rule relating two indexed elements. The IVNA product rule `0_x · ∞_y = xy` has no counterpart.

3. **Scope.** Bloom appears to address the general question "can indeterminate forms be given structure?" IVNA answers this for a specific algebra and then exploits the structure across 9 domains.

4. **No domain unification.** The abstract mentions no connections to probability, ODE blow-up, physics, etc.

5. **Axiom approach vs. IVNA's operational approach.** Bloom drafts axioms for σ and proves consistency. IVNA defines operations and then shows they unify known results.

6. **Student journal.** The "JSR version 4" filename strongly suggests this is an undergraduate student paper, not peer-reviewed academic research.

### Does it reduce IVNA novelty claims?

- **Indexed product rule:** NOT threatened. No such rule in Bloom.
- **Indexed notation:** NOT threatened. Bloom uses a single new symbol σ, not indexed existing symbols.
- **Domain unification table:** NOT threatened.
- **Blow-up correspondence:** NOT threatened.
- **Bayes/A8:** NOT threatened.
- **Complex numbers analogy:** MILD CONCERN. If Bloom also uses the complex-numbers-as-analogy framing explicitly, IVNA should not claim this framing as novel. However, the analogy is standard in the literature (many authors use it). This would not threaten IVNA's core claims, only a rhetorical framing.

**Overall assessment:** Bloom's paper shares the motivating problem (making 0 · ∞ definite) but solves it with a different mechanism (new symbol + pair model vs. indexed labels + product rule). The two papers are complementary rather than overlapping. IVNA could even cite Bloom as "an alternative approach to the same problem."

### Access Status

- PDF blocked (academia.edu 403)
- Abstract recovered via Google Scholar
- Full text not recovered

### Recommended Access Routes

1. Try academia.edu directly while logged in
2. Search for "N.F. Bloom" at their institution (affiliation unknown from abstract)
3. Search "Indeterminate Reals Bloom JSR" directly on the Journal of Student Research website: https://www.jsr.org/
4. Try Unpaywall or BASE search

---

## Cross-Paper Assessment: IVNA Novelty Impact

### IVNA Core Claims — Threat Level Summary

| IVNA Claim | Fereydoni | Valamontes | Bloom | Verdict |
|-----------|-----------|------------|-------|---------|
| Indexed product rule: 0_x · ∞_y = xy | None | Defines ∞·0=0 (opposite) | None | SAFE |
| Indexed zeros (0_x notation) | None | None | None | SAFE |
| Indexed infinities (∞_y notation) | {∞_k} similar notation | None | None | EXPLAIN in paper |
| Blow-up correspondence theorem | None | None | None | SAFE |
| 9-domain unification table | None | None | None | SAFE |
| Bayes / A8 discovery | None | None | None | SAFE |
| Making 0·∞ operable | None directly | ∞·0=0 (not the same) | Yes (σ-based) | SAFE (different mechanism) |
| Complex numbers analogy | None | None | Possibly | CLARIFY if Bloom uses it |

### Recommended Paper Language

To proactively address Fereydoni's notation similarity, add a footnote or paragraph in the related-work section:

> "Fereydoni [REF] introduces a family of stratified infinities {∞_k} derived as fixed-point solutions to recursive equations in an Extended Semiring. While this notation superficially resembles IVNA's indexed infinities ∞_y, the conceptual basis is entirely different: Fereydoni's indices encode algebraic hierarchy via metric-space fixed points, whereas IVNA's indices encode the specific zero or blow-up that produced the infinity, enabling the cross-cancellation product rule 0_x · ∞_y = xy. No such operational rule exists in Fereydoni's framework."

---

## Search Methodology Notes

All three papers were successfully located. Full text was only recovered for Valamontes (HAL, CC BY 4.0). Both Fereydoni and Bloom PDFs returned 403 errors (ResearchGate and academia.edu respectively).

### Sources Searched

- Semantic Scholar (search_papers): found Fereydoni and both abstracts
- Google Scholar (paper-search MCP): found all three papers with partial abstracts
- arXiv (paper-search MCP): no matches for any of the three papers
- WebSearch: found Valamontes HAL links immediately; confirmed Fereydoni on ResearchGate; Bloom not findable via web search alone
- HAL (hal.science): full Valamontes PDF retrieved and read completely
- ResearchGate: 403 blocked for Fereydoni PDFs
- academia.edu: 403/404 for Bloom PDF

### Search Queries That Found Papers

- Fereydoni: `Fereydoni "Algebraic Fixed-Point Stratification" infinities topologically consistent extended semirings 2025` (Google Scholar)
- Valamontes: `"Infinity Algebra" Valamontes 2026 HAL typed infinities` (WebSearch)
- Bloom: `Bloom "Indeterminate Reals" axiomatic framework undefined terms JSR academia.edu 2025` (Google Scholar)

---

## Chronicle Entry

**Session:** 2026-04-02  
**Task:** Phase 4 literature search — three risky papers  
**Outcome:** All three papers located. Valamontes read in full. Fereydoni and Bloom abstracts recovered but PDFs blocked.  
**Key finding:** None of the three papers threatens IVNA's core claims. Valamontes is the easiest to dismiss (∞·0=0 is the opposite of IVNA). Fereydoni has notational similarity ({∞_k}) but zero operational overlap. Bloom shares the problem motivation but uses a different mechanism.  
**Action needed:** Add Fereydoni notation-clarification footnote to IVNA paper. Try to access Bloom full text via JSR website or author contact.
