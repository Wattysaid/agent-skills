"""
Command-line utility to normalize and audit BPMN diagrams for consistency.

Domain-agnostic: works for NHS, trades, SaaS, etc.

Usage:
  python -m tools.bpmn_consistency_cli --fix Processes/*.bpmn
  python -m tools.bpmn_consistency_cli --audit Processes/*.bpmn
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import bpmn_consistency_tools as consistency


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize and audit BPMN diagrams.")
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="BPMN files or globs to process",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply size normalization in-place before audit",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Run audits (lane coverage, DI parity, backward flows, gateway pairing)",
    )
    args = parser.parse_args()

    if not args.fix and not args.audit:
        parser.error("Choose at least one of --fix or --audit.")

    exit_code = 0
    for path in args.files:
        matched = list(path.parent.glob(path.name)) if path.name.find("*") >= 0 else [path]
        for file in matched:
            if not file.exists():
                print(f"[skip] {file} does not exist", file=sys.stderr)
                continue
            if args.fix:
                changes = consistency.apply_normalization(file)
                if changes:
                    print(f"[fix] {file}: {len(changes)} shape(s) normalized")
            if args.audit:
                issues = consistency.run_audit(file)
                if issues:
                    exit_code = 1
                    for issue in issues:
                        loc = f" ({issue.element_id})" if issue.element_id else ""
                        print(f"[issue] {file}{loc}: {issue.kind} - {issue.message}")
                else:
                    print(f"[ok] {file}: no audit issues")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

