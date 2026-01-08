---
name: process-architect-bpmn
description: Create BPMN process maps and analyses from transcripts, event logs, or connector data. Use when asked for process discovery, variants/bottlenecks, or BPMN outputs (Camunda 7/8, Mermaid, PlantUML, or generic BPMN XML).
---

# Process Mining BPMN Skill

Create accurate, explainable BPMN process maps from transcripts or event data using the project standards in this folder.

## Quick Start (Chainable Workflow)

1. Confirm scope and data:
   - Systems, date range, workspace/region, time zone.
   - Event log availability (case_id, activity, timestamp, resource).
   - Transcript availability (speaker/actor, timestamps, turn boundaries).
   - Desired output target (Camunda 7, Camunda 8, Mermaid cross-functional, PlantUML cross-functional, generic BPMN XML, or textual mapping).
2. If transcripts are provided, extract events and map to the unified event schema.
3. Normalize inputs into the unified event schema.
4. Discover the model (DFG for preview; Inductive Miner for main model) using pm4py where applicable.
5. Compute metrics and variants.
6. Translate to BPMN elements (tasks, gateways, start/end).
7. Validate and package output with assumptions and limitations.

If any of the above is missing, ask a targeted question before proceeding.

## Prompt Chaining (For Complex Requests)

Break large tasks into sequential checkpoints and confirm each before rendering final BPMN:
1. Input summary and normalization mapping.
2. Discovery summary (miner choice, key paths, variants).
3. BPMN mapping (tasks, gateways, sequence flows).
4. Final render in the requested target format.

## Core Workflow

### 0) If transcripts are provided, extract events

- Identify case boundaries (ticket ID, order ID, call/session ID, or explicit conversation boundaries).
- Extract `activity` labels from actions and decisions; map speaker/actor to `resource_id`.
- Normalize timestamps, infer time zone if missing, and record any assumptions.
- If events are implied rather than explicit, provide a brief extraction rationale.

### 1) Normalize to the unified event schema

Use the canonical event fields: `global_case_id`, `activity`, `timestamp`, `resource_id`.
Capture provenance and schema fingerprints. Respect workspace isolation and region boundaries.

### 2) Build the event log and discover the model

- Use DFG for fast previews; Inductive Miner for the main model.
- Use pm4py discovery utilities when implementing or validating discovery logic.
- Store miner choice and parameters in provenance.
- Default noise threshold: 0.2 unless the user specifies otherwise.

### 3) Compute metrics and variants

Compute cycle time, wait time, throughput, and variants. Identify the happy path by frequency unless configured otherwise.

### 4) Map discovery output to BPMN

Translate the model into BPMN:
- Start/End events: case start/end.
- Tasks: activities.
- Gateways: use XOR for alternative paths, AND for parallel flows, and OR only if explicitly supported by evidence.
- Sequence flows: DFG edges with performance annotations where available.

If the miner output does not clearly define gateway types, call out the ambiguity and present options.

### 5) Validate the model before rendering

Validate that the mapping is consistent and explainable:
- Every activity in the log is mapped to a task or explicitly excluded.
- No dead ends or disconnected fragments.
- Gateway semantics align with observed concurrency or exclusivity.
- Start/end reflect observed case boundaries.

If validation fails, state the issue and ask for clarification or provide alternatives.

### 6) Add explainability and narrative context (when requested)

Use feature engineering and explainability to highlight drivers for bottlenecks and long cycle times. Provide role-based summaries (Analyst, COO, CFO, CEO) using only observed metrics.

### 7) Output packaging

Always include:
- A BPMN representation (or explicit text mapping if BPMN XML is not requested).
- KPI summary and top bottlenecks.
- Assumptions, thresholds, and data coverage notes.

## Target-Specific Instructions

Load the target guide before producing output:
- Camunda 7: `camunda-7/REFERENCE.md`
- Camunda 8: `camunda-8/REFERENCE.md`
- Mermaid cross-functional: `mermaid-cross-functional/REFERENCE.md`
- PlantUML cross-functional: `plantuml-cross-functional/REFERENCE.md`

## Output Formats

Ask which target is preferred if not specified:
- Camunda 7 BPMN 2.0 XML.
- Camunda 8 BPMN 2.0 XML.
- Mermaid cross-functional diagram.
- PlantUML cross-functional diagram.
- Generic BPMN 2.0 XML.
- Textual BPMN mapping (tasks, gateways, flows) for review and iteration.

If the user mentions Camunda or a specific diagram syntax, use that target without further prompting.

## Example Prompts (Use As Examples)

- "Discover the order-to-cash process from this event log and output Camunda 8 BPMN XML."
- "Show me a Mermaid cross-functional diagram with roles and bottlenecks for last quarter."
- "Provide a textual BPMN mapping with gateways and assumptions for review."

## Quality, Security, and Governance

- Follow role-based access, workspace isolation, and regional data residency.
- Never log secrets or raw connector payloads.
- Add tests for any non-trivial logic if code is written or updated.

## References (Use As Needed)

Use these files as the source of truth; load only what you need.

- `references/bpmn_modeling_rules.md` for generic BPMN modeling rules.
- `references/bpmn_grammar.md` for BPMN structural grammar.
- `references/bpmn_json_schema.json` for generic BPMN JSON validation.
- `camunda-7/REFERENCE.md` for Camunda 7 BPMN output expectations and constraints.
- `camunda-8/REFERENCE.md` for Camunda 8 BPMN output expectations and constraints.
- `mermaid-cross-functional/REFERENCE.md` for Mermaid cross-functional diagram syntax.
- `plantuml-cross-functional/REFERENCE.md` for PlantUML cross-functional diagram syntax.
- `mermaid-cross-functional/examples/` for Mermaid examples.
- `plantuml-cross-functional/examples/` for PlantUML examples.

Target-specific overrides live under each target's `references/` folder. Keep generic BPMN modeling rules in the root `references/` folder.
