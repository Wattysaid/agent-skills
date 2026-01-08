#!/usr/bin/env python3
"""Orchestrate the full process mining pipeline."""

import argparse
import logging
import os
from typing import Dict

import pandas as pd

from common import (
    ensure_output_dir,
    exit_with_error,
    load_config,
    merge_config,
    parse_list,
    require_file,
    save_json,
    setup_logging,
    write_manifest,
)
from process_mining_steps import (
    apply_filters,
    clean_event_log,
    compute_arrival_metrics,
    compute_start_end,
    compute_statistics,
    compute_variant_stats,
    discover_models,
    evaluate_models,
    load_event_log,
    log_to_dataframe,
    organisational_analysis,
    performance_analysis,
    plot_activity_distributions,
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="End-to-end process mining CLI pipeline.")
    parser.add_argument("--file", required=True, help="Path to the event log file (CSV or XES).")
    parser.add_argument("--format", choices=["csv", "xes"], required=True, help="Input file format.")
    parser.add_argument("--case", default="case:concept:name", help="Case ID column name (CSV only).")
    parser.add_argument("--activity", default="concept:name", help="Activity column name (CSV only).")
    parser.add_argument("--timestamp", default="time:timestamp", help="Timestamp column name (CSV only).")
    parser.add_argument("--output", default="output", help="Directory to store analysis results.")
    parser.add_argument("--noise-threshold", type=float, default=0.0, help="Noise threshold for inductive miner.")
    parser.add_argument("--dependency-threshold", type=float, default=0.5, help="Dependency threshold for heuristic miner.")
    parser.add_argument("--frequency-threshold", type=float, default=0.0, help="Frequency threshold for heuristic miner.")
    parser.add_argument("--start-activities", help="Comma-separated start activities to retain.")
    parser.add_argument("--end-activities", help="Comma-separated end activities to retain.")
    parser.add_argument("--config", help="Optional JSON/YAML config file.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase logging verbosity.")
    return parser.parse_args()


def generate_report(stats: Dict[str, int],
                    model_metrics: pd.DataFrame,
                    arrival_metrics: Dict[str, float],
                    start_end: Dict[str, Dict[str, int]],
                    output_dir: str,
                    report_path: str) -> None:
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("# Process Mining CLI Report\n\n")
        handle.write("## Summary Statistics\n")
        handle.write(f"- Number of events: {stats['num_events']}\n")
        handle.write(f"- Number of cases: {stats['num_cases']}\n")
        handle.write(f"- Number of variants: {stats['num_variants']}\n\n")
        handle.write("## Arrival Metrics\n")
        handle.write(f"- Mean inter-arrival (hours): {arrival_metrics.get('mean_interarrival_hours')}\n")
        handle.write(f"- Median inter-arrival (hours): {arrival_metrics.get('median_interarrival_hours')}\n\n")
        handle.write("## Start Activities\n")
        handle.write(pd.DataFrame(list(start_end["start_activities"].items()), columns=["activity", "count"]).to_markdown(index=False))
        handle.write("\n\n")
        handle.write("## End Activities\n")
        handle.write(pd.DataFrame(list(start_end["end_activities"].items()), columns=["activity", "count"]).to_markdown(index=False))
        handle.write("\n\n")
        handle.write("## Model Evaluation\n\n")
        handle.write(model_metrics.to_markdown(index=False))
        handle.write("\n\n")
        handle.write("The output directory includes plots and CSVs for variants, activity distributions, case durations, sojourn times, and organisational handovers. Use these artifacts to identify bottlenecks, deviations, and improvement opportunities.\n")


def main() -> None:
    args = parse_arguments()
    setup_logging(args.verbose)
    try:
        require_file(args.file)
        config = load_config(args.config)
        params = merge_config(args, config)
        ensure_output_dir(params["output"])
    except Exception as exc:
        exit_with_error(str(exc))

    try:
        event_log = load_event_log(
            params["file"],
            params["format"],
            params["case"],
            params["activity"],
            params["timestamp"],
        )
        event_log = clean_event_log(event_log)
        event_log = apply_filters(
            event_log,
            start_activities=parse_list(params.get("start_activities")),
            end_activities=parse_list(params.get("end_activities")),
        )
    except Exception as exc:
        exit_with_error(f"Failed to load or filter event log: {exc}")

    stats = compute_statistics(event_log)
    start_end = compute_start_end(event_log)
    arrival_metrics = compute_arrival_metrics(event_log)
    save_json({"stats": stats, "arrival_metrics": arrival_metrics, "start_end": start_end},
              os.path.join(params["output"], "summary_stats.json"))

    df = log_to_dataframe(event_log)
    dist_artifacts = plot_activity_distributions(df, params["output"])
    variant_artifacts = compute_variant_stats(event_log, params["output"], top_n=10)

    models = discover_models(
        event_log,
        params["output"],
        params["noise_threshold"],
        params["dependency_threshold"],
        params["frequency_threshold"],
    )
    model_metrics = evaluate_models(event_log, models, params["output"])
    perf_artifacts = performance_analysis(event_log, params["output"])
    org_artifact = organisational_analysis(event_log, params["output"])

    report_path = os.path.join(params["output"], "process_mining_report.md")
    generate_report(stats, model_metrics, arrival_metrics, start_end, params["output"], report_path)

    artifacts = {
        **dist_artifacts,
        **variant_artifacts,
        **perf_artifacts,
        "org_handover": org_artifact,
        "model_metrics": os.path.join(params["output"], "model_metrics.csv"),
        "report": report_path,
    }
    write_manifest(params["output"], params, artifacts)

    logging.info("Process mining analysis complete. Results saved in %s", params["output"])


if __name__ == "__main__":
    main()
