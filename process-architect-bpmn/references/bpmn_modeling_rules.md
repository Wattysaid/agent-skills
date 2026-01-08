# Generic BPMN Modeling Rules

Use this file for syntax-agnostic BPMN guidance. Target-specific syntax rules live in each target folder.

## Scope

- Build BPMN process models from user-provided narratives or event logs.
- Ask clarifying questions when data is missing or ambiguous.
- State assumptions and data coverage.

## Core Elements

- Start event: one per main process unless multiple starts are explicitly required.
- End event: at least one; multiple end events allowed for distinct outcomes.
- Tasks: one task per atomic activity; use verbs in names.
- Gateways:
  - XOR for alternative paths.
  - AND for parallel paths.
  - Avoid OR unless explicitly supported by evidence.
- Sequence flows: connect all elements; avoid orphan nodes.

## Lanes and Pools

- Use lanes for roles, teams, or systems when responsibilities matter.
- Keep lane names short and consistent.
- If lane ownership is uncertain, mark it as an assumption.

## Naming and IDs

- Use stable, readable IDs.
- Use consistent naming across all elements.
- Keep labels concise; avoid punctuation that breaks syntax.

## Quality Checks

- Every path from start reaches an end.
- Gateways have matching split and join where required.
- No dead ends or unreachable tasks.
- Model matches the stated scope; note exclusions.

## Output Package

- Provide the model in the requested syntax.
- Include a short assumptions block.
- Include a simple mapping table if needed (activity -> task).
