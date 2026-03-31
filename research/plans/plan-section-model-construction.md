# Section 4: Model Construction — Detailed Plan

*Date: 2026-03-31*
*Status: Plan complete, execution not started*
*Depends on: Section 1 (complete), Section 2 (complete), Section 3 (not started)*

---

## Goal

Build a concrete mathematical model satisfying the IVNA axioms — or prove that no such model exists. This is the make-or-break section. If a model exists, IVNA is consistent (by the soundness theorem: any theory with a model is consistent). If no model exists, the axioms are contradictory and must be revised.

---

## The Axioms Under Test

From Section 1 (consistency audit), the core IVNA axioms that passed all tests are:

**A1. Multiplication:**
- A1a: 0_x * 0_y = 0^2_{xy} (generalized: 0^m_x * 0^n_y = 0^{m+n}_{xy})
- A1b: inf_x * inf_y = inf^2_{xy} (generalized: inf^m_x * inf^n_y = inf^{m+n}_{xy})
- A1c: 0^m_x * inf^n_y = xy if m=n; 0^{m-n}_{xy} if m>n; inf^{n-m}_{xy} if n>m
- A1d: n * 0_x = 0_{nx}, n * inf_x = inf_{nx} for real n

**A2. Division:**
- A2a: y / 0_x = inf_{y/x}
- A2b: y / inf_x = 0_{y/x}
- A2c: 0_x / 0_y = x/y (same order); inf_x / inf_y = x/y (same order)

**A3. Addition/Subtraction:**
- A3a: 0_x + 0_y = 0_{x+y}, inf_x + inf_y = inf_{x+y} (same order)
- A3b: 0_x - 0_y = 0_{x-y}, inf_x - inf_y = inf_{x-y} (same order)

**A4. Powers:**
- A4a: (0_x)^n = 0^n_{x^n}, (inf_x)^n = inf^n_{x^n}

**A5. Negation:**
- A5a: -(0_x) = 0_{-x}, -(inf_x) = inf_{-x}

**A6. Collapse (=; operator):**
- A6a: 0_x =; 0 for all x
- A6b: inf_x =; infinity for all x

**A7. Duality:**
- A7a: 1/0_x = inf_{1/x}
- A7b: 1/inf_x = 0_{1/x}

**Known failures (Section 5 / Open Questions, not core axioms):**
- 0_1 - 0_1 = 0_0 != 0^2_1 = 0_1 * 0_1 (Section 5.4 claim)
- (1 + 1/inf)^inf = 1, not e (Section 5.1, the "e problem")
- 0_1 * inf_1 = 1 contradicts Section 5.3's proposal that 0_1 * inf_1 = 2pi
- 0_0 vs 0^2_1 identity claim
- Rational function derivatives need rule for 1/(n + 0_x)

---

## Approach 1: NSA Embedding Test (HIGHEST PRIORITY)

### The Idea

The literature review (Section 2, Risk 1) identified this candidate model: fix a positive infinitesimal epsilon_0 in the hyperreals *R. Define:

    0_r := r * epsilon_0       for each real r
    inf_r := r / epsilon_0     for each real r

Then check whether ALL core IVNA axioms hold under this interpretation.

### Why This Is the Fastest Path

If it works: IVNA is consistent, proven via the consistency of NSA (which is proven relative to ZFC). The model is *R itself with a distinguished infinitesimal. This is a one-line consistency proof.

If it fails: the specific axiom(s) that fail tell us exactly what IVNA does beyond NSA — those are either genuine novelty or genuine contradictions.

### Systematic Axiom Check

For each axiom, substitute the NSA definitions and verify algebraically:

**A1a: 0_x * 0_y = 0^2_{xy}**
- LHS: (x * epsilon_0) * (y * epsilon_0) = xy * epsilon_0^2
- RHS: We need 0^2_{xy} to map to xy * epsilon_0^2 under the embedding
- This requires extending the embedding to higher orders: 0^n_r := r * epsilon_0^n
- CHECK: xy * epsilon_0^2 = xy * epsilon_0^2. HOLDS.

**A1b: inf_x * inf_y = inf^2_{xy}**
- LHS: (x/epsilon_0) * (y/epsilon_0) = xy / epsilon_0^2
- RHS: inf^2_{xy} := xy / epsilon_0^2
- CHECK: HOLDS.

