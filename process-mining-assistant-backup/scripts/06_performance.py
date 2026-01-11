#!/usr/bin/env python3
"""Performance analysis for event logs."""

import argparse
import os

from common import ensure_notebook, ensure_output_dir, ensure_stage_dir, exit_with_error, require_file, save_json, write_stage_manifest
from process_mining_steps import load_event_log, performance_analysis


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Performance analysis for event logs.")
    parser.add_argument("--file", required=True, help="Path to the event log file (CSV or XES).")
    parser.add_argument("--format", choices=["csv", "xes"], required=True, help="Input file format.")
    parser.add_argument("--case", default="case:concept:name", help="Case ID column name (CSV only).")
    parser.add_argument("--activity", default="concept:name", help="Activity column name (CSV only).")
    parser.add_argument("--timestamp", default="time:timestamp", help="Timestamp column name (CSV only).")
    parser.add_argument("--output", default="output", help="Output directory.")
    parser.add_argument("--notebook-revision", default="R1.00", help="Notebook revision label.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    try:
        require_file(args.file)
        ensure_output_dir(args.output)
        stage_dir = ensure_stage_dir(args.output, "stage_07_performance")
        event_log = load_event_log(args.file, args.format, args.case, args.activity, args.timestamp)
        perf_artifacts, perf_summary = performance_analysis(event_log, stage_dir)
        if perf_summary:
            summary_path = os.path.join(stage_dir, "performance_summary.json")
            save_json(perf_summary, summary_path)
        else:
            summary_path = None
        notebook_path = ensure_notebook(
            args.output,
            args.notebook_revision,
            "07_performance.ipynb",
            "Performance Analysis",
            context_lines=[
                "",
                "Review case duration and sojourn time outputs.",
            ],
            code_lines=[
                "import pandas as pd",
                f"durations = pd.read_csv(r\"{stage_dir}/case_durations.csv\")",
                "durations.head()",
            ],
        )
        artifacts = {key: value for key, value in perf_artifacts.items()}
        if summary_path:
            artifacts["performance_summary_json"] = summary_path
        write_stage_manifest(
            stage_dir,
            vars(args),
            artifacts,
            args.notebook_revision,
            notebook_path=notebook_path,
        )
    except Exception as exc:
        exit_with_error(str(exc))


if __name__ == "__main__":
    main()
