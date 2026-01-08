"""
Generic BPMN consistency helpers focused on diagram hygiene and DI.

Key features (domain-agnostic):
- Normalize shape sizes to contract defaults (tasks 120x80, gateways 50x50, events 36x36, collapsed subprocesses 120x80).
- Detect leftward/backward sequence flows using DI waypoints.
- Flag missing DI parity (shape/edge) and lane flowNodeRef coverage.
- Spot likely unmatched splits (exclusive/parallel gateways with multiple outgoing flows and no merge of same type).
- Enforce complex gateway usage constraints (only for >2-branch splits/merges).

These helpers are intentionally conservative to work across domains (healthcare, trades, SaaS, etc.).
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}


# Utility helpers
def _q(tag: str) -> str:
    """Qualify a BPMN tag with the default namespace."""
    return f"{{{NS['bpmn']}}}{tag}"


def load_tree(path: Path) -> ET.ElementTree:
    return ET.parse(path)


def save_tree(tree: ET.ElementTree, path: Path) -> None:
    tree.write(path, encoding="UTF-8", xml_declaration=True)


def iter_flow_nodes(root: ET.Element) -> Iterable[ET.Element]:
    flow_node_tags = {
        _q("startEvent"),
        _q("intermediateCatchEvent"),
        _q("intermediateThrowEvent"),
        _q("endEvent"),
        _q("userTask"),
        _q("serviceTask"),
        _q("task"),
        _q("manualTask"),
        _q("scriptTask"),
        _q("businessRuleTask"),
        _q("sendTask"),
        _q("receiveTask"),
        _q("callActivity"),
        _q("subProcess"),
        _q("exclusiveGateway"),
        _q("inclusiveGateway"),
        _q("parallelGateway"),
        _q("eventBasedGateway"),
        _q("complexGateway"),
    }
    for el in root.iter():
        if el.tag in flow_node_tags:
            yield el


def is_gateway(el: ET.Element) -> bool:
    return el.tag.endswith("Gateway")


def is_task(el: ET.Element) -> bool:
    return el.tag.endswith("Task")


def is_event(el: ET.Element) -> bool:
    return el.tag.endswith("Event")


def is_subprocess(el: ET.Element) -> bool:
    return el.tag.endswith("subProcess")


def get_id(el: ET.Element) -> Optional[str]:
    return el.get("id")


@dataclass
class NormalizationChange:
    element_id: str
    from_size: Tuple[str, str]
    to_size: Tuple[str, str]


@dataclass
class AuditIssue:
    kind: str
    message: str
    element_id: Optional[str] = None


def normalize_shape_sizes(root: ET.Element) -> List[NormalizationChange]:
    """Normalize dc:Bounds sizes by element kind."""
    changes: List[NormalizationChange] = []
    bounds_by_id: Dict[str, ET.Element] = {}
    for shape in root.findall(".//bpmndi:BPMNShape", NS):
        be = shape.get("bpmnElement")
        b = shape.find("dc:Bounds", NS)
        if be and b is not None:
            bounds_by_id[be] = b
    for node in iter_flow_nodes(root):
        nid = get_id(node)
        if not nid or nid not in bounds_by_id:
            continue
        b = bounds_by_id[nid]
        target = None
        if is_task(node):
            target = ("120", "80")
        elif is_subprocess(node):
            shape = root.find(f".//bpmndi:BPMNShape[@bpmnElement='{nid}']", NS)
            if shape is not None and shape.get("isExpanded") == "true":
                target = None
            else:
                target = ("120", "80")
        elif is_gateway(node):
            target = ("50", "50")
        elif is_event(node):
            target = ("36", "36")
        if target:
            w, h = b.get("width"), b.get("height")
            if (w, h) != target:
                changes.append(NormalizationChange(nid, (w, h), target))
                b.set("width", target[0])
                b.set("height", target[1])
    return changes


def lane_flow_coverage(root: ET.Element) -> AuditIssue | None:
    """Ensure every flow node is listed in some lane flowNodeRef."""
    lanes = root.findall(".//bpmn:lane", NS)
    covered: Set[str] = set()
    for lane in lanes:
        for ref in lane.findall("bpmn:flowNodeRef", NS):
            if ref.text:
                covered.add(ref.text.strip())
    all_nodes = {get_id(n) for n in iter_flow_nodes(root) if get_id(n)}
    missing = sorted(all_nodes - covered)
    if missing:
        return AuditIssue(
            kind="lane_coverage",
            message=f"Flow nodes missing from lanes: {', '.join(missing)}",
        )
    return None


def di_parity(root: ET.Element) -> List[AuditIssue]:
    """Check every node has a shape and every sequenceFlow has an edge."""
    shapes = {s.get("bpmnElement") for s in root.findall(".//bpmndi:BPMNShape", NS)}
    edges = {e.get("bpmnElement") for e in root.findall(".//bpmndi:BPMNEdge", NS)}
    nodes = {get_id(n) for n in iter_flow_nodes(root) if get_id(n)}
    flows = {
        f.get("id")
        for f in root.findall(".//bpmn:sequenceFlow", NS)
        if f.get("id")
    }
    issues: List[AuditIssue] = []
    missing_shapes = sorted(nodes - shapes)
    if missing_shapes:
        issues.append(
            AuditIssue(
                kind="di_parity",
                message=f"Missing BPMNShape for nodes: {', '.join(missing_shapes)}",
            )
        )
    missing_edges = sorted(flows - edges)
    if missing_edges:
        issues.append(
            AuditIssue(
                kind="di_parity",
                message=f"Missing BPMNEdge for sequenceFlows: {', '.join(missing_edges)}",
            )
        )
    return issues


def detect_backward_flows(root: ET.Element) -> List[AuditIssue]:
    """Flag sequence flows whose DI waypoints move leftward (decreasing x)."""
    issues: List[AuditIssue] = []
    for edge in root.findall(".//bpmndi:BPMNEdge", NS):
        flow_id = edge.get("bpmnElement")
        points = edge.findall("di:waypoint", NS)
        xs = [float(p.get("x")) for p in points if p.get("x") is not None]
        for a, b in zip(xs, xs[1:]):
            if b < a:
                issues.append(
                    AuditIssue(
                        kind="backward_flow",
                        element_id=flow_id,
                        message=f"SequenceFlow {flow_id} has leftward waypoint {a}->{b}",
                    )
                )
                break
    return issues


def detect_unmatched_splits(root: ET.Element) -> List[AuditIssue]:
    """
    Find likely unmatched gateways: splits with >1 outgoing and no gateway of same type with >1 incoming.
    This is heuristic but catches common missing merges.
    """
    gateways = {
        g.get("id"): g for g in iter_flow_nodes(root) if is_gateway(g) and g.get("id")
    }
    incoming: Dict[str, int] = {gid: 0 for gid in gateways}
    outgoing: Dict[str, int] = {gid: 0 for gid in gateways}
    for flow in root.findall(".//bpmn:sequenceFlow", NS):
        src, tgt = flow.get("sourceRef"), flow.get("targetRef")
        if src in outgoing:
            outgoing[src] += 1
        if tgt in incoming:
            incoming[tgt] += 1
    merges_by_type: Dict[str, List[str]] = {}
    for gid, gw in gateways.items():
        if incoming.get(gid, 0) > 1:
            merges_by_type.setdefault(gw.tag, []).append(gid)
    issues: List[AuditIssue] = []
    for gid, gw in gateways.items():
        if outgoing.get(gid, 0) > 1:
            if not merges_by_type.get(gw.tag):
                issues.append(
                    AuditIssue(
                        kind="gateway_match",
                        element_id=gid,
                        message=f"Gateway {gid} splits but no matching {gw.tag.split('}')[-1]} merge found.",
                    )
                )
    return issues


def detect_complex_gateway_usage(root: ET.Element) -> List[AuditIssue]:
    """Ensure complex gateways are only used for >2-branch splits/merges."""
    gateways = {
        g.get("id"): g
        for g in iter_flow_nodes(root)
        if g.tag == _q("complexGateway") and g.get("id")
    }
    if not gateways:
        return []
    incoming: Dict[str, int] = {gid: 0 for gid in gateways}
    outgoing: Dict[str, int] = {gid: 0 for gid in gateways}
    for flow in root.findall(".//bpmn:sequenceFlow", NS):
        src, tgt = flow.get("sourceRef"), flow.get("targetRef")
        if src in outgoing:
            outgoing[src] += 1
        if tgt in incoming:
            incoming[tgt] += 1
    issues: List[AuditIssue] = []
    for gid in gateways:
        inc = incoming.get(gid, 0)
        out = outgoing.get(gid, 0)
        if out > 1 and out <= 2:
            issues.append(
                AuditIssue(
                    kind="complex-gateway-branches",
                    element_id=gid,
                    message="Complex gateway split must have >2 outgoing flows.",
                )
            )
        if out == 1 and inc <= 2:
            issues.append(
                AuditIssue(
                    kind="complex-gateway-branches",
                    element_id=gid,
                    message="Complex gateway merge must have >2 incoming flows.",
                )
            )
        if out == 0:
            issues.append(
                AuditIssue(
                    kind="complex-gateway-branches",
                    element_id=gid,
                    message="Complex gateway has no outgoing flows.",
                )
            )
    return issues


def audit(root: ET.Element) -> List[AuditIssue]:
    issues: List[AuditIssue] = []
    lc = lane_flow_coverage(root)
    if lc:
        issues.append(lc)
    issues.extend(di_parity(root))
    issues.extend(detect_backward_flows(root))
    issues.extend(detect_unmatched_splits(root))
    issues.extend(detect_complex_gateway_usage(root))
    return issues


def normalize_and_audit(path: Path) -> Tuple[List[NormalizationChange], List[AuditIssue]]:
    tree = load_tree(path)
    root = tree.getroot()
    changes = normalize_shape_sizes(root)
    issues = audit(root)
    return changes, issues


def apply_normalization(path: Path) -> List[NormalizationChange]:
    tree = load_tree(path)
    root = tree.getroot()
    changes = normalize_shape_sizes(root)
    if changes:
        save_tree(tree, path)
    return changes


def run_audit(path: Path) -> List[AuditIssue]:
    tree = load_tree(path)
    root = tree.getroot()
    return audit(root)
