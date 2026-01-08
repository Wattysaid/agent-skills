# Layout & BPMN-DI Rules

Goal: deliver BPMN XML that renders cleanly without manual layout fixes in Camunda 8 Modeler.

---

## Node Sizing (`dc:Bounds`)

- Start/Intermediate/End Events: `width=36` `height=36`
- Tasks (all types): `width=120` `height=80`
- Gateways (diamond): `width=50` `height=50`
- Expanded Subprocess: minimum `width=300` `height=200` (adjust for contained nodes)
- Collapsed Subprocess: `width=120` `height=80` (match standard task size)
- Lanes: `isHorizontal="true"`; height large enough to contain children (e.g., 200–260). Pools can wrap lanes or single lane.
- Annotations/Data Objects: size as needed; keep consistent margins.

---

## Coordinate Scheme

- Use a left-to-right flow. Start around `(x=120, y=180)` with ~150px horizontal spacing between nodes.
- Align nodes sharing the same lane on the same y-level where possible.
- When using lanes or multiple pools, stagger y-values so each node is centered within its lane height; leave vertical gaps (e.g., 120–160px) between pools to keep message flows legible.
- Keep gateways centered on the path; place merges directly opposite splits when possible to simplify edges.
- Avoid backtracking flows; do not draw outgoing flows to the left or incoming flows on the right. Minimize crossings; use link events sparingly for distant jumps.
- For parallel fork/join patterns, align the join opposite the fork to keep symmetry and readability.

---

## Waypoints (`BPMNEdge`)

- Every `<bpmndi:BPMNEdge>` needs ≥2 `<di:waypoint>`. Two points for straight lines; add midpoints when changing lanes.
- For straight flows: from source center-right to target center-left (`x1 = source.x + width`, `y1 = centerY`; `x2 = target.x`, `y2 = centerY`).
- When moving vertically between lanes, use three points: exit right, vertical shift at mid-x, enter target.
- Message flows: dashed style handled by renderer; still provide 2–3 waypoints and keep them clear of sequence flows.

---

## DI Parity

- One `<bpmndi:BPMNShape>` per flow node (events, tasks, gateways, subprocesses, annotations, data objects, groups).
- One `<bpmndi:BPMNEdge>` per `<bpmn:sequenceFlow>` / `<bpmn:messageFlow>` / `<bpmn:association>`.
- Shape `bpmnElement` must match the element id; edge `bpmnElement` must match the flow id.

---

## Lanes & Pools

- Always include at least one pool (participant) and one lane. Add lane shapes covering the full diagram width. Keep child node bounds within lane y-range plus small padding (8–12px).
- In XML, list every node id inside the lane `bpmn:flowNodeRef` list. Do not duplicate nodes across lanes.

---

## Event Subprocess & Boundary Events

- Event subprocesses sit inside the parent process coordinates. Dotted outline; no incoming/outgoing sequence flows.
- Boundary event bounds should touch the host activity bounds. For a task at `(x,y,width,height)`, place boundary at `(x+width-18, y+height-18)`.

---

## Visual Cleanliness Checklist

- Even spacing horizontally; avoid overlapping edges.
- Do not cross lines when avoidable; add simple bends instead of long zig-zags.
- Keep text labels short; names auto-wrap in Modeler.
