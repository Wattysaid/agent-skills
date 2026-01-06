#!/usr/bin/env bash
set -euo pipefail

if [[ ${1:-} == "" ]]; then
  echo "Usage: $0 <base-route>" >&2
  echo "Example: $0 blog" >&2
  exit 1
fi

base_route="$1"

if [[ ! -f package.json ]]; then
  echo "Run this script from the root of an Astro project (where package.json exists)." >&2
  exit 1
fi

page_dir="src/pages/${base_route}"
page_file="${page_dir}/[slug].astro"
mkdir -p "$page_dir"

if [[ -f "$page_file" ]]; then
  echo "Dynamic route already exists at $page_file" >&2
  exit 1
fi

cat <<'PAGE' > "$page_file"
---
import Base from "@/layouts/Base.astro";
const { slug } = Astro.params;
---
<Base title={slug}>
  <article>
    <h1>{slug}</h1>
    <p>Load data for this slug and render it here.</p>
  </article>
</Base>
PAGE

echo "Created dynamic route at $page_file"
