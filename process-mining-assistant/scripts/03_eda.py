#!/usr/bin/env python3
"""Exploratory data analysis for event logs."""

import argparse
import os

from common import ensure_output_dir, exit_with_error, require_file, save_json
from process_mining_steps import (
    compute_arrival_metrics,
    compute_start_end,
    compute_statistics,
    compute_variant_stats,
    load_event_log,
    log_to_dataframe,
    plot_activity_distributions,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="EDA for an event log.")
    parser.add_argument("--file", required=True, help="Path to the event log file (CSV or XES).")
    parser.add_argument("--format", choices=["csv", "xes"], required=True, help="Input file format.")
    parser.add_argument("--case", default="case:concept:name", help="Case ID column name (CSV only).")
    parser.add_argument("--activity", default="concept:name", help="Activity column name (CSV only).")
    parser.add_argument("--timestamp", default="time:timestamp", help="Timestamp column name (CSV only).")
    parser.add_argument("--output", default="output", help="Output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    try:
        require_file(args.file)
        ensure_output_dir(args.output)
        event_log = load_event_log(args.file, args.format, args.case, args.activity, args.timestamp)
        stats = compute_statistics(event_log)
        start_end = compute_start_end(event_log)
        arrival_metrics = compute_arrival_metrics(event_log)
        save_json({"stats": stats, "arrival_metrics": arrival_metrics, "start_end": start_end},
                  os.path.join(args.output, "summary_stats.json"))
        df = log_to_dataframe(event_log)
        plot_activity_distributions(df, args.output)
        compute_variant_stats(event_log, args.output, top_n=10)
    except Exception as exc:
        exit_with_error(str(exc))


if __name__ == "__main__":
    main()
