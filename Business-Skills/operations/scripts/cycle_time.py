#!/usr/bin/env python3
import argparse

def safe_div(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator


def main():
    parser = argparse.ArgumentParser(
        description="Estimate cycle time using Little's Law."
    )
    parser.add_argument("--completed", type=float, required=True, help="Items completed")
    parser.add_argument(
        "--period-days", type=float, required=True, help="Time window in days"
    )
    parser.add_argument("--avg-wip", type=float, required=True, help="Average WIP")
    args = parser.parse_args()

    throughput = safe_div(args.completed, args.period_days)
    if throughput is None:
        cycle_time = None
    else:
        cycle_time = safe_div(args.avg_wip, throughput)

    print("Operations Throughput")
    print(f"Throughput (items/day): {throughput:.2f}" if throughput is not None else "Throughput: n/a")
    print(f"Cycle time (days): {cycle_time:.2f}" if cycle_time is not None else "Cycle time: n/a")


if __name__ == "__main__":
    main()
