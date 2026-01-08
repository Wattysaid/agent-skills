#!/usr/bin/env python3
"""Validate environment dependencies for process mining."""

import importlib
import logging
import sys

from common import setup_logging


def check_package(name: str) -> str:
    module = importlib.import_module(name)
    return getattr(module, "__version__", "unknown")


def main() -> None:
    setup_logging(0)
    packages = ["pm4py", "pandas", "numpy", "matplotlib"]
    missing = []
    versions = {}
    for package in packages:
        try:
            versions[package] = check_package(package)
        except Exception:
            missing.append(package)
    if missing:
        logging.error("Missing packages: %s", ", ".join(missing))
        sys.exit(1)
    for package, version in versions.items():
        logging.info("%s: %s", package, version)
    print("Environment looks good.")


if __name__ == "__main__":
    main()
