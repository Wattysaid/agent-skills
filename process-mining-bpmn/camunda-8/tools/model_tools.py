"""
BPMN ↔ ProcessModel bridge.

This file defines a *very lightweight* ProcessModel representation that reflects
the reasoning steps from `reasoning_guide.md`. It is not a full BPMN semantic
model; it is meant as a convenience abstraction you can evolve over time.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import json
from .di_tools import NodeSpec, FlowSpec, generate_di_layout, apply_di_to_bpmn


@dataclass
class Actor:
    id: str
    name: str


@dataclass
class Step:
    id: str
    actor_id: str
    kind: str  # e.g. "startEvent", "endEvent", "task", "gateway"
    name: str
    metadata: Dict[str, Any]


@dataclass
class Flow:
    id: str
    source_id: str
    target_id: str
    condition: str | None = None


@dataclass
class ProcessModel:
    """
    High-level logical model derived from a BPMN diagram or reasoning steps.
    """
    id: str
    name: str
    actors: List[Actor]
    steps: List[Step]
    flows: List[Flow]


def process_model_to_json(model: ProcessModel, indent: int = 2) -> str:
    """
    Serialize a ProcessModel into pretty JSON.
    """
    return json.dumps(asdict(model), indent=indent)


def process_model_from_json(data: str | Dict[str, Any]) -> ProcessModel:
    """
    Deserialize a ProcessModel from JSON string or dict.
    """
    if isinstance(data, str):
        obj = json.loads(data)
    else:
        obj = data

    actors = [Actor(**a) for a in obj.get("actors", [])]
    steps = [Step(**s) for s in obj.get("steps", [])]
    flows = [Flow(**f) for f in obj.get("flows", [])]
    return ProcessModel(
        id=obj["id"],
        name=obj["name"],
        actors=actors,
        steps=steps,
        flows=flows,
    )


def bpmn_to_json(xml: str) -> str:
    """
    Minimal BPMN → ProcessModel conversion.

    Extracts:
      - process id/name
      - actors from lanes (fallback: participant, otherwise a single UNSPECIFIED)
      - tasks/events/gateways with names
      - sequence flows with optional name as condition hint
    """
    import xml.etree.ElementTree as ET

    NS = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"
    root = ET.fromstring(xml)
    proc = root.find(f".//{NS}process")
    if proc is None:
        model = ProcessModel(id="unspecified", name="UNSPECIFIED", actors=[], steps=[], flows=[])
        return process_model_to_json(model)

    process_id = proc.get("id", "process_1")
    process_name = proc.get("name", process_id)

    # Actors
    actors: List[Actor] = []
    lane_set = proc.find(f"{NS}laneSet")
    if lane_set is not None:
        for lane in lane_set.findall(f"{NS}lane"):
            lid = lane.get("id") or f"lane_{len(actors)+1}"
            actors.append(Actor(id=lid, name=lane.get("name", lid)))
    else:
        # fallback to participant name
        participant = root.find(f".//{NS}participant")
        if participant is not None:
            pid = participant.get("id", "actor_1")
            actors.append(Actor(id=pid, name=participant.get("name", pid)))
        else:
            actors.append(Actor(id="actor_1", name="UNSPECIFIED"))

    # Steps
    node_tags = {
        f"{NS}startEvent": "startEvent",
        f"{NS}endEvent": "endEvent",
        f"{NS}task": "task",
        f"{NS}userTask": "userTask",
        f"{NS}serviceTask": "serviceTask",
        f"{NS}sendTask": "sendTask",
        f"{NS}receiveTask": "receiveTask",
        f"{NS}manualTask": "manualTask",
        f"{NS}exclusiveGateway": "exclusiveGateway",
        f"{NS}parallelGateway": "parallelGateway",
        f"{NS}inclusiveGateway": "inclusiveGateway",
        f"{NS}eventBasedGateway": "eventBasedGateway",
        f"{NS}intermediateCatchEvent": "intermediateCatchEvent",
        f"{NS}intermediateThrowEvent": "intermediateThrowEvent",
        f"{NS}boundaryEvent": "boundaryEvent",
        f"{NS}callActivity": "callActivity",
        f"{NS}subProcess": "subProcess",
    }

    lane_membership: dict[str, str] = {}
    if lane_set is not None:
        for lane in lane_set.findall(f"{NS}lane"):
            lid = lane.get("id")
            for ref in lane.findall(f"{NS}flowNodeRef"):
                if lid and ref.text:
                    lane_membership[ref.text] = lid

    steps: List[Step] = []
    for node in proc.iter():
        if node.tag not in node_tags:
            continue
        nid = node.get("id") or f"node_{len(steps)+1}"
        steps.append(
            Step(
                id=nid,
                actor_id=lane_membership.get(nid, actors[0].id),
                kind=node_tags[node.tag],
                name=node.get("name", nid),
                metadata={},
            )
        )

    flows: List[Flow] = []
    for sf in proc.findall(f"{NS}sequenceFlow"):
        fid = sf.get("id") or f"flow_{len(flows)+1}"
        flows.append(
            Flow(
                id=fid,
                source_id=sf.get("sourceRef", ""),
                target_id=sf.get("targetRef", ""),
                condition=sf.get("name"),
            )
        )

    model = ProcessModel(
        id=process_id,
        name=process_name,
        actors=actors,
        steps=steps,
        flows=flows,
    )
    return process_model_to_json(model)


def json_to_bpmn(model_json: str) -> str:
    """
    Minimal ProcessModel → BPMN conversion.

    Builds:
      - <definitions> with required namespaces
      - collaboration + participant referencing the process
      - <process> with laneSet and flow nodes
      - sequence flows using Flow list
    Adds a simple DI layout so the result is contract-complete.
    """
    model = process_model_from_json(model_json)
    import xml.etree.ElementTree as ET

    NSMAP = {
        "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
        "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
        "di": "http://www.omg.org/spec/DD/20100524/DI",
        "dc": "http://www.omg.org/spec/DD/20100524/DC",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "zeebe": "http://camunda.org/schema/zeebe/1.0",
    }
    for prefix, uri in NSMAP.items():
        ET.register_namespace(prefix, uri)

    if not model.actors:
        model.actors = [Actor(id="Lane_Main", name="Main Lane")]

    defs = ET.Element(
        f"{{{NSMAP['bpmn']}}}definitions",
        attrib={"id": f"Definitions_{model.id}", "targetNamespace": "http://example.com/bpmn"},
    )
    proc = ET.SubElement(
        defs,
        f"{{{NSMAP['bpmn']}}}process",
        attrib={"id": model.id, "name": model.name, "isExecutable": "false"},
    )

    lane_set = ET.SubElement(proc, f"{{{NSMAP['bpmn']}}}laneSet", attrib={"id": f"LaneSet_{model.id}"})
    for actor in model.actors:
        ET.SubElement(lane_set, f"{{{NSMAP['bpmn']}}}lane", attrib={"id": actor.id, "name": actor.name})

    collab = ET.SubElement(defs, f"{{{NSMAP['bpmn']}}}collaboration", attrib={"id": f"Collab_{model.id}"})
    ET.SubElement(
        collab,
        f"{{{NSMAP['bpmn']}}}participant",
        attrib={"id": f"Participant_{model.id}", "name": model.name, "processRef": model.id},
    )

    tag_map = {
        "startEvent": "startEvent",
        "endEvent": "endEvent",
        "task": "task",
        "userTask": "userTask",
        "serviceTask": "serviceTask",
        "sendTask": "sendTask",
        "receiveTask": "receiveTask",
        "manualTask": "manualTask",
        "exclusiveGateway": "exclusiveGateway",
        "parallelGateway": "parallelGateway",
        "inclusiveGateway": "inclusiveGateway",
        "eventBasedGateway": "eventBasedGateway",
        "intermediateCatchEvent": "intermediateCatchEvent",
        "intermediateThrowEvent": "intermediateThrowEvent",
        "boundaryEvent": "boundaryEvent",
        "callActivity": "callActivity",
        "subProcess": "subProcess",
    }

    for step in model.steps:
        tag = tag_map.get(step.kind, "task")
        ET.SubElement(proc, f"{{{NSMAP['bpmn']}}}{tag}", attrib={"id": step.id, "name": step.name})

    for flow in model.flows:
        attrib = {
            "id": flow.id,
            "sourceRef": flow.source_id,
            "targetRef": flow.target_id,
        }
        if flow.condition:
            attrib["name"] = flow.condition
        ET.SubElement(proc, f"{{{NSMAP['bpmn']}}}sequenceFlow", attrib=attrib)

    # Populate lane membership
    lanes_by_id = {lane.get("id"): lane for lane in lane_set.findall(f"{{{NSMAP['bpmn']}}}lane")}
    for step in model.steps:
        lane = lanes_by_id.get(step.actor_id) or lanes_by_id.get(model.actors[0].id)
        if lane is not None:
            ET.SubElement(lane, f"{{{NSMAP['bpmn']}}}flowNodeRef").text = step.id

    diagram = ET.SubElement(defs, f"{{{NSMAP['bpmndi']}}}BPMNDiagram", attrib={"id": f"Diagram_{model.id}"})
    ET.SubElement(
        diagram,
        f"{{{NSMAP['bpmndi']}}}BPMNPlane",
        attrib={"id": f"Plane_{model.id}", "bpmnElement": f"Collab_{model.id}"},
    )

    # Build DI layout using simple left-to-right placement
    valid_lane_ids = set(lanes_by_id.keys())
    node_specs = [
        NodeSpec(id=step.id, lane_id=step.actor_id if step.actor_id in valid_lane_ids else model.actors[0].id, type=step.kind, order=index)
        for index, step in enumerate(model.steps)
    ]
    flow_specs = [FlowSpec(id=flow.id, source_id=flow.source_id, target_id=flow.target_id) for flow in model.flows]
    di = generate_di_layout(node_specs, flow_specs)
    xml = ET.tostring(defs, encoding="utf-8", xml_declaration=True).decode("utf-8")
    return apply_di_to_bpmn(xml, di)
