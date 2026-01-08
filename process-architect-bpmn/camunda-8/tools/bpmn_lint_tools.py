"""
BPMN linting and forbidden pattern detection.

The rules here are lightweight but actionable, mapping directly to the guidance in
`05_validation_checklist.md` and `forbidden_patterns.md`. The goal is to give fast
feedback that catches the most common mistakes before you hand results to a user.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import xml.etree.ElementTree as ET


@dataclass
class LintResult:
    rule_id: str
    severity: str  # e.g. "error", "warning", "info"
    message: str
    node_id: str | None = None


@dataclass
class ForbiddenPatternHit:
    pattern_id: str
    message: str
    node_id: str | None = None


NS = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"
DI_NS = "{http://www.omg.org/spec/DD/20100524/DI}"
DIAGRAM_NS = "{http://www.omg.org/spec/BPMN/20100524/DI}"
DC_NS = "{http://www.omg.org/spec/DD/20100524/DC}"

NODE_TAGS = {
    f"{NS}startEvent",
    f"{NS}endEvent",
    f"{NS}task",
    f"{NS}userTask",
    f"{NS}serviceTask",
    f"{NS}sendTask",
    f"{NS}receiveTask",
    f"{NS}manualTask",
    f"{NS}callActivity",
    f"{NS}subProcess",
    f"{NS}exclusiveGateway",
    f"{NS}parallelGateway",
    f"{NS}inclusiveGateway",
    f"{NS}eventBasedGateway",
    f"{NS}complexGateway",
    f"{NS}intermediateCatchEvent",
    f"{NS}intermediateThrowEvent",
    f"{NS}boundaryEvent",
}


def _find_main_process(root: ET.Element) -> ET.Element | None:
    return root.find(f".//{NS}process")


def run_bpmn_lint(xml: str) -> List[LintResult]:
    """
    Run basic BPMN linting rules.

    Current checks (quick and conservative):
      - Process exists
      - Participant exists and references process
      - LaneSet present with lane membership
      - BPMNDiagram/Plane present and bound correctly
      - isExecutable defaults to false
      - At least one start and one end event
      - Each start has outgoing sequence flows
      - Each end has incoming sequence flows
      - No orphaned nodes (must have incoming or outgoing, except start/end allowance)
      - Sequence flows reference real nodes
      - Exclusive split gateways should have 2+ outgoing flows; exclusive merges should have 1 outgoing flow
      - Complex gateways reserved for >2-branch splits/merges
      - Boundary event exception paths should terminate in an end event or a collapsed subprocess
      - Collapsed subprocesses should use standard task sizing
      - DI parity: every node has a shape and every sequence flow has an edge
    """
    results: List[LintResult] = []
    root = ET.fromstring(xml)
    process = _find_main_process(root)
    if process is None:
        return [
            LintResult(
                rule_id="require-process",
                severity="error",
                message="No <process> element found.",
                node_id=None,
            )
        ]

    proc_id = process.get("id")
    proc_executable = process.get("isExecutable")
    if proc_executable not in {"false", "False", None}:
        results.append(
            LintResult(
                rule_id="process-executable-default",
                severity="warning",
                message='Process should default to isExecutable="false" unless explicitly requested.',
                node_id=proc_id,
            )
        )

    participant = root.find(f".//{NS}participant")
    if participant is None or participant.get("processRef") != proc_id:
        results.append(
            LintResult(
                rule_id="participant-missing",
                severity="error",
                message="Participant referencing the main process is required.",
                node_id=proc_id,
            )
        )

    lane_set = process.find(f"{NS}laneSet")
    if lane_set is None:
        results.append(
            LintResult(
                rule_id="lanes-missing",
                severity="error",
                message="LaneSet with at least one lane is required.",
                node_id=proc_id,
            )
        )

    nodes = [n for n in process.iter() if n.tag in NODE_TAGS]
    node_ids = {n.get("id") for n in nodes if n.get("id")}
    start_events = [n for n in nodes if n.tag == f"{NS}startEvent"]
    end_events = [n for n in nodes if n.tag == f"{NS}endEvent"]

    seq_flows = process.findall(f".//{NS}sequenceFlow")
    outgoing_map: dict[str, List[str]] = {}
    incoming_map: dict[str, List[str]] = {}
    for flow in seq_flows:
        src = flow.get("sourceRef")
        tgt = flow.get("targetRef")
        fid = flow.get("id")
        if src:
            outgoing_map.setdefault(src, []).append(fid or "")
        if tgt:
            incoming_map.setdefault(tgt, []).append(fid or "")
        if src and src not in node_ids:
            results.append(
                LintResult(
                    rule_id="flow-source-missing",
                    severity="error",
                    message=f"SequenceFlow {fid} points to unknown source {src}.",
                    node_id=fid,
                )
            )
        if tgt and tgt not in node_ids:
            results.append(
                LintResult(
                    rule_id="flow-target-missing",
                    severity="error",
                    message=f"SequenceFlow {fid} points to unknown target {tgt}.",
                    node_id=fid,
                )
            )

    if not start_events:
        results.append(
            LintResult(
                rule_id="require-start-event",
                severity="error",
                message="No <startEvent> found in the BPMN model.",
                node_id=None,
            )
        )
    if not end_events:
        results.append(
            LintResult(
                rule_id="require-end-event",
                severity="error",
                message="No <endEvent> found in the BPMN model.",
                node_id=None,
            )
        )

    # Start/end connectivity
    for se in start_events:
        sid = se.get("id")
        if sid and not outgoing_map.get(sid):
            results.append(
                LintResult(
                    rule_id="start-needs-outgoing",
                    severity="error",
                    message="Start event has no outgoing sequence flow.",
                    node_id=sid,
                )
            )
    for ee in end_events:
        eid = ee.get("id")
        if eid and not incoming_map.get(eid):
            results.append(
                LintResult(
                    rule_id="end-needs-incoming",
                    severity="error",
                    message="End event has no incoming sequence flow.",
                    node_id=eid,
                )
            )

    # Orphan detection (allow start with no incoming and end with no outgoing)
    for node in nodes:
        nid = node.get("id")
        if not nid:
            continue
        incomings = incoming_map.get(nid, [])
        outgoings = outgoing_map.get(nid, [])
        if node.tag == f"{NS}startEvent":
            if not outgoings:
                continue
        elif node.tag == f"{NS}endEvent":
            if not incomings:
                continue
        if not incomings and not outgoings:
            results.append(
                LintResult(
                    rule_id="orphan-node",
                    severity="error",
                    message="Flow node is not connected to any sequence flow.",
                    node_id=nid,
                )
            )

    # Gateway fan-out
    for node in nodes:
        if "Gateway" not in node.tag:
            continue
        nid = node.get("id")
        outs = outgoing_map.get(nid or "", [])
        ins = incoming_map.get(nid or "", [])
        if node.tag == f"{NS}exclusiveGateway":
            if len(ins) <= 1 and len(outs) < 2:
                results.append(
                    LintResult(
                        rule_id="exclusive-split-branches",
                        severity="warning",
                        message="Exclusive split gateway should have 2+ outgoing flows.",
                        node_id=nid,
                    )
                )
            if len(ins) > 1 and len(outs) != 1:
                results.append(
                    LintResult(
                        rule_id="exclusive-merge-outgoing",
                        severity="warning",
                        message="Exclusive merge gateway should have exactly one outgoing flow.",
                        node_id=nid,
                    )
                )
        if node.tag == f"{NS}complexGateway":
            if len(outs) > 1 and len(outs) <= 2:
                results.append(
                    LintResult(
                        rule_id="complex-gateway-branches",
                        severity="error",
                        message="Complex gateway split must have >2 outgoing flows.",
                        node_id=nid,
                    )
                )
            if len(outs) == 1 and len(ins) <= 2:
                results.append(
                    LintResult(
                        rule_id="complex-gateway-branches",
                        severity="error",
                        message="Complex gateway merge must have >2 incoming flows.",
                        node_id=nid,
                    )
                )
            if len(outs) == 0:
                results.append(
                    LintResult(
                        rule_id="complex-gateway-branches",
                        severity="error",
                        message="Complex gateway must have at least one outgoing flow.",
                        node_id=nid,
                    )
                )

    # Lanes membership completeness
    if lane_set is not None:
        lane_refs = {ref.text for ref in lane_set.findall(f".//{NS}flowNodeRef") if ref.text}
        for nid in node_ids:
            if nid and nid not in lane_refs:
                results.append(
                    LintResult(
                        rule_id="lane-membership-missing",
                        severity="error",
                        message="Flow node not referenced by any lane.",
                        node_id=nid,
                    )
                )

    # DI parity checks and plane binding
    diagram = root.find(f".//{DIAGRAM_NS}BPMNDiagram")
    plane = diagram.find(f"{DIAGRAM_NS}BPMNPlane") if diagram is not None else None
    if diagram is None or plane is None:
        results.append(
            LintResult(
                rule_id="di-missing",
                severity="error",
                message="BPMNDiagram/BPMNPlane required for DI.",
                node_id=None,
            )
        )
    else:
        target = plane.get("bpmnElement")
        collab = root.find(f".//{NS}collaboration")
        collab_id = collab.get("id") if collab is not None else None
        expected_plane = collab_id if collab_id else proc_id
        if expected_plane and target != expected_plane:
            results.append(
                LintResult(
                    rule_id="di-plane-binding",
                    severity="error",
                    message=f"BPMNPlane should reference {expected_plane}.",
                    node_id=target,
                )
            )

        shapes = {sh.get("bpmnElement") for sh in plane.findall(f"{DIAGRAM_NS}BPMNShape")}
        edges = {ed.get("bpmnElement") for ed in plane.findall(f"{DIAGRAM_NS}BPMNEdge")}
        for nid in node_ids:
            if nid not in shapes:
                results.append(
                    LintResult(
                        rule_id="di-missing-shape",
                        severity="error",
                        message="Flow node missing BPMNShape.",
                        node_id=nid,
                    )
                )
        for flow in seq_flows:
            fid = flow.get("id")
            if fid and fid not in edges:
                results.append(
                    LintResult(
                        rule_id="di-missing-edge",
                        severity="error",
                        message="SequenceFlow missing BPMNEdge.",
                        node_id=fid,
                    )
                )
        # Collapsed subprocess sizing
        for shape in plane.findall(f"{DIAGRAM_NS}BPMNShape"):
            elem_id = shape.get("bpmnElement")
            if not elem_id:
                continue
            subprocess = process.find(f".//{NS}subProcess[@id='{elem_id}']")
            if subprocess is None:
                continue
            if shape.get("isExpanded") == "true":
                continue
            bounds = shape.find(f"{DC_NS}Bounds")
            if bounds is None:
                continue
            if bounds.get("width") != "120" or bounds.get("height") != "80":
                results.append(
                    LintResult(
                        rule_id="collapsed-subprocess-size",
                        severity="warning",
                        message="Collapsed subprocess should use standard task size (120x80).",
                        node_id=elem_id,
                    )
                )

    return results


def check_forbidden_patterns(xml: str) -> List[ForbiddenPatternHit]:
    """
    Detect forbidden modelling patterns.

    Current checks:
      - Left-pointing sequence flows (based on DI waypoints if present)
      - Start → End directly with no work
      - Boundary events without attachedToRef
      - Flow nodes missing lane membership (when lanes exist)
      - Gateway splits exceeding merges (rough balance heuristic)
    """
    hits: List[ForbiddenPatternHit] = []
    root = ET.fromstring(xml)
    diagram = root.find(f".//{DIAGRAM_NS}BPMNDiagram")
    plane = diagram.find(f"{DIAGRAM_NS}BPMNPlane") if diagram is not None else None

    if plane is not None:
        for edge in plane.findall(f"{DIAGRAM_NS}BPMNEdge"):
            points: List[Tuple[float, float]] = []
            for wp in edge.findall(f"{DI_NS}waypoint"):
                x = float(wp.get("x", "0"))
                y = float(wp.get("y", "0"))
                points.append((x, y))
            if len(points) >= 2 and points[0][0] > points[-1][0]:
                hits.append(
                    ForbiddenPatternHit(
                        pattern_id="left-pointing-flow",
                        message="Sequence flow appears to go right-to-left.",
                        node_id=edge.get("bpmnElement"),
                    )
                )

    # Start followed immediately by end (no tasks/gateways between)
    process = _find_main_process(root)
    if process is not None:
        seq_flows = {sf.get("sourceRef"): sf.get("targetRef") for sf in process.findall(f".//{NS}sequenceFlow")}
        for se in process.findall(f".//{NS}startEvent"):
            first = seq_flows.get(se.get("id"))
            if first:
                target = process.find(f".//{NS}endEvent[@id='{first}']")
                if target is not None:
                    hits.append(
                        ForbiddenPatternHit(
                            pattern_id="start-to-end-direct",
                        message="Start event flows directly to an end event.",
                        node_id=se.get("id"),
                    )
                )

        # Boundary events must be attached
        for be in process.findall(f".//{NS}boundaryEvent"):
            attached = be.get("attachedToRef")
            if not attached:
                hits.append(
                    ForbiddenPatternHit(
                        pattern_id="boundary-without-attachment",
                        message="Boundary event missing attachedToRef.",
                        node_id=be.get("id"),
                    )
                )
        # Boundary exception paths should terminate or be modeled as subprocesses
        seq_by_source: dict[str, List[str | None]] = {}
        for sf in process.findall(f".//{NS}sequenceFlow"):
            src = sf.get("sourceRef")
            if src:
                seq_by_source.setdefault(src, []).append(sf.get("targetRef"))
        for be in process.findall(f".//{NS}boundaryEvent"):
            targets = seq_by_source.get(be.get("id"), [])
            for target in targets:
                if target is None:
                    continue
                end = process.find(f".//{NS}endEvent[@id='{target}']")
                sub = process.find(f".//{NS}subProcess[@id='{target}']")
                if end is None and sub is None:
                    hits.append(
                        ForbiddenPatternHit(
                            pattern_id="boundary-path-termination",
                            message="Boundary exception path should terminate in an end event or a collapsed subprocess.",
                            node_id=be.get("id"),
                        )
                    )

        # Lane membership completeness
        lane_set = process.find(f"{NS}laneSet")
        if lane_set is not None:
            lane_refs = {ref.text for ref in lane_set.findall(f".//{NS}flowNodeRef") if ref.text}
            for node in process.iter():
                nid = node.get("id")
                if nid and node.tag in NODE_TAGS and nid not in lane_refs:
                    hits.append(
                        ForbiddenPatternHit(
                            pattern_id="lane-membership-missing",
                            message="Flow node not referenced by any lane.",
                            node_id=nid,
                        )
                    )

        # Gateway split/merge rough balance
        xor_split = sum(1 for g in process.findall(f".//{NS}exclusiveGateway") if len(process.findall(f".//{NS}sequenceFlow[@sourceRef='{g.get('id')}']")) > 1)
        xor_merge = sum(1 for g in process.findall(f".//{NS}exclusiveGateway") if len(process.findall(f".//{NS}sequenceFlow[@targetRef='{g.get('id')}']")) > 1)
        if xor_split > xor_merge:
            hits.append(
                ForbiddenPatternHit(
                    pattern_id="xor-split-without-merge",
                    message="More XOR splits than merges detected; ensure splits are closed.",
                    node_id=None,
                )
            )

    return hits