**A1c: 0_x * inf_y = xy (when orders match)**
- LHS: (x * epsilon_0) * (y / epsilon_0) = xy * (epsilon_0 / epsilon_0) = xy
- CHECK: HOLDS. This is the key axiom and it works perfectly.

**A1c (general): 0^m_x * inf^n_y with m != n**
- LHS: (x * epsilon_0^m) * (y / epsilon_0^n) = xy * epsilon_0^{m-n}
- If m > n: = xy * epsilon_0^{m-n}, which is 0^{m-n}_{xy}. HOLDS.
- If n > m: = xy / epsilon_0^{n-m}, which is inf^{n-m}_{xy}. HOLDS.

**A1d: n * 0_x = 0_{nx}**
- LHS: n * (x * epsilon_0) = (nx) * epsilon_0 = 0_{nx}
- CHECK: HOLDS.

**A2a: y / 0_x = inf_{y/x}**
- LHS: y / (x * epsilon_0) = (y/x) / epsilon_0 = (y/x) * (1/epsilon_0) = inf_{y/x}
- CHECK: HOLDS.

**A2b: y / inf_x = 0_{y/x}**
- LHS: y / (x / epsilon_0) = (y/x) * epsilon_0 = 0_{y/x}
- CHECK: HOLDS.

**A2c: 0_x / 0_y = x/y**
- LHS: (x * epsilon_0) / (y * epsilon_0) = x/y
- CHECK: HOLDS.

**A3a: 0_x + 0_y = 0_{x+y}**
- LHS: x * epsilon_0 + y * epsilon_0 = (x+y) * epsilon_0 = 0_{x+y}
- CHECK: HOLDS.

**A3b: inf_x + inf_y = inf_{x+y}**
- LHS: x/epsilon_0 + y/epsilon_0 = (x+y)/epsilon_0 = inf_{x+y}
- CHECK: HOLDS.

**A4a: (0_x)^n = 0^n_{x^n}**
- LHS: (x * epsilon_0)^n = x^n * epsilon_0^n = 0^n_{x^n}
- CHECK: HOLDS.

**A5a: -(0_x) = 0_{-x}**
- LHS: -(x * epsilon_0) = (-x) * epsilon_0 = 0_{-x}
- CHECK: HOLDS.

**A6a: 0_x =; 0**
- st(x * epsilon_0) = 0 for any standard real x, since x * epsilon_0 is infinitesimal.
- The standard part function maps infinitesimals to 0.
- CHECK: HOLDS. The =; operator IS the standard part function.

**A6b: inf_x =; infinity**
- x/epsilon_0 is infinite for any nonzero standard real x.
- st() is undefined on infinite hyperreals (st applies only to finite hyperreals).
- IVNA's =; maps inf_x to infinity. This is like saying "if it's infinite, report infinity."
- CHECK: HOLDS (with the understanding that =; extends st() to infinite elements by mapping them to a symbolic infinity).

**A7a: 1/0_x = inf_{1/x}**
- 1/(x * epsilon_0) = (1/x) / epsilon_0 = inf_{1/x}
- CHECK: HOLDS.

### Preliminary Verdict on NSA Embedding

**Every core IVNA axiom (A1-A7) holds under the NSA embedding.** The mapping is:

    0^n_r  <-->  r * epsilon_0^n     (for any standard real r, positive integer n)
    inf^n_r  <-->  r / epsilon_0^n   (= r * epsilon_0^{-n})
    =;  <-->  st() extended to map infinite hyperreals to "infinity"

This means: **IVNA's core algebra IS a structured fragment of NSA.** It is the sub-algebra of hyperreals generated by {r * epsilon_0^n : r in R, n in Z} under the standard hyperreal operations. This is isomorphic to R[epsilon_0, epsilon_0^{-1}] — the ring of Laurent polynomials in epsilon_0 with real coefficients.

### What This Means

1. **IVNA is consistent** — its axioms hold in a model (a specific sub-structure of the hyperreals). Consistency is inherited from NSA, which is consistent relative to ZFC.

2. **IVNA is not new mathematics** in the foundation sense — it is a notational system for a specific fragment of NSA. But this is not fatal. The complex number notation a + bi is "just notation" for R^2 with specific operations, yet it transformed mathematics.

