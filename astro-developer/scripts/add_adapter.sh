#!/usr/bin/env bash
set -euo pipefail

if [[ ${1:-} == "" ]]; then
  echo "Usage: $0 <adapter>" >&2
  echo "Example: $0 netlify" >&2
  exit 1
fi

adapter="$1"

if [[ ! -f package.json ]]; then
  echo "Run this script from the root of an Astro project (where package.json exists)." >&2
  exit 1
fi

npm run astro add "$adapter"
