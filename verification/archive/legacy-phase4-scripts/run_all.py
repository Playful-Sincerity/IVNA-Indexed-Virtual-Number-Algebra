#!/usr/bin/env python3
"""Master runner: execute all Phase 4 verification scripts and report results.

Usage:
    python3 run_all.py              # run all, print summary
    python3 run_all.py --save       # also save raw output to results/
"""
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path

SCRIPTS = [
    ("verify_01_bayes.py",                "A8 = Bayes' theorem"),
    ("verify_02_borel_kolmogorov.py",     "Borel-Kolmogorov dissolution"),
    ("verify_03_dirac_delta.py",          "Dirac delta from product rule"),
    ("verify_04_removable_singularities.py", "Removable singularities"),
    ("verify_05_infinity_subtraction.py", "Infinity subtraction"),
    ("verify_06_residue_extraction.py",   "Residue extraction"),
    ("verify_07_compound_growth.py",      "Compound growth / e"),
    ("verify_08_blow_up.py",              "Blow-up correspondence"),
    ("verify_09_kl_divergence.py",        "KL divergence"),
]

def main():
    save = "--save" in sys.argv
    script_dir = Path(__file__).parent
    results_dir = script_dir / "results"

    if save:
        results_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print(f"IVNA Phase 4 Verification Suite — {datetime.now().isoformat()}")
    print("=" * 70)

    verdicts = []

    for script_name, description in SCRIPTS:
        script_path = script_dir / script_name
        print(f"\n{'─' * 70}")
        print(f"Running: {description} ({script_name})")
        print(f"{'─' * 70}")

        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes max per script
            )

            output = result.stdout + result.stderr
            print(output)

            if save:
                output_file = results_dir / f"{script_name}.output.txt"
                with open(output_file, "w") as f:
                    f.write(f"# {description}\n")
                    f.write(f"# Run: {datetime.now().isoformat()}\n")
                    f.write(f"# Exit code: {result.returncode}\n\n")
                    f.write(output)

            passed = result.returncode == 0
            verdicts.append((description, "PASS" if passed else "FAIL"))

        except subprocess.TimeoutExpired:
            verdicts.append((description, "TIMEOUT"))
            print(f"  TIMEOUT after 300s")
        except Exception as e:
            verdicts.append((description, f"ERROR: {e}"))
            print(f"  ERROR: {e}")

    # --- Final Summary ---
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    total_pass = sum(1 for _, v in verdicts if v == "PASS")
    total = len(verdicts)

    for description, verdict in verdicts:
        icon = "✓" if verdict == "PASS" else "✗"
        print(f"  [{icon}] {verdict:8s}  {description}")

    print(f"\n  {total_pass}/{total} scripts passed")
    overall = "ALL PASS" if total_pass == total else "FAILURES DETECTED"
    print(f"  OVERALL: {overall}")

    if save:
        # Write summary file
        summary_file = results_dir / "summary.txt"
        with open(summary_file, "w") as f:
            f.write(f"IVNA Phase 4 Verification — {datetime.now().isoformat()}\n\n")
            for description, verdict in verdicts:
                f.write(f"{verdict:8s}  {description}\n")
            f.write(f"\n{total_pass}/{total} passed. {overall}\n")
        print(f"\n  Results saved to {results_dir}/")

    sys.exit(0 if total_pass == total else 1)

if __name__ == "__main__":
    main()
