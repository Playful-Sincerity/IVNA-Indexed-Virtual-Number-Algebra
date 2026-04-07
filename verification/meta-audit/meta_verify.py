"""
IVNA Meta-Verification — Verifying the Verification Suite
===========================================================

This is the Meta-GVR step: before trusting the verification results,
check that the tests themselves are sound. Catches:
- Tautological assertions (check(name, True))
- Circular tests (output = input)
- Category misuse (Cat A must import ivna, Cat C must not)
- Trivial Z3 checks (x == x)
"""

import sys
import os
import ast
import re

verification_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
passed = 0
failed = 0
results = []

FILE_MAP = {
    "cat_a_ivna_native.py": os.path.join("core-algebra", "cat_a_ivna_native.py"),
    "cat_b_nsa_embedding.py": os.path.join("nsa-embedding", "cat_b_nsa_embedding.py"),
    "cat_c_classical_correspondence.py": os.path.join("classical-correspondence", "cat_c_classical_correspondence.py"),
    "cat_z3_real.py": os.path.join("z3-axioms", "cat_z3_real.py"),
}

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        results.append(("PASS", name))
    else:
        failed += 1
        results.append(("FAIL", name + (f" [{detail}]" if detail else "")))


def read_file(filename):
    rel = FILE_MAP.get(filename, filename)
    path = os.path.join(verification_dir, rel)
    if os.path.exists(path):
        with open(path) as f:
            return f.read()
    return None


# ============================================================
# META-CHECK 1: Category A imports ivna
# ============================================================

cat_a = read_file("cat_a_ivna_native.py")
if cat_a:
    check("Meta: cat_a imports from ivna module",
          "from ivna import" in cat_a or "import ivna" in cat_a)
    check("Meta: cat_a uses Z() constructor",
          "Z(" in cat_a)
    check("Meta: cat_a uses I() constructor",
          "I(" in cat_a)
    check("Meta: cat_a uses Virtual class",
          "Virtual" in cat_a)


# ============================================================
# META-CHECK 2: Category C does NOT import ivna
# ============================================================

cat_c = read_file("cat_c_classical_correspondence.py")
if cat_c:
    check("Meta: cat_c does NOT import ivna (honest about being classical)",
          "from ivna import" not in cat_c and "import ivna" not in cat_c)
    check("Meta: cat_c imports sympy",
          "import sympy" in cat_c or "from sympy" in cat_c)


# ============================================================
# META-CHECK 3: No tautological assertions
# ============================================================

for filename in ["cat_a_ivna_native.py", "cat_b_nsa_embedding.py",
                 "cat_c_classical_correspondence.py", "cat_z3_real.py"]:
    content = read_file(filename)
    if content:
        # Check for check(name, True) — tautological
        tautology_count = len(re.findall(r'check\([^,]+,\s*True\s*[,)]', content))
        check(f"Meta: {filename} has no tautological check(name, True) calls",
              tautology_count == 0,
              f"found {tautology_count} tautological assertions")


# ============================================================
# META-CHECK 4: Z3 has no x == x tautologies
# ============================================================

cat_z3 = read_file("cat_z3_real.py")
if cat_z3:
    # Look for standalone tautologies like "s.add(x * y == x * y)"
    # Must be the ENTIRE constraint, not part of a larger expression like "c * x * y == x * y"
    trivial_patterns = [
        r'\.add\(\s*x\s*\*\s*y\s*==\s*x\s*\*\s*y\s*\)',
        r'\.add\(\s*x\s*==\s*x\s*\)',
    ]
    trivial_count = 0
    for pat in trivial_patterns:
        trivial_count += len(re.findall(pat, cat_z3))
    check("Meta: Z3 file has no trivial tautologies (x*y == x*y)",
          trivial_count == 0,
          f"found {trivial_count} trivial tautologies")


# ============================================================
# META-CHECK 5: ivna_derivative is not a passthrough
# ============================================================

ivna_path = os.path.join(verification_dir, '..', 'code', 'ivna.py')
if os.path.exists(ivna_path):
    with open(ivna_path) as f:
        ivna_content = f.read()

    # Check that ivna_derivative calls virtual_taylor (not just returns input)
    # Find the function body
    in_func = False
    func_body = []
    for line in ivna_content.split('\n'):
        if 'def ivna_derivative' in line:
            in_func = True
            continue
        if in_func:
            if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
                break
            func_body.append(line)

    func_text = '\n'.join(func_body)
    check("Meta: ivna_derivative() calls virtual_taylor()",
          "virtual_taylor" in func_text,
          "function should use A-VT, not be a passthrough")

    check("Meta: ivna_derivative() does division (A8)",
          "/ h" in func_text or "/ Z(" in func_text,
          "function should divide by Z(1) via A8")

    # Ensure it's not just "return f_derivatives_at_x[1]"
    check("Meta: ivna_derivative() is not a passthrough",
          "return f_derivatives_at_x[1]" not in func_text,
          "OLD circular implementation detected!")


# ============================================================
# META-CHECK 6: Each category file exits with proper code
# ============================================================

for filename in ["cat_a_ivna_native.py", "cat_b_nsa_embedding.py",
                 "cat_c_classical_correspondence.py", "cat_z3_real.py"]:
    content = read_file(filename)
    if content:
        check(f"Meta: {filename} uses sys.exit for pass/fail signaling",
              "sys.exit" in content)


# ============================================================
# REPORT
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("IVNA META-VERIFICATION — Checking the Verification Suite")
    print("=" * 70)
    print()

    for status, name in results:
        icon = "PASS" if status == "PASS" else "FAIL"
        print(f"  [{icon}] {name}")

    print()
    print(f"  PASSED: {passed}")
    print(f"  FAILED: {failed}")
    print(f"  TOTAL:  {passed + failed}")
    print()

    if failed == 0:
        print("  META-VERIFICATION PASSED — suite is structurally sound")
    else:
        print(f"  {failed} META-CHECKS FAILED — fix before trusting results")

    sys.exit(0 if failed == 0 else 1)
