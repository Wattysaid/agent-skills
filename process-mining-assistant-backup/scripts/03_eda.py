#!/usr/bin/env python3
"""Exploratory data analysis for event logs."""

import argparse
import os

from common import ensure_notebook, ensure_output_dir, ensure_stage_dir, exit_with_error, require_file, save_json, write_stage_manifest
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
    parser.add_argument("--notebook-revision", default="R1.00", help="Notebook revision label.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    try:
        require_file(args.file)
        ensure_output_dir(args.output)
        stage_dir = ensure_stage_dir(args.output, "stage_04_eda")
        event_log = load_event_log(args.file, args.format, args.case, args.activity, args.timestamp)
        stats = compute_statistics(event_log)
        start_end = compute_start_end(event_log)
        arrival_metrics = compute_arrival_metrics(event_log)
        summary_path = os.path.join(stage_dir, "summary_stats.json")
        save_json({"stats": stats, "arrival_metrics": arrival_metrics, "start_end": start_end},
                  summary_path)
        df = log_to_dataframe(event_log)
        plot_activity_distributions(df, stage_dir)
        compute_variant_stats(event_log, stage_dir, top_n=10)
        notebook_path = ensure_notebook(
            args.output,
            args.notebook_revision,
            "04_eda.ipynb",
            "Exploratory Data Analysis",
            context_lines=[
                "",
                f"- Events: {stats.get('num_events')}",
                f"- Cases: {stats.get('num_cases')}",
                f"- Variants: {stats.get('num_variants')}",
            ],
            code_lines=[
                "import json",
                f"with open(r\"{summary_path}\", \"r\", encoding=\"utf-8\") as handle:",
                "    summary = json.load(handle)",
                "summary",
            ],
        )
        artifacts = {
            "summary_stats_json": summary_path,
            "variant_counts_csv": os.path.join(stage_dir, "variant_counts.csv"),
            "variant_pareto_png": os.path.join(stage_dir, "variant_pareto.png"),
        }
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
