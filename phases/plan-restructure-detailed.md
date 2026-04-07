# IVNA Paper Restructure — Detailed Edit Plan

**Date:** 2026-04-02
**Input sessions:** VERIFY (155/0), SEARCH (2 novel, 4 partial), EXPLORE (3 deep dives), DEBATE (CON wins on framing)
**Paper:** `paper/ivna-paper.tex` (1416 lines, ~35 pages)
**Constraint:** Stay under 40 pages (~1600 lines)
**Guiding principle:** Division by zero is the thesis. Cross-domain observation is the evidence. Playful in framing, sincere in mathematics.

---

## Proposed New Structure

```
  Epigraph (NEW)
  Abstract (REVISED — add cross-domain teaser, update verification count)
1. Introduction (REVISED — add footnote, add "bigger nothing", add cross-domain teaser in Summary)
2. Core Algebra (KEEP — minor: update index domain remark)
3. Extended Axioms (KEEP)
4. Consistency (KEEP — minor: mention K* × Z explicitly if not already)
5. Applications: Calculus (KEEP — tighten L'Hôpital subsection slightly)
6. The Product Rule Across Domains (NEW — the cross-domain observation)
   6.1 The Observation (table)
   6.2 Probability: A8 as Bayes' Theorem (NEW — star section)
   6.3 The Dirac Delta from A3 (NEW)
   6.4 Removable Singularities as Index Cancellation (NEW)
   6.5 Blow-up Correspondence (PROMOTED from Section 8)
   6.6 Structural Remark (universal receiver framing from category deep dive)
7. Applications: Physics (KEEP — condensed slightly)
8. Applications: Computer Science (KEEP)
9. Literature Positioning (UPDATED — new citations, blow-up moved out, comparison updated)
10. Limitations and Scope (UPDATED — harmonic limitation, honest restatement assessment)
11. Research Methodology (NEW — brief, ~1/2 page)
12. Conclusion (REVISED — preserve division-by-zero arc, add cross-domain coda)
Bibliography (UPDATED — ~10 new citations)
Appendix A: Verification Details (UPDATED — new counts, methodology expansion)
```

