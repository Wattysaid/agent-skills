# Camunda BPMN Modelling Agents

This guide distills the master prompt (`00a_master_system_prompt.md`) and master README (`00b_README_MASTER.md`) into a quick reference for how agents should behave when generating Camunda 8–ready BPMN 2.0 XML with DI. The agent must read and honour **every** file in this repository; nothing here is optional.

## Mission
- Convert natural-language process descriptions into valid BPMN 2.0 XML (with full BPMN-DI) that opens cleanly in Camunda 8 Modeler/Web Modeler.
- Prefer clarity and correctness; make reasonable assumptions when details are missing and state them briefly.
- Always save output to a `.bpmn` file and report its path.

## Ground-Truth References (read-all checklist)
- `00a_master_system_prompt.md`: the canonical system prompt; aligns all behaviours.
- `00b_README_MASTER.md`: high-level overview; confirms authoritative files and principles.
- `01_authoring_contract.md`: canonical authoring rules (namespaces, envelope, pools/lanes, DI requirements, structural rules, output expectations).
- `02_shape_catalogue_llm.md`: semantic guidance for choosing events, tasks, gateways, subprocesses, artifacts; includes invalid/valid event types (e.g., no error/terminate start events).
- `03_shape_catalogue_formal.md`: execution/support matrix for Camunda 8 (what runs vs illustrative-only).
- `04_di_layout_rules.md`: layout, sizing, spacing, waypoint patterns; always combine with `di_templates.md` for reusable coordinates.
- `05_validation_checklist.md`: mandatory preflight; must be passed before returning XML.
- `06_archiving_rules.md`: project wrap-up steps and archive format.
- `../../references/bpmn_grammar.md` + `../../references/bpmn_json_schema.json`: structural grammar and required attributes.
- `forbidden_patterns.md`: do-not-do list (no left-pointing flows, no gateways with single outgoing path, no pools without lanes, no orphan nodes, no boundary events floating, no start→end direct).
- `error_catalogue.md`: minimal fix recipes for missing shapes/edges.
- `reasoning_guide.md` + `micro_prompt_mapping.md`: reasoning steps and phrase-to-shape hints; drive discovery of lanes, events, tasks, gateways.
- `di_templates.md`: coordinate snippets for common patterns (e.g., XOR decision).
- `domain_templates.md`: starter flows for common domains.
- `examples/`: few-shot BPMN with DI; use for IDs/layout patterns (`best_practice_simple_user_task.bpmn`, `best_practice_exclusive_decision.bpmn`, `best_practice_message_start.bpmn`, `best_practice_parallel_review.bpmn`, `best_practice_call_activity_error.bpmn`, `approval_process_gateway.bpmn`, `Error Handling.bpmn`, `simple_user_task.bpmn`, etc.).
- `Processes/HR Processes/*.bpmn`: additional, ready-made process references (recruitment, onboarding, offboarding, leave request, performance review); use as inspiration and layout patterns but never copy IDs verbatim.

## Behavioural Principles
- Always include at least one pool and one lane; keep flow left-to-right with no orphan nodes or pools without lanes.
- Always include start and end events; ensure every start has a path to at least one end; avoid direct start→end with no work.
- Maintain DI parity: one `BPMNShape` per flow node, one `BPMNEdge` per flow, each with valid bounds/waypoints following layout rules.
- Use human-friendly, outcome-focused names; default `isExecutable="false"` and omit Zeebe metadata unless explicitly requested.
- Avoid forbidden patterns: left-pointing flows, gateways with single outgoing path, complex gateways used for two-way decisions, boundary exception paths that rejoin without end events, boundary events not touching activities, link events across pools, missing lane membership, orphans.
- Use complex gateways only for multi-branch cases (>2 branches); collapsed subprocesses follow standard activity sizing.

## Agent Roles
- **Authoring Agent**: apply reasoning steps and shape catalogues to draft BPMN with DI that already respects authoring rules and forbidden patterns.
- **Reviewer Agent**: run validation checklist and forbidden-pattern scan; report concrete issues and recommended fixes.
- **Repair Agent**: use error catalogue, grammar, and DI templates to implement fixes; re-validate before handoff.
- **Archivist Agent**: when the user confirms completion, follow archiving rules to package `.bpmn` files and document the archive.
- Single-agent runs perform all roles sequentially.

## Core Workflow (for new/updated diagrams)
1. Understand the request: actors → pools/lanes; triggers → start events; outcomes → end events; decisions/parallelism → gateways.
2. Map steps using `micro_prompt_mapping.md` and shape catalogues to select correct task/event/gateway types; obey catalogue prohibitions (e.g., no error start events, no conditions on event-based gateways).
3. Build sequence flow left-to-right; ensure structural rules from the authoring contract are satisfied; add lanes and flowNodeRefs.
4. Add DI: one shape per node with correct bounds; one edge per flow with 2+ waypoints; follow layout rules/DI templates; keep plane bound to process for single-pool or collaboration for multi-pool.
5. Validate: apply the validation checklist, forbidden-patterns, grammar/schema; fix issues via the error catalogue; repeat until clean.
6. Output: save BPMN XML to a `.bpmn` file, report the filename and a brief description.

## Common Mistakes to Avoid (cross-file)
- Missing lanes/pools or missing lane `flowNodeRef` entries.
- Start/end omissions or paths that never reach an end.
- Left-pointing/backtracking flows, overlapping/missing waypoints, or edges without DI.
- Gateways lacking matching merges; event-based gateways pointing to tasks instead of catches; complex gateways used for two-way decisions; collapsed subprocesses oversized.
- Boundary events not attached to activities; event subprocesses with incoming/outgoing flows.
- Using invalid start types (error, escalate, terminate, cancel, compensation) or message flows within a pool.
- Reusing IDs or copying example IDs without renaming; forgetting descriptive filenames when saving.

## Reading Order Suggestion
1. `00a_master_system_prompt.md` and `00b_README_MASTER.md` for global behaviour.
2. `01_authoring_contract.md` for envelope/structure and mandatory file output.
3. `02_shape_catalogue_llm.md` + `03_shape_catalogue_formal.md` for shape semantics/execution support.
4. `04_di_layout_rules.md` + `di_templates.md` for coordinates/spacing; use examples/ and Processes/HR samples to anchor DI.
5. `reasoning_guide.md` + `micro_prompt_mapping.md` for modelling flow.
6. `05_validation_checklist.md`, `forbidden_patterns.md`, `../../references/bpmn_grammar.md`, `../../references/bpmn_json_schema.json`, `error_catalogue.md` for validation and repair.
7. `06_archiving_rules.md` when a project is declared complete.

## When Archiving
- Confirm project completion with the user.
- Create an archive folder named `<project>_YYYYMMDD-HHMM`, move relevant `.bpmn` files, and add an archive `README.md` summarising scope and decisions.
- Confirm archive contents and be ready to start a new project folder if needed.
