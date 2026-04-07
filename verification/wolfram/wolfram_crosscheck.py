"""
IVNA Verification — Wolfram Cross-Verification
================================================

Independent cross-verification of IVNA claims using Wolfram Engine.
Each check runs wolframscript and parses the result.

Requires: wolframscript installed and configured.
"""

import subprocess
import sys
import os
import re

passed = 0
failed = 0
results = []

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        results.append(("PASS", name))
    else:
        failed += 1
        results.append(("FAIL", name + (f" [{detail}]" if detail else "")))

def wolfram(code, timeout=30):
    """Run Mathematica code via wolframscript, return output string."""
    try:
        r = subprocess.run(
            ["wolframscript", "-code", code],
            capture_output=True, text=True, timeout=timeout
        )
        return r.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return f"ERROR: {e}"

def wolfram_bool(code, timeout=30):
    """Run Mathematica code expected to return True/False."""
    result = wolfram(code, timeout)
    return result == "True"

def wolfram_numeric(code, timeout=30):
    """Run Mathematica code expected to return a number."""
    result = wolfram(code, timeout)
    try:
        return float(result)
    except ValueError:
        return None


# ============================================================
# CHECK 0: Wolfram is working
# ============================================================

check("Wolfram: engine responds", wolfram("1+1") == "2")


# ============================================================
# SECTION 1: CORE AXIOM VERIFICATION (NSA Embedding)
# ============================================================

# A3: (x*eps)*(y/eps) = x*y
check("Wolfram-A3: (x*eps)*(y/eps) simplifies to x*y",
      wolfram_bool("Simplify[x*eps*(y/eps) == x*y]"))

# A1: (x*eps)*(y*eps) = x*y*eps^2
check("Wolfram-A1: (x*eps)*(y*eps) = x*y*eps^2",
      wolfram_bool("Simplify[x*eps*(y*eps) == x*y*eps^2]"))

# A2: (x/eps)*(y/eps) = x*y/eps^2
check("Wolfram-A2: (x/eps)*(y/eps) = x*y/eps^2",
      wolfram_bool("Simplify[(x/eps)*(y/eps) == x*y/eps^2]"))

# A8: (x*eps)/(y*eps) = x/y (index cancellation)
check("Wolfram-A8: (x*eps)/(y*eps) = x/y",
      wolfram_bool("Simplify[(x*eps)/(y*eps) == x/y]"))

# A9: (x/eps)/(y/eps) = x/y
check("Wolfram-A9: (x/eps)/(y/eps) = x/y",
      wolfram_bool("Simplify[(x/eps)/(y/eps) == x/y]"))

# A10: x*eps + y*eps = (x+y)*eps
check("Wolfram-A10: x*eps + y*eps = (x+y)*eps",
      wolfram_bool("Simplify[x*eps + y*eps == (x+y)*eps]"))

# A4: n*(x*eps) = (n*x)*eps
check("Wolfram-A4: n*(x*eps) = (n*x)*eps",
      wolfram_bool("Simplify[n*(x*eps) == (n*x)*eps]"))

# A5: n*(x/eps) = (n*x)/eps
check("Wolfram-A5: n*(x/eps) = (n*x)/eps",
      wolfram_bool("Simplify[n*(x/eps) == (n*x)/eps]"))

# A6: y/(x*eps) = (y/x)/eps
check("Wolfram-A6: y/(x*eps) = (y/x)/eps",
      wolfram_bool("Simplify[y/(x*eps) == (y/x)/eps]"))

# A7: y/(x/eps) = (y/x)*eps
check("Wolfram-A7: y/(x/eps) = (y/x)*eps",
      wolfram_bool("Simplify[y/(x/eps) == (y/x)*eps]"))

# D-INDEX-ZERO: x*eps - x*eps = 0
check("Wolfram-DIZ: x*eps - x*eps = 0",
      wolfram_bool("Simplify[x*eps - x*eps == 0]"))


# ============================================================
# SECTION 2: ROUNDTRIP VERIFICATION
# ============================================================

# Division-by-zero roundtrip: (y/(x*eps))*(x*eps) = y
check("Wolfram-Roundtrip: (y/(x*eps))*(x*eps) = y",
      wolfram_bool("Simplify[(y/(x*eps))*(x*eps) == y]"))

# Double reciprocal: 1/(1/(x*eps)) = x*eps
check("Wolfram-DoubleRecip: 1/(1/(x*eps)) = x*eps",
      wolfram_bool("Simplify[1/(1/(x*eps)) == x*eps]"))

# Numeric roundtrips
for y_val, x_val in [(5, 1), (7, 3), (42, 2)]:
    result = wolfram_numeric(f"({y_val}/(x*eps))*(x*eps) /. x -> {x_val} /. eps -> 1/1000000")
    check(f"Wolfram-Roundtrip-Numeric: ({y_val}/0_{x_val})*0_{x_val} = {y_val}",
          result is not None and abs(result - y_val) < 1e-6,
          f"got {result}")


# ============================================================
# SECTION 3: A-EXP (EXPONENTIAL AXIOM)
# ============================================================

# Leading term of (y/eps)*Log[1 + x*eps] is x*y
check("Wolfram-AEXP: leading term of (y/eps)*Log[1+x*eps] is x*y",
      wolfram_bool("Limit[(y/eps)*Log[1 + x*eps], eps -> 0] == x*y"))

