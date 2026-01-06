#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Estimate runway in months.")
    parser.add_argument("--cash", type=float, required=True, help="Cash on hand")
    parser.add_argument("--net-burn", type=float, required=True, help="Monthly net burn")
    args = parser.parse_args()

    if args.net_burn <= 0:
        print("Runway: n/a (net burn must be > 0)")
        return

    runway = args.cash / args.net_burn
    print("Runway")
    print(f"Months: {runway:.2f}")


if __name__ == "__main__":
    main()
