#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Compute a simple TAM model.")
    parser.add_argument("--population", type=float, required=True)
    parser.add_argument("--penetration", type=float, required=True, help="0-1")
    parser.add_argument("--price", type=float, required=True)
    parser.add_argument("--frequency", type=float, required=True, help="Purchases per year")
    args = parser.parse_args()

    tam = args.population * args.penetration * args.price * args.frequency
    print("Market Sizing")
    print(f"TAM: {tam:.2f}")


if __name__ == "__main__":
    main()