# e = Limit[(1 + 1/n)^n, n -> Infinity]
check("Wolfram-AEXP: (1+1/n)^n -> e",
      wolfram_bool("Limit[(1 + 1/n)^n, n -> Infinity] == E"))

# Scaling: substituting n=3 into (1+x/N)^N -> e^x where N=3m, so x->3x
check("Wolfram-AEXP-scaling: (1+3x/N)^N -> e^(3x)",
      wolfram_bool("Limit[(1 + 3*x/N)^N, N -> Infinity] == E^(3*x)"))


# ============================================================
# SECTION 4: DERIVATIVE VERIFICATION
# ============================================================

# d/dx(x^2) = 2x via limit definition
check("Wolfram-Deriv: d/dx(x^2) = 2x",
      wolfram_bool("D[x^2, x] == 2*x"))

# d/dx(sin x) = cos x
check("Wolfram-Deriv: d/dx(sin x) = cos x",
      wolfram_bool("D[Sin[x], x] == Cos[x]"))

# d/dx(e^x) = e^x
check("Wolfram-Deriv: d/dx(e^x) = e^x",
      wolfram_bool("D[Exp[x], x] == Exp[x]"))

# d/dx(ln x) = 1/x
check("Wolfram-Deriv: d/dx(ln x) = 1/x",
      wolfram_bool("D[Log[x], x] == 1/x"))

# d/dx(1/x) = -1/x^2
check("Wolfram-Deriv: d/dx(1/x) = -1/x^2",
      wolfram_bool("D[1/x, x] == -1/x^2"))

# IVNA-specific: (f(x+h) - f(x))/h for f=x^2, leading term = 2x
check("Wolfram-IVNA-Deriv: ((x+h)^2 - x^2)/h leading term = 2x",
      wolfram_bool("Limit[((x+h)^2 - x^2)/h, h -> 0] == 2*x"))


# ============================================================
# SECTION 5: HIGHER-ORDER EMBEDDING
# ============================================================

# (x*eps^2)*(y/eps^2) = x*y (order-2 cancel)
check("Wolfram-HiOrder: (x*eps^2)*(y/eps^2) = x*y",
      wolfram_bool("Simplify[x*eps^2*(y/eps^2) == x*y]"))

# (x*eps^3)*(y/eps^2) = x*y*eps (one zero remains)
check("Wolfram-HiOrder: (x*eps^3)*(y/eps^2) = x*y*eps",
      wolfram_bool("Simplify[x*eps^3*(y/eps^2) == x*y*eps]"))

# (x*eps^3)*(y/eps) = x*y*eps^2 (two zeros remain)
check("Wolfram-HiOrder: (x*eps^3)*(y/eps) = x*y*eps^2",
      wolfram_bool("Simplify[x*eps^3*(y/eps) == x*y*eps^2]"))

# Integration: eps^(k+1) * (1/eps)^(k+1) = 1 for k=0..4
for k in range(5):
    check(f"Wolfram-Integration: eps^{k+1} * (1/eps)^{k+1} = 1",
          wolfram_bool(f"Simplify[eps^{k+1} * (1/eps)^{k+1} == 1]"))


# ============================================================
# SECTION 6: CLASSICAL CORRESPONDENCE (Wolfram-independent check)
# ============================================================

# sin(x)/x -> 1
check("Wolfram-Classical: Limit[Sin[x]/x, x->0] = 1",
      wolfram_bool("Limit[Sin[x]/x, x -> 0] == 1"))

# (e^x - 1)/x -> 1
check("Wolfram-Classical: Limit[(E^x-1)/x, x->0] = 1",
      wolfram_bool("Limit[(Exp[x]-1)/x, x -> 0] == 1"))

# (1-Cos[x])/x^2 -> 1/2
check("Wolfram-Classical: Limit[(1-Cos[x])/x^2, x->0] = 1/2",
      wolfram_bool("Limit[(1-Cos[x])/x^2, x -> 0] == 1/2"))

# eps*Log[eps] -> 0
check("Wolfram-Classical: Limit[eps*Log[eps], eps->0+] = 0",
      wolfram_bool("Limit[eps*Log[eps], eps -> 0, Direction -> \"FromAbove\"] == 0"))

# Residue of 1/z at z=0 is 1
check("Wolfram-Classical: Residue[1/z, {z,0}] = 1",
      wolfram_bool("Residue[1/z, {z, 0}] == 1"))

# Residue of 1/(z-1) at z=1 is 1
check("Wolfram-Classical: Residue[1/(z-1), {z,1}] = 1",
      wolfram_bool("Residue[1/(z-1), {z, 1}] == 1"))

# Integral of DiracDelta = 1
check("Wolfram-Classical: Integrate[DiracDelta[x], {x,-Inf,Inf}] = 1",
      wolfram_bool("Integrate[DiracDelta[x], {x, -Infinity, Infinity}] == 1"))

# Sifting: Integrate[f(x)*DiracDelta[x-a]] = f(a)
check("Wolfram-Classical: DiracDelta sifting property",
      wolfram_bool("Integrate[x^2 * DiracDelta[x - 3], {x, -Infinity, Infinity}] == 9"))


# ============================================================
# REPORT
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("IVNA VERIFICATION — WOLFRAM CROSS-VERIFICATION")
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
        print("  ALL WOLFRAM CHECKS PASSED")
    else:
        print(f"  {failed} CHECKS FAILED")

    sys.exit(0 if failed == 0 else 1)
