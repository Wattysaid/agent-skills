---
name: process-mining-assistant
description: Perform an end-to-end process mining analysis via a command-line workflow that progressively ingests, profiles, cleans, mines and reports on event logs using PM4Py. The workflow generates stage-based artefacts (including versioned notebooks) and pauses at decision checkpoints so the user can validate findings and choose how to proceed.
---

## Overview

This skill defines a **progressive, evidence-led** command-line workflow for end-to-end process mining using **PM4Py**.
It is designed for business analysts and data scientists who want repeatable outputs with an audit trail, while still keeping a human-in-the-loop for key decisions.

Core principles:
- **Sequential execution:** ingest first, then decide. Decisions must be grounded in the dataset’s observed state.
- **Decision checkpoints:** the assistant pauses at each phase that changes assumptions or outputs.
- **Artefact-first validation:** each phase generates a dedicated output folder with logs, summaries, charts and a **versioned notebook** that the user can run and edit.
- **Reproducibility:** every run produces a manifest of parameters and derived artefacts, and the assistant checks for user edits before progressing.

## Decision-First Interaction (Required)

### Evidence-led sequencing (mandatory)

It is not useful to ask about cleaning, thresholds, filtering or mining strategies before the data is loaded and profiled.
The assistant must therefore follow this order:

1. **Validate environment**
2. **Ingest and profile data**
3. **Ask phase-specific questions based on findings**
4. **Execute the phase with the user’s chosen options**
5. **Write artefacts and a versioned notebook**
6. **Check for notebook changes**
7. **Proceed to the next phase**

### Decision question format (mandatory)

For each phase that changes outputs or assumptions, ask the user to decide. Each decision must include:

- **Ask:** “Choose how we should handle X.”
- **Complication:** why the decision matters for correctness, privacy, interpretability, or downstream metrics.
- **Options:** 2 to 4 approaches, mark the preferred option.
- **Impact:** what each choice changes in outputs or artefacts.

Do not proceed until the user chooses.

### Step-by-step questioning (mandatory)

- Ask decisions **by phase** (mapping, data quality, cleaning and filtering, mining, conformance, performance, reporting).
- Do not ask questions for future phases until the current phase is resolved.
- After each user answer, proceed to the next relevant decision based on the data and prior choices.
- Prefer progressive disclosure: start with mapping, then data quality, then filtering, then mining, then conformance, then performance and organisational mining, then reporting.
- Never ask the user to reply with all phases’ option numbers in one message.
- When in doubt about pacing or sequencing, consult `references/interaction_examples.md` and follow the phase-based patterns.

## Prerequisites and Dependencies

Required:
- **Python 3.8+**
- **PM4Py**
- **pandas**, **numpy**, **matplotlib**

Install:
```bash
pip install pm4py pandas numpy matplotlib
```

For YAML configs:
```bash
pip install pyyaml
```

The repository includes a `requirements.txt` with tested ranges for production use.

## Project Structure and Versioning

### Inputs

- Event logs: **XES** or **CSV**
- Optional config: **YAML** or **JSON**

### Output directory conventions

The assistant creates a project output directory with stage folders:

```
output/
  manifest.json
  run_log.txt
  stage_00_validate_env/
  stage_01_ingest_profile/
  stage_02_data_quality/
  stage_03_clean_filter/
  stage_04_eda/
  stage_05_discover/
  stage_06_conformance/
  stage_07_performance/
  stage_08_org_mining/
  stage_09_report/
  notebooks/
    R1.00/
      01_ingest_profile.ipynb
      02_data_quality.ipynb
      ...
```

Version control rules:
- Use **R1.00, R1.01, R1.02…** for notebooks and stage outputs.
- Increment the revision when:
  - the user changes a notebook, or
  - parameters change, or
  - the assistant re-runs a phase due to detected inconsistencies.
- Every stage writes or updates `manifest.json` to record:
  - inputs (file, format, columns, time window)
  - chosen options (thresholds, filters, miners, privacy settings)
  - artefact paths
  - revision history (R-code, timestamp, reason)

## CLI Workflow (Sequential)

### Phase 0: Validate environment (fast gate)

Run:
- `scripts/00_validate_env.py`

Outputs:
- `output/stage_00_validate_env/validate_env.json`
- `output/stage_00_validate_env/validate_env.log`

Decision checkpoint:
- If dependencies are missing or incompatible, stop and instruct remediation before continuing.

### Phase 1: Ingest and profile (must happen before decisions)

Run:
- `scripts/01_ingest.py`

Purpose:
- Load the log (CSV or XES), normalise schema, parse timestamps, and compute an initial profile.

Outputs:
- `normalised_log.csv` (and/or normalised XES if needed)
- `ingest_profile.json` (columns, inferred types, parse success, missingness, duplicates)
- `sample_rows.csv` (small sample for inspection)
- Notebook: `notebooks/Rx.xx/01_ingest_profile.ipynb`

Decision checkpoint (asked after profiling):
- **Schema mapping (CSV):** confirm case, activity, timestamp, and resource columns.
- **Timestamp parsing:** confirm timezone and parse format if failures are detected.
- **Sensitive columns:** confirm masking patterns if PII-like fields are detected.

