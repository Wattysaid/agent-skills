---
name: process-mining-assistant
description: Perform an end‑to‑end process mining analysis via a command‑line tool. Use this skill when a user needs to load, clean and analyse event logs, discover process models, evaluate conformance and performance, or generate reports using PM4Py outside of a notebook.
---

## Overview

This skill equips you with a repeatable command‑line workflow for conducting comprehensive process mining analyses.  It is designed for business analysts and data scientists who need to run the entire process mining lifecycle—from data ingestion through discovery, conformance checking and performance analysis—without relying on a notebook environment.  The skill assumes familiarity with Python and the PM4Py library.

### Decision-First Interaction (Required)

For every phase that changes outputs or assumptions, ask the user to decide. Each question must include:

- Ask: "Choose how we should handle X."
- Complication: why the decision matters for correctness, privacy, or interpretability.
- Options: 2-4 approaches, mark the preferred option.
- Impact: what each choice changes in the outputs or artifacts.

Do not proceed until the user chooses. Use this framing for data loading, schema mapping, data quality thresholds, filtering, mining strategy, conformance methods, privacy controls, and reporting formats.

#### Step-by-Step Questioning (Required)

- Ask decisions by phase (schema, data quality, filtering, mining/conformance, reporting). You may ask multiple questions within a single phase if needed for accuracy.
- Do not ask questions for future phases until the current phase is resolved.
- After each user answer, proceed to the next relevant decision based on the data and prior choices.
- Be verbose and decision-supportive: briefly restate the current context, why the decision matters, and what you will do next after their choice.
- Prefer progressive disclosure: start with schema and resource mapping, then data quality, then filtering, then mining/conformance, then reporting.
- Never ask the user to reply with all phases' option numbers in one message.
- When in doubt about pacing or sequencing, consult `references/interaction_examples.md` and follow the phase-based patterns.

### Prerequisites & Dependencies

To use this skill effectively, ensure the following software is available on your system:

- **Python 3.8** or higher – The CLI script is implemented in Python.
- **PM4Py** – Process mining library providing algorithms for discovery, conformance checking and performance analysis.
- **pandas**, **numpy**, **matplotlib** – Standard Python data‑science packages used for data manipulation, numerical computations and visualisation.

Install these packages via pip (or use the bundled `requirements.txt`):

```bash
pip install pm4py pandas numpy matplotlib
```

For YAML configs, install PyYAML:

```bash
pip install pyyaml
```

The skill includes `requirements.txt` with tested ranges for production use.

The CLI workflow accepts event logs in either **XES** or **CSV** format and outputs reports, visualisations and diagnostic metrics.  It follows best practices for modularity and reproducibility, mirroring the notebook‑based process mining guidance but adapted for non‑interactive execution.  The tool automatically performs data preparation, exploratory analysis, model discovery, conformance checking and organisational mining, then summarises findings and recommends improvements.

## CLI Workflow

1. **Installation**

   - Ensure Python 3.8 or higher is available on the system.
   - Install dependencies using pip:
     ```bash
     pip install pm4py pandas numpy matplotlib
     ```
   - Optional: set up a virtual environment to isolate packages.

2. **Prepare the CLI Scripts**

   - Use the modular scripts in `scripts/` for each process mining phase.  The main orchestration entrypoint is `scripts/run_pipeline.py`, while `scripts/process_mining_cli.py` is kept as a backward‑compatible wrapper.
   - Each script focuses on a single phase (ingest, EDA, discovery, conformance, performance, organisational mining, reporting) and shares common utilities in `scripts/common.py`.
   - Use the PM4Py APIs to implement process discovery and conformance checking.  Leverage pandas for data manipulation and matplotlib for visualisations.

3. **Command‑Line Arguments**

   - The pipeline accepts arguments for the input file path (`--file`), file type (`--format=csv` or `--format=xes`), case column, activity column and timestamp column names (for CSV), output directory (`--output`), and optional thresholds (e.g., `--noise-threshold` for miners).
   - Include flags to enable or disable differential privacy mechanisms (e.g., `--anonymise` with parameters ε, k and p) when processing sensitive datasets.

