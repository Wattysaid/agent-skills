"""
BPMN diff and patch helpers.

These are intentionally minimal — they operate at whole-XML-string level and
produce a simple line-based diff you can show to users or use for logging.

For finer-grained patching, you could enhance this to operate over the BPMN AST.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List
import difflib


@dataclass
class Patch:
    """
    A simple wrapper for a unified diff, primarily for human inspection.
    """
    unified_diff: str


def diff_bpmn(old_xml: str, new_xml: str, from_label: str = "old", to_label: str = "new") -> Patch:
    """
    Compute a unified diff between two BPMN XML strings.
    """
    old_lines = old_xml.splitlines(keepends=True)
    new_lines = new_xml.splitlines(keepends=True)
    diff_lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=from_label,
            tofile=to_label,
        )
    )
    return Patch(unified_diff="".join(diff_lines))


def apply_bpmn_patch(xml: str, patch: Patch) -> str:
    """
    Placeholder for applying a patch.

    Implementing a robust patch apply is non-trivial. In many cases it's easier
    for the agent to re-generate an updated BPMN from context rather than apply
    a textual patch.

    For now, this function simply returns the original xml and exists as a hook
    if you decide to implement a real patch-apply mechanism.
    """
    # TODO: implement patch application if needed.
    return xml
