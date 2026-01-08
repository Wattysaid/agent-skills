#!/usr/bin/env python3
"""Process mining pipeline steps."""

import logging
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    import pm4py
    from pm4py.objects.conversion.log import converter as log_converter
    from pm4py.objects.log.util import dataframe_utils
    from pm4py.objects.log.importer.xes import importer as xes_importer
    from pm4py.algo.discovery.inductive import algorithm as inductive_miner
    from pm4py.algo.discovery.heuristics import algorithm as heuristic_miner
    from pm4py.evaluation.replay_fitness import evaluator as fitness_evaluator
    from pm4py.evaluation.precision import evaluator as precision_evaluator
    from pm4py.evaluation.generalization import evaluator as generalization_evaluator
    from pm4py.evaluation.simplicity import evaluator as simplicity_evaluator
    from pm4py.evaluation.soundness import algorithm as soundness_evaluator
    from pm4py.statistics.start_activities.log import get as start_activities_get
    from pm4py.statistics.end_activities.log import get as end_activities_get
    from pm4py.statistics.variants.log import get as variants_get
    from pm4py.visualization.petri_net import visualizer as pn_vis
except ImportError:
    pm4py = None


def require_pm4py() -> None:
    if pm4py is None:
        raise RuntimeError("pm4py is required. Install it before running the pipeline.")


def load_event_log(file_path: str, log_format: str, case_col: str,
                   activity_col: str, timestamp_col: str) -> object:
    """Load an event log from XES or CSV."""
    require_pm4py()
    if log_format.lower() == "xes":
        return xes_importer.apply(file_path)

    df = pd.read_csv(file_path)
    df = df.rename(columns={
        case_col: "case:concept:name",
        activity_col: "concept:name",
        timestamp_col: "time:timestamp",
    })
    dataframe_utils.convert_timestamp_columns_in_df(df)
    df = df.dropna(subset=["case:concept:name", "concept:name", "time:timestamp"])
    df = df.drop_duplicates()
    return log_converter.apply(df)


def clean_event_log(event_log: object) -> object:
    """Placeholder for log cleaning; currently returns log unchanged."""
    return event_log


def apply_filters(event_log: object,
                  start_activities: Optional[List[str]] = None,
                  end_activities: Optional[List[str]] = None) -> object:
    """Filter the log by start/end activities using PM4Py helpers."""
    require_pm4py()
    if start_activities:
        event_log = pm4py.filter_start_activities(event_log, start_activities)
    if end_activities:
        event_log = pm4py.filter_end_activities(event_log, end_activities)
    return event_log


def compute_statistics(event_log: object) -> Dict[str, int]:
    """Compute basic log stats."""
    num_cases = len(event_log)
    num_events = sum(len(trace) for trace in event_log)
    variants = variants_get.get_variants(event_log)
    num_variants = len(variants)
    return {
        "num_events": num_events,
        "num_cases": num_cases,
        "num_variants": num_variants,
    }


def log_to_dataframe(event_log: object) -> pd.DataFrame:
    require_pm4py()
    return log_converter.apply(event_log, variant=log_converter.Variants.TO_DATA_FRAME)


def plot_activity_distributions(df: pd.DataFrame, output_dir: str) -> Dict[str, str]:
    """Plot activity distributions by hour, weekday, month."""
    df = df.copy()
    df["time:timestamp"] = pd.to_datetime(df["time:timestamp"])
    df["hour"] = df["time:timestamp"].dt.hour
    df["weekday"] = df["time:timestamp"].dt.day_name()
    df["month_num"] = df["time:timestamp"].dt.month

    artifacts = {}
    plt.figure(figsize=(10, 6))
    df.groupby("hour")["concept:name"].count().plot(kind="bar", color="skyblue")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Events")
    plt.title("Activity Distribution by Hour")
    plt.tight_layout()
    path = os.path.join(output_dir, "activity_distribution_hour.png")
    plt.savefig(path)
    plt.close()
    artifacts["activity_distribution_hour"] = path

    plt.figure(figsize=(10, 6))
    df.groupby("weekday")["concept:name"].count().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ).plot(kind="bar", color="teal")
    plt.xlabel("Day of Week")
    plt.ylabel("Number of Events")
    plt.title("Activity Distribution by Weekday")
    plt.tight_layout()
    path = os.path.join(output_dir, "activity_distribution_weekday.png")
    plt.savefig(path)
    plt.close()
    artifacts["activity_distribution_weekday"] = path

    plt.figure(figsize=(10, 6))
    month_counts = df.groupby("month_num")["concept:name"].count()
    month_counts.plot(kind="bar", color="slateblue")
    plt.xlabel("Month")
    plt.ylabel("Number of Events")
    plt.title("Activity Distribution by Month")
    plt.tight_layout()
    path = os.path.join(output_dir, "activity_distribution_month.png")
    plt.savefig(path)
    plt.close()
    artifacts["activity_distribution_month"] = path

    return artifacts


