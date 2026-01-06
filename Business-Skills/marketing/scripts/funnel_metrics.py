#!/usr/bin/env python3
import argparse

def safe_div(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator


def pct(value):
    if value is None:
        return "n/a"
    return f"{value:.2%}"


def main():
    parser = argparse.ArgumentParser(description="Compute funnel metrics.")
    parser.add_argument("--impressions", type=float, required=True)
    parser.add_argument("--clicks", type=float, required=True)
    parser.add_argument("--leads", type=float, required=True)
    parser.add_argument("--customers", type=float, required=True)
    parser.add_argument("--spend", type=float, required=True)
    args = parser.parse_args()

    ctr = safe_div(args.clicks, args.impressions)
    lead_rate = safe_div(args.leads, args.clicks)
    close_rate = safe_div(args.customers, args.leads)
    cac = safe_div(args.spend, args.customers)
    cpl = safe_div(args.spend, args.leads)

    print("Funnel Metrics")
    print(f"CTR: {pct(ctr)}")
    print(f"Lead rate: {pct(lead_rate)}")
    print(f"Close rate: {pct(close_rate)}")
    print(f"CAC: {cac:.2f}" if cac is not None else "CAC: n/a")
    print(f"CPL: {cpl:.2f}" if cpl is not None else "CPL: n/a")


if __name__ == "__main__":
    main()
