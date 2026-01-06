#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate a brand guidelines markdown template.")
    parser.add_argument("--brand", required=True, help="Brand name")
    args = parser.parse_args()

    print(f"# {args.brand} Brand Guidelines")
    print("\n## Brand promise")
    print("- [One sentence promise]")
    print("\n## Voice and tone")
    print("- Voice traits: [e.g., direct, optimistic, expert]")
    print("- Tone by context: [sales, support, product]")
    print("\n## Visual identity")
    print("- Primary color: #RRGGBB")
    print("- Secondary colors: #RRGGBB, #RRGGBB")
    print("- Typography: headings, body")
    print("- Logo usage: clear space, min size")
    print("\n## Messaging hierarchy")
    print("- Value proposition")
    print("- Proof points")
    print("- Feature highlights")
    print("\n## Do/Don't examples")
    print("- Do: [example]")
    print("- Don't: [example]")


if __name__ == "__main__":
    main()
