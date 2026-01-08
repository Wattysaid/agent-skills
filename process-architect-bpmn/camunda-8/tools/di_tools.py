"""
DI (Diagram Interchange) helpers aligned to the modelling contract.

These helpers stay intentionally simple but respect the sizing and lane/pool
expectations from `04_di_layout_rules.md`:
- Tasks 120x80, gateways 50x50, events 36x36
- Left-to-right flow with ~150px spacing
- Lanes sized generously so child nodes sit inside lane bounds
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET


@dataclass
class NodeSpec:
    id: str
    lane_id: str | None
    type: str  # e.g. "startEvent", "task", "exclusiveGateway"
    order: int  # left-to-right order within a lane


@dataclass
class FlowSpec:
    id: str
    source_id: str
    target_id: str


@dataclass
class Bounds:
    x: float
    y: float
    width: float
    height: float


@dataclass
class EdgeWaypoints:
    waypoints: List[Tuple[float, float]]


# nodes/flows/lanes keyed by id
DiSpec = Dict[str, Dict[str, object]]


def generate_di_layout(nodes: List[NodeSpec], flows: List[FlowSpec]) -> DiSpec:
    """
    Generate a left-to-right layout for nodes with simple orthogonal edges.

    - Nodes are placed by lane_id rows with ~150px spacing.
    - Lane bounds are sized to cover contained nodes.
    - Uses contract sizes for tasks/gateways/events.
    """
    lane_y_offset: Dict[str | None, float] = {}
    lane_bounds: Dict[str | None, Bounds] = {}
    current_lane_index = 0
    lane_height = 220.0
    x_step = 150.0
    base_x = 120.0

    max_order_by_lane: Dict[str | None, int] = {}
    for node in nodes:
        max_order_by_lane[node.lane_id] = max(max_order_by_lane.get(node.lane_id, 0), node.order)

    for node in nodes:
        if node.lane_id not in lane_y_offset:
            lane_y_offset[node.lane_id] = 180.0 + current_lane_index * lane_height
            current_lane_index += 1

    for lane_id, y_center in lane_y_offset.items():
        max_order = max_order_by_lane.get(lane_id, 0)
        width = base_x + (max_order + 2) * x_step
        lane_bounds[lane_id] = Bounds(
            x=base_x - 80.0,
            y=y_center - lane_height / 2,
            width=width,
            height=lane_height,
        )

    node_bounds: Dict[str, Bounds] = {}
    for node in nodes:
        y_center = lane_y_offset[node.lane_id]
        x_center = base_x + node.order * x_step
        if node.type.endswith("Event"):
            width = height = 36.0
        elif "Gateway" in node.type:
            width = height = 50.0
        else:
            width = 120.0
            height = 80.0
        node_bounds[node.id] = Bounds(
            x=x_center - width / 2,
            y=y_center - height / 2,
            width=width,
            height=height,
        )

    flow_edges: Dict[str, EdgeWaypoints] = {}
    for flow in flows:
        src = node_bounds.get(flow.source_id)
        tgt = node_bounds.get(flow.target_id)
        if not src or not tgt:
            continue
        src_centre = (src.x + src.width, src.y + src.height / 2)
        tgt_centre = (tgt.x, tgt.y + tgt.height / 2)
        if src.y == tgt.y:
            flow_edges[flow.id] = EdgeWaypoints(waypoints=[src_centre, tgt_centre])
        else:
            mid_x = (src.x + src.width + tgt.x) / 2
            flow_edges[flow.id] = EdgeWaypoints(
                waypoints=[src_centre, (mid_x, src_centre[1]), (mid_x, tgt_centre[1]), tgt_centre]
            )

    return {
        "nodes": {k: {"bounds": v} for k, v in node_bounds.items()},
        "flows": {k: {"edge": v} for k, v in flow_edges.items()},
        "lanes": {k: {"bounds": v} for k, v in lane_bounds.items()},
    }


def apply_di_to_bpmn(xml: str, di: DiSpec) -> str:
    """
    Attach or update BPMN-DI elements in a BPMN XML string using a DiSpec.

    - Creates BPMNShape for each node/lane if missing
    - Creates BPMNEdge for each flow if missing
    - Keeps BPMNPlane bound to collaboration id when present, else process id
    """
    ET.register_namespace("bpmn", "http://www.omg.org/spec/BPMN/20100524/MODEL")
    ET.register_namespace("bpmndi", "http://www.omg.org/spec/BPMN/20100524/DI")
    ET.register_namespace("dc", "http://www.omg.org/spec/DD/20100524/DC")
    ET.register_namespace("di", "http://www.omg.org/spec/DD/20100524/DI")

    root = ET.fromstring(xml)
    ns = {
        "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
        "dc": "http://www.omg.org/spec/DD/20100524/DC",
        "di": "http://www.omg.org/spec/DD/20100524/DI",
    }

    diagram = root.find("bpmndi:BPMNDiagram", ns)
    if diagram is None:
        diagram = ET.SubElement(root, f"{{{ns['bpmndi']}}}BPMNDiagram", attrib={"id": "Diagram_1"})
    plane = diagram.find("bpmndi:BPMNPlane", ns)
    if plane is None:
        plane = ET.SubElement(diagram, f"{{{ns['bpmndi']}}}BPMNPlane", attrib={"id": "Plane_1", "bpmnElement": ""})
    if not plane.get("bpmnElement"):
        collab = root.find("bpmn:collaboration", ns)
        proc = root.find("bpmn:process", ns)
        target = collab.get("id") if collab is not None and collab.get("id") else (proc.get("id") if proc is not None else "")
        if target:
            plane.set("bpmnElement", target)

    def _find_shape_for(element_id: str):
        for shape in plane.findall("bpmndi:BPMNShape", ns):
            if shape.get("bpmnElement") == element_id:
                return shape
        return None

    def _find_edge_for(element_id: str):
        for edge in plane.findall("bpmndi:BPMNEdge", ns):
            if edge.get("bpmnElement") == element_id:
                return edge
        return None

    for lane_id, info in di.get("lanes", {}).items():
        bounds = info["bounds"]
        shape = _find_shape_for(lane_id)
        if shape is None:
            shape = ET.SubElement(
                plane,
                f"{{{ns['bpmndi']}}}BPMNShape",
                attrib={"id": f"{lane_id}_di", "bpmnElement": lane_id},
            )
        for child in list(shape):
            if child.tag == f"{{{ns['dc']}}}Bounds":
                shape.remove(child)
        ET.SubElement(
            shape,
            f"{{{ns['dc']}}}Bounds",
            attrib={
                "x": str(bounds.x),
                "y": str(bounds.y),
                "width": str(bounds.width),
                "height": str(bounds.height),
            },
        )

    for node_id, info in di.get("nodes", {}).items():
        bounds = info["bounds"]
        shape = _find_shape_for(node_id)
        if shape is None:
            shape = ET.SubElement(
                plane,
                f"{{{ns['bpmndi']}}}BPMNShape",
                attrib={"id": f"{node_id}_di", "bpmnElement": node_id},
            )
        for child in list(shape):
            if child.tag == f"{{{ns['dc']}}}Bounds":
                shape.remove(child)
        ET.SubElement(
            shape,
            f"{{{ns['dc']}}}Bounds",
            attrib={
                "x": str(bounds.x),
                "y": str(bounds.y),
                "width": str(bounds.width),
                "height": str(bounds.height),
            },
        )

    for flow_id, info in di.get("flows", {}).items():
        edge_spec = info["edge"]
        edge = _find_edge_for(flow_id)
        if edge is None:
            edge = ET.SubElement(
                plane,
                f"{{{ns['bpmndi']}}}BPMNEdge",
                attrib={"id": f"{flow_id}_di", "bpmnElement": flow_id},
            )
        for child in list(edge):
            if child.tag == f"{{{ns['di']}}}waypoint":
                edge.remove(child)
        for x, y in edge_spec.waypoints:
            ET.SubElement(
                edge,
                f"{{{ns['di']}}}waypoint",
                attrib={"x": str(x), "y": str(y)},
            )

    return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")
