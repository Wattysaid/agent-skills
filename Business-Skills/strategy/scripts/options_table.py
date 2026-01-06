#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Create a markdown options table.")
    parser.add_argument("--options", required=True, help="Comma-separated options")
    parser.add_argument(
        "--criteria",
        required=True,
        help="Comma-separated criteria (e.g., impact,effort,risk)",
    )
    args = parser.parse_args()

    options = [o.strip() for o in args.options.split(",") if o.strip()]
    criteria = [c.strip() for c in args.criteria.split(",") if c.strip()]

    headers = ["Option"] + criteria
    divider = ["---"] * len(headers)

    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(divider) + " |")
    for option in options:
        row = [option] + ["" for _ in criteria]
        print("| " + " | ".join(row) + " |")


if __name__ == "__main__":
    main()
