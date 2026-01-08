# Camunda 7 BPMN Output Guide

Use this when the user requests Camunda 7 output or "Camunda 7 BPMN".

Start with `Instructions/00b_README_MASTER.md` and `Instructions/01_authoring_contract.md`.

Use `references/` in this folder for Camunda 7-specific overrides; generic BPMN rules live in the root `references/`.
Start with `references/syntax_overrides.md` for Camunda 7 output constraints.

## Target Output

- BPMN 2.0 XML executable by Camunda 7.
- Include `definitions`, `process`, `startEvent`, `endEvent`, `task`, `gateway`, and `sequenceFlow`.
- Use stable IDs for elements; ensure all `sequenceFlow` references resolve.
- Only add Camunda extensions if explicitly requested or provided (e.g., task listeners, form keys).

## Workflow (Camunda 7)

1) Normalize to unified event schema:
   - `global_case_id`, `activity`, `timestamp`, `resource_id`.
   - Capture provenance and schema fingerprints.
2) Discover the model:
   - DFG for preview; Inductive Miner for final.
   - Default noise threshold: 0.2 unless specified.
3) Compute metrics and variants:
   - Cycle time, wait time, throughput, variants.
   - Identify happy path by frequency unless configured otherwise.
4) Map to BPMN:
   - Start/End events for case boundaries.
   - Tasks for activities.
   - XOR gateways for alternatives, AND for parallelism.
   - Avoid OR gateways unless explicitly supported by evidence.
5) Package outputs:
   - BPMN XML plus KPI summary, bottlenecks, assumptions.

## Required Clarifications (Ask if missing)

- Executable or documentation-only?
- Naming or ID conventions?
- Required extensions (forms, listeners, jobs)?
- Lanes/pools required?

## Output Checklist

- Single main process with clear start/end events.
- Gateways align with discovered model (XOR/AND).
- Sequence flows are valid and resolve.
- Assumptions and data coverage are explicit.
