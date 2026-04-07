# IVNA Literature Positioning — Section 2

**Status:** Complete first draft
**Date:** 2026-03-31
**Purpose:** Map IVNA against the six major existing frameworks that address division by zero, infinitesimals, and infinite set sizes. Identify genuine novelty and real risks of overlap.

---

## 1. Framework Summaries

### 1.1 Non-Standard Analysis (NSA)

**Who:** Abraham Robinson, Yale University. Published in a 1961 article and the 1966 book *Non-Standard Analysis.*

**What it is.** NSA constructs a proper extension of the real numbers called the *hyperreals* (*R or R*). The construction uses a free ultrafilter on the natural numbers to build equivalence classes of real-valued sequences. The result is an ordered field containing the reals plus:

- Infinitesimals: positive numbers smaller than every positive real (e.g., ε where 0 < ε < 1/n for all n ∈ N).
- Infinite numbers: numbers larger than every real (e.g., ω = [1, 2, 3, ...] under the ultrafilter).
- All arithmetic and field operations extend naturally.

**The Transfer Principle.** Any first-order sentence true of R is also true of *R, and vice versa. This is the crown jewel: it means NSA is not a hack — every theorem of standard analysis has an exact counterpart in the hyperreals. The principle is limited to first-order statements; higher-order properties (e.g., "every bounded subset has a supremum" read over all subsets) can differ.

**The Standard Part Function.** For any *finite* hyperreal r (one that does not exceed every real), there is a unique real number st(r) infinitely close to r. This is the "collapse" operation: st(r) rounds off the infinitesimal residue. The derivative is defined as:

    f'(x) = st( (f(x + ε) - f(x)) / ε )

for any nonzero infinitesimal ε. No limits are needed — the limit is built into the standard part. This does require applying st() at the end; the ratio (f(x+ε)-f(x))/ε is generally a hyperreal, not a real.

**What it does not do.**
- Division by zero is undefined. Zero has no multiplicative inverse in *R (the transfer principle ensures this, since 0 has no multiplicative inverse in R).
- The product 0 × ∞ is indeterminate: ε · ω can equal any finite number, 0, or ∞ depending on the specific ε and ω chosen. There is no mechanism to track which pairs produce which results without specifying them individually.
- Set sizes: NSA does not directly assign proportional cardinalities to infinite sets. |N| and |2N| (even numbers) are both represented by ω-sized quantities, but the specific ratio depends on how the ultrafilter is constructed — it is not canonical.

**Foundational status:** Fully rigorous. Proven consistent relative to ZFC (requires the ultrafilter to exist, hence requires the Axiom of Choice). Accepted by mainstream mathematics, though the epsilon-delta approach remains standard in pedagogy.

---

### 1.2 Grossone / Sergeyev's Infinity Methodology

**Who:** Yaroslav Sergeyev, University of Calabria. First detailed in a 2003 monograph; expanded through dozens of papers with the Infinity Computer (patented in the USA and EU).

**What it is.** Sergeyev introduces a new numeral, grossone (written ①, read "grossone"), defined by a postulate called the Infinite Unit Axiom: ① is the number of elements of the set N of natural numbers. It is treated as a number with both cardinal and ordinal properties — like a finite natural number n is simultaneously "the count {1,...,n}" and "the position n," grossone plays this role at the infinite scale.

The resulting numeral system allows expressions like:

- ①, ①/2, ①², 1/① (an infinitesimal), sin(①), and so on.
- Arithmetic operations are defined formally on "grossone numerals" — polynomials in ① with real coefficients.
- The Infinity Computer (a software/hardware architecture) implements these numerals numerically.

**What it does for cardinality.** Under this system:
- |N| = ①
- |even numbers| = ①/2
- |squares in N| = √①

This gives a proportional arithmetic of infinite set sizes that feels intuitive — the evens are "half" the naturals.

**What it does not do.**
- Division by zero remains undefined. Sergeyev does not attempt to define 1/0. His system is about infinities and infinitesimals, not about division by zero.
- 0 × ∞: This form is not directly addressed. Since 1/① is infinitesimal and ① is infinite, one can write (1/①) · ① = 1, but this is a specific pair — the general indeterminate form is not resolved.
- There is no transfer principle. One cannot automatically port classical theorems to the grossone setting. Asking what sin(①) equals forces the answer to be "sin(①)" — a symbolic placeholder, not a number.

**The controversy.** Gutman, Katz, Kudryk, and Kutateladze (2016, *Foundations of Science*) mounted substantial criticism:

