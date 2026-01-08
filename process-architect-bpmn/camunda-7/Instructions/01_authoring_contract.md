# BPMN Authoring Contract (Camunda 7)

Use this contract for every response that returns BPMN XML. Always persist the generated diagram to a `.bpmn` file.

## Output Envelope

- Use one `<bpmn:definitions>` with one main `<bpmn:process>`.
- Default to `isExecutable="false"` unless the user requests automation.
- Include BPMN-DI for every node and flow.
- Namespaces (use exactly these):
  - `xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"`
  - `xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"`
  - `xmlns:di="http://www.omg.org/spec/DD/20100524/DI"`
  - `xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"`
  - `xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"`
  - `xmlns:camunda="http://camunda.org/schema/1.0/bpmn"`
- IDs: unique, readable, stable (`Task_ReviewOrder`, `Flow_Start_to_Review`).

## Pools and Lanes

- Use at least one pool and one lane unless the user explicitly requests no lanes.
- Every flow node must be inside a lane and listed in `bpmn:flowNodeRef`.

## File Output

- Always write a `.bpmn` file with a descriptive name.
- Return the file path to the user.

## Execution Metadata (only when asked)

- Add `camunda:` extensions only when provided (e.g., `camunda:formKey`, task listeners).
- Do not add `zeebe:` extensions.

## Structural Rules

- At least one start and one end event.
- No orphan nodes or dangling flows.
- Gateways must split and merge correctly.
- Message flows only connect between pools.
