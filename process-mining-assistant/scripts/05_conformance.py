#!/usr/bin/env python3
"""Conformance checking and model evaluation."""

import argparse

from common import ensure_output_dir, exit_with_error, require_file
from process_mining_steps import discover_models, evaluate_models, load_event_log


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conformance checking for event logs.")
    parser.add_argument("--file", required=True, help="Path to the event log file (CSV or XES).")
    parser.add_argument("--format", choices=["csv", "xes"], required=True, help="Input file format.")
    parser.add_argument("--case", default="case:concept:name", help="Case ID column name (CSV only).")
    parser.add_argument("--activity", default="concept:name", help="Activity column name (CSV only).")
    parser.add_argument("--timestamp", default="time:timestamp", help="Timestamp column name (CSV only).")
    parser.add_argument("--output", default="output", help="Output directory.")
    parser.add_argument("--noise-threshold", type=float, default=0.0, help="Noise threshold for inductive miner.")
    parser.add_argument("--dependency-threshold", type=float, default=0.5, help="Dependency threshold for heuristic miner.")
    parser.add_argument("--frequency-threshold", type=float, default=0.0, help="Frequency threshold for heuristic miner.")
    parser.add_argument("--miner-selection", choices=["auto", "inductive", "heuristic", "both"], default="auto", help="Miner selection strategy.")
    parser.add_argument("--variant-noise-threshold", type=float, default=0.01, help="Variant frequency threshold for auto selection.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    try:
        require_file(args.file)
        ensure_output_dir(args.output)
        event_log = load_event_log(args.file, args.format, args.case, args.activity, args.timestamp)
        models = discover_models(
            event_log,
            args.output,
            args.noise_threshold,
            args.dependency_threshold,
            args.frequency_threshold,
            args.miner_selection,
            args.variant_noise_threshold,
        )
        evaluate_models(event_log, models, args.output)
    except Exception as exc:
        exit_with_error(str(exc))


if __name__ == "__main__":
    main()
