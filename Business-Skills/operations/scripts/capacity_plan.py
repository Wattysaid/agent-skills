#!/usr/bin/env python3
import argparse
import math


def main():
    parser = argparse.ArgumentParser(description="Estimate required headcount.")
    parser.add_argument("--demand", type=float, required=True, help="Units per week")
    parser.add_argument(
        "--units-per-person",
        type=float,
        required=True,
        help="Units per person per week",
    )
    parser.add_argument(
        "--buffer",
        type=float,
        default=0.2,
        help="Buffer percentage as decimal (default 0.2)",
    )
    args = parser.parse_args()

    if args.units_per_person <= 0:
        print("Headcount: n/a")
        return

    raw = args.demand / args.units_per_person
    headcount = math.ceil(raw * (1 + args.buffer))

    print("Capacity Plan")
    print(f"Required headcount: {headcount}")


if __name__ == "__main__":
    main()
