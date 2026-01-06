#!/usr/bin/env python3
import argparse

def clamp(value):
    return max(0.0, min(100.0, value))


def main():
    parser = argparse.ArgumentParser(description="Compute a simple customer health score.")
    parser.add_argument("--usage", type=float, required=True, help="0-100")
    parser.add_argument("--nps", type=float, required=True, help="0-100")
    parser.add_argument("--tickets", type=float, required=True, help="0-100 (higher is worse)")
    parser.add_argument(
        "--payment-risk", type=float, required=True, help="0-100 (higher is worse)"
    )
    parser.add_argument("--w-usage", type=float, default=0.4)
    parser.add_argument("--w-nps", type=float, default=0.3)
    parser.add_argument("--w-tickets", type=float, default=0.2)
    parser.add_argument("--w-payment", type=float, default=0.1)
    args = parser.parse_args()

    usage = clamp(args.usage)
    nps = clamp(args.nps)
    tickets = 100.0 - clamp(args.tickets)
    payment = 100.0 - clamp(args.payment_risk)

    score = (
        usage * args.w_usage
        + nps * args.w_nps
        + tickets * args.w_tickets
        + payment * args.w_payment
    )

    print("Customer Health Score")
    print(f"Score: {score:.2f}")


if __name__ == "__main__":
    main()
