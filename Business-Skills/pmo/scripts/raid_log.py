#!/usr/bin/env python3
import argparse
import csv
import sys


def main():
    parser = argparse.ArgumentParser(description="Create a RAID log CSV template.")
    parser.add_argument("--output", help="Output CSV path; default stdout")
    args = parser.parse_args()

    headers = ["Type", "Description", "Owner", "Severity", "Mitigation", "Due date"]

    if args.output:
        with open(args.output, "w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
    else:
        writer = csv.writer(sys.stdout)
        writer.writerow(headers)


if __name__ == "__main__":
    main()
