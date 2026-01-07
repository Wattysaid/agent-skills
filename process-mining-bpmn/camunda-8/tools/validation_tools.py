"""
Validation checklist mapper inspired by `05_validation_checklist.md`.

Outputs a list of dicts with:
  - id: rule id
  - status: "pass" | "fail" | "warn"
  - message: human-readable description
"""

from __future__ import annotations
from typing import List, Dict
import xml.etree.ElementTree as ET

NS = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"
DIAGRAM_NS = "{http://www.omg.org/spec/BPMN/20100524/DI}"
DI_NS = "{http://www.omg.org/spec/DD/20100524/DI}"
DC_NS = "{http://www.omg.org/spec/DD/20100524/DC}"


def _status(rule_id: str, ok: bool, message: str, warn: bool = False) -> Dict[str, str]:
    return {
        "id": rule_id,
        "status": "pass" if ok else ("warn" if warn else "fail"),
        "message": message,
    }


def run_validation_checklist(xml: str) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    root = ET.fromstring(xml)
    process = root.find(f".//{NS}process")
    proc_id = process.get("id") if process is not None else None
    diagram = root.find(f".//{DIAGRAM_NS}BPMNDiagram")
    plane = diagram.find(f"{DIAGRAM_NS}BPMNPlane") if diagram is not None else None

    results.append(_status("definitions-exists", root.tag.endswith("definitions"), "Root is <definitions>."))
    results.append(_status("process-exists", process is not None, "Process element exists."))

    if process is None:
        return results

    # Participant and isExecutable defaults
    participant = root.find(f".//{NS}participant")
    results.append(_status("participant-present", participant is not None and participant.get("processRef") == proc_id, "Participant references main process."))
    results.append(_status("process-isExecutable-false", process.get("isExecutable") in {"false", "False"}, 'Process defaults to isExecutable="false".', warn=True))

    # Start/end coverage
    starts = process.findall(f".//{NS}startEvent")
    ends = process.findall(f".//{NS}endEvent")
    results.append(_status("start-event-present", len(starts) > 0, "At least one start event."))
    results.append(_status("end-event-present", len(ends) > 0, "At least one end event."))

    # Sequence flow connectivity
    seq_flows = process.findall(f".//{NS}sequenceFlow")
    node_ids = {n.get("id") for n in process.iter() if n.get("id")}
    for flow in seq_flows:
        src = flow.get("sourceRef")
        tgt = flow.get("targetRef")
        results.append(_status(f"flow-source-{flow.get('id')}", src in node_ids, "SequenceFlow sourceRef exists."))
        results.append(_status(f"flow-target-{flow.get('id')}", tgt in node_ids, "SequenceFlow targetRef exists."))

    # Lanes/pool
    lane_set = process.find(f"{NS}laneSet")
    results.append(_status("lane-set-present", lane_set is not None, "Lane set present."))
    if lane_set is not None:
        lane_refs = {ref.text for ref in lane_set.findall(f".//{NS}flowNodeRef") if ref.text}
        missing = [nid for nid in node_ids if nid not in lane_refs]
        results.append(
            _status("lane-membership-complete", len(missing) == 0, "All nodes referenced by lanes.")
        )

    # Gateways split/merge counts
    splits = sum(1 for g in process.findall(f".//{NS}exclusiveGateway") if len(process.findall(f".//{NS}sequenceFlow[@sourceRef='{g.get('id')}']")) > 1)
    merges = sum(1 for g in process.findall(f".//{NS}exclusiveGateway") if len(process.findall(f".//{NS}sequenceFlow[@targetRef='{g.get('id')}']")) > 1)
    results.append(
        _status("xor-split-merge-balance", merges >= splits, "Exclusive gateways have merges for splits.", warn=True)
    )

    # DI parity
    if plane is not None:
        collab = root.find(f".//{NS}collaboration")
        expected_plane = (collab.get("id") if collab is not None else proc_id)
        results.append(_status("di-plane-binding", plane.get("bpmnElement") == expected_plane, "BPMNPlane bound to collaboration or process."))
        shapes = {s.get("bpmnElement") for s in plane.findall(f"{DIAGRAM_NS}BPMNShape")}
        edges = {e.get("bpmnElement") for e in plane.findall(f"{DIAGRAM_NS}BPMNEdge")}
        results.append(_status("di-shapes-complete", all(nid in shapes for nid in node_ids), "All nodes have shapes."))
        results.append(_status("di-edges-complete", all(sf.get("id") in edges for sf in seq_flows if sf.get("id")), "All flows have edges."))
    else:
        results.append(_status("di-present", False, "BPMNDiagram/BPMNPlane present."))

    return results