3. **The value proposition shifts to interface:** IVNA's contribution is making the NSA fragment usable without requiring model theory, ultrafilters, or the transfer principle. A student can learn 0_x * inf_y = xy in minutes; learning the ultrapower construction takes a semester.

### What Needs Computational Verification

The algebraic checks above are straightforward, but we should verify them computationally to catch any hidden issues:

**Task 1.1: Python script verifying all axiom checks**
- For each axiom, implement both the IVNA operation (using ivna.py) and the NSA embedding operation (direct arithmetic on Fraction objects representing the coefficient, tracking epsilon_0 power symbolically)
- Verify they agree for a range of test values
- Tools: Python + Fraction (already available)
- Difficulty: Low
- Time: 1-2 hours
- Success: All axioms produce identical results under both representations
- Failure: Some axiom diverges — that axiom represents something beyond NSA

**Task 1.2: Check the failure cases under NSA**
- Does the NSA embedding shed light on WHY the Section 5 axioms fail?
- The e problem: (1 + epsilon_0)^{1/epsilon_0} in NSA DOES give e (that's exactly how NSA defines e). So the e problem is not about IVNA's axioms being wrong — it's about IVNA's collapse operator (=;) being applied too early. In NSA, you evaluate the full expression THEN apply st(). In IVNA, the paper applies =; to subexpressions, destroying information. This is a critical insight for Section 3.
- The 0_0 problem: 0_0 = 0 * epsilon_0 = 0. Under NSA, 0_0 is literally the real number 0, not an infinitesimal. This explains why 0_0 behaves differently from 0^2_1 = epsilon_0^2 (which is a genuine infinitesimal).
- Tools: Analytical reasoning, no computation needed
- Difficulty: Low
- Time: 30 minutes
- This directly informs Section 3

**Task 1.3: Identify what the NSA embedding CANNOT capture**
- Are there IVNA features that go beyond the Laurent polynomial sub-algebra?
- Candidate: virtual numbers with virtual indices (0_{0_1}). Under NSA, this would be 0_{epsilon_0} = epsilon_0 * epsilon_0 = epsilon_0^2 = 0^2_1. So nested virtual indices collapse to higher-order virtuals. This is consistent but means IVNA doesn't get "new" objects from nesting.
- Candidate: the =; operator applied selectively (to some terms but not others). NSA's st() is all-or-nothing. IVNA's derivative computation applies =; only at the end, which is fine. But if someone tried to apply =; to part of an expression, it could differ from NSA behavior.
- Tools: Analytical reasoning
- Difficulty: Medium
- Time: 1 hour

---

## Approach 2: Algebraic Model (Free Algebra Quotient)

### The Idea

Construct IVNA as a quotient algebra. Start with the free algebra F generated by:
- Symbols 0_x for each x in R
- Symbols inf_x for each x in R
- Symbols r for each r in R
- Operations: +, *, /, -, ^, neg, collapse

Impose the IVNA axioms as relations (equations). Form the quotient algebra F/~ where ~ is the congruence generated by these relations. If F/~ is nontrivial (has more than one element), the axioms are consistent.

### Why This Matters Even If NSA Embedding Works

The free algebra quotient is the UNIVERSAL model — every other model of the IVNA axioms is a quotient of it. If we can characterize this algebra, we understand the full space of IVNA models, not just the NSA one.

### Implementation Plan

**Task 2.1: Define the free algebra formally**
- Write the generators and relations as a formal algebraic specification
- This is a pen-and-paper task (or LaTeX), not computation
- Difficulty: Medium
- Time: 2-3 hours

**Task 2.2: Check for collapse to the trivial algebra**
- The danger: if the axioms imply 0 = 1 (or any two distinct reals are equal), the quotient is trivial and the axioms are inconsistent.
- If the NSA embedding works (Approach 1), this check is unnecessary — the existence of a non-trivial model (NSA) proves the quotient is non-trivial.
- However, we should still check whether the free algebra quotient is LARGER than the NSA model — i.e., are there non-isomorphic models?
- Difficulty: High (requires algebraic reasoning about the congruence closure)
- Time: 3-5 hours
- Depends on: Approach 1 results

**Task 2.3: Characterize the quotient**
- If the NSA embedding is the only model (up to isomorphism), then IVNA is categorically equivalent to the Laurent polynomial ring R[epsilon, epsilon^{-1}].
- If there are other models, IVNA has genuine freedom beyond NSA.
- This matters for the "is IVNA novel?" question.
- Tools: SymPy for symbolic algebra, pen-and-paper reasoning
- Difficulty: High
- Time: 5-8 hours

### Success/Failure Criteria
- Success: The quotient is characterized and shown to be non-trivial. Relationship to the NSA model is clear.
- Failure: The quotient collapses to a trivial algebra — axioms are inconsistent. (Extremely unlikely if Approach 1 succeeds.)

### Dependencies on Section 3
- If Section 3 modifies axioms, the free algebra must be re-computed with the new relations.
- However, for the CORE axioms (which all passed consistency checks), we can proceed now.

---

## Approach 3: Z3 Satisfiability Check

### The Idea

Encode the IVNA axioms as first-order constraints in Z3 (SMT solver) and check satisfiability. Z3 can find models or prove unsatisfiability for finite domains.

### Why This Complements the Other Approaches

- Z3 is automated — no human algebraic reasoning needed, reduces error risk
- Z3 can find counterexamples to proposed additional axioms (e.g., Section 5 claims)
- Z3 can check consistency of axiom subsets — useful for Section 3's contradiction resolution

### Implementation Plan

**Task 3.1: Encode core axioms in Z3**
- Represent virtual numbers as pairs (index, order) with a kind flag
- Encode each axiom as a universally quantified constraint
- Z3 cannot handle full universal quantification over reals, so we test with:
  a) Finite domain: indices in {-2, -1, -1/2, 0, 1/2, 1, 2}
  b) Orders in {1, 2, 3}
  c) All combinations of virtual types (zero, inf, real)
