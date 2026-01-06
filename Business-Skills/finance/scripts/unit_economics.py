#!/usr/bin/env python3
import argparse

def safe_div(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator


def main():
    parser = argparse.ArgumentParser(
        description="Compute basic unit economics from monthly inputs."
    )
    parser.add_argument("--price", type=float, required=True, help="Monthly price")
    parser.add_argument("--cogs", type=float, required=True, help="Monthly COGS")
    parser.add_argument(
        "--monthly-churn",
        type=float,
        required=True,
        help="Monthly churn rate as decimal (e.g., 0.05)",
    )
    parser.add_argument("--cac", type=float, required=True, help="Customer acquisition cost")
    args = parser.parse_args()

    gross_margin = safe_div(args.price - args.cogs, args.price)
    contribution = args.price - args.cogs
    ltv = None
    payback = None
    if args.monthly_churn > 0:
        ltv = contribution / args.monthly_churn
    if contribution > 0:
        payback = safe_div(args.cac, contribution)

    print("Unit Economics Summary")
    print(f"Price: {args.price:.2f}")
    print(f"COGS: {args.cogs:.2f}")
    print(f"Contribution: {contribution:.2f}")
    if gross_margin is None:
        print("Gross margin: n/a")
    else:
        print(f"Gross margin: {gross_margin:.2%}")
    if ltv is None:
        print("LTV: n/a")
    else:
        print(f"LTV (gross): {ltv:.2f}")
    if payback is None:
        print("Payback (months): n/a")
    else:
        print(f"Payback (months): {payback:.2f}")


if __name__ == "__main__":
    main()
