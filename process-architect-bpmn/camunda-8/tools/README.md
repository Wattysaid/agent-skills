# Camunda BPMN Modelling Tools (Skeleton)

This folder contains **Python skeleton implementations** for the tools described in your BPMN Modelling Agent design.

They are designed to be:

- Simple to read and extend
- Usable as a local utility library
- Easy to wrap as tools for multi‑agent frameworks (CrewAI, LangChain, MCP, etc.)

Each module includes:

- Clear function signatures
- Docstrings explaining the intent
- Minimal placeholder logic (marked with TODOs) that you can replace with real behaviour

## Modules

- `file_tools.py` — file I/O, workspace, archiving helpers
- `bpmn_schema_tools.py` — BPMN parse/serialize + schema validation stubs
- `bpmn_lint_tools.py` — linting + forbidden pattern detection stubs
- `di_tools.py` — DI layout helpers (skeleton)
- `examples_tools.py` — helpers for loading examples and domain templates
- `diff_tools.py` — diff/patch helpers
- `model_tools.py` — BPMN ↔ ProcessModel JSON bridge (very lightweight example format)
- `bpmn_consistency_tools.py` — normalize task/gateway/event sizes and audit for lane coverage, DI parity, backward flows, and unmatched splits
- `bpmn_consistency_cli.py` — CLI wrapper to run normalization/audit across `.bpmn` files (`python -m tools.bpmn_consistency_cli --fix --audit Processes/*.bpmn`)

You can import these in your orchestration layer and expose them as tools to your BPMN modelling agents.