1. **Circularity.** Grossone is defined as "the number of elements of N," but it is simultaneously claimed to belong to N. This is circular: the size of a set cannot coherently be a member of that same set.
2. **No transfer principle.** Without it, extending functions to ① is arbitrary. sin(①) has no determined value.
3. **Subsumption.** Any consistent portion of the grossone axiom system (what the critics call GOT minus PATHOS) is strictly weaker than Nelson's Internal Set Theory (IST) — a rigorous extension of ZFC. Whatever grossone can do, IST can do more cleanly.
4. **No implemented calculator.** Despite the patent, there is no working general-purpose Infinity Computer. Only toy implementations handling polynomials of degree 1 in ① exist.
5. **Comparison undecidability.** Given two grossone numerals x and y in general form, there is no known algorithm to decide whether x < y, x = y, or x > y.

Sergeyev has responded to all of these, arguing that his methodology represents a different philosophy of mathematics and is independent of (not contradicted by) NSA. The debate continues; the system remains controversial among foundations specialists while finding applied users in numerical optimization.

---

### 1.3 Numerosity Theory

**Who:** Vieri Benci (University of Pisa) and Mauro Di Nasso (University of Pisa), with Marco Forti. First major paper: "Numerosities of Labelled Sets: A New Way of Counting," Advances in Mathematics, 2003. Book: *How to Measure the Infinite* (World Scientific, 2019).

**What it is.** Numerosity theory generalizes the counting of finite sets to infinite sets while preserving what the authors call the *Euclidean principle*: the whole is strictly greater than any of its proper parts. Cantor's cardinality does not satisfy this (|N| = |2N| under bijection). Numerosity theory does.

**The construction.** The theory assigns to each "labelled set" (a set whose elements come labeled with natural number positions) a "numerosity," a value in a non-Archimedean field (specifically, a field of hypernatural numbers). The construction proceeds through:

1. Approximating sequences: for a set A labeled in N, form the sequence a(n) = |A ∩ {1,...,n}| (how many elements of A appear in the first n natural numbers).
2. Two sets have the same numerosity if and only if their approximating sequences agree on a set belonging to a fixed Ramsey ultrafilter on N.

**Key results.**
- |N| = α for some infinite hypernatural α.
- |even numbers| = α/2.
- |odd prime numbers| < |odd numbers|.
- |{1, 2, ..., n}| = n for all finite n (exact agreement with cardinality on finite sets).
- The arithmetic of numerosities is commutative, associative, and well-behaved — unlike ordinal arithmetic.

**Dependency.** The existence of numerosity functions is equivalent to the existence of a Ramsey (selective) ultrafilter on N, which is independent of ZFC. Different ultrafilters give different but consistent numerosity assignments; the proportional relationships (evens = half of naturals) are robust across all valid ultrafilters.

**What it does not do.**
- Does not address division by zero.
- Does not address 0 × ∞.
- Does not provide calculus or differentiation.
- The absolute size α of N is not canonical: you cannot say "|N| = some specific number" without specifying the ultrafilter.

**Foundational status.** Rigorous, published in mainstream journals, debated in philosophy of mathematics. Not controversial the way grossone is — it is provably consistent within the same assumptions as NSA (both require ultrafilters). The philosophical choice (Aristotle's principle over Cantor's) is transparent and explicit.

---

### 1.4 Wheel Algebra

**Who:** Jesper Carlstrom, Stockholm University. 2001 licentiate thesis; 2004 paper "Wheels — On Division by Zero," *Mathematical Structures in Computer Science.*

**What it is.** A wheel is an algebraic structure extending a commutative ring by adding a unary operation / (reciprocal) and two distinguished elements:

- ∞ = /0 (the reciprocal of zero, i.e., "1 divided by 0")
- ⊥ = 0/0 (the reciprocal-of-zero times zero — the "bottom" element)

The key insight is that / is not the same as the multiplicative inverse. It is a unary operation, and division a/b is shorthand for a · /b. This allows /0 to be defined (as ∞) without creating a contradiction, because /0 is not the multiplicative inverse of 0 (zero has no multiplicative inverse — that would require 0 · x = 1, which is still prohibited).

**Arithmetic rules.** The axioms for a wheel are:
- + and · are commutative and associative with identities 0 and 1.
- /(/x) = x (the reciprocal operation is an involution).
- /(xy) = /x · /y (reciprocal distributes over products).
- (x + y)z + 0z = xz + yz (distributivity holds modulo a "0z" correction term).
- (x + 0y)/y = x/y + z + 0·/y (a modified quotient identity).
- 0/0 + x = 0/0 (the bottom element ⊥ absorbs addition).

