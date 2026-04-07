# IVNA Paper — Writing Style Guide for Wisdom's Voice

*Derived from: PSTS book manuscript, ULP CLAUDE.md, GDGM core tenets & derivation sketch, IVNA value-assessment & applications docs.*

---

## 1. Voice Characteristics

- **Sentence length**: Medium. Rarely compound-complex. Favors one-idea-per-sentence clarity, then follows with a short punch line. "That's it for now." / "This is not a metaphor." / "Everything else is interpretation."
- **Formality**: Serious but never stiff. Uses contractions sparingly. Avoids jargon when a plain word works ("clump" not "agglomeration"), but deploys precise technical terms without apology when they earn their place.
- **First person**: Uses "we" naturally (inclusive, not royal). Occasionally "you" when walking the reader through a derivation. Almost never "I" in technical writing.
- **Tone**: Confident without bluster. States claims directly, then immediately flags where confidence drops. No hedging on what is known; no overclaiming on what is not.
- **Contrasts**: Draws sharp before/after or standard-vs-IVNA contrasts. Likes showing what a framework *cannot* do before showing what it *can*.

## 2. Structure Patterns

- **Headings do real work**: Not decorative. Each heading is a question or a claim. "What Is Space?" / "What Is Charge?" / "The Stability Problem."
- **Paragraphs**: Short (2-5 sentences). One idea per paragraph. Longer explanatory passages are broken by bold lead-ins or inline subheadings.
- **Examples first, then abstraction**: Shows the concrete computation, then names the principle. The Coulomb singularity example comes before the general classification table.
- **Honest assessment blocks**: After presenting a result, adds a short "Value assessment" or "What follows" paragraph that evaluates what the result actually buys you. Never leaves the reader to guess significance.
- **Tables for comparison**: Uses markdown tables to compress parallel comparisons (IVNA vs. NSA vs. grossone, or singularity types side by side). Tables replace paragraphs that would otherwise be repetitive.
- **Summary chains**: Ends major sections with a visual chain (ASCII arrows or numbered flow) showing the logical dependency. "A1 + A2 -> Space -> Time -> Stability -> Particles."

## 3. Mathematical Writing Habits

- **Equations in context, not display-only**: Introduces each equation with a plain-English sentence saying what it means, then shows the math, then interprets the result. The equation is always sandwiched.
- **Variables are introduced immediately**: "Call the distance between graviton i and graviton j: r_ij." Never uses a symbol without naming it in the same breath.
- **Prefers code-block math over LaTeX**: Uses triple-backtick blocks for equations. Inline math uses plain unicode (subscripts, Greek letters). This keeps the manuscript readable in any editor.
- **Shows the algebra step by step**: Does not skip intermediate steps. Writes out the substitution, the simplification, and the result as separate lines. Trusts that the reader benefits from seeing the work.
- **Dimensionless forms highlighted**: When an equation simplifies to "no free parameters," calls this out explicitly as a key insight.
- **Uncertainty handled in-line**: Uses bold labels like **First fork**, **Experiment needed**, **Most likely answer** to flag open questions directly inside the derivation, not in a separate caveats section.

## 4. What to Preserve (Wisdom's Distinctive Qualities)

- **Direct declarations followed by grounding**: "There is exactly one type of fundamental particle." Then the implication. This rhythm (claim-then-ground) is the signature move.
- **Intellectual honesty as a structural element**: Sections like "What These Tenets Do NOT Specify" and "Where IVNA Does NOT Help" are not afterthoughts; they are load-bearing. The willingness to explicitly bound claims builds trust.
- **Analogies to familiar systems**: The complex-number analogy for IVNA (a+bi was notation, not new math) and the hydrostatic equilibrium analogy for particles. These bridge gaps without dumbing down.
- **The word "clean"**: Uses it to mean "logically minimal" or "structurally elegant." Keep this.
- **Warmth without softness**: Even in mathematical writing, there is a sense of invitation: "Think of a particle as a self-gravitating clump." Never cold, never chatty.
- **The evaluative voice**: Wisdom rates things. "Value: HIGH." "This is the key mathematical program." "This is testable in principle." The paper should rank its own contributions.

## 5. What to Adapt for Academic Context

- **Add formal theorem/definition/proof structure** where the content supports it (IVNA axioms, the NSA embedding theorem). Wisdom's natural flow is discursive; the paper needs some LaTeX-style theorem blocks to signal rigor.
- **Reduce conversational asides** ("That's it for now"). Keep the directness but trim the informality to one or two moments per major section, not every paragraph.
- **Strengthen citations**: Wisdom's drafts reference frameworks by name ("Robinson, 1966") but inconsistently. Every factual claim about prior work needs a proper citation.
- **Limit bold/italic emphasis**: The drafts use bold heavily for inline emphasis. In a paper, reserve bold for definitions and key terms only; let sentence structure do the emphasis work.
- **Section numbering over named headings**: Keep the question-style headings as subsection titles but nest them inside numbered sections (1.1, 1.2...) for referenceability.

## 6. Concrete Rules for Drafting the IVNA Paper

1. **Sandwich every equation**: Plain-English setup sentence, then the math, then a sentence interpreting the result. No orphan equations.
2. **Show one worked example before stating the general rule.** Coulomb singularity first, classification table second. The reader should see the specific case working before being asked to trust the abstraction.
3. **Every claim gets one of three labels** (even if only mentally during drafting): *proven* (via NSA embedding or computation), *demonstrated* (via examples, not yet proven in generality), or *conjectured* (open). Never let a conjecture sit next to a theorem unmarked.
4. **The honest-scope paragraph is mandatory.** After each application section, include 2-3 sentences on what IVNA does NOT do in that domain. This is Wisdom's most distinctive and trust-building move.
5. **Use the complex-number analogy exactly once**, in the introduction, to frame the entire paper. Do not repeat it in every section. Let it echo, not hammer.
6. **Keep the evaluative voice for the conclusion.** The body should present; the conclusion should assess. Use the "Value: HIGH / MODERATE / LOW" table in the conclusion or a summary section, not scattered through the body.
7. **Write transitions as logical dependencies, not narrative bridges.** Instead of "Having established X, we now turn to Y," write "X requires Y. We define Y as follows." The paper's flow should feel like a derivation chain, not a tour.
