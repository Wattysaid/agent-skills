"""
Helpers to provide reusable DI coordinate templates referenced in `di_templates.md`.

These templates are intentionally simple so they can be composed with `apply_di_to_bpmn`.
Each template returns a dict with node bounds and edge waypoints you can merge into a DiSpec.
"""

from __future__ import annotations
from typing import Dict, Tuple, List
from .di_tools import Bounds, EdgeWaypoints, DiSpec


def xor_split_merge_template(x0: float = 100.0, y0: float = 100.0, h_gap: float = 140.0, v_gap: float = 80.0) -> DiSpec:
    """
    Create a basic XOR split/merge pattern with two branches.
    Node ids:
      - gw_split, task_top, task_bottom, gw_merge
    Flow ids:
      - f_split_top, f_split_bottom, f_top_merge, f_bottom_merge
    """
    nodes = {
        "gw_split": {"bounds": Bounds(x0, y0, 50, 50)},
        "task_top": {"bounds": Bounds(x0 + h_gap, y0 - v_gap, 120, 80)},
        "task_bottom": {"bounds": Bounds(x0 + h_gap, y0 + v_gap, 120, 80)},
        "gw_merge": {"bounds": Bounds(x0 + 2 * h_gap, y0, 50, 50)},
    }
    flows = {
        "f_split_top": {"edge": EdgeWaypoints([(x0 + 50, y0 + 25), (x0 + h_gap, y0 - v_gap + 40)])},
        "f_split_bottom": {"edge": EdgeWaypoints([(x0 + 50, y0 + 25), (x0 + h_gap, y0 + v_gap + 40)])},
        "f_top_merge": {"edge": EdgeWaypoints([(x0 + h_gap + 120, y0 - v_gap + 40), (x0 + 2 * h_gap, y0 + 25)])},
        "f_bottom_merge": {"edge": EdgeWaypoints([(x0 + h_gap + 120, y0 + v_gap + 40), (x0 + 2 * h_gap, y0 + 25)])},
    }
    return {"nodes": nodes, "flows": flows}


def parallel_split_merge_template(x0: float = 100.0, y0: float = 100.0, h_gap: float = 140.0, v_gap: float = 80.0) -> DiSpec:
    """
    Create a basic parallel split/merge pattern with two branches.
    Node ids:
      - gw_and_split, task_top, task_bottom, gw_and_merge
    Flow ids:
      - f_split_top, f_split_bottom, f_top_merge, f_bottom_merge
    """
    base = xor_split_merge_template(x0, y0, h_gap, v_gap)
    # Rename gateway ids to avoid XOR-specific naming
    nodes = {
        "gw_and_split": base["nodes"].pop("gw_split"),
        "task_top": base["nodes"]["task_top"],
        "task_bottom": base["nodes"]["task_bottom"],
        "gw_and_merge": base["nodes"].pop("gw_merge"),
    }
    flows = {
        "f_split_top": base["flows"]["f_split_top"],
        "f_split_bottom": base["flows"]["f_split_bottom"],
        "f_top_merge": base["flows"]["f_top_merge"],
        "f_bottom_merge": base["flows"]["f_bottom_merge"],
    }
    return {"nodes": nodes, "flows": flows}


def merge_specs(base: DiSpec, overlay: DiSpec) -> DiSpec:
    """
    Merge two DiSpecs, with overlay taking precedence on conflicts.
    """
    merged = {"nodes": {}, "flows": {}}
    merged["nodes"].update(base.get("nodes", {}))
    merged["flows"].update(base.get("flows", {}))
    merged["nodes"].update(overlay.get("nodes", {}))
    merged["flows"].update(overlay.get("flows", {}))
    return merged