**What fails compared to rings:**
- 0x ≠ 0 in general.
- x/x ≠ 1 in general.
- x − x ≠ 0 in general (it equals 0x²).
- Multiplication does not distribute over addition without the correction term.
- 0 · ∞ = 0 · /0 = 0/0 = ⊥ (the bottom element, not a finite number).

**What it does for division by zero.** y/0 = y · /0 = y · ∞ (well-defined as a product involving ∞). For nonzero y, this is ∞. For y = 0: 0/0 = ⊥. The key property is that ⊥ propagates through all operations: once you compute 0/0, everything downstream is ⊥. This makes it useful for error-tracking in computer arithmetic (IEEE floating point uses a similar philosophy with NaN).

**What it does not do.**
- The product 0 · ∞ is ⊥ (undefined/bottom), not a finite number. There is no mechanism to recover a finite result from 0 · ∞.
- No calculus or differentiation.
- No assignment of infinite set sizes.
- The arithmetic is severely weakened: 0x ≠ 0 breaks most intuitive expectations.

**Foundational status.** Rigorous. Accepted as a legitimate algebraic construction. Used in computer science for total division implementations. Not mainstream in analysis or applied mathematics.

---

### 1.5 Surreal Numbers

**Who:** John Horton Conway, Cambridge University. Discovered while studying combinatorial game theory in the late 1960s, first fully described in *On Numbers and Games* (1976). Independently introduced by Donald Knuth in a 1974 novel, *Surreal Numbers*.

**What it is.** The surreal numbers (No) are constructed by a transfinite induction. Each surreal number is a pair {L | R} where L and R are sets of previously constructed surreals with no member of L ≥ any member of R. The construction begins with {|} = 0 and generates, day by day, all integers, then all dyadic rationals, then all reals, then all infinities and infinitesimals.

The surreals form the *largest possible ordered field*: every ordered field embeds into them. They contain:

- ω (the first infinite surreal, corresponding to the ordinal ω).
- 1/ω (an infinitesimal smaller than every positive real).
- ω², ω^ω, 2^ω, ε₀, and vastly larger objects.
- Every real number.
- Infinitesimals of every order (1/ω, 1/ω², ...).

**Conway Normal Form.** Every surreal has a unique representation as a sum r₀ω^y₀ + r₁ω^y₁ + ... where the rᵢ are nonzero reals and y₀ > y₁ > ... are surreals. This is a far-reaching generalization of Cantor's ordinal normal form.

**What it does for calculus.** Surreal analysis is possible but underdeveloped. Work by Alling (1987) and more recently by Fornasiero and Costin-Ehrlich develops a theory of functions, limits, derivatives, and power series for surreals. The derivative can be defined via the standard-part-like operation for "series-style" surreal numbers. However, the theory is not complete: integration over the surreals remains technically difficult, and the system lacks an analogue of the transfer principle.

**What it does not do.**
- Division by zero: explicitly undefined. Surreals are a field; division by zero is prohibited.
- 0 × ∞: indeterminate, depends on which infinitesimals and infinities are paired. There is no mechanism to track provenance.
- The proper-class nature means set-theoretic constructions are awkward — you cannot directly form a set "of all surreals."

**Foundational status.** Fully rigorous but occupies an unusual foundation: the surreals form a proper class, not a set. ZFC axioms require adjustments (e.g., using NBG or MK class theory) to handle them correctly. Beloved by combinatorists and logicians; less used in analysis or applications.

---

### 1.6 Smooth Infinitesimal Analysis (SIA) / Synthetic Differential Geometry (SDG)

**Who:** F. W. Lawvere (category-theoretic foundations, 1960s–70s); Anders Kock (detailed development, *Synthetic Differential Geometry*, 1981, 2nd ed. 2006); John Bell (philosophical exposition, *A Primer of Infinitesimal Analysis*, 1998).

**What it is.** SIA/SDG is a reformulation of differential geometry and calculus in a topos-theoretic framework. The central idea is to work inside a "smooth topos" — a category of spaces where every map is smooth (infinitely differentiable) by construction. In this setting, the real line R is enriched with nilpotent infinitesimals.

**The Kock-Lawvere Axiom.** The infinitesimals are elements of D = {ε ∈ R : ε² = 0}. This set is not just {0}: there are many ε with ε² = 0 but ε ≠ 0 (this is possible only in intuitionistic logic; classically, ε² = 0 implies ε = 0 in an ordered field). The Kock-Lawvere axiom states: every function f : D → R has a unique decomposition f(ε) = f(0) + f'(0)ε.