### Phase 2: Data quality assessment (after mapping)

Run:
- `scripts/03_data_quality.py` (or compatible file name, see Script Layout)

Purpose:
- Validate required fields, compute missingness and parse failure rates, identify duplicates, detect sensitive columns (if enabled), and propose thresholds based on observed rates.

Outputs:
- `data_quality.json`
- `data_quality_recommendations.json`
- Notebook: `notebooks/Rx.xx/02_data_quality.ipynb`

Decision checkpoint:
- Choose how to handle:
  - missing values (drop vs impute vs flag)
  - timestamp parse failures (drop vs repair vs manual mapping)
  - duplicates (drop exact vs deduplicate by keys)
  - masking/anonymisation (on/off and scope)

### Phase 3: Cleaning and filtering (after data quality decisions)

Run:
- `scripts/04_clean_filter.py`

Purpose:
- Apply cleaning actions and optional filtering (start/end activities, time window, rare activities, variant thresholding).

Outputs:
- `filtered_log.csv`
- `filter_summary.json`
- Notebook: `notebooks/Rx.xx/03_clean_filter.ipynb`

Decision checkpoint:
- Choose:
  - rare activity filtering (on/off and minimum frequency)
  - start/end activity constraints
  - time range restrictions
  - variant frequency threshold

### Phase 4: Exploratory analysis (EDA)

Run:
- `scripts/05_eda.py`

Outputs (examples):
- `summary_stats.json`
- `variant_counts.csv`, `variant_pareto.png`
- distribution charts (hour, weekday, month)
- arrival and throughput time series
- Notebook: `notebooks/Rx.xx/04_eda.ipynb`

Decision checkpoint:
- Confirm whether to continue with:
  - full log vs filtered subset
  - additional segmentation (time windows, case types, org unit)

### Phase 5: Process discovery

Run:
- `scripts/06_discover.py`

Purpose:
- Discover models using inductive miner, heuristic miner, or an auto strategy.

Outputs:
- model visualisations (DFG/Petri net artefacts)
- `model_metrics.csv`
- Notebook: `notebooks/Rx.xx/05_discover.ipynb`

Decision checkpoint:
- Choose miner strategy (auto vs inductive vs heuristic vs both) and thresholds.

### Phase 6: Conformance checking

Run:
- `scripts/07_conformance.py`

Purpose:
- Evaluate fitness and precision using token-based replay and or alignments.

Outputs:
- conformance metrics tables (CSV/JSON)
- deviations summaries
- Notebook: `notebooks/Rx.xx/06_conformance.ipynb`

Decision checkpoint:
- Choose method:
  - token-based replay (faster, broad) [preferred]
  - alignments (more precise, more costly)
- Choose deviation reporting detail (executive vs technical).

### Phase 7: Performance analysis

Run:
- `scripts/08_performance.py`

Outputs:
- `case_durations.csv`, distribution plots, SPC chart
- `sojourn_times.csv`, chart
- `performance_summary.json`
- Notebook: `notebooks/Rx.xx/07_performance.ipynb`

Decision checkpoint:
- Choose performance lens:
  - case duration focus
  - activity sojourn focus
  - both (recommended)

### Phase 8: Organisational mining

Run:
- `scripts/09_org_mining.py`

Outputs:
- `handover_of_work.csv`
- optional network artefacts
- Notebook: `notebooks/Rx.xx/08_org_mining.ipynb`

Decision checkpoint:
- Choose whether to include resource-level analysis if privacy constraints apply.

### Phase 9: Reporting and packaging

Run:
- `scripts/10_report.py`
- optionally `scripts/export_artifacts.py`

Outputs:
- `process_mining_report.md`
- `manifest.json` (finalised)
- zipped artefacts package (optional)
- Notebook: `notebooks/Rx.xx/09_report.ipynb` (optional)

Decision checkpoint:
- Choose reporting formats and audience:
  - executive summary
  - management deck inputs
  - technical report
  - data quality log
- Choose whether to generate a zipped bundle of artefacts.

## Notebook Change Detection (Required)

Before proceeding from any phase to the next, the assistant must check whether the user has edited:
- the phase notebook
- config files
- phase outputs that act as inputs to the next stage

Rules:
- If changes are detected, the assistant must:
  - record the change in `manifest.json` (revision bump)
  - re-run only the impacted phase(s)
  - regenerate downstream artefacts if needed
- The assistant must never silently continue using stale artefacts.

Implementation guidance:
- Track notebook modification timestamps and or hash checksums per file.
- Store these in `manifest.json` and compare on every phase transition.

## CLI Arguments

The pipeline accepts arguments for:
- input file path (`--file`), file type (`--format=csv` or `--format=xes`)
- CSV schema mapping: `--case`, `--activity`, `--timestamp`
- output directory (`--output`)
- mining thresholds and filters (examples below)
- config file (`--config`)

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

Optional but recommended flags (implement if not present):
- `--generate-notebooks` (default true)
- `--notebook-dir` (default `output/notebooks`)
- `--resume` (resume from latest successful stage)
- `--strict-repro` (fail if artefacts and manifest do not match)
- `--check-notebook-changes` (default true)

