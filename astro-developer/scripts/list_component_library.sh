#!/usr/bin/env bash
set -euo pipefail

root=".codex/skills/astro-developer/assets"

if [[ ! -d "$root/components" ]]; then
  echo "Missing assets/components" >&2
  exit 1
fi

echo "Astro components:"
ls "$root/components" | sort

echo ""
if [[ -d "$root/vue" ]]; then
  echo "Vue islands:"
  ls "$root/vue" | sort
else
  echo "No Vue islands folder found."
fi
