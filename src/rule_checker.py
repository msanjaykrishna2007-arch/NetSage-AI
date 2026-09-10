import re


def check_missing_vlan(show_output):
    if "vlan" in show_output.lower() and "missing" in show_output.lower():
        return {
            "rule": "missing_vlan",
            "status": "FAIL",
            "message": "Required VLAN appears to be missing."
        }

    return {
        "rule": "missing_vlan",
        "status": "PASS",
        "message": "No missing VLAN detected."
    }


def check_duplicate_ip(show_output):
    text = show_output.lower()

    if "duplicate" in text:
        return {
            "rule": "duplicate_ip",
            "status": "FAIL",
            "message": "Duplicate IP address detected."
        }

    return {
        "rule": "duplicate_ip",
        "status": "PASS",
        "message": "No duplicate IP detected."
    }


def check_wrong_mask(show_output):
    text = show_output.lower()

    if "255.255.0.0" in text:
        return {
            "rule": "wrong_mask",
            "status": "FAIL",
            "message": "Possible incorrect subnet mask detected."
        }

    if "route exists" in text and "/16" in text:
        return {
            "rule": "wrong_mask",
            "status": "FAIL",
            "message": "Possible incorrect routing mask detected."
        }

    return {
        "rule": "wrong_mask",
        "status": "PASS",
        "message": "No obvious wrong mask detected."
    }


def check_gateway_mismatch(show_output):
    text = show_output.lower()

    if "default gateway" in text:
        match = re.search(
            r"default gateway\s+([0-9.]+)",
            text
        )

        if match:
            gateway = match.group(1)

            if gateway != "192.168.10.1":
                return {
                    "rule": "gateway_mismatch",
                    "status": "FAIL",
                    "message": f"Gateway {gateway} does not match expected gateway 192.168.10.1."
                }

    if "default-router" in text and "192.168.20.254" in text:
        return {
            "rule": "gateway_mismatch",
            "status": "FAIL",
            "message": "DHCP is providing an incorrect default gateway."
        }

    return {
        "rule": "gateway_mismatch",
        "status": "PASS",
        "message": "No gateway mismatch detected."
    }


def check_interface_down(show_output):
    text = show_output.lower()

    if "administratively down" in text:
        return {
            "rule": "interface_down",
            "status": "FAIL",
            "message": "Interface is administratively down."
        }

    if "line protocol down" in text:
        return {
            "rule": "interface_down",
            "status": "FAIL",
            "message": "Interface line protocol is down."
        }

    return {
        "rule": "interface_down",
        "status": "PASS",
        "message": "No interface-down condition detected."
    }


def check_missing_route(show_output):
    text = show_output.lower()

    if "no route" in text:
        return {
            "rule": "missing_route",
            "status": "FAIL",
            "message": "No route to the destination network was found."
        }

    return {
        "rule": "missing_route",
        "status": "PASS",
        "message": "No missing route detected."
    }


def run_all_checks(show_output):
    results = [
        check_missing_vlan(show_output),
        check_duplicate_ip(show_output),
        check_wrong_mask(show_output),
        check_gateway_mismatch(show_output),
        check_interface_down(show_output),
        check_missing_route(show_output)
    ]

    failed = [
        result for result in results
        if result["status"] == "FAIL"
    ]

    return {
        "overall_status": "FAIL" if failed else "PASS",
        "failed_rules": failed,
        "all_rules": results
    }


if __name__ == "__main__":
    sample_output = """
    show ip interface brief:
    G0/0.10 administratively down
    """

    result = run_all_checks(sample_output)

    print("NetSage AI - Deterministic Rule Checker")
    print("=" * 45)
    print("Overall status:", result["overall_status"])
    print()

    for rule in result["all_rules"]:
        print(
            f"{rule['rule']:20} "
            f"{rule['status']:5} "
            f"{rule['message']}"
        )


