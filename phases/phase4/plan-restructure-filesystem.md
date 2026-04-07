# IVNA Filesystem Restructure Plan

## Principles (from Noble 2009, Cookiecutter Data Science, general best practices)

1. **Logical at the top, chronological at the leaves.** Top-level dirs organize by PURPOSE (paper, code, proofs, research). Within research, entries are dated because logical names go stale as a project evolves.
2. **Separate source from output.** Code that generates results lives apart from the results themselves. Verification scripts separate from verification logs.
3. **Progressive disclosure.** A new reader should understand the project from the root README alone. Deeper directories serve deeper engagement.
4. **No orphan files at root.** Every file at root level should be project-level (README, LICENSE, CLAUDE.md). Everything else belongs in a directory.
5. **Naming convention: lowercase-kebab for dirs, descriptive for files.** No spaces, no CamelCase for directories.
6. **Archive, don't delete.** Old phases live under `archive/` rather than being scattered or removed.

## Current Problems

| Problem | Example | Fix |
|---------|---------|-----|
| `research/findings/` is a flat dumping ground | 28 files mixing findings, verification logs, demo outputs | Split by type |
| Verification .txt files mixed with findings .md | `verification-mcp-sympy.txt` next to `e-exploration.md` | Move to `verification/` |
| Demo outputs mixed with research | `output-demo-gradient.txt` | Move to `code/demos/output/` |
| Phase plans scattered | `research/plans/phase1/`, `phase4/` at root | Consistent location |
| Agent raw outputs are opaque | `research/agent-outputs/01-literature-positioning.txt` | Keep but link from findings |
| `vex-web/` at root (single file demo) | `vex-web/index.html` | Move under `code/` |
| `TIMELINE.md` at root (not updated) | Stale artifact | Move to `archive/` or update |

## Proposed Structure

```
IVNA/
├── README.md                    # Project overview, quick start, links to paper
├── LICENSE                      # MIT
├── CLAUDE.md                    # Claude Code context (stays at root per convention)
├── .gitignore
│
├── paper/                       # THE DELIVERABLE
│   ├── ivna-paper.tex           # LaTeX source
│   ├── ivna-paper.pdf           # Compiled PDF
│   └── figures/                 # (future — when paper gets figures)
│
├── lean/                        # FORMAL PROOFS (renamed from lean-ivna for brevity)
│   ├── LeanIvna/
│   │   ├── Basic.lean
│   │   ├── Axioms.lean
│   │   ├── Model.lean
│   │   └── Theorems.lean
│   ├── lakefile.lean
│   ├── lean-toolchain
│   ├── lake-manifest.json
│   ├── LeanIvna.lean
│   ├── build.sh
│   └── README.md
│
├── code/                        # IMPLEMENTATION & VERIFICATION CODE
│   ├── ivna.py                  # Core IVNA implementation
│   ├── vex-calculator.py        # VEA calculator / demo
│   ├── vex-web/                 # Web calculator demo (moved from root)
│   │   └── index.html
│   ├── demos/                   # Demo scripts
│   │   ├── gradient.py
│   │   ├── ieee754.py
│   │   ├── nbody.py
│   │   └── ode-singular.py
│   └── verify/                  # Verification scripts
│       ├── verify-calculus.py
│       ├── verify-comprehensive.py
│       ├── verify-derivatives-ftc.py
│       ├── verify-sympy-comprehensive.py
│       ├── verify-odes.py
│       ├── verify-nsa-embedding.py
│       └── verify-z3-comprehensive.py
│
├── research/                    # RESEARCH PROCESS & FINDINGS
│   ├── README.md                # Index of all findings and their status
│   ├── findings/                # Research findings (markdown only)
│   │   ├── algebraic-characterization.md
│   │   ├── blow-up-comparison.md
│   │   ├── deep-dive-unification.md
│   │   ├── e-exploration.md
│   │   ├── recursive-indexing-closure.md
│   │   ├── residue-theorem-feasibility.md
│   │   ├── ... (other .md findings)
│   │   └── abandoned/          # Findings that led nowhere (educational)
│   │       ├── bezout-feasibility.md
│   │       └── ode-confluence-feasibility.md
│   ├── verification/            # Verification logs and outputs (txt + subdirs)
│   │   ├── README.md            # Summary table of all verification runs
│   │   ├── phase2-mcp-sympy.txt
│   │   ├── phase2-mcp-z3.txt
│   │   ├── phase2-mcp-wolfram.txt
│   │   ├── phase2-mcp-literature.txt
│   │   ├── phase3-calculus.txt
│   │   ├── comprehensive.txt
│   │   ├── nsa-embedding.txt
│   │   ├── critical-claims.txt
│   │   ├── section5-final.txt
│   │   ├── odes.txt
│   │   ├── ivna-tests.txt
│   │   ├── deep-dive-unification/   # Phase 4 verification
│   │   │   ├── README.md
│   │   │   ├── 01-dirac-delta-normalization.md
│   │   │   ├── 02-removable-singularities.md
│   │   │   └── ...
│   │   └── phase4/             # New phase 4 verifications go here
│   ├── agent-outputs/           # Raw agent outputs (keep for traceability)
│   │   ├── README.md            # Maps each file to its agent/stream
│   │   └── ... (existing .txt files)
│   └── writing/                 # Writing aids (style guide, books research)
│       ├── style-guide.md
│       ├── books-writing-research-papers.md
│       └── case-study-ai-assisted-research.md
│
├── phases/                      # PHASE PLANS (all phases, one place)
│   ├── phase1/                  # Validation & core algebra
│   │   └── ... (existing plan files)
│   ├── phase2/                  # Paper drafting
│   │   └── ...
│   ├── phase3/                  # Framework to contribution
│   │   └── ...
│   └── phase4/                  # Unification thesis pivot (CURRENT)
│       ├── plan.md              # Master plan
│       ├── plan-session-verify.md
│       ├── plan-session-search.md
│       ├── plan-session-explore.md
│       ├── plan-session-restructure.md
│       └── plan-session-debate.md
│
├── debates/                     # ADVERSARIAL ANALYSIS (keep as-is, well-organized)
│   ├── 2026-03-31-mathematical-contribution/
│   ├── 2026-04-01-ivna-paper-merit/
│   └── 2026-04-01-unification-thesis/
│
├── distribution/                # OUTREACH & PUBLICATION (keep as-is)
│   ├── distribution-strategy.md
│   └── outreach/
│       └── ...
│
├── sessions/                    # SESSION LOGS (keep as-is)
│   └── ...
│
└── archive/                     # HISTORICAL / SUPERSEDED
    ├── TIMELINE.md              # Original timeline (superseded by phases/)
    ├── original-paper.pdf       # Original pre-IVNA paper
    ├── verification-log.md      # Old verification log (superseded by research/verification/)
    └── session-carryover-2026-03-31.md
```

