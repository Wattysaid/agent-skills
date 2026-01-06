#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Estimate team capacity in hours.")
    parser.add_argument("--team-size", type=float, required=True)
    parser.add_argument("--focus-hours", type=float, required=True, help="Focus hours per week")
    parser.add_argument("--weeks", type=float, required=True)
    parser.add_argument(
        "--efficiency",
        type=float,
        default=0.8,
        help="Efficiency factor 0-1 (default 0.8)",
    )
    args = parser.parse_args()

    capacity = args.team_size * args.focus_hours * args.weeks * args.efficiency
    print("Team Capacity")
    print(f"Capacity hours: {capacity:.2f}")


if __name__ == "__main__":
    main()
