#!/usr/bin/env bash
set -euo pipefail

src_root=".codex/skills/astro-developer/assets"

dest_components="src/components/ui"
dest_vue="src/components/vue"

overwrite=0

if [[ ${1:-} == "--overwrite" ]]; then
  overwrite=1
fi

if [[ ! -d "$src_root/components" ]]; then
  echo "Missing assets/components in the skill." >&2
  exit 1
fi

mkdir -p "$dest_components" "$dest_vue"

copy_file() {
  local source="$1"
  local dest="$2"

  if [[ -f "$dest" && $overwrite -ne 1 ]]; then
    echo "Skip existing: $dest"
    return
  fi

  cp "$source" "$dest"
  echo "Copied: $dest"
}

for file in "$src_root"/components/*.astro; do
  base="$(basename "$file")"
  copy_file "$file" "$dest_components/$base"
done

if [[ -d "$src_root/vue" ]]; then
  for file in "$src_root"/vue/*.vue; do
    base="$(basename "$file")"
    copy_file "$file" "$dest_vue/$base"
  done
fi

echo "Component library copy complete."