## Script Layout

The orchestration entry point is `scripts/run_pipeline.py`.
A backwards compatible wrapper may be provided as `scripts/process_mining_cli.py`.

| Script | Purpose |
| --- | --- |
| `scripts/00_validate_env.py` | Verify PM4Py, pandas, numpy, matplotlib availability |
| `scripts/01_ingest.py` | Load and normalise logs, export normalised CSV/XES, produce ingest profile |
| `scripts/02_validate_schema.py` | Validate required CSV schema and mappings (compatible alias: `scripts/validate_schema.py`) |
| `scripts/03_data_quality.py` | Data quality checks, missingness, parse failures, duplicates, sensitive column detection |
| `scripts/04_clean_filter.py` | Clean and filter logs (start/end activity filters, rare activity filtering) |
| `scripts/05_eda.py` | Stats, distributions, variants, arrival metrics |
| `scripts/06_discover.py` | Process discovery (inductive, heuristics, auto selection) |
| `scripts/07_conformance.py` | Conformance metrics and evaluation artefacts |
| `scripts/08_performance.py` | Case durations and sojourn analysis |
| `scripts/09_org_mining.py` | Organisational mining and handover-of-work |
| `scripts/10_report.py` | Report generation from artefacts |
| `scripts/run_pipeline.py` | Full end-to-end orchestration with checkpoints |
| `scripts/export_artifacts.py` | Zip and index output artefacts |
| `scripts/common.py` | Shared utilities (logging, config, IO, paths) |
| `scripts/process_mining_cli.py` | Wrapper for `run_pipeline.py` (optional) |

## Configuration

The pipeline accepts JSON or YAML via `--config`.

Example YAML:
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
generate_notebooks: true
notebook_revision: "R1.00"
```

## Input Schema (CSV)

Minimum required columns (after mapping):
- Case identifier (mapped to `case:concept:name`)
- Activity (mapped to `concept:name`)
- Timestamp (mapped to `time:timestamp`)

Optional:
- `org:resource` for organisational mining

## Output Artefacts

The pipeline produces artefacts per stage and a consolidated set in the root output directory.

Common artefacts:
- `summary_stats.json`
- `variant_counts.csv`
- `variant_pareto.png`
- `activity_distribution_hour.png`
- `activity_distribution_weekday.png`
- `activity_distribution_month.png`
- `activity_frequency.csv`
- `event_throughput_timeseries.png`
- `case_arrival_timeseries.png`
- `model_metrics.csv`
- `case_durations.csv`
- `case_duration_distribution.png`
- `case_duration_boxplot.png`
- `case_duration_spc.png`
- `sojourn_times.csv`
- `sojourn_time_chart.png`
- `handover_of_work.csv`
- `process_mining_report.md`
- `manifest.json`
- `data_quality.json`
- `data_quality_recommendations.json`
- `performance_summary.json`
- `notebooks/` (versioned notebooks by stage)

## Output Documentation Outline

Use generated artefacts to produce stakeholder-specific deliverables.

**Executive Summary Report (Senior Leadership)**
- Purpose and scope
- Key insights and KPIs (durations, throughput, conformance)
- Strategic implications (risk, cost, compliance)
- Recommended actions (impact and effort)
- Next steps

**Management Slide Deck Inputs**
- Objectives and scope
- Method overview
- Data quality and preparation
- Discovered models and bottlenecks
- Conformance and performance highlights
- Recommendations and decisions required

**Technical Analysis Report**
- Data inventory and assumptions
- Data preparation and transformations
- EDA results and caveats
- Discovery, parameters and selection rationale
- Conformance evaluation and deviations
- Performance and organisational analysis
- Limitations, bias and privacy controls
- Appendices (configs and manifest extracts)

**Data Quality and Preparation Log**
- Issues found and how addressed
- Thresholds chosen and rationale
- Post-cleaning validation results
- Privacy and compliance notes
- Data collection recommendations

## Quick Start

Run the end-to-end pipeline:
```bash
python scripts/run_pipeline.py   --file assets/sample_log.csv   --format csv   --case CaseID --activity Activity --timestamp Timestamp   --output output
```

If a config is used:
```bash
python scripts/run_pipeline.py --config config/example.yaml
```

## Additional Resources

- PM4Py documentation (official)
- IEEE XES standard (event log format)
- `references/improved_prompt.md` (notebook-based guidance mirrored here)
- `references/interaction_examples.md` (phase-by-phase question flows)

## Packaging and Testing

- Create a folder named `process-mining-assistant/` containing:
  - this `SKILL.md`
  - `scripts/`
  - `references/`
  - `assets/`
  - `requirements.txt`
  - `config/example.yaml` (optional but recommended)
- Zip the folder so the archive contains the `process-mining-assistant/` directory at its root.
- Test with sample logs (CSV and XES) and confirm:
  - stage folders are created
  - manifest is updated per phase
  - notebooks are generated and versioned
  - re-running after a notebook edit triggers the expected revision bump and selective re-execution