- Tools: Z3 Python API (available in /tmp/ivna-env)
- Difficulty: Medium
- Time: 3-4 hours
- Success: Z3 returns SAT with a model
- Failure: Z3 returns UNSAT — indicates inconsistency in the tested domain

**Task 3.2: Test Section 5 axioms for satisfiability**
- Add each disputed axiom (e problem, 0_0 = 0^2_1, etc.) to the core axioms
- Check whether adding it makes the system UNSAT
- This directly supports Section 3
- Difficulty: Low (incremental on Task 3.1)
- Time: 1-2 hours

**Task 3.3: Search for non-NSA models**
- Constrain Z3 to find models where 0_1 * inf_1 != standard NSA answer
- If Z3 finds such a model: IVNA has models beyond NSA
- If Z3 proves no such model exists (for the finite domain): evidence that NSA is the only model
- Difficulty: Medium
- Time: 2-3 hours

### Limitations
- Z3 works with finite/decidable fragments, not full first-order arithmetic
- A Z3 SAT result for a finite domain does not prove consistency for all reals
- But combined with the NSA embedding (Approach 1), it provides additional confidence

### Dependencies on Section 3
- Minimal. Core axiom encoding is independent of Section 3.
- Section 5 axiom checks (Task 3.2) directly feed into Section 3.

---

## Approach 4: Concrete Construction (Explicit Model)

### The Idea

If approaches 1-3 confirm that a model exists, write it down explicitly and prove each axiom holds. This is the publishable version of the consistency proof.

### The Construction (Based on Approach 1 Results)

Define the set V (IVNA virtual number system):

    V = R  union  { (r, n) : r in R, n in Z \ {0} }

where:
- Elements of R are the "non-virtual" (standard real) numbers
- (r, n) with n > 0 represents 0^n_r (indexed zero of order n)
- (r, n) with n < 0 represents inf^{|n|}_r (indexed infinity of order |n|)
- Equivalently: (r, n) represents r * epsilon_0^n for a formal variable epsilon_0

Operations:

    (r, m) * (s, n) = begin
        if m + n = 0:  return rs        (element of R)
        else:          return (rs, m+n)  (element of V \ R)
    end

    r * (s, n) = (rs, n)                (scalar times virtual)

    (r, m) + (s, n) = begin
        if m = n:  return (r+s, n)
        else:      coexist as formal sum (not in V — requires extending V to formal sums)
    end

    r + s = r + s                       (standard real addition)

    collapse((r, n)) = begin
        if n > 0:  return 0
        if n < 0:  return +infinity (as a symbol, not a real)
    end

    collapse(r) = r                     (reals collapse to themselves)

