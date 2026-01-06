#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate a SIPOC template.")
    parser.add_argument("--process", required=True, help="Process name")
    args = parser.parse_args()

    headers = ["Suppliers", "Inputs", "Process", "Outputs", "Customers"]
    divider = ["---"] * len(headers)

    print(f"SIPOC: {args.process}")
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(divider) + " |")
    print("|  |  |  |  |  |")


if __name__ == "__main__":
    main()