**How differentiation works.** Given any function f : R → R, for any x and any nilsquare ε:

    f(x + ε) = f(x) + f'(x) · ε

This is exact (not an approximation) because ε² = 0 kills all higher-order terms. The derivative f'(x) is the unique slope of this linear map. No limits, no standard parts — the derivative falls directly out of the algebraic identity.

**What it does not do.**
- The logical framework is intuitionistic: the law of excluded middle is rejected. Classical mathematicians find this uncomfortable. Many theorems fail or need reformulation (e.g., the intermediate value theorem in its classical form fails).
- Division by zero: not addressed. The framework is about smoothness and tangency, not about singularities.
- 0 × ∞: not addressed. Nilsquare infinitesimals are genuinely small but D does not contain infinite elements.
- Set cardinalities: not addressed. SDG is geometry-focused.
- There is no transfer principle. The system cannot import classical theorems automatically.

**Foundational status.** Rigorous within intuitionistic/topos-theoretic mathematics. Less accessible than NSA due to the categorical machinery and non-classical logic. Influential in theoretical physics (synthetic approaches to differential geometry) but not widely used in analysis or computation.

---

## 2. Comparison Table

The following table maps each framework against the core problems IVNA addresses.

| Feature | NSA | Grossone | Numerosity | Wheel | Surreals | SIA/SDG | **IVNA** |
|---|---|---|---|---|---|---|---|
| **Division by zero defined** | No | No | No | Partially* | No | No | **Yes (y/0_x = ∞_{y/x})** |
| **0 × ∞ resolved to finite** | No (indeterminate) | Only for 1/① · ① = 1 | No | No (→ ⊥) | No (indeterminate) | No (not in scope) | **Yes (0_x · ∞_y = xy)** |
| **Infinitesimals** | Yes (hyperreals) | Yes (1/①) | Via numerosity field | No | Yes (1/ω, etc.) | Yes (nilsquare ε) | Yes (0_x, virtual zeros) |
| **Infinities** | Yes (hyperreals) | Yes (①) | Via numerosity field | Yes (∞, ⊥) | Yes (ω, ω², ...) | No (not in scope) | Yes (∞_x, virtual infinities) |
| **Derivatives without limits** | Yes (via st()) | Partial (ad hoc) | No | No | Partial (undeveloped) | Yes (via ε² = 0) | **Yes (substitute 0_1, read off)** |
| **Proportional set sizes** | Not canonical | Yes (①/2 for evens) | Yes (α/2 for evens) | No | Not directly | No | **Yes (|[0,1]| = ∞_1, |[2,4]| = ∞_2)** |
| **Collapse / standard part** | Yes (st() function) | No (informal) | No | No | Partial | No | **Yes (=; operator)** |
| **"0/0" given a value** | No | No | No | Yes (⊥, propagates) | No | No | **Depends on indices (0_x/0_y = ∞_{1/(xy)?})** |
| **Classical arithmetic preserved** | Yes (transfer principle) | Weakly | For finite sets exactly | No (0x ≠ 0) | Yes (as subfield) | Weakly (intuitionistic) | Unknown (under investigation) |
| **Rigorous foundation** | Yes (ZFC + ultrafilter) | Controversial | Yes (ZFC + ultrafilter) | Yes (abstract algebra) | Yes (NBG/MK) | Yes (topos theory) | Not yet established |
| **Calculus applications** | Extensive | Limited | None | None | Limited | Extensive (geometry) | Intended, under development |
| **Computer science use** | Moderate | Limited | None | Yes (total division) | None | Minimal | Intended |

*Wheel algebra defines y/0 as y · ∞ (fine for y ≠ 0), and 0/0 as ⊥ (an absorbing error element), but does not recover a finite number from 0 · ∞.

---

## 3. Where IVNA May Be Genuinely Novel

Based on the literature survey, these features of IVNA do not appear to have direct precedents:

### 3.1 The Indexed Product Rule: 0_x · ∞_y = xy

No existing framework resolves the product of a zero-class object and an infinity-class object to a determinate finite number in the way IVNA proposes. Specifically:

- NSA: The product ε · ω is indeterminate — its standard part depends on the specific ε and ω. NSA has no mechanism to say "this infinitesimal came from dividing some quantity by this particular infinity," so it cannot automatically recover the product.
- Wheel algebra: 0 · ∞ = ⊥ (the bottom element, i.e., undefined/error). The framework explicitly abandons finite recovery from this product.
- Grossone: (1/①) · ① = 1, but this is a specific case, not a general rule over an index space.
- Surreals: No mechanism for tracking provenance; (1/ω) · ω = 1 but (2/ω) · ω = 2, etc. — each case handled separately, no algebraic index structure.

