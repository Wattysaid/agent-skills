#!/usr/bin/env python3
"""Wrapper for 05_conformance.py."""

import os
import subprocess
import sys


def main() -> int:
    target = os.path.join(os.path.dirname(__file__), "05_conformance.py")
    cmd = [sys.executable, target] + sys.argv[1:]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
