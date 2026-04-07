---
debate: "IVNA paper makes a significant and publishable contribution"
round: 3
position: CON
model: sonnet
---

## CON CLOSING ARGUMENT — Round 3

### 1. DIRECT RESPONSE — Their Strongest New Points

**On Lean 4 formalization:** Formalization papers are a legitimate genre — but they have a specific burden: the formalized content must be *independently interesting*, and the formalization must be *non-trivial*. The Archive of Formal Proofs publishes formalizations of the Jordan curve theorem, Gödel's incompleteness theorems, the prime number theorem. What makes these publishable is that the underlying mathematics is deep, and the formalization reveals something about proof structure.

What does the IVNA Lean 4 proof demonstrate? That a graded ring with a choice function is internally consistent. This is not a surprising result — the algebraic structure was already known to be consistent before IVNA existed. Compare: formalizing that Roman numeral arithmetic is internally consistent would not be publishable in AFP, because the consistency was never in question and the formalization reveals nothing.

**On the Dirac delta analogy:** This actually cuts against the PRO position. Dirac's delta was published because it was *doing work no existing tool could do* — solving differential equations, modeling point charges — with empirical results that demanded explanation. IVNA has the causation reversed: it proposes formalization of edge cases that existing tools already handle, without any demonstrated results that existing tools fail to produce.

**On NaN resolution and economic/safety stakes:** The safety-critical software community already has IEEE 754, interval arithmetic, formal verification of floating-point behavior, and hardware-level exception handling — all with decades of standardization and tooling. Applied math and formal methods journals publishing in this space will require benchmarks, case studies, or proofs of improvement over existing standards. None are present.

### 2. DEEPENED ANALYSIS — Arguments Not Yet Made

**The "framework before implementation" argument conceals a crucial distinction.** Theoretical CS papers proposing frameworks before implementation satisfy one of two conditions: (a) they prove the framework can be implemented with specified complexity bounds, or (b) they demonstrate it solves a problem formally stated as open. IVNA does neither. VEA mode has no formal problem statement, no complexity analysis, no proof of implementability. A framework paper without these is a design document.

**The "semantic interpretation" argument requires soundness.** Soundness here means showing that the index assignments to derivatives and singularity classifications correspond correctly to the mathematical objects they represent, under all compositions, limit operations, and edge cases. The paper shows the notation works in selected examples. That is illustration, not a soundness proof.

**The innovation attribution problem is more serious than previously stated.** Assigning indices to distinguish types of undefined/infinite behavior is present in non-standard analysis (distinguishing orders of infinitesimals), asymptotic analysis (big-O tracking rates), and distributional calculus (classifying singularities by type). The paper's contribution would need to show IVNA's indexing captures distinctions *none* of these capture, or captures them more efficiently. Without the comparison table (which PRO conceded is weak), the case for novelty rests almost entirely on unification — and unification papers must show the unified framework is at least as expressive as each constituent.

### 3. CONCESSIONS

The Lean 4 formalization represents genuine technical work. If the paper were reframed as a formalized notation proposal for a specialized venue like *Formalized Mathematics*, the bar is lower and the formalization becomes the lead contribution.

PRO is also right that the complex-number analogy, while imperfect, has some structural validity: complex numbers also extended a domain, resolved previously undefined operations, and faced initial resistance.

### 4. CLOSING STATEMENT — The Single Most Devastating Case

The paper's deepest failure is structural. **IVNA conflates the problem of representation with the problem of computation.**

Every genuine mathematical framework contribution solves a *computational or inferential* problem: it lets you derive things you couldn't derive, prove things you couldn't prove, or compute things you couldn't compute. Distribution theory let you differentiate functions that weren't differentiable. Non-standard analysis let you make infinitesimal arguments rigorous. IEEE 754 let you specify floating-point behavior formally enough to build reliable hardware.

IVNA gives you a way to *write down* what type of undefined or infinite expression you have. It does not give you new rules for what to *do* with that expression once you've written it down. When you write ∞₂ or 0₋₁ in IVNA notation, what inference rules apply? What can you prove that you couldn't prove before? What computations become tractable? The paper does not answer these questions — because the indexed notation does not generate new derivational power. It generates new descriptive precision.

Descriptive precision is valuable. Taxonomies are valuable. But in mathematics, describing a phenomenon more carefully than before is not a contribution unless the description enables something new. The paper has not shown what IVNA *enables* that existing tools do not.

A publishable paper answers: *what can you do now that you couldn't do before?* IVNA's answer is: *write certain expressions more carefully.* That is a contribution to mathematical communication, possibly to pedagogy, possibly to software interface design. It is not a contribution to mathematics. The paper is not unpublishable in any venue. It is publishable in none of the venues it implicitly targets.
