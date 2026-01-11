#!/usr/bin/env python3
"""Generate a Markdown report from pipeline artifacts."""

import argparse
import json
import os

import pandas as pd

from common import ensure_notebook, ensure_stage_dir, exit_with_error, write_stage_manifest


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a report from process mining artifacts.")
    parser.add_argument("--output", default="output", help="Directory containing analysis results.")
    parser.add_argument("--report", default="process_mining_report.md", help="Report filename.")
    parser.add_argument("--notebook-revision", default="R1.00", help="Notebook revision label.")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    stage_dir = ensure_stage_dir(args.output, "stage_09_report")
    summary_path = os.path.join(args.output, "stage_04_eda", "summary_stats.json")
    metrics_path = os.path.join(args.output, "stage_05_discover", "model_metrics.csv")
    if not os.path.isfile(summary_path):
        summary_path = os.path.join(args.output, "summary_stats.json")
    if not os.path.isfile(metrics_path):
        metrics_path = os.path.join(args.output, "model_metrics.csv")
    if not os.path.isfile(summary_path):
        exit_with_error(f"Missing summary stats: {summary_path}")
    if not os.path.isfile(metrics_path):
        exit_with_error(f"Missing model metrics: {metrics_path}")

    with open(summary_path, "r", encoding="utf-8") as handle:
        summary = json.load(handle)
    model_metrics = pd.read_csv(metrics_path)

    report_path = os.path.join(stage_dir, args.report)
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("# Process Mining CLI Report\n\n")
        stats = summary.get("stats", {})
        handle.write("## Summary Statistics\n")
        handle.write(f"- Number of events: {stats.get('num_events')}\n")
        handle.write(f"- Number of cases: {stats.get('num_cases')}\n")
        handle.write(f"- Number of variants: {stats.get('num_variants')}\n\n")

        arrival = summary.get("arrival_metrics", {})
        handle.write("## Arrival Metrics\n")
        handle.write(f"- Mean inter-arrival (hours): {arrival.get('mean_interarrival_hours')}\n")
        handle.write(f"- Median inter-arrival (hours): {arrival.get('median_interarrival_hours')}\n\n")

        start_end = summary.get("start_end", {})
        if start_end.get("start_activities"):
            handle.write("## Start Activities\n")
            handle.write(pd.DataFrame(list(start_end["start_activities"].items()), columns=["activity", "count"]).to_markdown(index=False))
            handle.write("\n\n")
        if start_end.get("end_activities"):
            handle.write("## End Activities\n")
            handle.write(pd.DataFrame(list(start_end["end_activities"].items()), columns=["activity", "count"]).to_markdown(index=False))
            handle.write("\n\n")

        handle.write("## Model Evaluation\n\n")
        handle.write(model_metrics.to_markdown(index=False))
        handle.write("\n\n")
        handle.write("Review the output directory for plots and CSVs covering activity distributions, variants, case durations, sojourn times, and organisational handovers.\n")
    notebook_path = ensure_notebook(
        args.output,
        args.notebook_revision,
        "09_report.ipynb",
        "Reporting",
        context_lines=[
            "",
            f"- Report: {report_path}",
        ],
        code_lines=[
            f"report_path = r\"{report_path}\"",
            "print(report_path)",
        ],
    )
    artifacts = {"process_mining_report_md": report_path}
    write_stage_manifest(
        stage_dir,
        vars(args),
        artifacts,
        args.notebook_revision,
        notebook_path=notebook_path,
    )


if __name__ == "__main__":
    main()
