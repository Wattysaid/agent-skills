#!/usr/bin/env python3
"""Clean and filter an event log."""

import argparse
import os

from common import ensure_output_dir, exit_with_error, parse_list, require_file
from process_mining_steps import apply_filters, clean_event_log, load_event_log, log_to_dataframe, require_pm4py


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean and filter an event log.")
    parser.add_argument("--file", required=True, help="Path to the event log file (CSV or XES).")
    parser.add_argument("--format", choices=["csv", "xes"], required=True, help="Input file format.")
    parser.add_argument("--case", default="case:concept:name", help="Case ID column name (CSV only).")
    parser.add_argument("--activity", default="concept:name", help="Activity column name (CSV only).")
    parser.add_argument("--timestamp", default="time:timestamp", help="Timestamp column name (CSV only).")
    parser.add_argument("--start-activities", help="Comma-separated start activities to retain.")
    parser.add_argument("--end-activities", help="Comma-separated end activities to retain.")
    parser.add_argument("--output", default="output", help="Output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    try:
        require_file(args.file)
        ensure_output_dir(args.output)
        event_log = load_event_log(args.file, args.format, args.case, args.activity, args.timestamp)
        event_log = clean_event_log(event_log)
        event_log = apply_filters(
            event_log,
            start_activities=parse_list(args.start_activities),
            end_activities=parse_list(args.end_activities),
        )
        df = log_to_dataframe(event_log)
        df.to_csv(os.path.join(args.output, "filtered_log.csv"), index=False)
        require_pm4py()
        import pm4py
        pm4py.write_xes(event_log, os.path.join(args.output, "filtered_log.xes"))
    except Exception as exc:
        exit_with_error(str(exc))


if __name__ == "__main__":
    main()
