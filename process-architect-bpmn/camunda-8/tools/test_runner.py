"""
CLI test runner to validate BPMN files quickly.

Usage:
  python3 -m tools.test_runner path/to/file.bpmn
Exits non-zero when blocking issues are found.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from . import bpmn_schema_tools, bpmn_lint_tools, validation_tools


def run(path: Path) -> int:
    xml = path.read_text(encoding="utf-8")

    schema = bpmn_schema_tools.validate_bpmn_schema(xml)
    lint_results = bpmn_lint_tools.run_bpmn_lint(xml)
    forbidden = bpmn_lint_tools.check_forbidden_patterns(xml)
    checklist = validation_tools.run_validation_checklist(xml)

    errors = []
    warnings = []

    if not schema["valid"]:
        errors.extend(schema["errors"])

    for r in lint_results:
        (errors if r.severity == "error" else warnings).append(
            {"rule": r.rule_id, "message": r.message, "node": r.node_id}
        )
    for h in forbidden:
        errors.append({"rule": h.pattern_id, "message": h.message, "node": h.node_id})

    # Checklist: treat "fail" as error, "warn" as warning
    for item in checklist:
        if item["status"] == "fail":
            errors.append({"rule": item["id"], "message": item["message"]})
        elif item["status"] == "warn":
            warnings.append({"rule": item["id"], "message": item["message"]})

    if errors:
        print("❌ BPMN issues found:")
        for e in errors:
            print(f" - [{e.get('rule')}] {e.get('message')} (node={e.get('node')})")
    else:
        print("✅ No blocking errors.")

    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f" - [{w.get('rule')}] {w.get('message')} (node={w.get('node')})")

    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description="Run BPMN lint/schema/forbidden checks.")
    parser.add_argument("file", type=Path, help="Path to BPMN file")
    args = parser.parse_args()
    if not args.file.exists():
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    sys.exit(run(args.file))


if __name__ == "__main__":
    main()