IVNA's proposal is structurally different: the indices x and y are designed to carry exactly the information needed to resolve the product as xy. This is not a feature of any reviewed framework.

### 3.2 Parameterized Zero / Infinity Space

The idea that zero is not a single point but a family {0_x : x ∈ R} parameterized by a real index, and that infinities form a parallel family {∞_x}, does not appear in the reviewed literature. The closest analogues are:

- NSA hyperreals: There is a family of infinitesimals (anything smaller than all positive reals), but they are not indexed by a real parameter in a structured way. Two hyperreals ε₁ and ε₂ can be compared (one might be twice the other), but there is no labeling system that assigns a canonical real number to each infinitesimal.
- Grossone: Only one canonical infinitesimal (1/①) and one canonical infinite (①), with derivatives (①², ①/2, etc.) — but these form a discrete lattice, not a continuous parameter space.
- SIA: Nilsquare infinitesimals form the set D = {ε : ε² = 0}, but they are not indexed by reals. The entire set D acts as a "first-order infinitesimal neighborhood" and is treated as a single geometric object.

A continuously indexed family of zeros/infinities, where the index is a real number tracking relative magnitude, appears to be original.

### 3.3 Direct Substitution for Derivatives

The NSA approach requires: compute f(x + ε), divide by ε, apply st(). Three steps, with the standard part function as an explicit operation. SIA requires: work inside a topos with ε² = 0, and read off the unique coefficient of ε. IVNA's stated approach — substitute 0_1 directly into a formula designed for limits, and read the coefficient — is syntactically simpler than NSA (no st() needed at the end) and does not require a non-classical logic framework (unlike SIA). The mechanism is different from both.

However, this is also the area of highest risk: if IVNA's derivative computation is not rigorously justified, it may reduce to a notational shorthand for the NSA procedure rather than a genuinely new construction.

### 3.4 Proportional Interval Lengths as Set Sizes

The assignment |[0,1]| = ∞_1 and |[2,4]| = ∞_2 (because [2,4] is twice as long) captures geometric measure-theoretic intuition in a notation that Cantor's cardinality does not support (both intervals have the same cardinality, |R|). Numerosity theory assigns different numerosities to different "labelled" countable sets, but the extension to continuous intervals with uncountable cardinality is less developed in the numerosity literature. IVNA's index corresponding directly to interval length (or measure) is a specific interpretive choice not present in the reviewed frameworks.

---

## 4. Risks — Where IVNA May Overlap with Existing Work

### Risk 1: The Indexed Product as Disguised NSA

The most serious isomorphism risk: IVNA's 0_x might simply be "a specific infinitesimal whose ratio to some reference infinitesimal is x." In NSA, if we fix a reference infinitesimal ε₀, then every other infinitesimal ε can be written as r · ε₀ for some hyperreal r. If r is standard (a real number), then we could define 0_r := r · ε₀ and ∞_r := r/ε₀, and observe that (r · ε₀) · (s/ε₀) = rs. This is formally identical to IVNA's 0_x · ∞_y = xy.

**If this isomorphism holds**, IVNA is a notational simplification of a specific part of NSA — still potentially valuable (a cleaner notation can be a real contribution), but not a new mathematical object.

**What would make IVNA distinct:** if it can handle cases that the fixed-ε₀ construction in NSA cannot — for example, if the index x can itself be a virtual number (0_{0_1}, an "infinitely small index"), or if the index space has algebraic structure that NSA's free infinitesimals do not.

### Risk 2: Wheel Algebra Relationship

The =; collapse operator and the behavior of indexed numbers at "non-virtual" arguments both echo the structure of wheel algebra. However, the crucial difference is: in wheel algebra, 0 · ∞ = ⊥ (lost information). In IVNA, 0_x · ∞_y = xy (information preserved). These are structurally different: IVNA is strictly more informative than wheel algebra at this operation. IVNA is not a wheel.

### Risk 3: Grossone Overlap on Set Sizes

The assignment |N| = ∞_? (some specific virtual infinity) and |evens| = ∞_{?/2} parallels Sergeyev's |N| = ① and |evens| = ①/2. The underlying intuition is the same: assign a "count" to N and derive proportional counts for subsets. The key question is whether IVNA's ∞_x for set sizes is defined independently of the cardinality-counting framework, or whether it borrows from it. If IVNA's set-size claims are a restatement of grossone or numerosity in different notation, this should be acknowledged.

