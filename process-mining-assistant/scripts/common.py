#!/usr/bin/env python3
"""Shared utilities for the process mining CLI workflow."""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional, Tuple


def setup_logging(verbosity: int) -> None:
    """Configure logging output."""
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    """Load configuration from JSON or YAML if available."""
    if not config_path:
        return {}
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    ext = os.path.splitext(config_path)[1].lower()
    with open(config_path, "r", encoding="utf-8") as handle:
        if ext in (".yaml", ".yml"):
            try:
                import yaml  # type: ignore
            except ImportError as exc:
                raise RuntimeError("PyYAML is required for YAML configs. Install pyyaml.") from exc
            return yaml.safe_load(handle) or {}
        return json.load(handle)


def merge_config(args: argparse.Namespace, config: Dict[str, Any]) -> Dict[str, Any]:
    """Merge CLI args over config, returning a flat dictionary."""
    merged = dict(config)
    for key, value in vars(args).items():
        if value is not None:
            merged[key] = value
    return merged


def ensure_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_json(payload: Dict[str, Any], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def write_manifest(output_dir: str, params: Dict[str, Any], artifacts: Dict[str, str]) -> None:
    """Write a simple manifest describing run parameters and artifacts."""
    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "parameters": params,
        "artifacts": artifacts,
    }
    save_json(manifest, os.path.join(output_dir, "manifest.json"))


def require_file(path: str) -> None:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Input file not found: {path}")


def parse_list(value: Optional[object]) -> Optional[list]:
    if value is None:
        return None
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        items = [item.strip() for item in value.split(",")]
        return [item for item in items if item]
    return [value]


def exit_with_error(message: str, code: int = 1) -> None:
    logging.error(message)
    sys.exit(code)


def validate_csv_columns(df, required: Tuple[str, ...]) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
