#!/usr/bin/env python3
import argparse

def checklist(contract_type):
    common = [
        "Parties and scope",
        "Confidentiality",
        "Liability and indemnity",
        "Term and termination",
        "Governing law",
    ]
    if contract_type == "nda":
        return common + ["Definition of confidential info", "Exclusions", "Term length"]
    if contract_type == "msa":
        return common + ["Payment terms", "IP ownership", "Service levels"]
    if contract_type == "vendor":
        return common + ["Data protection", "Security requirements", "Audit rights"]
    return common


def main():
    parser = argparse.ArgumentParser(description="Print a contract review checklist.")
    parser.add_argument(
        "--type",
        required=True,
        choices=["nda", "msa", "vendor"],
        help="Contract type",
    )
    args = parser.parse_args()

    print("Contract Checklist")
    for item in checklist(args.type):
        print(f"- {item}")


if __name__ == "__main__":
    main()
