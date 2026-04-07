# Paper Update Plan — Post-Audit Revision

## Goal
Update ivna-paper.tex to reflect the 2026-04-06 re-verification audit. Core math unchanged — only verification numbers, derivative framing, methodology section, and the appendix.

## Changes (by location in the paper)

### 1. Author footnote (line 39)
- Change "707 automated checks" → "403 automated checks across six independent tool chains"
- Change "Five independent verification tool chains" → "Six independent verification tool chains—Python, SymPy, Z3, Lean 4, Wolfram, and a meta-verification layer"

### 2. Abstract (lines 72-73)
- NSA embedding verification numbers: "37 symbolic checks via SymPy, 11 satisfiability checks via Z3" → update to reflect new Cat B (70 checks) and Cat Z3 (13 checks)

### 3. Summary of Results — item 1 (line 217)
- "707 checks across SymPy, Z3, and Wolfram" → "403 checks across six tools"

### 4. Core Algebra intro (lines 263-276)
- "28 core tests, 145 comprehensive checks" → "30 core tests" + mention verification/run_all.py as single entry point
- Update the run command to `python3 verification/run_all.py`

### 5. Consistency proof (lines 631-634)
- "five independent tool chains...totaling 707 checks" → "six independent tool chains...totaling 403 checks, honestly categorized (see Appendix)"

### 6. Derivative description (lines 700-735)
- No change to the math (the binomial theorem + A-VT derivation is correct)
- Add a sentence noting the computational verification exercises the full A-VT → A8 pipeline (not just a numerical comparison): "The computational verification constructs the Virtual Taylor expansion, divides the leading term by $\vz{1}$ via Axiom~\ref{ax:zzdiv}, and confirms all residual terms are higher-order virtual zeros that collapse."

### 7. Cross-domain section framing (lines 960-992, 1021-1023, 1051-1052, 1104)
- These are already well-framed ("IVNA's contribution is the directness", "the observation's value is not that the pattern is surprising in retrospect", etc.)
- The paper already says "structural observation" not "unification" — the earlier debate caught this
- Minor: update specific check counts in each verification line to match new suite numbers or remove specific counts (they're in the appendix anyway)

### 8. Methodology section (lines 1476-1517)
- Add a paragraph about meta-verification:
  "A post-completion audit (April 2026) revealed that the original verification suite conflated genuine IVNA-native checks with classical mathematical computations narrated in IVNA notation. Approximately 270 of the original 707 checks tested standard results (e.g., confirming Bayes' theorem via SymPy) rather than exercising IVNA's axiom system. The suite was rebuilt with three explicit categories: Category A (IVNA-native, using the Virtual class), Category B (NSA embedding consistency), and Category C (classical correspondence, honestly labeled). A meta-verification layer was added to check that the tests themselves are structurally sound—catching tautological assertions, circular passthrough functions, and category violations. This meta-GVR step—verifying the verification—is itself a methodological contribution."

### 9. Conclusion (lines 1527-1532)
- "707 automated checks across five independent tool chains" → "403 automated checks across six independent tool chains"

### 10. Appendix: Verification Details (lines 1753-1893)
- Replace the entire verification table with the new honest categorized one
- Update the Python test suite section (28 → 30 tests)
- Update the Z3 section with real axiom encoding + independence finding (D-INDEX-ZERO derivable)
- Add Wolfram cross-verification section (42 checks)
- Add meta-verification section
- Update file paths to new verification/ structure
- Remove references to old scripts/MCP tools that no longer exist in the suite

## What Does NOT Change
- The axioms (Section 2)
- The proofs (consistency, blow-up theorem)
- The cross-domain structural observation (already well-hedged)
- The Lean4 description (unchanged)
- The e definition, calculus derivations, L'Hopital elimination
- Any mathematical content

## Verification After Edit
- Compile with tectonic: `cd paper && tectonic ivna-paper.tex`
- Visual check: ensure no LaTeX errors, table renders correctly
