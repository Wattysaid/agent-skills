# Camunda BPMN Modelling Agent — Master Instruction Pack
**Version 1.0 — Final**

This instruction pack is designed for Large Language Models (LLMs) that generate **BPMN 2.0 XML with DI** suitable for **Camunda 8 Modeler/Web Modeler**.

It provides a complete, self-contained system for:
- Authoring BPMN 2.0 XML
- Choosing correct BPMN shapes
- Applying DI layout rules
- Validating diagrams before returning them
- Archiving projects when modelling is complete

All files here are final and ready for use in an automated BPMN-modelling agent.

---

## 📁 File Overview

### `01_authoring_contract.md`
Defines the **BPMN authoring rules**, namespaces, DI requirements, lane/pool rules, and mandatory output format.
This is the **core behavioural contract** for the modelling agent and overrides other files if there is a conflict.

### `02_shape_catalogue_llm.md`
A complete, merged **BPMN 2.0 Shape Catalogue** optimised for LLMs. It explains:
- What each shape means
- When and how to use it
- Camunda 8 execution vs. illustrative-only support
- Best-practice modelling guidance

Use this when deciding which events, tasks, gateways, subprocesses, and artefacts to use in a diagram.

### `03_shape_catalogue_formal.md`
A concise, **Camunda-style reference** that lists:
- Supported BPMN constructs
- Whether they are executable in Camunda 8
- High-level modelling constraints

Use this as a quick reference or “support matrix” when you only need to know what is executable.

### `04_di_layout_rules.md`
Defines how to lay out diagrams so they render cleanly in Camunda 8:
- Node sizes (events, tasks, gateways, subprocesses, lanes)
- Coordinate and spacing conventions
- Waypoint rules for sequence flows and message flows
- DI parity (one shape per node, one edge per flow)
- Pool and lane layout expectations

### `05_validation_checklist.md`
A **preflight checklist** to run mentally (or via script) before returning BPMN XML:
- Structural integrity
- Gateway matching
- Lane and pool completeness
- DI completeness (shapes and edges)
- Content hygiene (names, timers, conditions)
- Collaboration and message-flow correctness

No BPMN XML should be returned to the user until all checklist items are satisfied.

### `06_archiving_rules.md`
Defines how to wrap up a modelling project:
- Confirming project completion
- Naming archive folders with timestamps
- Moving `.bpmn` files into an archive folder
- Writing an archive `README.md` recap
- Confirming handoff to the user

Use this when the user indicates that they are finished with a given modelling theme or project.

---

## 🧠 Recommended Agent Workflow

1. **Read `01_authoring_contract.md` first**  
   - Lock in namespaces, base XML skeleton, pool/lane rules, and file-output behaviour.
   - Always create a `.bpmn` file with a descriptive name.

2. **Use `02_shape_catalogue_llm.md` for semantic decisions**  
   - Choose the right BPMN shapes based on the process description.
   - Understand how Camunda 8 treats each event, task, gateway, and subprocess.

3. **Apply `04_di_layout_rules.md` when building DI**  
   - Place nodes using left-to-right flow.
   - Size nodes correctly.
   - Ensure one shape per node and one edge per flow.

4. **Run `05_validation_checklist.md` before responding**  
   - Ensure all IDs exist and are unique.
   - Ensure every start leads to an end.
   - Ensure no orphan nodes, broken edges, or mismatched gateways.
   - Ensure lane/pool and DI rules are satisfied.

5. **When the user confirms no further changes**  
   - Follow `06_archiving_rules.md` to archive BPMN files for that project.
   - If a new project starts, ask for (or generate) a new folder name.

---

## 🎯 Behavioural Principles for the Modelling Agent

- Always include at least one pool and one lane.
- Always include full BPMN-DI (shapes and edges).
- Always save a `.bpmn` file and tell the user its path.
- Never create orphaned flow nodes or flows.
- Never omit start/end events.
- Keep diagrams left-to-right, clean, and readable.
- Use human-friendly, outcome-focused names.
- Only add execution metadata (Zeebe extensions, `isExecutable="true"`, messages, errors, etc.) when explicitly requested.

This pack is intended to be **dropped directly into an LLM environment** as a complete modelling reference. No external documentation is required for basic operation.
