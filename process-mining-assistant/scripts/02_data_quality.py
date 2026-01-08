#!/usr/bin/env python3
"""Run data quality checks and output a cleaned CSV."""

import argparse
import os

from common import ensure_output_dir, exit_with_error, require_file, save_json, ExitCodes
from process_mining_steps import load_csv_dataframe, run_data_quality_checks


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data quality checks for CSV event logs.")
    parser.add_argument("--file", required=True, help="Path to the CSV event log.")
    parser.add_argument("--case", default="case:concept:name", help="Case ID column name.")
    parser.add_argument("--activity", default="concept:name", help="Activity column name.")
    parser.add_argument("--timestamp", default="time:timestamp", help="Timestamp column name.")
    parser.add_argument("--output", default="output", help="Output directory.")
    parser.add_argument("--missing-value-threshold", type=float, default=0.05, help="Missing value threshold.")
    parser.add_argument("--timestamp-parse-threshold", type=float, default=0.02, help="Timestamp parse failure threshold.")
    parser.add_argument("--duplicate-threshold", type=float, default=0.02, help="Duplicate rate threshold.")
    parser.add_argument("--auto-filter-rare-activities", action="store_true", help="Filter low-frequency activities.")
    parser.add_argument("--min-activity-frequency", type=float, default=0.01, help="Min activity frequency for filtering.")
    parser.add_argument("--min-timestamp", help="Minimum timestamp (inclusive).")
    parser.add_argument("--max-timestamp", help="Maximum timestamp (inclusive).")
    parser.add_argument("--impute-missing-timestamps", action="store_true", help="Impute missing timestamps above threshold.")
    parser.add_argument("--timestamp-impute-strategy", choices=["median", "mean"], default="median", help="Timestamp imputation strategy.")
    parser.add_argument("--auto-mask-sensitive", dest="auto_mask_sensitive", action="store_true",
                        help="Mask detected sensitive columns.")
    parser.add_argument("--no-auto-mask-sensitive", dest="auto_mask_sensitive", action="store_false",
                        help="Disable masking detected sensitive columns.")
    parser.set_defaults(auto_mask_sensitive=True)
    parser.add_argument("--sensitive-column-patterns", help="Comma-separated patterns for sensitive columns.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    try:
        require_file(args.file)
        ensure_output_dir(args.output)
        df = load_csv_dataframe(args.file, args.case, args.activity, args.timestamp)
        df, quality, recommendations = run_data_quality_checks(df, vars(args))
        df.to_csv(os.path.join(args.output, "cleaned_log.csv"), index=False)
        save_json(quality, os.path.join(args.output, "data_quality.json"))
        if recommendations:
            save_json(recommendations, os.path.join(args.output, "data_quality_recommendations.json"))
    except ValueError as exc:
        message = str(exc)
        if "Timestamp parse failure" in message:
            exit_with_error(message, ExitCodes.TIMESTAMP_ERROR)
        if "Missing required columns" in message:
            exit_with_error(message, ExitCodes.SCHEMA_ERROR)
        exit_with_error(message, ExitCodes.MISSING_VALUES_ERROR)
    except Exception as exc:
        exit_with_error(str(exc), ExitCodes.RUNTIME_ERROR)


if __name__ == "__main__":
    main()
