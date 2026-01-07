"""
Pretty-printer for BPMN XML to make diffs and reviews easier.
"""

from __future__ import annotations
import xml.dom.minidom


def pretty_print_bpmn(xml_str: str, indent: int = 2) -> str:
    """
    Return a pretty-printed BPMN XML string.
    """
    dom = xml.dom.minidom.parseString(xml_str)
    return dom.toprettyxml(indent=" " * indent)
