#!/usr/bin/env python3
"""Organisational mining for event logs."""

import argparse

from common import ensure_notebook, ensure_output_dir, ensure_stage_dir, exit_with_error, require_file, write_stage_manifest
from process_mining_steps import load_event_log, organisational_analysis


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Organisational analysis for event logs.")
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
        stage_dir = ensure_stage_dir(args.output, "stage_08_org_mining")
        event_log = load_event_log(args.file, args.format, args.case, args.activity, args.timestamp)
        handover_path = organisational_analysis(event_log, stage_dir)
        notebook_path = ensure_notebook(
            args.output,
            args.notebook_revision,
            "08_org_mining.ipynb",
            "Organisational Mining",
            context_lines=[
                "",
                "Review handover-of-work results.",
            ],
            code_lines=[
                "import pandas as pd",
                f"handover = pd.read_csv(r\"{handover_path}\")",
                "handover.head()",
            ],
        )
        artifacts = {"handover_of_work_csv": handover_path}
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
