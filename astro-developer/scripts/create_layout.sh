#!/usr/bin/env bash
set -euo pipefail

force=0
if [[ ${1:-} == "--force" ]]; then
  force=1
fi

if [[ ! -f package.json ]]; then
  echo "Run this script from the root of an Astro project (where package.json exists)." >&2
  exit 1
fi

layout_dir="src/layouts"
layout_file="$layout_dir/Base.astro"

mkdir -p "$layout_dir"

if [[ -f "$layout_file" && $force -ne 1 ]]; then
  echo "Layout already exists at $layout_file. Use --force to overwrite." >&2
  exit 1
fi

cat <<'LAYOUT' > "$layout_file"
---
const { title = "Astro Site" } = Astro.props;
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
LAYOUT

echo "Created layout at $layout_file"