**The formal structure:** V under multiplication is isomorphic to the multiplicative group of the Laurent polynomial ring R[epsilon, epsilon^{-1}], restricted to monomials. Under addition, it is a partial operation (only same-order elements can be added within V; cross-order addition requires a formal sum extension).

### Implementation Plan

**Task 4.1: Write the explicit model definition**
- Define V, the operations, and the axiom verification as a formal document
- Tools: LaTeX or Markdown
- Difficulty: Medium
- Time: 2-3 hours

**Task 4.2: Verify each axiom in the model**
- For each axiom A1-A7, write the proof that it holds in V
- These should be straightforward given the NSA embedding analysis
- Tools: Pen-and-paper / LaTeX
- Difficulty: Low-Medium
- Time: 2-3 hours

**Task 4.3: Implement the model in Python as an independent verification**
- Write a `Model` class that implements V with the explicit operations
- Run all 25 tests from ivna.py against this model
- Verify that Model and Virtual produce identical results
- Tools: Python
- Difficulty: Low
- Time: 2-3 hours
- Success: All tests pass on both implementations

**Task 4.4: Characterize what the model IS**
- The model is the graded ring of Laurent monomials in one variable with real coefficients
- Relate this to standard algebraic structures
- Identify the algebraic name and properties (is it a field? a ring? a group under multiplication?)
- Tools: Algebraic reasoning
- Difficulty: Medium
- Time: 2-3 hours

### Dependencies on Section 3
- If Section 3 adds new axioms, they must be verified in the model
- If Section 3 modifies existing axioms, the model may need modification
- The CORE model construction (for axioms A1-A7) does not depend on Section 3

---

## Execution Order

### Phase A: NSA Embedding (can start immediately)
1. Task 1.1: Computational verification of NSA embedding (1-2 hours)
2. Task 1.2: Analyze failure cases under NSA (30 min)
3. Task 1.3: Identify what NSA cannot capture (1 hour)

**Checkpoint A:** If all axioms hold under NSA embedding, we have a consistency proof. Proceed to Phase B. If some axiom fails, those axioms are the focus of Section 3.

### Phase B: Z3 Verification (can run in parallel with Phase A)
4. Task 3.1: Encode core axioms in Z3 (3-4 hours)
5. Task 3.2: Test Section 5 axioms (1-2 hours) — feeds into Section 3

**Checkpoint B:** Z3 results confirm or challenge the NSA embedding findings.

### Phase C: Concrete Construction (after Phases A and B)
6. Task 4.1: Write explicit model definition (2-3 hours)
7. Task 4.2: Verify axioms formally (2-3 hours)
8. Task 4.3: Python implementation of the model (2-3 hours)

**Checkpoint C:** We have a complete, verified, explicit model.

### Phase D: Algebraic Characterization (after Phase C)
9. Task 4.4: Characterize the model algebraically (2-3 hours)
10. Task 2.1-2.3: Free algebra analysis (5-8 hours) — only if needed to determine uniqueness

**Checkpoint D:** We know whether the NSA model is the ONLY model, or whether IVNA has additional models.

### Total Estimated Time
- Phase A: 2.5-3.5 hours
- Phase B: 4-6 hours (parallel with A)
- Phase C: 7-9 hours
- Phase D: 7-11 hours (optional, only if novelty question matters)
- **Minimum viable result (Phases A+B): 5-8 hours**
- **Full result (all phases): 15-25 hours**

---

## The Critical Question: Does the NSA Embedding Work for All Axioms?

### Answer: Almost certainly YES for all core axioms (A1-A7).

The algebraic verification above shows that every core axiom maps directly to standard hyperreal arithmetic. The mapping is:

    0^n_r  =  r * epsilon_0^n
    inf^n_r  =  r * epsilon_0^{-n}
    r  =  r
    =;  =  st() extended to infinite elements

Under this mapping, every IVNA operation is just standard multiplication, division, addition, etc. on the hyperreals. The axioms are not independent postulates — they are THEOREMS of hyperreal arithmetic.