| Argument | Default | Description |
| --- | --- | --- |
| `--file` | Required | Input CSV/XES log path |
| `--format` | Required | `csv` or `xes` |
| `--case` | `case:concept:name` | Case ID column (CSV only) |
| `--activity` | `concept:name` | Activity column (CSV only) |
| `--timestamp` | `time:timestamp` | Timestamp column (CSV only) |
| `--output` | `output` | Output directory |
| `--noise-threshold` | `0.0` | Inductive miner noise threshold |
| `--dependency-threshold` | `0.5` | Heuristic miner dependency threshold |
| `--frequency-threshold` | `0.0` | Heuristic miner frequency threshold |
| `--start-activities` | None | Comma-separated start activities |
| `--end-activities` | None | Comma-separated end activities |
| `--config` | None | JSON/YAML config file |
| `--missing-value-threshold` | `0.05` | Missing value threshold |
| `--timestamp-parse-threshold` | `0.02` | Timestamp parse failure threshold |
| `--duplicate-threshold` | `0.02` | Duplicate rate warning threshold |
| `--auto-filter-rare-activities` | False | Filter low-frequency activities |
| `--min-activity-frequency` | `0.01` | Minimum activity frequency |
| `--impute-missing-timestamps` | False | Impute timestamps above threshold |
| `--timestamp-impute-strategy` | `median` | Timestamp imputation strategy |
| `--auto-mask-sensitive` | True | Mask detected sensitive columns |
| `--sensitive-column-patterns` | None | Patterns for sensitive columns |
| `--miner-selection` | `auto` | Miner selection strategy |
| `--variant-noise-threshold` | `0.01` | Variant frequency threshold |

### Decision Checkpoints (Ask Before Running)

- Input format and schema mapping (CSV column names, timestamp format).
- Data quality thresholds (missing, parse failure, duplicates).
- Privacy handling (masking/anonymization settings).
- Filtering (start/end activities, rare activity filtering).
- Miner selection (auto vs inductive vs heuristic vs both).
- Conformance method preference (token replay vs alignments if applicable).
- Output/reporting formats and audience (executive vs technical vs data quality log).

### Script Layout

| Script | Purpose |
| --- | --- |
| `scripts/00_validate_env.py` | Verify pm4py/pandas/numpy/matplotlib availability |
| `scripts/01_ingest.py` | Load and normalize logs, export normalized CSV/XES |
| `scripts/02_data_quality.py` | Data quality checks, schema validation, missing values |
| `scripts/02_clean_filter.py` | Clean and filter logs (start/end activity filters) |
| `scripts/03_eda.py` | Stats, distributions, variants, arrival metrics |
| `scripts/04_discover.py` | Process discovery (inductive/heuristic miners) |
| `scripts/05_conformance.py` | Conformance metrics and evaluation CSV |
| `scripts/06_performance.py` | Case durations and sojourn analysis |
| `scripts/07_org_mining.py` | Handover-of-work analysis |
| `scripts/08_report.py` | Report generation from artifacts |
| `scripts/run_pipeline.py` | Full end-to-end orchestration |
| `scripts/export_artifacts.py` | Zip and index output artifacts |
| `scripts/validate_schema.py` | Validate required CSV schema |

### Configuration

The pipeline accepts a JSON or YAML configuration file via `--config`. Example:

```yaml
file: path/to/event_log.csv
format: csv
case: CaseID
activity: Activity
timestamp: Timestamp
output: output
noise_threshold: 0.2
dependency_threshold: 0.5
frequency_threshold: 0.01
start_activities: "Start"
end_activities: "End"
missing_value_threshold: 0.05
timestamp_parse_threshold: 0.02
duplicate_threshold: 0.02
auto_filter_rare_activities: false
min_activity_frequency: 0.01
impute_missing_timestamps: false
timestamp_impute_strategy: median
auto_mask_sensitive: true
sensitive_column_patterns: "name,email,phone,ssn,address,user,customer,patient,employee,resource"
miner_selection: auto
variant_noise_threshold: 0.01
```

### Input Schema (CSV)

| Column | Required | Description |
| --- | --- | --- |
| Case ID | Yes | Case identifier (mapped to `case:concept:name`) |
| Activity | Yes | Activity label (mapped to `concept:name`) |
| Timestamp | Yes | Event timestamp (mapped to `time:timestamp`) |
| org:resource | No | Resource performing the activity |

### Output Artifacts

| Artifact | Description |
| --- | --- |
| `summary_stats.json` | Basic counts, arrival metrics, start/end activities |
| `variant_counts.csv` | Variant frequencies |
| `variant_pareto.png` | Pareto chart of top variants |
| `activity_distribution_hour.png` | Event distribution by hour |
| `activity_distribution_weekday.png` | Event distribution by weekday |
| `activity_distribution_month.png` | Event distribution by month |
| `activity_frequency.csv` | Activity frequency table |
| `event_throughput_timeseries.png` | Events per day over time |
| `case_arrival_timeseries.png` | Case arrivals over time |
| `model_metrics.csv` | Fitness/precision/generalisation/simplicity/soundness |
| `case_durations.csv` | Case duration distribution data |
| `case_duration_distribution.png` | Case duration histogram |
| `case_duration_boxplot.png` | Case duration boxplot |
| `case_duration_spc.png` | Case duration SPC chart |
| `sojourn_times.csv` | Average sojourn time per activity |
| `sojourn_time_chart.png` | Sojourn time bar chart |
| `handover_of_work.csv` | Handover-of-work counts |
| `process_mining_report.md` | Markdown report |
| `manifest.json` | Parameters and artifact map |
| `data_quality.json` | Missing rates, parse failures, duplicate rates |
| `data_quality_recommendations.json` | Suggested thresholds and masks |
| `performance_summary.json` | Performance recommendations |

