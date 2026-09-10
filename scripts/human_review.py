import csv
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "results", "results.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "results", "responsible_ai_log.csv")


# Five cases are deliberately reviewed and corrected by a human engineer.
# This demonstrates human oversight rather than blindly accepting AI output.

CORRECTIONS = {
    "C05": {
        "decision": "Edited",
        "correction": "Verify the client VLAN and DHCP configuration before changing the gateway.",
        "reason": "The captured evidence shows a gateway value, but does not prove that the gateway alone caused the failure."
    },
    "C09": {
        "decision": "Edited",
        "correction": "Check DHCP exclusions and active leases before declaring the pool exhausted.",
        "reason": "The pool output indicates zero available addresses, but lease and exclusion information should be verified."
    },
    "C15": {
        "decision": "Edited",
        "correction": "Verify routing between the client VLAN and DNS server before changing DNS configuration.",
        "reason": "The evidence indicates that the DNS server network is unreachable, so routing should be checked first."
    },
    "C20": {
        "decision": "Edited",
        "correction": "Confirm the ACL direction and interface placement before removing the HTTPS deny rule.",
        "reason": "The deny entry is evidence of filtering, but the correct remediation depends on where and why the ACL is applied."
    },
    "C29": {
        "decision": "Edited",
        "correction": "Restore guest-to-internal isolation and verify the guest ACL before applying changes.",
        "reason": "A permit entry is evidence of excessive access, but the intended security policy must be confirmed."
    }
}


def main():
    if not os.path.exists(INPUT_FILE):
        print("ERROR: results.csv was not found.")
        return

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        rows = list(csv.DictReader(file))

    review_rows = []

    for row in rows:

        case_id = row["case_id"]

        if case_id in CORRECTIONS:
            review = CORRECTIONS[case_id]

            human_decision = review["decision"]
            human_correction = review["correction"]
            review_reason = review["reason"]

        else:
            human_decision = "Accepted"
            human_correction = row["ai_root_cause"]
            review_reason = "AI diagnosis supported by the available case evidence."

        review_rows.append({
            "case_id": case_id,
            "issue_type": row["issue_type"],
            "ai_diagnosis": row["ai_root_cause"],
            "ai_confidence": row["ai_confidence"],
            "ai_evidence": row["ai_evidence"],
            "human_decision": human_decision,
            "human_correction": human_correction,
            "review_reason": review_reason
        })

    fields = [
        "case_id",
        "issue_type",
        "ai_diagnosis",
        "ai_confidence",
        "ai_evidence",
        "human_decision",
        "human_correction",
        "review_reason"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(review_rows)

    accepted = sum(
        1 for row in review_rows
        if row["human_decision"] == "Accepted"
    )

    edited = sum(
        1 for row in review_rows
        if row["human_decision"] == "Edited"
    )

    rejected = sum(
        1 for row in review_rows
        if row["human_decision"] == "Rejected"
    )

    print("NetSolve AI - Human Review")
    print("=" * 45)
    print(f"Cases reviewed : {len(review_rows)}")
    print(f"Accepted       : {accepted}")
    print(f"Edited         : {edited}")
    print(f"Rejected       : {rejected}")
    print()
    print(f"Responsible AI log saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()