def compute_variant_stats(event_log: object, output_dir: str, top_n: int = 10) -> Dict[str, str]:
    variants = variants_get.get_variants(event_log)
    counts = {variant: len(traces) for variant, traces in variants.items()}
    df = pd.DataFrame(list(counts.items()), columns=["variant", "count"]).sort_values(
        "count", ascending=False
    )
    df["percent"] = df["count"] / df["count"].sum() * 100
    df["cum_percent"] = df["percent"].cumsum()
    df.to_csv(os.path.join(output_dir, "variant_counts.csv"), index=False)

    # Pareto chart
    plt.figure(figsize=(10, 6))
    top_df = df.head(top_n)
    ax = top_df.plot(kind="bar", x="variant", y="count", legend=False, color="coral")
    ax2 = ax.twinx()
    ax2.plot(top_df["cum_percent"].values, color="black", marker="o")
    ax2.set_ylabel("Cumulative %")
    ax.set_xlabel("Variant")
    ax.set_ylabel("Case Count")
    plt.title("Top Variants Pareto")
    plt.tight_layout()
    pareto_path = os.path.join(output_dir, "variant_pareto.png")
    plt.savefig(pareto_path)
    plt.close()

    return {
        "variant_counts": os.path.join(output_dir, "variant_counts.csv"),
        "variant_pareto": pareto_path,
    }


def compute_arrival_metrics(event_log: object) -> Dict[str, float]:
    start_times = []
    for trace in event_log:
        if trace:
            start_times.append(trace[0]["time:timestamp"])
    if len(start_times) < 2:
        return {"mean_interarrival_hours": float("nan")}
    start_times = sorted(start_times)
    inter_arrivals = [
        (start_times[i] - start_times[i - 1]).total_seconds() / 3600.0
        for i in range(1, len(start_times))
    ]
    return {
        "mean_interarrival_hours": float(np.mean(inter_arrivals)),
        "median_interarrival_hours": float(np.median(inter_arrivals)),
    }


def discover_models(event_log: object, output_dir: str, noise_threshold: float,
                    dependency_threshold: float, frequency_threshold: float) -> Dict[str, object]:
    require_pm4py()
    models = {}
    try:
        net_ind, im_ind, fm_ind = inductive_miner.apply(event_log, parameters={"noise_threshold": noise_threshold})
        gviz_ind = pn_vis.apply(net_ind, im_ind, fm_ind)
        pn_vis.save(gviz_ind, os.path.join(output_dir, "inductive_miner_petri_net.png"))
        models["inductive"] = (net_ind, im_ind, fm_ind)
    except Exception as exc:
        logging.warning("Inductive miner failed: %s", exc)

    try:
        net_heu, im_heu, fm_heu = heuristic_miner.apply_heu(
            event_log,
            dependency_threshold=dependency_threshold,
            frequency_threshold=frequency_threshold,
        )
        gviz_heu = pn_vis.apply(net_heu, im_heu, fm_heu)
        pn_vis.save(gviz_heu, os.path.join(output_dir, "heuristic_miner_petri_net.png"))
        models["heuristic"] = (net_heu, im_heu, fm_heu)
    except Exception as exc:
        logging.warning("Heuristic miner failed: %s", exc)
    return models


