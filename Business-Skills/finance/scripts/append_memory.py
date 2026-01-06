#!/usr/bin/env python3
import argparse
from datetime import date
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Append a memory entry to memory-context.md.")
    parser.add_argument("--input", required=True, help="User-provided facts or constraints")
    parser.add_argument("--summary", required=True, help="Key context to reuse")
    parser.add_argument("--related-skills", default="", help="Comma-separated skills")
    parser.add_argument("--file", default="memory-context.md", help="Memory file path")
    args = parser.parse_args()

    related = ", ".join([s.strip() for s in args.related_skills.split(",") if s.strip()])
    lines = [
        f"- Date: {date.today().isoformat()}",
        f"- Input: {args.input}",
        f"- Summary: {args.summary}",
        f"- Related skills: {related}",
        "",
    ]
    entry = "\n".join(lines)

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"Memory file not found: {path}")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(entry)


if __name__ == "__main__":
    main()
