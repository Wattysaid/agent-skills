"""
File and workspace utilities for the Camunda BPMN Modelling Agent.

These helpers intentionally stay simple and filesystem-agnostic so you can:
- Call them directly from Python
- Wrap them as tools in frameworks like LangChain / CrewAI / MCP
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import List


BASE_WORKSPACE = Path(os.environ.get("BPMN_WORKSPACE", ".")).resolve()


def _resolve(path: str) -> Path:
    """
    Resolve a relative path into the configured BASE_WORKSPACE to avoid escaping.
    """
    p = (BASE_WORKSPACE / path).resolve()
    if not str(p).startswith(str(BASE_WORKSPACE)):
        raise ValueError(f"Path {p} is outside of workspace {BASE_WORKSPACE}")
    return p


def read_text_file(path: str) -> str:
    """
    Read a UTF-8 text file from the workspace.

    :param path: Path relative to BASE_WORKSPACE.
    """
    full = _resolve(path)
    with open(full, "r", encoding="utf-8") as f:
        return f.read()


def write_text_file(path: str, content: str) -> None:
    """
    Write a UTF-8 text file to the workspace, creating parent directories if needed.

    :param path: Path relative to BASE_WORKSPACE.
    :param content: Text content to write.
    """
    full = _resolve(path)
    full.parent.mkdir(parents=True, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def list_files(path: str = ".", pattern: str | None = None) -> List[str]:
    """
    List files under a workspace path.

    :param path: Folder relative to BASE_WORKSPACE.
    :param pattern: Optional suffix pattern (e.g. '.bpmn') to filter files.
    """
    folder = _resolve(path)
    results: List[str] = []
    for root, _, files in os.walk(folder):
        for name in files:
            if pattern and not name.endswith(pattern):
                continue
            full = Path(root) / name
            rel = str(full.relative_to(BASE_WORKSPACE))
            results.append(rel)
    return sorted(results)


def create_folder(path: str) -> None:
    """
    Create a folder (and parents) under the workspace if it does not exist.
    """
    folder = _resolve(path)
    folder.mkdir(parents=True, exist_ok=True)


def move_file(from_path: str, to_path: str) -> None:
    """
    Move/rename a file within the workspace.
    """
    src = _resolve(from_path)
    dest = _resolve(to_path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dest)


def get_timestamp() -> str:
    """
    Return a simple timestamp string suitable for archive folder naming.
    Format: YYYYMMDD-HHMMSS
    """
    from datetime import datetime
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")