### Output Documentation Outline

Use the artifacts generated by the pipeline to produce stakeholder‑specific deliverables. The outlines below map directly to the metrics, charts and logs created by the scripts.

**Executive Summary Report (Senior Leadership)**
- Purpose & scope: business process analysed and project goals.
- Key insights & KPIs: average case duration, throughput, compliance metrics, top variants.
- Strategic implications: alignment with objectives, compliance risks, cost/efficiency impacts.
- Recommended actions: priority initiatives with expected impact/effort.
- Next steps: roadmap and follow‑up analyses.

**Management Slide Deck / Presentation (Managers)**
- Introduction: objectives, scope, stakeholders.
- Methodology overview: data sources, discovery, conformance, performance.
- Data preparation & quality: cleaning steps, duplicates, missing values, timestamp handling.
- Discovered models: inductive/heuristic visuals with main paths and bottlenecks.
- Conformance & performance: fitness/precision charts, throughput, resource utilization.
- Recommendations: improvement opportunities and cost/benefit notes.
- Q&A points for discussion.

**Technical Analysis Report (Analysts / Process‑Mining Specialists)**
- Data inventory: sources, fields, volumes, time window.
- Data preparation procedures: column normalization, duplicate removal, missing/invalid handling, datetime conversion.
- EDA: events/cases/activities/variants, activity frequency charts, case duration plots.
- Process discovery: algorithms used, parameters, selection rationale.
- Conformance checking: method, fitness/precision/generalization/simplicity/soundness.
- Performance & organizational analysis: bottlenecks, sojourn times, handovers.
- Limitations & data challenges: missingness, skew, privacy safeguards.
- Appendices: config files, parameters, reproducibility notes.

**Data Quality & Preparation Log**
- Overview: purpose and link to analysis.
- Data cleaning summary: issues found, methods used, assumptions.
- Validation results: schema checks, parsing success, post‑cleaning metrics.
- Privacy & compliance: masking/anonymization steps.
- Recommendations for future data collection.

**Conformance & Performance Dashboard (PDF / Interactive)**
- Metrics overview: fitness, precision, throughput, sojourn by variant or time window.
- Visualizations: DFG/Petri nets, variant Pareto, bottleneck heatmaps.
- Drill‑downs: filters by case type, time range, org unit.
- Export options: charts/tables for reporting.

**Recommendations & Implementation Roadmap (Action Plan)**
- Summary of findings: key issues and risks.
- Prioritized recommendations: owners, benefits, resources, risks.
- Timeline: quick wins, mid‑term redesign, long‑term initiatives.
- Monitoring plan: KPIs and cadence for ongoing mining.

4. **Data Loading & Cleaning**

   - **XES Logs**: load using `pm4py.read_xes(file_path)`.  PM4Py automatically recognises the case identifier, activity name and timestamp.
   - **CSV Logs**: read with `pandas.read_csv(file_path)`.  Rename the case, activity and timestamp columns to PM4Py’s standard keys (`case:concept:name`, `concept:name`, `time:timestamp`).  Convert timestamps to datetime using `pm4py.objects.conversion.log.converter`.  Remove duplicate rows with `drop_duplicates()` and handle missing values through imputation or removal.  Document any assumptions about data types.
   - **Data Quality Checks**: run `scripts/02_data_quality.py` or the pipeline’s built‑in checks to validate required columns, validate timestamp parsing, assess missing rates, drop or impute missing timestamps based on thresholds, and mask detected sensitive columns when enabled.
   - **Filtering**: apply PM4Py’s filtering functions (`filter_start_activities`, `filter_end_activities`, `filter_event_attribute_values`, `filter_trace_attribute_values`, `filter_variants`, `filter_time_range`) to remove noise and outliers.  Provide optional CLI flags for setting frequency thresholds.
   - **Privacy**: if the user enables anonymisation, apply control‑flow anonymisation (e.g., SaCoFa) and contextual anonymisation (PRIPEL) with the specified ε, k and p values.

