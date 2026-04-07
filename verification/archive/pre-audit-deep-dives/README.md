# Pre-Audit Verification Archive

**Archived:** 2026-04-06

These deep-dive verification directories were archived after a meta-verification audit found they test classical mathematics, not IVNA's axiom system.

## What's Here

- `deep-dive-unification/` — 5 Wolfram Mathematica files verifying classical facts (Dirac delta normalization, removable singularities, delta scaling, conditional probability, KL divergence). IVNA notation applied as post-hoc commentary.
- `deep-dive-category/` — 6 SymPy files using `eps = Symbol('epsilon')` as a standin for virtual numbers. Two files contain tautological tests (`a*b - a*b == 0`). Never imports `ivna.py`.
- `deep-dive-fourier/` — 6 Wolfram files verifying Fourier transform properties. IVNA derivation is pen-and-paper reasoning, not computed.
- `deep-dive-harmonic/` — 5 Python files verifying Euler-Mascheroni, Basel problem, Mertens theorem, etc. Pure number theory with zero IVNA content.

## Why Archived

None of these files import `ivna.py` or use the `Virtual` class. They verify classical mathematical facts and then narrate the results in IVNA notation. While the classical computations are correct, they don't constitute verification of IVNA's axiom system.

The originals remain at `research/verification/deep-dive-*/` for reference.

## See Also

- `research/verification/meta-audit-2026-04-06.md` — Full audit report
- `code/verify/suite/` — The new, honestly-categorized verification suite