**Estimated line budget:**
- Current: 1416 lines
- Removing: ~40 lines (blow-up from Lit. Positioning, L'Hôpital tightening, Physics condensing)
- Adding: ~220 lines (Section 6: ~120, methodology: ~30, new citations: ~30, playful elements: ~15, misc updates: ~25)
- New total: ~1596 lines (~39.5 pages) — within budget

---

## Section-by-Section Edit Plan

### 0. Epigraph (NEW — before Abstract)

**Add after `\begin{document}` and `\maketitle`, before `\begin{abstract}`:**

```latex
\begin{center}
\textit{``The limit does not exist!''}\\[0.3em]
--- Cady Heron, \textit{Mean Girls} (2004)
\end{center}
\vspace{1em}
```

**Risk:** LOW. Epigraphs are common in math papers. This one is culturally recognizable, literally about a math competition, and sets the paper's tone. Reviewers who get it will smile; those who don't will ignore it.

---

### 1. Abstract (REVISED)

**Current:** Lines 48-81 (~33 lines). Focuses on calculus applications and VEA mode.

**Changes:**
- Add one sentence after the applications paragraph teasing the cross-domain observation
- Update verification count from 489 to new total (489 + 155 phase 4 + 63 explore = 707, but needs reconciliation — see Appendix section)
- Keep division by zero as the headline

**Draft — add after "...when operand indices are tracked." (line 77) and before the closing of abstract:**

```latex
Beyond calculus, the product rule $\vz{x} \cdot \vi{y} = xy$ recurs as
the resolution mechanism across multiple domains---the Dirac delta in
distribution theory, conditional densities in probability, residue
extraction in complex analysis, and blow-up resolution in algebraic
geometry---suggesting a shared algebraic skeleton underlying how
mathematics handles singularities.
```

**Risk:** LOW. This is a factual observation backed by 155 verification checks. Framed as "suggesting" (not "proving unification"), which is defensible.

---

### 2. Introduction (REVISED)

**Current:** Lines 84-234 (~150 lines). Four subsections: Problem, Precedent, Proposal, Summary.

**Changes:**

#### 2a. Add "undefined" footnote (line ~103)

After "...all classified as *indeterminate forms*" (line 103), add footnote:

```latex
\footnote{``Undefined'' is mathematics' way of saying the question
contains more information than the notation can hold.}
```

#### 2b. Add "bigger nothing" passage (near line 157)

After the definition of virtual number families (line 156), add a remark:

```latex
\begin{remark}[Why ``virtual'']
More nothing will fit into a bigger thing than it would a smaller
thing, even though it is still nothing. A swimming pool drained of
water contains more ``nothing'' than a thimble. The index captures
this: $\vz{5}$ represents the same mathematical zero as $\vz{1}$
under the collapse operator ($\vz{5} \ceq 0 = \vz{1} \ceq 0$),
but it is a zero with five times the capacity. In the NSA embedding,
$\vz{5} = 5\varepsilon_0$ is literally five times larger than
$\vz{1} = \varepsilon_0$---still infinitesimal, but proportionally
larger. The term ``virtual'' reflects this: these zeros are not
the absence of quantity but the presence of an infinitesimal one.
\end{remark}
```

**Risk:** LOW. This is pedagogically valuable and mathematically correct via the NSA embedding.

#### 2c. Add cross-domain teaser to Summary of Results (line ~233)

Add a 7th item to the enumerated list:

```latex
\item \textbf{Cross-domain structural observation}
  (Section~\ref{sec:crossdomain}): the product rule
  $\vz{x} \cdot \vi{y} = xy$ recurs as the resolution mechanism
  in at least nine mathematical domains, from derivatives to the
  Dirac delta to Bayes' theorem for continuous densities. This
  suggests a shared algebraic skeleton underlying singularity
  resolution across mathematics.
```

---

### 3. Core Algebra (KEEP — minor updates)

**Current:** Lines 238-479 (~241 lines)

**Changes:** None required. The axioms, definitions, and proofs are solid and verified. The index domain remark (line 465-479) already covers virtual-valued indices.

---

### 4. Extended Axioms (KEEP)

**Current:** Lines 483-545 (~62 lines)

**Changes:** None.

---

### 5. Consistency (KEEP — minor)

**Current:** Lines 549-655 (~106 lines)

**Changes:**
- Update verification count in proof sketch (line 599): change "489 checks" to reconciled new total
- The K* × Z characterization (lines 607-628) is already well-stated. No changes needed.

---

### 6. Applications: Calculus (KEEP — tighten slightly)

**Current:** Lines 658-838 (~180 lines)

**Changes:**
- Tighten the L'Hôpital Elimination subsection (lines 698-724): the four cases are clear but could lose ~5 lines of prose without losing content
- The Residues subsection (lines 789-822) stays — it's now an example of the cross-domain pattern, and Section 6 will reference it
- Proportional Infinite Set Sizes (lines 824-838) stays — it's unique and interesting

**Net:** Save ~5-8 lines.

---

### 7. NEW: The Product Rule Across Domains (Section 6)

**Insert after Section 5 (Calculus), before Section 6 (Physics). ~120 lines total.**

This is the heart of the restructure. It collects the cross-domain observation WITHOUT claiming "unification" — instead, it observes a structural pattern and presents verified instances.

#### 6.1 The Observation (~20 lines)

```latex
\section{The Product Rule Across Domains}
\label{sec:crossdomain}

The indexed product rule $\vz{x} \cdot \vi{y} = xy$
(Axiom~\ref{ax:zi}) was introduced in Section~\ref{sec:core} as an
algebraic rule for resolving $0 \cdot \infty$. In
Section~\ref{sec:calculus}, it appeared as the mechanism behind
derivatives, integration, and residue extraction.

A broader pattern emerges: across at least nine mathematical domains,
the standard resolution of an indeterminate form reduces to the same
operation---the product of an indexed zero and an indexed infinity.
Each domain invented independent machinery (limits, distributions,
measure theory, blow-ups) to handle what IVNA resolves with one
algebraic rule.

\begin{center}
\begin{tabular}{llll}
\toprule
\textbf{Domain} & \textbf{Standard form} & \textbf{IVNA form} & \textbf{Section} \\
\midrule
Derivatives       & $\lim \frac{f(x+h)-f(x)}{h}$ & $\frac{\vz{f'(x)}}{\vz{1}} = f'(x)$  & \ref{sec:calculus} \\
Integration       & $\int f\,dx = \lim \sum f \Delta x$ & $\sum f \cdot \vz{1}$ over $\vi{1}$ terms & \ref{sec:calculus} \\
Compound growth   & $\lim (1+1/n)^n = e$   & $(1+\vz{1})^{\vi{1}} = e$  & \ref{sec:calculus} \\
Residues          & $\lim_{z\to a}(z-a)R(z)$  & $\vz{Q'(a)} \cdot \vi{P(a)/Q'(a)}$  & \ref{sec:calculus} \\
Dirac delta       & $\lim h \cdot (1/h)$   & $\vz{1} \cdot \vi{1} = 1$  & \ref{subsec:dirac} \\
Bayes / densities & $f(y|x) = \frac{f(x,y)}{f_X(x)}$ & $\frac{\vz{f(x,y)}}{\vz{f_X(x)}}$   & \ref{subsec:bayes} \\
Removable sing.   & $\lim_{x\to a} f(x)$   & $\frac{\vz{f_a}}{\vz{g_a}} = f_a/g_a$  & \ref{subsec:removable} \\
Blow-up           & Proper transform on $E$ & $(f_a, a)/(g_b, b)$  & \ref{subsec:blowup} \\
$\infty - \infty$ & Renormalization         & $\vi{a} - \vi{b} = \vi{a-b}$  & \ref{sec:core} \\
\bottomrule
\end{tabular}
\end{center}

We do not claim that this observation constitutes mathematical
unification in the sense that complex numbers unified $\R^2$ arithmetic.
What we observe is that a single algebraic rule---one that falls out
of the basic axioms with no additional machinery---recurs as the
computational core of techniques that were developed independently
across different branches of mathematics. The following subsections
verify the less familiar instances.
```

**Risk:** MEDIUM. The table is the boldest visual claim. The caveat paragraph ("We do not claim...") is essential. Every entry is verified (155 checks). The framing as "observation" rather than "unification" is defensible.

#### 6.2 Probability: A8 as Bayes' Theorem (~35 lines)

```latex
\subsection{Conditional Densities and Bayes' Theorem}
\label{subsec:bayes}

Let $X, Y$ be continuous random variables with joint density $f_{X,Y}$.
The event $\{X = x\}$ has probability zero---specifically, IVNA
probability $\vz{f_X(x)}$, where $f_X$ is the marginal density.
Bayes' theorem for the conditional density follows from Axiom~A8
($\vz{a}/\vz{b} = a/b$):
\[
f_{Y|X}(y \mid x) = \frac{P(X = x, Y = y)}{P(X = x)}
= \frac{\vz{f_{X,Y}(x,y)}}{\vz{f_X(x)}}
= \frac{f_{X,Y}(x,y)}{f_X(x)}.
\]
The density \emph{is} the index. No measure theory, no Radon--Nikodym
theorem, no limiting argument is required---just the zero-zero
quotient rule applied to indexed probabilities.

This resolves the Borel--Kolmogorov paradox transparently. The
``paradox'' arises when conditioning on the same geometric event
(e.g., a great circle on $S^2$) using different parameterizations
yields different conditional densities. In IVNA, different
parameterizations produce different indexed zeros---$\vz{f_X(x)}$
vs.\ $\vz{g_U(u)}$---and Axiom~A8 correctly produces different
quotients. The result is not paradoxical; it is the expected
consequence of dividing different indexed zeros.

Verification: tested on bivariate normal ($\rho$ general),
Gumbel bivariate exponential ($\theta = 0.5$), and bivariate
Cauchy (no finite moments). All conditionals integrate to~1.
The Cauchy case is the strongest test: a distribution with no
mean or variance still produces correct conditional densities
via A8 (6 checks, 0 failures; see supplementary
\texttt{verify-01-bayes-theorem.md}).

The closest prior work is Jacobs~\cite{jacobs2021}, who uses
infinitesimal ratios for conditional densities within a
categorical probability framework. IVNA's contribution is the
directness: A8 \emph{is} Bayes' theorem, stated as a single
axiom that was already present in the core algebra for independent
reasons.
```

**Risk:** MEDIUM-HIGH. This is the boldest new claim. Mitigation: cite Jacobs (2021) explicitly, frame as "directness" contribution, verification backs it up. The debate identified this as strong when properly grounded.

#### 6.3 The Dirac Delta (~25 lines)

```latex
\subsection{The Dirac Delta from the Product Rule}
\label{subsec:dirac}

The Dirac delta ``function'' $\delta(x)$ satisfies $\int \delta(x)\,dx = 1$
and $\delta(x) = 0$ for $x \neq 0$. Distribution theory
(Schwartz, 1950) formalizes this as a linear functional, not a function.

In IVNA, $\delta$ is a function: at $x = 0$, it takes the value $\vi{1}$
(infinite height), defined on a domain of width $\vz{1}$ (infinitesimal
support). Its ``area'' is:
\[
\vi{1} \cdot \vz{1} = 1 \quad \text{(Axiom~A3)}.
\]
The four standard properties follow algebraically:
\begin{enumerate}
\item \textbf{Normalization}: $\vi{1} \cdot \vz{1} = 1$. \checkmark
\item \textbf{Sifting}: $f(0) \cdot \vi{1} \cdot \vz{1} = f(0)$. \checkmark
\item \textbf{Scaling}: $\delta(ax)$ has height $\vi{1/a}$, so
  $\vi{1/a} \cdot \vz{1} = 1/|a|$. \checkmark
\item \textbf{Convolution}: index product of two deltas composes. \checkmark
\end{enumerate}

For any nascent delta family $h(\varepsilon) \cdot w(\varepsilon) = 1$
(height times width), the product $h \cdot w = 1$ holds at every
$\varepsilon > 0$---not just in the limit. Axiom~A3 characterizes the
\emph{entire family}, not its limit.

Verification: 28 checks across rectangular, Gaussian, and Lorentzian
nascent delta families (see supplementary
\texttt{verify-03-dirac-delta.md}).

The NSA treatment of delta functions dates to
Robinson~\cite{robinson1966}; Todorov~\cite{todorov1990} and
Vernaeve~\cite{vernaeve2025} develop this further. IVNA's
contribution is that the single axiom A3 unifies all four
properties, and the characterization is exact equality (not
the ``infinitely close'' relation $\approx$ of NSA).
```

**Risk:** MEDIUM. Partially anticipated by NSA literature. Mitigation: cite Todorov and Vernaeve, frame as "single axiom" simplification. 28 verification checks.

#### 6.4 Removable Singularities (~15 lines)

```latex
\subsection{Removable Singularities as Index Cancellation}
\label{subsec:removable}

A removable singularity of $f(x)/g(x)$ at $x = a$ occurs when both
$f$ and $g$ vanish at $a$ with the same order. In IVNA:
\[
\frac{f(a)}{\,g(a)\,} = \frac{\vz{f'(a)}}{\vz{g'(a)}} = \frac{f'(a)}{g'(a)}.
\]
The singularity ``removes itself'' by index cancellation (A8). No limit
is computed; the value at the point is defined by the algebra.

More generally, if $f$ vanishes to order $m$ and $g$ to order $n$ with
$m = n$, the IVNA quotient $\vzn{m}{c_f}/\vzn{n}{c_g} = c_f/c_g$
exits to a finite number. When $m > n$, the result is $\vz{c_f/c_g}$
(the function has a zero). When $m < n$, the result is $\vi{c_f/c_g}$
(a genuine pole). The order comparison determines the singularity type;
the index carries the value.

Verification: 24 checks across polynomial and trigonometric examples
(see supplementary \texttt{verify-04-removable-singularities.md}).
```

**Risk:** LOW. This is a clean, verifiable restatement of classical results in IVNA notation. 24 checks.

#### 6.5 Blow-up Correspondence (MOVED from Literature Positioning)

**Move Theorem 8.4 and its proof/example (current lines 1029-1071) here.** Rename subsection label to `\label{subsec:blowup}`. No content changes needed — the theorem and proof are already well-written.

```latex
\subsection{The Blow-Up Correspondence}
\label{subsec:blowup}

% [Move existing Theorem 8.4, proof, example, and discussion
%  from current lines 1029-1071 here verbatim]
```

**Risk:** LOW. Content already exists, verified, and reviewed. Moving it to a more prominent position was the debate's top recommendation.

#### 6.6 Structural Remark (~10 lines)

```latex
\subsection{A Structural Remark}

The observation that Axiom~A3 ($\vz{x} \cdot \vi{y} = xy$)
independently resolves indeterminate forms in nine domains can be
understood algebraically: each domain's resolution mechanism is an
independent embedding into IVNA's graded algebra $K^* \times \mathbb{Z}$,
where the product rule serves as the universal resolution step. The
index carries domain-specific information (derivative coefficients,
probability densities, residues, blow-up coordinates), while the
grade crossing from virtual to real ($+1 + (-1) = 0$) performs the
resolution.

Whether this algebraic observation has deeper structural significance---a
functorial relationship between domains, perhaps---is an open question
for future work.
```

**Risk:** LOW. Explicitly framed as observation and open question. Grounded in the K* × Z characterization already in the paper.

---

### 8. Applications: Physics (CONDENSED slightly)

**Current:** Lines 842-889 (~47 lines)

**Changes:**
- Tighten the prose slightly (~5 lines saved)
- Keep the singularity classification table (it's excellent)
- Keep "What IVNA Does Not Do for Physics" (essential honesty)
- Renumber to Section 7

---

### 9. Applications: Computer Science (KEEP)

**Current:** Lines 892-979 (~87 lines)

**Changes:**
- Renumber to Section 8
- No content changes

---

### 10. Literature Positioning (UPDATED)

**Current:** Lines 983-1134 (~151 lines)

**Changes:**
- **REMOVE** blow-up correspondence theorem and proof (lines 1024-1071, ~47 lines) — moved to Section 6.5
- **ADD** brief paragraph noting the blow-up result now lives in Section 6.5
- **ADD** citations: Jacobs (2021), Vernaeve (2025), Todorov (1990), Albeverio et al. (1986), Yamashita (2002), Connes & Kreimer (1999-2001), Meyenburg (2025), Anderson & Bergstra (2021)
- **UPDATE** "Genuine Novelty" subsection to reflect SEARCH results: 2 fully novel claims (blow-up, cross-domain table), 4 partially anticipated
- **RENAME** Section 9.2 from "The Isomorphism Question" to **"Is IVNA 'Just Notation'?"** — more conversational, sets up the a+bi answer
- Renumber to Section 9

**Net:** Remove ~47 lines (blow-up), add ~25 lines (new citations, updated novelty). Save ~22 lines.

**Draft for updated Genuine Novelty subsection:**

```latex
\subsection{Genuine Novelty}

The indexed product rule $\vz{x} \cdot \vi{y} = xy$ has no exact
precedent in the reviewed literature. A systematic search of arXiv,
Semantic Scholar, Google Scholar, and the general web (approximately
125 targeted queries across six claim streams) confirmed this. The
terms ``indexed zeros'' and ``indexed infinities'' together return
zero results in the academic literature.

Of the new results presented in this paper, two appear to be fully
novel: the IVNA--Blow-Up Correspondence (Theorem~\ref{thm:blowup})
and the cross-domain structural observation (Section~\ref{sec:crossdomain}).
No prior division-by-zero framework has connected to blow-up theory,
and no prior work has identified the same algebraic operation
recurring across nine domains.

Four results are partially anticipated by prior work but with
meaningful IVNA-specific differentiation:
the probability/Bayes connection (cf.\ Jacobs~\cite{jacobs2021}),
the Dirac delta treatment (cf.\ Todorov~\cite{todorov1990},
Vernaeve~\cite{vernaeve2025}),
the infinity subtraction / renormalization connection
(cf.\ Albeverio et al.~\cite{albeverio1986}),
and the $K^* \times \mathbb{Z}$ algebraic characterization
(cf.\ Santangelo~\cite{santangelo2016}).
In each case, IVNA's contribution is the directness and algebraic
operability of the result, not the underlying mathematical fact.
```

---

### 11. Limitations and Scope (UPDATED)

**Current:** Lines 1138-1176 (~38 lines)

**Changes:**
- **ADD** harmonic series limitation from explore deep dive:

```latex
\item \textbf{Sub-first-order infinities.} IVNA's indexed infinities
  $\vi{x} = x/\varepsilon_0$ are first-order (linear in
  $1/\varepsilon_0$). The harmonic series $H_n \sim \ln n + \gamma$
  diverges to an infinity of \emph{lower} order than any $\vi{x}$:
  $\ln(1/\varepsilon_0)$ grows slower than $x/\varepsilon_0$ for any
  $x > 0$. IVNA's current notation does not parameterize logarithmic
  or sub-logarithmic infinities. This precisely delineates the scope
  of the indexed notation---it covers the most common singularities
  (poles, essential singularities, distributional objects) but not
  all infinite quantities.
```

- **ADD** honest assessment of cross-domain restatements:

```latex
\item \textbf{Restatements vs.\ new results.} Several results in
  Section~\ref{sec:crossdomain} are IVNA restatements of facts
  known from standard analysis or NSA. The Dirac delta properties
  follow from NSA (Robinson, 1966); the conditional density
  formula is Bayes' theorem in different clothing. What IVNA adds
  in each case is directness and algebraic operability, not the
  underlying mathematical fact. We state this explicitly because
  honest positioning is more valuable than overclaiming.
```

- **RENAME** subsection from "The Isomorphism Question" to "Is IVNA 'Just Notation'?"
- Renumber to Section 10

---

### 12. NEW: Research Methodology (Section 11, ~30 lines)

```latex
\section{Research Methodology}
\label{sec:methodology}

The development of IVNA employed a structured AI-assisted research
methodology that may be of independent interest.

\textbf{Generate--Verify--Revise (GVR) loop.} Every mathematical
claim was first generated from theoretical reasoning, then verified
by at least two independent computational tools (drawn from Python,
SymPy, Z3, Lean~4, and Wolfram Mathematica), and revised if
verification failed. This protocol, inspired by the Aletheia
architecture~\cite{feng2026aletheia}, enforces falsifiability at the
point of creation rather than after publication.

\textbf{Adversarial debate.} Key thesis claims were stress-tested
via structured adversarial analysis: independent AI agents assigned
PRO and CON positions argued from the paper's source text, with a
neutral agent synthesizing. This identified that the cross-domain
observation in Section~\ref{sec:crossdomain}, while verified, should
be framed as a structural remark rather than a unification claim---a
distinction that significantly improved the paper's intellectual
honesty.

\textbf{Multi-tool cross-verification.} High-priority claims (the
Bayes/A8 identification, the Borel--Kolmogorov dissolution, the
Dirac delta properties) were verified with three independent tool
chains rather than two. Tool disagreement triggers investigation,
not averaging.

The complete methodology, including all agent transcripts, debate
records, and verification logs, is available in the supplementary
repository. A detailed case study of the AI-assisted research
process is in preparation as a companion document.
```

**Risk:** LOW-MEDIUM. Unusual for a math paper but appropriate for a math/CS hybrid. The methodology is genuinely novel and reproducible. Citing Aletheia grounds it in existing literature.

---

### 13. Conclusion (REVISED)

**Current:** Lines 1180-1231 (~51 lines)

**Changes:**
- **UPDATE** Summary to mention cross-domain observation and new verification total
- **UPDATE** Future Work to add: measure-theoretic formalization of probability claims, sub-first-order infinity notation, functoriality investigation
- **KEEP** The Vision subsection verbatim — "Before Bombelli, √-1 was impossible. After Gauss, it was i." This is the paper's best passage.
- Renumber to Section 12

**Draft updated Summary:**

```latex
\subsection{Summary}

Indexed Virtual Number Algebra is a consistent, computationally verified,
and formally proven algebraic framework for zeros and infinities. Its
central rule---$\vz{x} \cdot \vi{y} = xy$---resolves indeterminate forms
by preserving index information through operations. Consistency is proven
via NSA embedding, with [TOTAL] automated checks across five independent
tool chains and Lean~4 formalization, with zero failures.

The same product rule that defines IVNA's core algebra recurs as the
resolution mechanism in at least nine mathematical domains, from
derivatives to the Dirac delta to conditional densities. This
structural observation---verified but not yet fully
explained---suggests that the indexed product rule captures something
fundamental about how mathematics resolves singularities.

IVNA is not new foundational mathematics. It is a structured interface to
Non-Standard Analysis, analogous to $a + bi$ for $\R^2$. Its value is in
making existing mathematics more accessible and computable at the boundary
between zero and infinity.
```

**Draft additional Future Work items:**

```latex
\item \textbf{Measure-theoretic formalization}: rigorously establish
  the connection between IVNA's indexed zero probabilities and the
  Radon--Nikodym derivative, and determine whether the
  Borel--Kolmogorov dissolution (Section~\ref{subsec:bayes}) holds
  under weaker regularity conditions than joint density existence.
\item \textbf{Sub-first-order infinities}: extend the indexed
  notation to parameterize logarithmic and iterated-logarithmic
  infinities, which arise in the harmonic series
  (Section~\ref{sec:limitations}) and asymptotic analysis.
\item \textbf{Functorial structure}: investigate whether the
  cross-domain pattern of Section~\ref{sec:crossdomain} admits
  a categorical formalization---specifically, whether the index
  map defines a functor between suitable categories of singular
  expressions and $K^* \times \mathbb{Z}$.
```

---

### 14. Bibliography (UPDATED)

**Add these citations:**

```latex
\bibitem{jacobs2021}
B.~Jacobs, ``Multinomial and hypergeometric distributions in Markov
categories,'' \emph{Proceedings of POPL 2021}, arXiv:2101.03391.

\bibitem{todorov1990}
T.~D.~Todorov, ``An existence result for a class of partial differential
equations with smooth coefficients,'' \emph{Proceedings of the AMS},
vol.~109, no.~1, pp.~1--10, 1990.

\bibitem{vernaeve2025}
H.~Vernaeve, ``Nonstandard analysis and the theory of distributions,''
arXiv:2510.16484, 2025.

\bibitem{albeverio1986}
S.~Albeverio, J.~E.~Fenstad, R.~H\o egh-Krohn, and T.~Lindstr\o m,
\emph{Nonstandard Methods in Stochastic Analysis and Mathematical Physics},
Academic Press, 1986.

\bibitem{yamashita2002}
H.~Yamashita, ``Nonstandard analysis and renormalization,''
\emph{Journal of Mathematical Physics}, vol.~43, 2002.

\bibitem{connes1999}
A.~Connes and D.~Kreimer, ``Renormalization in quantum field theory and
the Riemann--Hilbert problem,'' \emph{JHEP}, 1999.

\bibitem{meyenburg2025}
J.~Meyenburg, ``On indexed zeros and infinities,''
\emph{International Journal of Mathematics Trends and Technology},
vol.~71, 2025.

\bibitem{anderson2021}
J.~A.~D.~W.~Anderson and J.~A.~Bergstra, ``Defining extension type
instances of division-related operations,'' 2021.
```

**Note:** Fereydoni (2025), Valamontes (2026), and Bloom (2025) citations are pending full-text review. Add if/when obtained. The paper MUST NOT go to arXiv without assessing these three.

---

### 15. Appendix A: Verification Details (UPDATED)

**Current:** Lines 1357-end (~59 lines)

**Changes:**
- **UPDATE** verification table with new phase 4 rows:

```latex
Phase 4 cross-verif.  & SymPy + Wolfram + Z3      & 155 & 155/155 pass \\
Phase 4 exploration   & SymPy + Wolfram            & 63  & 63/63 pass \\
```

- **UPDATE** total row to new grand total
- **ADD** brief paragraph on multi-tool methodology: "High-priority claims were tested with ≥3 independent tools. Tool disagreement triggers investigation, not averaging."
- **ADD** verification count reconciliation note

---

## Risk Assessment

| Change | Risk | Mitigation |
|--------|------|------------|
| Epigraph (Mean Girls) | LOW | Common in math papers; culturally recognizable |
| "Bigger nothing" remark | LOW | Mathematically correct via NSA embedding |
| "Undefined" footnote | LOW | Pedagogically valuable |
| Cross-domain table | MEDIUM | Verified (155 checks); framed as "observation" not "unification" |
| Bayes/A8 section | MEDIUM-HIGH | Cite Jacobs (2021); frame as "directness" contribution; 6 checks |
| Dirac delta section | MEDIUM | Cite Todorov, Vernaeve; frame as "single axiom" simplification; 28 checks |
| Removable singularities | LOW | Clean restatement; 24 checks |
| Blow-up promotion | LOW | Already in paper; just moving to more prominent position |
| Methodology section | LOW-MEDIUM | Unusual for math but appropriate for math/CS hybrid |
| Harmonic limitation | LOW | Honest assessment; strengthens paper's credibility |
| "Is IVNA 'Just Notation'?" title | LOW | More conversational; same content |
| Updated novelty assessment | LOW | Backed by systematic search (~125 queries) |

**Highest risk:** The Bayes/A8 section. If Jacobs (2021) or another prior work already makes this exact claim, the section needs to pivot from "IVNA discovers this" to "IVNA simplifies this." The SEARCH session found Jacobs but assessed IVNA as adding meaningful differentiation.

**Three blocking risks (external):**
1. Fereydoni (2025) — if stratified infinities have a product rule, IVNA's novelty claim narrows significantly
2. Valamontes (2026) — if typed infinities include the same algebra, same issue
3. Bloom (2025) — if IndeterminateReals uses the complex-number analogy with full axioms, same issue

These are searched in parallel. The paper should NOT go to arXiv until they are assessed.

---

## Deliverables Checklist

- [x] Section-by-section edit plan with line numbers
- [x] Draft LaTeX for all new content
- [x] Cross-domain unification table as LaTeX (Section 6.1)
- [x] Bayes/probability section as LaTeX (Section 6.2)
- [x] Risk assessment for each change
- [ ] Abstract rewrite (draft above, needs final verification count)
- [ ] Verification count reconciliation (489 existing + 155 phase4 + 63 explore = ~707, needs exact count)
- [ ] Three risky papers assessed (background search running)

---

## Approval Gate

**Wisdom:** Please review this edit plan. Once approved, I will apply all edits to `ivna-paper.tex` in a single pass, then compile with `tectonic` to verify.

Changes can be applied incrementally (section by section) or all at once. I recommend all at once with a git commit before starting, so we can easily diff or revert.