5. **Exploratory Data Analysis (EDA)**

   - **Statistics**: compute the number of events, cases and unique variants via `pm4py.get_variants(log)`.  Save these metrics to a summary report.
   - **Distributions**: plot activity frequency over time (hour, day, month) and case throughput times using histograms or boxplots.  Use matplotlib to create charts and save them to the output directory.
   - **Variants**: calculate variant counts and generate a Pareto chart showing the top variants and their percentage of total cases.
   - **Start/End Activities**: identify start and end activities using `pm4py.get_start_activities(log)` and `pm4py.get_end_activities(log)`.
   - **Additional Metrics**: compute events per case, case arrival rates and inter‑arrival times to reveal process dynamics.

6. **Process Discovery**

   - **Inductive Miner**: run `pm4py.discover_petri_net_inductive(log, noise_threshold=t)` where *t* is a user‑defined noise threshold.  Save the resulting Petri net image.
   - **Heuristic Miner**: run `pm4py.discover_petri_net_heuristics(log, dependency_threshold=d, frequency_threshold=f)` with user‑defined thresholds.  The heuristic miner filters infrequent behaviour to produce robust models.  Save the model visualisation.
   - Compare models by computing the five quality dimensions (fitness, precision, generalisation, simplicity, soundness) using PM4Py’s evaluation functions.
   - Provide guidance in the report on when to prefer each miner: the Inductive Miner yields sound models but may overfit noisy logs; the Heuristic Miner is more robust to noise but may lack soundness.
   - When `--miner-selection=auto`, the pipeline selects a miner based on variant diversity and rare-variant ratios, defaulting to the Heuristic Miner when logs are noisy.

7. **Conformance Checking**

   - Use token‑based replay and alignments to evaluate how well the discovered models reproduce the observed behaviour.  Implement `pm4py.conformance_token_based_replay` and `pm4py.conformance_alignments` as appropriate.
   - Summarise fitness and precision scores in a table.  Identify deviations (e.g., missing or extra activities) and include them in the report.
   - Compute generalisation, simplicity and soundness metrics.  Highlight trade‑offs between complex models and simpler ones with lower precision.

8. **Performance & Organisational Analysis**

   - **Bottleneck Detection**: calculate sojourn times per activity to identify steps with long waiting or processing times.  Plot bar charts of average sojourn times and highlight outliers.
   - **Throughput & Arrival**: compute case durations, arrival rates and length of stay metrics.  Visualise event counts over time to identify peaks and slack periods.
   - **Social Network Analysis**: use PM4Py’s social network analysis tools to generate handover‑of‑work and working‑together networks.  Optionally export network graphs to interactive formats (e.g., HTML) for stakeholder review.
   - **Resource Utilisation**: correlate resource workloads with bottlenecks and suggest reallocation or additional resources during busy periods.

9. **Reporting & Recommendations**

   - Generate a final report (e.g., Markdown or HTML) summarising:
     - Key statistics and visualisations from the EDA phase.
     - Discovered process models with their quality metrics.
     - Deviations identified during conformance checking.
     - Performance bottlenecks and resource insights.
     - Actionable recommendations for process improvement, such as reducing variants, updating reference models or reallocating staff.
   - Save the report and all associated plots in the output directory specified by the user.

## Additional Resources

- **PM4Py Documentation** – Official documentation for process mining algorithms and APIs.
- **IEEE XES Standard** – Details of the standard event log format.
- **Improved Prompt Reference** – Consult `references/improved_prompt.md` for a comprehensive notebook‑based version of this workflow.  The CLI implementation in this skill mirrors that guidance in a scriptable form.
- **Interaction Examples** – Consult `references/interaction_examples.md` for realistic, phase-by-phase question flows and common situations.

## Packaging & Testing

To prepare and distribute this skill:

- Create a folder named `process-mining-assistant` (matching the `name` field) containing this `SKILL.md`, the CLI scripts in `scripts/`, any reference files (e.g., `improved_prompt.md`), and assets (sample logs, images).
- Zip the folder such that the archive contains the `process-mining-assistant/` directory at its root.  This structure is required when uploading the skill to Claude.
- Before uploading, verify that the description accurately reflects when and how to use the skill, and that all referenced resources exist.  Check that required Python packages are installed.
- Test the CLI with sample logs to ensure it produces meaningful results.  Adjust noise or dependency thresholds as needed.
 - Keep `requirements.txt` and `config/example.yaml` in sync with the scripts to ensure reproducible runs.
4. **Quick Start**

   Run the end‑to‑end pipeline:

   ```bash
   python scripts/run_pipeline.py \
     --file assets/sample_log.csv \
     --format csv \
     --case CaseID --activity Activity --timestamp Timestamp \
     --output output
   ```