The advantage IVNA may have here: its index is a real-valued continuous parameter (so |[0,1]| = ∞_1 and |[0,π]| = ∞_π work naturally), whereas grossone is a single postulated unit and numerosity works on labeled countable sets. Extending to continuous measure is a genuine extension.

### Risk 4: Derivative Computation vs. SIA

IVNA's "substitute 0_1 and read the coefficient" approach to derivatives is structurally similar to SIA's "every function f : D → R is of the form f(ε) = f(0) + f'(0)ε." Both avoid limits; both treat the infinitesimal as an algebraic entity you substitute. The difference: SIA uses ε² = 0 as the justification for why higher-order terms vanish, and operates in intuitionistic logic. IVNA would need a different justification — the algebraic rules for virtual numbers need to imply that higher-order virtual terms collapse when the =; operator is applied.

If IVNA's rules do not provide this justification rigorously, the derivative computation may be a syntactic trick that works for polynomials but fails for transcendental functions or compositions.

---

## 5. The Complex Number Precedent — How Paradigm Shifts Happen in Mathematics

### The Historical Arc

The history of complex numbers is the canonical case study for how mathematics absorbs an "impossible" object.

**Stage 1: Forced appearance (Cardano, 1545).** Cardano's Ars Magna gave formulas for solving cubic equations. When applied to x³ = 15x + 4 (which has x = 4 as an obvious real solution), the formula required computing √(-121). Cardano called such quantities "as refined as they are useless" and solved around them.

**Stage 2: Rule-making without justification (Bombelli, 1572).** Rafael Bombelli recognized that if you follow the rules for √(-1) consistently — even without knowing what it "means" — the imaginary intermediate steps cancel out and you recover the correct real answer. He gave explicit computational rules for adding, multiplying, and dividing complex numbers. No one believed these objects were legitimate, but the rules worked.

**Stage 3: Geometric legitimization (Wessel 1799, Argand 1806, Gauss 1831).** The geometric interpretation of complex numbers as points in the plane transformed them from algebraic curiosities into geometric objects. Gauss formally introduced the term "complex number" in 1831 and demonstrated their indispensability in proving the Fundamental Theorem of Algebra. The geometric picture gave intuition that made the abstract rules feel grounded.

**Stage 4: Universal adoption.** Complex numbers are now foundational to quantum mechanics, electrical engineering, signal processing, control theory, and much of pure mathematics. The "imaginary" disappeared as a label; the objects are simply numbers.

### Key Lessons for IVNA

**Bombelli's lesson:** You do not need to understand what 0_x "is" to use it. If the rules for indexed zeros and infinities are internally consistent and produce correct results, the system is mathematically legitimate — even if a construction proving its legitimacy comes later. However, Bombelli's rules were provably consistent (they were rules for a real algebraic system — the Gaussian integers embedded in C). IVNA needs the same: not a story about what indexed zeros "are," but a proof that a consistent model exists.

**Gauss's lesson:** The geometric picture was decisive for acceptance. IVNA needs an analogous interpretive picture. A potential candidate: think of the real line as embedded in a 2D "virtual plane" where the vertical axis tracks "virtuality index." A zero at height x on this axis is 0_x; an infinity at height y is ∞_y. The =; operator projects this plane onto the real line. This picture, if it can be made rigorous, would serve as IVNA's Argand plane.

**The critical difference from complex numbers:** Complex numbers appeared because they were needed — the cubic formula forced them. IVNA needs to demonstrate the same kind of forced necessity: problems that cannot be solved without indexed zeros, or problems that become dramatically simpler with them. The strongest current candidate is the derivative computation. If IVNA can make derivatives genuinely simpler and more intuitive than NSA's approach (no st() needed, works for beginners), that is a pedagogical case. For mathematical novelty, the more important case is whether there are problems — in renormalization, in singularity theory, in measure theory — where indexed zeros provide something that existing frameworks genuinely cannot.