## Migration Steps

All moves use `git mv` to preserve history.

### Step 1: Create new directories
```bash
mkdir -p code/demos code/verify research/verification research/writing research/findings/abandoned phases archive
```

### Step 2: Move code files
```bash
git mv code/demo-gradient.py code/demos/gradient.py
git mv code/demo-ieee754.py code/demos/ieee754.py
git mv code/demo-nbody.py code/demos/nbody.py
git mv code/demo-ode-singular.py code/demos/ode-singular.py
git mv code/verify-calculus.py code/verify/
git mv code/verify-comprehensive.py code/verify/
git mv code/verify-ivna-derivatives-ftc.py code/verify/verify-derivatives-ftc.py
git mv code/verify-ivna-sympy-comprehensive.py code/verify/verify-sympy-comprehensive.py
git mv code/verify-odes.py code/verify/
git mv code/verify_nsa_embedding.py code/verify/verify-nsa-embedding.py
git mv code/verify_z3_comprehensive.py code/verify/verify-z3-comprehensive.py
git mv vex-web code/vex-web
```

### Step 3: Move verification outputs out of findings
```bash
git mv research/findings/verification-*.txt research/verification/
git mv research/findings/verify-odes-output.txt research/verification/odes.txt
git mv research/findings/output-demo-*.txt code/demos/   # demo outputs with demos
git mv research/findings/deep-dive-unification-verification research/verification/deep-dive-unification
```

### Step 4: Move abandoned findings
```bash
git mv research/findings/bezout-feasibility.md research/findings/abandoned/
git mv research/findings/ode-confluence-feasibility.md research/findings/abandoned/
```

### Step 5: Move writing aids
```bash
git mv research/findings/writing-style-guide.md research/writing/style-guide.md
git mv research/findings/books-writing-research-papers.md research/writing/
git mv research/case-study-ai-assisted-research.md research/writing/
```

### Step 6: Consolidate phases
```bash
git mv research/plans/phase1 phases/phase1
git mv research/plans/phase2 phases/phase2
git mv research/plans/phase3 phases/phase3
git mv phase4 phases/phase4
git mv research/plans/next-steps.md phases/
rmdir research/plans  # should be empty now
```

### Step 7: Archive stale files
```bash
git mv TIMELINE.md archive/
git mv research/Indexed_Virtual_Number_Algebra.pdf archive/original-paper.pdf
git mv research/verification-log.md archive/
git mv research/session-carryover-2026-03-31.md archive/
```

### Step 8: Rename lean-ivna for brevity (optional — impacts lakefile)
Skip this for now — Lean tooling depends on the directory name. Flag for later.

### Step 9: Update CLAUDE.md
Update the project structure section to reflect the new layout.

### Step 10: Commit
```bash
git add -A
git commit -m "Reorganize project structure: separate verification from findings, consolidate phases, archive stale files"
```

## What NOT to Move
- `lean-ivna/` — Lean tooling depends on directory name
- `debates/` — already well-organized
- `distribution/` — already well-organized
- `sessions/` — already well-organized
- `.claude/` — system directory

## Impact on Other Sessions
The 3 parallel sessions (VERIFY, SEARCH, EXPLORE) reference file paths in their briefs. If you do this restructure BEFORE starting those sessions, update the brief files. If those sessions are already running, do the restructure AFTER they complete and update paths in their output.

## Future Rule Candidate
This restructure follows principles that could become a general rule:
- Logical at top, chronological at leaves
- Separate source from output
- `findings/` for conclusions, `verification/` for evidence, `agent-outputs/` for raw data
- `phases/` for temporal plans, `archive/` for superseded work
- `abandoned/` for dead ends (they're educational, don't delete)
