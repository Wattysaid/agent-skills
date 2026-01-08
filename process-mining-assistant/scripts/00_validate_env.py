#!/usr/bin/env python3
"""Validate environment dependencies for process mining."""

import importlib
import logging
import sys

from common import ensure_notebook, ensure_stage_dir, save_json, setup_logging, write_stage_manifest


def check_package(name: str) -> str:
    module = importlib.import_module(name)
    return getattr(module, "__version__", "unknown")


def main() -> None:
    setup_logging(0)
    import argparse
    parser = argparse.ArgumentParser(description="Validate environment dependencies.")
    parser.add_argument("--output", default="output", help="Output root directory.")
    parser.add_argument("--notebook-revision", default="R1.00", help="Notebook revision label.")
    args = parser.parse_args()
    stage_dir = ensure_stage_dir(args.output, "stage_00_validate_env")
    packages = ["pm4py", "pandas", "numpy", "matplotlib"]
    missing = []
    versions = {}
    for package in packages:
        try:
            versions[package] = check_package(package)
        except Exception:
            missing.append(package)
    if missing:
        message = f"Missing packages: {', '.join(missing)}"
        logging.error(message)
        with open(f"{stage_dir}/validate_env.log", "w", encoding="utf-8") as handle:
            handle.write(message + "\n")
        save_json({"status": "missing", "missing": missing}, f"{stage_dir}/validate_env.json")
        notebook_path = ensure_notebook(
            args.output,
            args.notebook_revision,
            "00_validate_env.ipynb",
            "Environment Validation",
            context_lines=[
                "",
                "This notebook captures the environment validation step.",
                f"- Status: missing ({', '.join(missing)})",
            ],
            code_lines=["# Review missing packages above."],
        )
        write_stage_manifest(
            stage_dir,
            {"output": args.output, "notebook_revision": args.notebook_revision},
            {"validate_env_json": f"{stage_dir}/validate_env.json", "validate_env_log": f"{stage_dir}/validate_env.log"},
            args.notebook_revision,
            notebook_path=notebook_path,
            notes="Dependency validation failed.",
        )
        sys.exit(1)
    for package, version in versions.items():
        logging.info("%s: %s", package, version)
    with open(f"{stage_dir}/validate_env.log", "w", encoding="utf-8") as handle:
        handle.write("Environment looks good.\n")
        for package, version in versions.items():
            handle.write(f"{package}: {version}\n")
    save_json({"status": "ok", "versions": versions}, f"{stage_dir}/validate_env.json")
    notebook_path = ensure_notebook(
        args.output,
        args.notebook_revision,
        "00_validate_env.ipynb",
        "Environment Validation",
        context_lines=[
            "",
            "This notebook captures the environment validation step.",
            "Versions:",
        ] + [f"- {pkg}: {ver}" for pkg, ver in versions.items()],
        code_lines=["# Environment looks good."],
    )
    write_stage_manifest(
        stage_dir,
        {"output": args.output, "notebook_revision": args.notebook_revision},
        {"validate_env_json": f"{stage_dir}/validate_env.json", "validate_env_log": f"{stage_dir}/validate_env.log"},
        args.notebook_revision,
        notebook_path=notebook_path,
    )
    print("Environment looks good.")


if __name__ == "__main__":
    main()
