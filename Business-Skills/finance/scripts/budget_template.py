#!/usr/bin/env python3
import argparse
import csv
import sys


def main():
    parser = argparse.ArgumentParser(description="Create a 12-month budget CSV template.")
    parser.add_argument("--output", help="Output CSV path; default stdout")
    args = parser.parse_args()

    headers = ["Category"] + [f"M{i}" for i in range(1, 13)] + ["Notes"]
    rows = [
        ["Revenue"],
        ["COGS"],
        ["Gross margin"],
        ["Sales and marketing"],
        ["R&D"],
        ["G&A"],
        ["Other"],
        ["Operating income"],
        ["Cash burn"],
    ]

    if args.output:
        handle = open(args.output, "w", newline="")
    else:
        handle = sys.stdout

    writer = csv.writer(handle)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row + [""] * (len(headers) - len(row)))

    if args.output:
        handle.close()


if __name__ == "__main__":
    main()
