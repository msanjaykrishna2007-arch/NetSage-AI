import csv
import json
import os
from collections import Counter


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CASES_FILE = os.path.join(BASE_DIR, "data", "cases.csv")
RESULTS_FILE = os.path.join(BASE_DIR, "results", "results.csv")
REVIEW_FILE = os.path.join(BASE_DIR, "results", "responsible_ai_log.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "results", "evaluation.json")


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    cases = read_csv(CASES_FILE)
    results = read_csv(RESULTS_FILE)
    reviews = read_csv(REVIEW_FILE)

    issue_types = Counter(row["issue_type"] for row in cases)
    severity = Counter(row["severity"] for row in cases)

    rule_results = Counter(row["rule_status"] for row in results)
    human_results = Counter(row["human_decision"] for row in reviews)

    correct_diagnoses = sum(
        1
        for row in results
        if row["ai_root_cause"].strip().lower()
        == row["expected_fault"].strip().lower()
    )

    edited_cases = [
        row["case_id"]
        for row in reviews
        if row["human_decision"] == "Edited"
    ]

    evaluation = {
        "project": "NetSage AI",
        "dataset": {
            "total_cases": len(cases),
            "processed_cases": len(results)
        },
        "ai_evaluation": {
            "diagnoses_matching_expected_fault": correct_diagnoses,
            "diagnosis_match_rate": round(
                correct_diagnoses / len(results) * 100, 2
            ) if results else 0
        },
        "issue_types": dict(issue_types),
        "severity": dict(severity),
        "deterministic_checker": {
            "PASS": rule_results.get("PASS", 0),
            "FAIL": rule_results.get("FAIL", 0)
        },
        "human_review": {
            "Accepted": human_results.get("Accepted", 0),
            "Edited": human_results.get("Edited", 0),
            "Rejected": human_results.get("Rejected", 0),
            "edited_case_ids": edited_cases
        },
        "responsible_ai": {
            "human_oversight_required": True,
            "correction_cases": len(edited_cases),
            "minimum_required_corrections": 5,
            "requirement_satisfied": len(edited_cases) >= 5
        }
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(evaluation, file, indent=2)

    print("NetSage AI - Evaluation")
    print("=" * 45)
    print(f"Total cases       : {len(cases)}")
    print(f"Processed cases   : {len(results)}")
    print(f"Diagnosis matches : {correct_diagnoses}")
    print(
        f"Match rate        : "
        f"{evaluation['ai_evaluation']['diagnosis_match_rate']}%"
    )
    print()
    print("Human review:")
    print(f"  Accepted : {human_results.get('Accepted', 0)}")
    print(f"  Edited   : {human_results.get('Edited', 0)}")
    print(f"  Rejected : {human_results.get('Rejected', 0)}")
    print()
    print(
        "Responsible AI requirement:",
        "SATISFIED"
        if evaluation["responsible_ai"]["requirement_satisfied"]
        else "NOT SATISFIED"
    )
    print()
    print(f"Evaluation saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()


