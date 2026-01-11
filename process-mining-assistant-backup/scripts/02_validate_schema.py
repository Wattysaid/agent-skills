#!/usr/bin/env python3
"""Wrapper for validate_schema.py."""

import os
import subprocess
import sys


def main() -> int:
    target = os.path.join(os.path.dirname(__file__), "validate_schema.py")
    cmd = [sys.executable, target] + sys.argv[1:]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
