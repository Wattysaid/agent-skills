#!/usr/bin/env python3
import argparse
import json


def main():
    parser = argparse.ArgumentParser(
        description="Compute weighted scores for scenarios from JSON input."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="JSON string with weights and scenarios",
    )
    args = parser.parse_args()

    data = json.loads(args.input)
    weights = data.get("weights", {})
    scenarios = data.get("scenarios", {})

    print("Scenario Scorecard")
    for name, scores in scenarios.items():
        total = 0.0
        for metric, weight in weights.items():
            total += float(scores.get(metric, 0)) * float(weight)
        print(f"{name}: {total:.2f}")


if __name__ == "__main__":
    main()
