#!/usr/bin/env python3
"""Wrapper for 07_org_mining.py."""

import os
import subprocess
import sys


def main() -> int:
    target = os.path.join(os.path.dirname(__file__), "07_org_mining.py")
    cmd = [sys.executable, target] + sys.argv[1:]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
