-- IVNA: Indexed Virtual Number Algebra
-- Machine-checked formalization in Lean 4
--
-- This project formalizes the core axioms of IVNA and proves:
--   1. Internal consistency (axioms don't contradict each other)
--   2. Key theorems (roundtrip, commutativity, associativity)
--   3. Satisfiability via explicit model construction

import LeanIvna.Basic
import LeanIvna.Axioms
import LeanIvna.Model
import LeanIvna.Theorems
