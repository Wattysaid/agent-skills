"""
Helpers for loading examples and domain templates.

You can place BPMN examples under an `examples/` folder in your workspace and
reference them by name. This module just provides a small convenience wrapper.
"""

from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from .file_tools import BASE_WORKSPACE, read_text_file, list_files


def load_example(name: str) -> dict:
    """
    Load a named example.

    The function tries the following paths (relative to BASE_WORKSPACE):
      - examples/{name}.bpmn
      - examples/{name}.xml

    :returns: dict with keys:
      - name
      - path
      - xml (file content as string)
    :raises FileNotFoundError: if no example file is found.
    """
    candidates = [
        Path("examples") / f"{name}.bpmn",
        Path("examples") / f"{name}.xml",
    ]
    for candidate in candidates:
        full = BASE_WORKSPACE / candidate
        if full.exists():
            xml = read_text_file(str(candidate))
            return {"name": name, "path": str(candidate), "xml": xml}

    raise FileNotFoundError(f"No example found for {name!r} under examples/")


def list_examples() -> List[str]:
    """
    List available examples under the workspace `examples/` folder.
    """
    files = list_files("examples")
    return [Path(f).stem for f in files if Path(f).suffix in {".bpmn", ".xml"}]
