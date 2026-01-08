# BPMN Authoring Contract (Camunda 8, Illustrative)

Use this contract for every response that returns BPMN XML. Always persist the generated diagram to a `.bpmn` file without waiting for the user to ask.

---

## Output Envelope

- Always model inside at least one pool/participant. For single-actor diagrams, add a `<bpmn:participant>` that references the main process; add at least one lane to group the flow nodes.
- Return one `<bpmn:definitions>` with exactly one main `<bpmn:process>`. If modeling multiple pools, include a `<bpmn:collaboration>` with `<bpmn:participant>` entries and one process per executable pool.
- Default to `isExecutable="false"`; only set `true` and add Zeebe extensions when explicitly asked for automation.
- Namespaces (use exactly these):
  - `xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"`
  - `xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"`
  - `xmlns:di="http://www.omg.org/spec/DD/20100524/DI"`
  - `xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"`
  - `xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"`
  - `xmlns:zeebe="http://camunda.org/schema/zeebe/1.0"` (keep even if non-executable so imports stay smooth)
- IDs: unique, descriptive, stable (`Task_ReviewOrder`, `Flow_Start_to_Screen`).
- Always include DI: one `<bpmndi:BPMNDiagram>`, one `<bpmndi:BPMNPlane>` bound to the **process id** for single-pool models, or bound to the **collaboration id** when using multiple pools; shapes for all nodes, edges for all sequence/message/association flows.

---

## File Output (mandatory)

- Always write the BPMN XML to a `.bpmn` file in the workspace with a descriptive name (e.g., `invoice_process.bpmn`); do this even if the user does not explicitly request a file.
- After saving, tell the user the file path. If they also want inline XML, provide it in addition to the saved file.

---

## Structural Rules

- **Start/End coverage**: ≥1 start event and ≥1 end event. Every start must lead to at least one path to an end.
- **Connectivity**: no orphan nodes; every `sequenceFlow` has valid `sourceRef` and `targetRef` that exist.
- **Gateways**: every split (XOR/AND) must be matched by a downstream merge of the same type unless each branch ends independently. Event-based gateways only point to catching events; do not add conditions there. Exclusive splits must have ≥2 outgoing flows; exclusive merges may have 1 outgoing flow.
- **Complex gateways**: use only when there are multiple branches (more than two). Complex splits must have >2 outgoing flows; complex merges must have >2 incoming flows and only one outgoing flow.
- **Lanes/Pools**: required. Add a `<bpmn:laneSet>` with one or more `<bpmn:lane>` elements and lane shapes. Place node bounds within lane y-range and list all node refs in `bpmn:flowNodeRef`.
- **Collaborations**: if multiple pools are present, define `<bpmn:collaboration>` with participants pointing to their processes. Add message flows only between participants. Set BPMNPlane `bpmnElement` to the collaboration id.
- **Subprocesses**: if expanded, include their internal flow nodes and flows; if collapsed, do not include internals. Event subprocesses must sit inside their parent process scope. Collapsed subprocesses must follow the same modeling rules as any other activity and use standard task sizing in DI.
- **Exception paths**: boundary-event exception paths must terminate with an end event unless they are explicitly modeled as collapsed subprocesses (which must then be modeled out separately).
- **Artifacts** (annotations/data objects) are allowed for clarity but must also have DI shapes.
- **Executable references (when applicable)**: call activities must have `calledElement`; message events/receive tasks must reference a defined message (and correlation key if executable); error/escalation events should reference defined errors/escalations with codes; FEEL expressions must be syntactically valid.
- **Loops**: avoid straight-through automated loops; insert a timer, wait state, or user task to prevent infinite execution.
- **Patterns reference**: see `examples/best_practice_simple_user_task.bpmn`, `best_practice_exclusive_decision.bpmn`, `best_practice_call_activity_error.bpmn`, `best_practice_message_start.bpmn`, and `best_practice_parallel_review.bpmn` for working layouts and DI.

---

## Execution Metadata (only when asked)

For executable service tasks, include:

```xml
<bpmn:extensionElements>
  <zeebe:taskDefinition type="job-type" retries="3"/>
</bpmn:extensionElements>
```

Do **not** add headers, IO mappings, or messages unless the user provided them. For non-executable diagrams omit `extensionElements` entirely.

---

## Base Template (non-executable)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:zeebe="http://camunda.org/schema/zeebe/1.0"
  id="Definitions_1" targetNamespace="http://example.com/schema/bpmn">
  <bpmn:process id="Process_Main" name="Process Name" isExecutable="false">
    <bpmn:startEvent id="StartEvent_1" name="Start" />
    <bpmn:userTask id="Task_Describe" name="Describe step" />
    <bpmn:endEvent id="EndEvent_1" name="End" />
    <bpmn:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="Task_Describe" />
    <bpmn:sequenceFlow id="Flow_2" sourceRef="Task_Describe" targetRef="EndEvent_1" />
  </bpmn:process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Process_Main">
      <bpmndi:BPMNShape id="Shape_StartEvent_1" bpmnElement="StartEvent_1">
        <dc:Bounds x="100" y="180" width="36" height="36" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_Task_Describe" bpmnElement="Task_Describe">
        <dc:Bounds x="180" y="160" width="120" height="80" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNShape id="Shape_EndEvent_1" bpmnElement="EndEvent_1">
        <dc:Bounds x="340" y="180" width="36" height="36" />
      </bpmndi:BPMNShape>
      <bpmndi:BPMNEdge id="Edge_Flow_1" bpmnElement="Flow_1">
        <di:waypoint x="136" y="198" />
        <di:waypoint x="180" y="198" />
      </bpmndi:BPMNEdge>
      <bpmndi:BPMNEdge id="Edge_Flow_2" bpmnElement="Flow_2">
        <di:waypoint x="300" y="198" />
        <di:waypoint x="340" y="198" />
      </bpmndi:BPMNEdge>
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
```

---

## Authoring Habits

- Use human-readable names that describe the outcome ("Confirm customer identity").
- When branching, design the merge before finalizing waypoints to keep symmetry.
- Keep y-levels aligned for readability; stagger lanes vertically.
- Use ISO-8601 for timers (`PT5M`, `R/2024-10-01T08:00:00Z/P1D`).
- Message names should be unique per process.
- Label gateways as questions; label outgoing flows as answers/conditions. Prefer explicit gateways over implicit conditional flows.
- Keep flow direction left-to-right, minimize crossings and backward flows; place the happy path on the main line.