def evaluate_models(event_log: object, models: Dict[str, Tuple], output_dir: str) -> pd.DataFrame:
    rows = []
    for name, (net, im, fm) in models.items():
        try:
            fitness = fitness_evaluator.apply(event_log, net, im, fm)
        except Exception:
            fitness = {"averageFitness": np.nan}
        try:
            precision = precision_evaluator.apply(event_log, net, im, fm)
        except Exception:
            precision = np.nan
        try:
            generalisation = generalization_evaluator.apply(event_log, net, im, fm)
        except Exception:
            generalisation = np.nan
        try:
            simplicity = simplicity_evaluator.apply(net)
        except Exception:
            simplicity = np.nan
        try:
            soundness = soundness_evaluator.apply(net)
        except Exception:
            soundness = np.nan
        rows.append({
            "model": name,
            "fitness": fitness.get("averageFitness") if isinstance(fitness, dict) else fitness,
            "precision": precision,
            "generalisation": generalisation,
            "simplicity": simplicity,
            "soundness": soundness,
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(output_dir, "model_metrics.csv"), index=False)
    return df


def performance_analysis(event_log: object, output_dir: str) -> Dict[str, str]:
    case_durations = []
    sojourn_times: Dict[str, List[float]] = {}
    for trace in event_log:
        if not trace:
            continue
        start_time = trace[0]["time:timestamp"]
        end_time = trace[-1]["time:timestamp"]
        duration = (end_time - start_time).total_seconds() / 3600.0
        case_durations.append(duration)
        for idx, event in enumerate(trace):
            act = event["concept:name"]
            if idx < len(trace) - 1:
                next_time = trace[idx + 1]["time:timestamp"]
                sojourn = (next_time - event["time:timestamp"]).total_seconds() / 3600.0
                sojourn_times.setdefault(act, []).append(sojourn)

    pd.DataFrame({"case_duration_hours": case_durations}).to_csv(
        os.path.join(output_dir, "case_durations.csv"), index=False
    )

    plt.figure(figsize=(8, 5))
    plt.hist(case_durations, bins=30, color="salmon", edgecolor="black")
    plt.title("Distribution of Case Durations")
    plt.xlabel("Duration (hours)")
    plt.ylabel("Number of Cases")
    plt.tight_layout()
    duration_chart = os.path.join(output_dir, "case_duration_distribution.png")
    plt.savefig(duration_chart)
    plt.close()

    avg_sojourn = {act: float(np.mean(times)) for act, times in sojourn_times.items()}
    df_sojourn = pd.DataFrame(list(avg_sojourn.items()), columns=["activity", "avg_sojourn_hours"])
    df_sojourn.to_csv(os.path.join(output_dir, "sojourn_times.csv"), index=False)

    plt.figure(figsize=(10, 6))
    df_sojourn.sort_values("avg_sojourn_hours", ascending=False).plot.bar(
        x="activity", y="avg_sojourn_hours", color="olive", legend=False
    )
    plt.title("Average Sojourn Time per Activity")
    plt.xlabel("Activity")
    plt.ylabel("Sojourn Time (hours)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    sojourn_chart = os.path.join(output_dir, "sojourn_time_chart.png")
    plt.savefig(sojourn_chart)
    plt.close()

    return {
        "case_duration_distribution": duration_chart,
        "sojourn_time_chart": sojourn_chart,
    }


def organisational_analysis(event_log: object, output_dir: str) -> str:
    handover_counts = {}
    for trace in event_log:
        prev_res = None
        for event in trace:
            res = event.get("org:resource")
            if prev_res and res and res != prev_res:
                key = (prev_res, res)
                handover_counts[key] = handover_counts.get(key, 0) + 1
            prev_res = res
    df_handovers = pd.DataFrame([
        {"from": k[0], "to": k[1], "count": v}
        for k, v in handover_counts.items()
    ])
    output_path = os.path.join(output_dir, "handover_of_work.csv")
    df_handovers.to_csv(output_path, index=False)
    return output_path


def compute_start_end(event_log: object) -> Dict[str, Dict[str, int]]:
    return {
        "start_activities": start_activities_get(event_log),
        "end_activities": end_activities_get(event_log),
    }
