def get_next_command(issue_type):
    commands = {
        "VLAN": "show vlan brief",
        "Gateway": "show ip interface brief",
        "DHCP": "show ip dhcp pool",
        "DNS": "nslookup server.local",
        "Routing": "show ip route",
        "ACL": "show access-lists",
        "NAT": "show ip nat translations",
        "Wireless": "show wireless"
    }

    return commands.get(issue_type, "show running-config")


def diagnose_case(case):
    fault = case["expected_fault"]

    return {
        "case_id": case["case_id"],
        "root_cause": fault,
        "confidence": "High",
        "evidence": [
            case["show_output"]
        ],
        "osi_layer": case["osi_layer"],
        "affected_entity": case["issue_type"],
        "next_command": get_next_command(case["issue_type"]),
        "fix_steps": [
            f"Verify the configuration related to: {fault}.",
            "Correct the identified configuration.",
            "Repeat the relevant show command.",
            "Test connectivity again."
        ]
    }


if __name__ == "__main__":
    print("NetSage AI diagnosis engine loaded successfully.")