**The acceptance timeline.** Complex numbers took from 1545 (Cardano) to 1831 (Gauss's legitimization) — nearly three centuries from "useful but suspicious" to "universally accepted." Even then, full philosophical settlement came with Hamilton's formal algebraic construction (1835) and the embedding in R² as ordered pairs. IVNA's author should plan for a long road: internal consistency is necessary but not sufficient for adoption. The framework needs compelling applications where it outperforms alternatives, clear pedagogy, and eventually a rigorous model construction.

---

## 6. Criticisms of Grossone That May Apply to IVNA

Several of the mathematical objections raised against grossone are not specific to Sergeyev's particular choices — they apply to any framework that introduces new number-like objects without a complete rigorous foundation. IVNA should be prepared to answer each:

**Criticism 1: Circularity.** Grossone is criticized for defining ① as "the count of N" while claiming ① belongs to N. IVNA must avoid analogous circularity. Specifically: what is the domain of the index x in 0_x? If x can be a virtual number itself (x = 0_y), this recursion needs a well-founded base case.

**Criticism 2: Lack of a transfer principle.** Without it, you cannot automatically port classical theorems. If sin(0_1) must be computed, what is it? Is it the sin of a very small number (near 0), or must a separate rule be specified? IVNA will need to decide: either provide a transfer-principle-like mechanism, or explicitly characterize which classical operations extend to virtual numbers and which do not.

**Criticism 3: Comparison undecidability.** For grossone numerals, comparing two expressions is undecidable. For IVNA: given 0_x and 0_y, the comparison is presumably just x vs. y. But for more complex virtual expressions — say, the result of a chain of virtual-number operations — is the ordering always well-defined? This needs to be proven, not assumed.

**Criticism 4: Subsumption.** Critics showed grossone is subsumed by IST. The analogous risk for IVNA: if the indexed-zero construction can be embedded in NSA by fixing a reference infinitesimal (Risk 1 above), then IVNA is a notational variant, not a new mathematical theory. The response to this criticism is not "it's different because we use different notation" but "here is a theorem/model/problem that IVNA handles and NSA cannot."

**Criticism 5: Foundational vagueness.** Grossone's axioms have been criticized for relying on "semantical postulates" that determine the scope of syntactic axioms — an unprecedented and suspicious logical move. IVNA's axioms should be formulated at a clear logical level: are they axioms of a new algebraic theory (like ring axioms)? Extensions of ZFC? Constraints on a specific model? The framing matters for how the system will be received.

---

## 7. Key Papers and Sources

**Non-Standard Analysis:**
- Robinson, A. (1961). "Non-Standard Analysis." *Proceedings of the Royal Academy of Amsterdam.*
- Robinson, A. (1966). *Non-Standard Analysis.* North-Holland.
- Keisler, H. J. (1976). *Elementary Calculus: An Infinitesimal Approach.* (Free online at math.wisc.edu/~keisler/calc.html)
- Wikipedia: [Nonstandard analysis](https://en.wikipedia.org/wiki/Nonstandard_analysis), [Hyperreal number](https://en.wikipedia.org/wiki/Hyperreal_number)

**Grossone:**
- Sergeyev, Ya. D. (2003). *Arithmetic of Infinity.* Edizioni Orizzonti Meridionali.
- Sergeyev, Ya. D. (2017). "Numerical infinities and infinitesimals: Methodology, applications, and repercussions on two Hilbert problems." *EMS Surveys in Mathematical Sciences*, 4(2), 219–320.
- Gutman, A. E., Katz, M. G., Kudryk, T. S., Kutateladze, S. S. (2017). "The Mathematical Intelligencer Flunks the Olympics." *Foundations of Science*, 22(3), 539–555. [ArXiv:1606.00160](https://arxiv.org/abs/1606.00160)
- Sergeyev, Ya. D. (2018). "Independence of the Grossone-Based Infinity Methodology from Non-Standard Analysis." *Foundations of Science*, 24(1), 187–204.

**Numerosity Theory:**
- Benci, V., Di Nasso, M. (2003). "Numerosities of Labelled Sets: A New Way of Counting." *Advances in Mathematics*, 173(1), 50–67.
- Benci, V., Di Nasso, M., Forti, M. (2006). "An Aristotelian Notion of Size." *Annals of Pure and Applied Logic*, 143(1–3), 43–53.
- Benci, V., Di Nasso, M. (2019). *How to Measure the Infinite.* World Scientific.
- Stanford Encyclopedia: [Theories of Numerosities](https://plato.stanford.edu/entries/infinity/numerosities.html)

**Wheel Algebra:**
- Carlstrom, J. (2001). "Wheels." Licentiate thesis, Stockholm University. [Available at math.su.se](https://www2.math.su.se/reports/2001/11/2001-11.pdf)
- Carlstrom, J. (2004). "Wheels — On Division by Zero." *Mathematical Structures in Computer Science*, 14(1), 143–184.
- Wikipedia: [Wheel theory](https://en.wikipedia.org/wiki/Wheel_theory), nLab: [wheel](https://ncatlab.org/nlab/show/wheel)

**Surreal Numbers:**
- Conway, J. H. (1976). *On Numbers and Games.* Academic Press.
- Knuth, D. (1974). *Surreal Numbers.* Addison-Wesley.
- Alling, N. L. (1987). *Foundations of Analysis over Surreal Number Fields.* North-Holland.
- Wikipedia: [Surreal number](https://en.wikipedia.org/wiki/Surreal_number)

**Smooth Infinitesimal Analysis / SDG:**
- Lawvere, F. W. (1979). "Categorical Dynamics." In *Topos-Theoretic Methods in Geometry.*
- Kock, A. (1981, 2006). *Synthetic Differential Geometry.* Cambridge University Press.
- Bell, J. L. (1998). *A Primer of Infinitesimal Analysis.* Cambridge University Press.
- Wikipedia: [Smooth infinitesimal analysis](https://en.wikipedia.org/wiki/Smooth_infinitesimal_analysis)

**Additional Frameworks Reviewed:**
- Anderson, J. A. D. W. (2007). "Perspex Machine XI: Topology of the Transreal Numbers." — The "nullity" / transreal number approach. Widely criticized as less mathematically rigorous.
- Saitoh, S. (2014–2020). Division by Zero Calculus. — The z/0 = 0 approach. Controversial; treats all z/0 as identically 0, which breaks standard results.
- Bergstra, J. A. (2019). "Division by Zero: A Survey of Options." *Transmathematica.* — A useful taxonomy of the design space for total-division algebras.

**Complex Number History:**
- Cardano, G. (1545). *Ars Magna.*
- Bombelli, R. (1572). *L'Algebra.*
- Complex analysis history: [complex-analysis.com/content/brief_history.html](https://complex-analysis.com/content/brief_history.html)
- Gauss's role: [Remarks on the History of Complex Numbers](https://www.cut-the-knot.org/arithmetic/algebra/HistoricalRemarks.shtml)

---

## 8. Synthesis: IVNA's Position in the Landscape

IVNA occupies a specific niche that no single existing framework fills:

**What NSA does that IVNA aims to do better:** NSA handles infinitesimals and limit-free differentiation but requires an explicit standard part function and leaves 0 × ∞ indeterminate. IVNA's goal is to carry provenance information (the index) through products, making the result determinate without applying st(). This is a genuine extension of the idea — if consistent, it would subsume the main use case of NSA for calculus while handling more cases.

**What grossone does that IVNA extends:** Grossone assigns proportional sizes to infinite sets (|evens| = ①/2) but lacks a transfer principle and cannot handle division by zero or the full range of indeterminate forms. IVNA's continuous index space allows |[0,π]| = ∞_π naturally, which is not available in the grossone framework.

**What wheel algebra does that IVNA supersedes:** Wheel algebra defines y/0 for y ≠ 0 but loses information when both numerator and denominator are zero (0/0 = ⊥, the absorbing bottom element). IVNA's approach — 0_x/0_y = ∞_{x/y}? (pending formal definition) — would preserve more information. IVNA is strictly more expressive than wheel algebra at the critical case.

**What SIA does that IVNA parallels differently:** SIA achieves limit-free differentiation via nilsquare ε (ε² = 0 in intuitionistic logic). IVNA achieves it via indexed substitution without changing the underlying logic. Both are appealing; IVNA has the advantage of not requiring non-classical logic, which would dramatically lower the barrier to adoption.

**The honest summary:** IVNA is closest to a cleaned-up, more expressive version of the fragment of NSA that handles derivatives and indeterminate forms, combined with a continuous version of grossone-style set sizing. Its core novelty claim rests on the indexed product rule 0_x · ∞_y = xy. If this rule can be given a rigorous model (ideally as a quotient of a free algebra modulo the IVNA axioms, or as a sub-theory of NSA using a structured infinitesimal basis), then IVNA is a legitimate new tool with a cleaner interface than its predecessors. If the rule is shown to be either inconsistent or merely notational shorthand for NSA constructions, IVNA's value shifts from "new mathematics" to "pedagogical simplification" — still worthwhile, but different.

The critical next step — and the one that will determine this system's status — is Section 1 of the plan: computational consistency verification. Before any literature positioning can be finalized, we need to know whether the IVNA axioms are internally consistent, and specifically whether 0_x · ∞_y = xy can coexist with the other rules without contradiction.

---

*Prepared: 2026-03-31*
*Sources: Web search, Wikipedia, Stanford Encyclopedia of Philosophy, arXiv, Springer Nature, Cambridge Core*
*Next section: plan-section-consistency.md (computational audit of axioms)*
