#!/usr/bin/env bash
set -euo pipefail

if [[ ${1:-} == "" ]]; then
  echo "Usage: $0 <project-directory> [template]" >&2
  echo "Example: $0 my-site blog" >&2
  exit 1
fi

project_dir="$1"
template="${2:-}"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to scaffold an Astro project." >&2
  exit 1
fi

if [[ -n "$template" ]]; then
  npm create astro@latest "$project_dir" -- --template "$template"
else
  npm create astro@latest "$project_dir"
fi

cat <<'MSG'
Next steps:
  cd <project-directory>
  npm install
  npm run dev
MSG
