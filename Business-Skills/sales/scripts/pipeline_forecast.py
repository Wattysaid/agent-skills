#!/usr/bin/env python3
import argparse

def parse_stage(stage):
    parts = stage.split(":")
    if len(parts) != 3:
        raise ValueError("Stage must be name:amount:prob")
    name, amount, prob = parts
    return name, float(amount), float(prob)


def main():
    parser = argparse.ArgumentParser(
        description="Compute weighted pipeline forecast from stages."
    )
    parser.add_argument(
        "--stages",
        required=True,
        help="Comma-separated list name:amount:prob (prob 0-1)",
    )
    args = parser.parse_args()

    total = 0.0
    weighted = 0.0
    print("Pipeline Forecast")
    for raw in args.stages.split(","):
        name, amount, prob = parse_stage(raw)
        total += amount
        weighted += amount * prob
        print(f"- {name}: {amount:.2f} @ {prob:.2%}")
    print(f"Total pipeline: {total:.2f}")
    print(f"Weighted forecast: {weighted:.2f}")


if __name__ == "__main__":
    main()
