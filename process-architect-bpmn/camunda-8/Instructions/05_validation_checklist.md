# Validation Checklist (Preflight Before Responding)

Run through these points after generating the BPMN XML.

---

## Structure

- [ ] Exactly one `<bpmn:definitions>` and one `<bpmn:process>` (unless modeling a collaboration with multiple pools/processes).
- [ ] `isExecutable="false"` unless explicitly requested; Zeebe extensions only when requested.
- [ ] At least one start and one end event. Every start has a path to an end.
- [ ] No orphan nodes; every flow node has expected incoming/outgoing sequence flows.
- [ ] All ids are unique across elements and DI.
- [ ] Gateways: every split has a matching merge of the same type (unless branches all end); event-based gateways only target catching events/receive tasks.
- [ ] Exclusive split gateways have ≥2 outgoing flows; exclusive merge gateways may have a single outgoing flow.
- [ ] Complex gateways are only used for multi-branch scenarios (>2 branches). Complex splits have >2 outgoing flows; complex merges have >2 incoming flows and a single outgoing flow.
- [ ] Message start/end and receive/send tasks reference distinct message names when execution is requested.
- [ ] Call activities have `calledElement`; error/escalation events reference defined errors/escalations with codes (or intentionally catch-all if acceptable); FEEL expressions are valid; avoid infinite straight-through loops (ensure a wait/user step exists).
- [ ] If collaborations: participants are defined, processes exist for referenced participants, and BPMNPlane `bpmnElement` targets the collaboration id.
- [ ] A `.bpmn` file has been written with a descriptive name; path shared with the user.
- [ ] For message starts/receives in executable models: message definitions exist and include correlation/subscription keys when required.

---

## Lanes & Pools

- [ ] At least one participant and one lane present; laneSet exists, lane shapes included, every lane lists all contained node ids in `bpmn:flowNodeRef` (no duplicates across lanes).
- [ ] If collaboration used: participants defined and message flows connect only across pools.

---

## BPMN-DI

- [ ] One BPMNDiagram/BPMNPlane bound to the process id (or collaboration id when using multiple pools).
- [ ] Every flow node (events, tasks, gateways, subprocesses, annotations, data objects) has exactly one BPMNShape with correct bounds.
- [ ] Every sequence/message/association flow has exactly one BPMNEdge with ≥2 waypoints.
- [ ] Waypoints connect from source center-right to target center-left (or via clean bends for lane changes).
- [ ] Collapsed subprocesses use standard task sizing (`120x80`).

---

## Content Hygiene

- [ ] Names are human-readable and describe outcomes.
- [ ] Timer definitions use ISO-8601; message names are unique per process.
- [ ] Conditions only on XOR/Inclusive flows; none on event-based gateway outgoing flows.
- [ ] Event subprocesses have no incoming/outgoing sequence flows; boundary events are attached to activities.
- [ ] Boundary-event exception paths terminate in an end event unless modeled as collapsed subprocesses.

---

## Optional Quick Script Logic

```python
# pseudo
assert one_definitions and one_process
assert start_count >=1 and end_count >=1
for node in flow_nodes: assert node.id in shapes
for flow in sequence_flows: assert flow.id in edges and flow.sourceRef in nodes and flow.targetRef in nodes
assert ids_are_unique
if lanes:
    assert all(flowNodeRef in nodes and appears_once)
```
