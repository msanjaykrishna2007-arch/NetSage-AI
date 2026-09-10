import csv
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ai_engine import diagnose_case
from rule_checker import run_all_checks


INPUT_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "cases.csv"
)

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "results"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR, "results.csv"
)


def load_cases():
    with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    cases = load_cases()
    results = []

    for case in cases:

        diagnosis = diagnose_case(case)

        checker = run_all_checks(case["show_output"])

        result = {
            "case_id": case["case_id"],
            "issue_type": case["issue_type"],
            "severity": case["severity"],
            "expected_fault": case["expected_fault"],
            "ai_root_cause": diagnosis["root_cause"],
            "ai_confidence": diagnosis["confidence"],
            "ai_evidence": " | ".join(diagnosis["evidence"]),
            "osi_layer": diagnosis["osi_layer"],
            "affected_entity": diagnosis["affected_entity"],
            "next_command": diagnosis["next_command"],
            "fix_steps": " | ".join(diagnosis["fix_steps"]),
            "rule_status": checker["overall_status"],
            "failed_rules": " | ".join(
                rule["rule"] for rule in checker["failed_rules"]
            ),
            "human_decision": "Accepted"
        }

        results.append(result)

    fieldnames = list(results[0].keys())

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print("NetSolve AI - Case Runner")
    print("=" * 45)
    print(f"Cases processed : {len(results)}")
    print(f"Results saved   : {OUTPUT_FILE}")
    print()

    for result in results:
        print(
            f"{result['case_id']} | "
            f"{result['issue_type']:8} | "
            f"AI: {result['ai_root_cause']} | "
            f"Rules: {result['rule_status']}"
        )


if __name__ == "__main__":
    main()