### What Fails Under NSA (and What This Means)

The Section 5 "open questions" fail for illuminating reasons:

1. **The e problem:** In NSA, (1 + epsilon_0)^{1/epsilon_0} DOES converge to e (its standard part is e). The IVNA failure comes from collapsing 1 + 0_1 to 1 before exponentiating. The fix (from Section 3): do NOT apply =; to subexpressions. Define IVNA evaluation as: compute the full expression in the virtual algebra, THEN apply =; at the very end. This matches NSA's protocol exactly.

2. **0_0 = 0^2_1:** Under NSA, 0_0 = 0 * epsilon_0 = 0 (the real number zero), while 0^2_1 = epsilon_0^2 (a nonzero infinitesimal). These are genuinely different objects. The paper's claim that they're equal is wrong. Section 3 should retract this claim.

3. **0_1 * inf_1 = 2pi:** Under NSA, epsilon_0 * (1/epsilon_0) = 1, period. The proposed alternative axiom is incompatible with the NSA model. Section 3 should reject this proposal.

### The Deeper Implication

IVNA is consistent because it is a notational system for a specific, well-understood algebraic structure. This is GOOD NEWS:

- Consistency is proven (no new proof needed — inherited from NSA/ZFC)
- Every IVNA computation can be verified by translating to hyperreals
- The system cannot produce contradictions (for the core axioms)
- The open questions all have clear resolutions via the NSA interpretation

The trade-off: IVNA is not new mathematics in the foundational sense. It is a new INTERFACE to existing mathematics. The Bombelli parallel is apt: Bombelli's rules for complex numbers were "just" rules for R^2 arithmetic, but they changed how people thought about algebra. IVNA's rules for indexed zeros are "just" rules for Laurent monomials in an infinitesimal, but they could change how people think about division by zero and limits.

---

## Key Decisions for Section 3 (Contradiction Resolution)

The model construction provides clear guidance for Section 3:

1. **The e problem is a protocol error, not an axiom error.** Fix: define the =; operator as applying only to FINAL results, never to subexpressions. This matches NSA's standard part function behavior.

2. **0_0 is the real number 0, not a higher-order infinitesimal.** The claim 0_0 = 0^2 should be retracted. Under the model, 0_0 = 0 is a real number and 0^2_1 = epsilon_0^2 is an infinitesimal. They are categorically different.

3. **The 2pi axiom is incompatible with the core algebra.** It should be removed. The core multiplication rule 0_x * inf_y = xy is what makes the system work, and it's what the model validates.

4. **Rational function derivatives** require extending IVNA with a rule for expressions like 1/(x + 0_1). Under NSA, this is just 1/(x + epsilon_0) = (1/x)(1/(1 + epsilon_0/x)), which can be expanded as a geometric series. The IVNA equivalent would be a power series rule for virtual-number arguments.

---

## Deliverables

After execution, this section produces:

1. **NSA Embedding Verification** — Python script confirming all axioms hold
2. **Z3 Satisfiability Check** — Script confirming SAT for core axioms, identifying UNSAT for Section 5 additions
3. **Explicit Model Definition** — The set V, its operations, and proofs that all axioms hold
4. **Python Model Implementation** — Independent implementation verifying agreement with ivna.py
5. **Algebraic Characterization** — What V is in standard algebraic terms (Laurent monomials)
6. **Recommendations for Section 3** — Specific fixes for each open question, derived from the model

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| NSA embedding fails on some axiom | Very Low | High — means IVNA has genuine novelty OR a bug | Check algebraically first, then computationally |
| Z3 encoding misrepresents an axiom | Medium | Medium — false positive/negative | Cross-check Z3 results against NSA embedding |
| Free algebra quotient analysis is intractable | Medium | Low — NSA embedding is sufficient for consistency | Defer to Phase D, do only if needed |
| Section 3 modifies axioms after model is built | High | Low — core axioms unlikely to change | Build model for core axioms first; add Section 3 modifications incrementally |
| The "just notation for NSA" finding disappoints | Medium | N/A — truth over comfort | Frame honestly: notation matters (see complex numbers). The calculator vision is validated. |

---

*Plan prepared: 2026-03-31*
*Next step: Execute Phase A (NSA embedding verification)*
