#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a simple issue tree template.")
    parser.add_argument("--objective", required=True, help="Decision or objective")
    args = parser.parse_args()

    print("Issue Tree")
    print(f"Objective: {args.objective}")
    print("- Demand")
    print("  - Market size and growth")
    print("  - Segment needs and willingness to pay")
    print("- Supply")
    print("  - Capabilities and capacity")
    print("  - Delivery or operational constraints")
    print("- Economics")
    print("  - Unit economics and margins")
    print("  - Investment and payback")


if __name__ == "__main__":
    main()
