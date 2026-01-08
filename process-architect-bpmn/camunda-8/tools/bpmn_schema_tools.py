"""
BPMN schema-related helpers.

These are deliberately light-weight skeletons. They provide:
- XML parse/serialize helpers
- A *stub* schema validation function you can connect to a real validator
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List
import xml.etree.ElementTree as ET


@dataclass
class ValidationError:
    path: str
    code: str
    message: str


class BpmnAst:
    """
    Minimal BPMN AST wrapper around an ElementTree.

    You can extend this to provide richer helpers, or switch to `bpmn-moddle`
    or a dedicated BPMN library in another language.
    """

    def __init__(self, tree: ET.ElementTree):
        self.tree = tree

    @property
    def root(self) -> ET.Element:
        return self.tree.getroot()


def parse_bpmn(xml: str) -> BpmnAst:
    """
    Parse BPMN XML into a minimal AST wrapper.

    :param xml: BPMN 2.0 XML string
    """
    tree = ET.ElementTree(ET.fromstring(xml))
    return BpmnAst(tree)


def serialize_bpmn(ast: BpmnAst) -> str:
    """
    Serialize a BPMN AST back into an XML string.

    Note: uses compact ElementTree serialisation by default.
    You may want to pretty-print in your own tooling.
    """
    return ET.tostring(ast.root, encoding="utf-8", xml_declaration=True).decode("utf-8")


def validate_bpmn_schema(xml: str) -> dict:
    """
    Lightweight structural validation.

    What it checks:
      - Root element is <definitions> in the BPMN namespace
      - At least one <process>
      - Processes have unique ids
      - Sequence flows reference existing nodes
      - Participant references process
      - LaneSet exists and covers all nodes
      - BPMNDiagram/BPMNPlane present
    This is intentionally conservative but more useful than a stub. Swap this
    with a JSON-schema or XSD-backed validator when you are ready.
    """
    errors: List[ValidationError] = []
    try:
        ast = parse_bpmn(xml)
        tag = ast.root.tag
        if "definitions" not in tag:
            errors.append(
                ValidationError(
                    path="/",
                    code="ROOT_NOT_DEFINITIONS",
                    message=f"Expected <definitions> root, got {tag!r}",
                )
            )
        process_elems = ast.root.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}process")
        if not process_elems:
            errors.append(
                ValidationError(
                    path="/definitions",
                    code="PROCESS_MISSING",
                    message="No <process> element found.",
                )
            )
        else:
            seen_ids: set[str] = set()
            for proc in process_elems:
                pid = proc.get("id")
                if not pid:
                    errors.append(
                        ValidationError(
                            path="/definitions/process",
                            code="PROCESS_ID_MISSING",
                            message="Process element missing required id.",
                        )
                    )
                elif pid in seen_ids:
                    errors.append(
                        ValidationError(
                            path=f"/definitions/process[@id='{pid}']",
                            code="PROCESS_ID_DUPLICATE",
                            message=f"Duplicate process id {pid!r}.",
                        )
                    )
                seen_ids.add(pid)

            # Sequence flow references
            nodes = proc.findall(".//*")
            node_ids = {n.get("id") for n in nodes if n.get("id")}
            for flow in proc.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"):
                fid = flow.get("id", "")
                src = flow.get("sourceRef")
                tgt = flow.get("targetRef")
                if src and src not in node_ids:
                    errors.append(
                        ValidationError(
                            path=f"/definitions/process/sequenceFlow[@id='{fid}']",
                            code="SEQUENCEFLOW_SOURCE_MISSING",
                            message=f"SequenceFlow sourceRef {src!r} not found.",
                        )
                    )
                if tgt and tgt not in node_ids:
                    errors.append(
                        ValidationError(
                            path=f"/definitions/process/sequenceFlow[@id='{fid}']",
                            code="SEQUENCEFLOW_TARGET_MISSING",
                            message=f"SequenceFlow targetRef {tgt!r} not found.",
                        )
                    )

            # Participant referencing process
            participant = ast.root.find(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}participant")
            if participant is None or participant.get("processRef") != pid:
                errors.append(
                    ValidationError(
                        path="/definitions/collaboration/participant",
                        code="PARTICIPANT_MISSING",
                        message="Participant referencing main process is required.",
                    )
                )

            # Lane coverage
            lane_set = proc.find("{http://www.omg.org/spec/BPMN/20100524/MODEL}laneSet")
            if lane_set is None:
                errors.append(
                    ValidationError(
                        path="/definitions/process/laneSet",
                        code="LANESET_MISSING",
                        message="LaneSet with at least one lane is required.",
                    )
                )
            else:
                lane_refs = {ref.text for ref in lane_set.findall(".//{http://www.omg.org/spec/BPMN/20100524/MODEL}flowNodeRef") if ref.text}
                missing = sorted(n for n in node_ids if n not in lane_refs)
                if missing:
                    errors.append(
                        ValidationError(
                            path="/definitions/process/laneSet",
                            code="LANESET_COVERAGE",
                            message=f"Flow nodes missing from lanes: {', '.join(missing)}",
                        )
                    )

        # DI presence
        diagram = ast.root.find(".//{http://www.omg.org/spec/BPMN/20100524/DI}BPMNDiagram")
        plane = diagram.find("{http://www.omg.org/spec/BPMN/20100524/DI}BPMNPlane") if diagram is not None else None
        if diagram is None or plane is None:
            errors.append(
                ValidationError(
                    path="/definitions",
                    code="DI_MISSING",
                    message="BPMNDiagram/BPMNPlane required for DI.",
                )
            )
    except Exception as exc:  # noqa: BLE001
        errors.append(
            ValidationError(
                path="/",
                code="XML_PARSE_ERROR",
                message=str(exc),
            )
        )

    return {
        "valid": len(errors) == 0,
        "errors": [e.__dict__ for e in errors],
    }
