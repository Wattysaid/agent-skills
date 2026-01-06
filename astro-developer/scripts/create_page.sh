#!/usr/bin/env bash
set -euo pipefail

if [[ ${1:-} == "" ]]; then
  echo "Usage: $0 <route-path> [--no-layout]" >&2
  echo "Example: $0 about" >&2
  echo "Example: $0 blog/index" >&2
  exit 1
fi

route_path="$1"
no_layout=0
if [[ ${2:-} == "--no-layout" ]]; then
  no_layout=1
fi

if [[ ! -f package.json ]]; then
  echo "Run this script from the root of an Astro project (where package.json exists)." >&2
  exit 1
fi

page_file="src/pages/${route_path}.astro"
page_dir="$(dirname "$page_file")"
mkdir -p "$page_dir"

if [[ -f "$page_file" ]]; then
  echo "Page already exists at $page_file" >&2
  exit 1
fi

if [[ $no_layout -eq 0 && -f "src/layouts/Base.astro" ]]; then
  cat <<'PAGE' > "$page_file"
---
import Base from "@/layouts/Base.astro";
const title = "Page Title";
---
<Base title={title}>
  <main>
    <h1>{title}</h1>
    <p>Replace this content.</p>
  </main>
</Base>
PAGE
else
  cat <<'PAGE' > "$page_file"
---
const title = "Page Title";
---
<main>
  <h1>{title}</h1>
  <p>Replace this content.</p>
</main>
PAGE
fi

echo "Created page at $page_file"
