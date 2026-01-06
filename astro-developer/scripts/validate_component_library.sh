#!/usr/bin/env bash
set -euo pipefail

root=".codex/skills/astro-developer/assets"

if [[ ! -d "$root/components" ]]; then
  echo "Missing assets/components" >&2
  exit 1
fi

missing=0

for file in "$root"/components/*.astro; do
  base="$(basename "$file")"
  if [[ "$base" =~ [a-z] ]]; then
    echo "Non-PascalCase component: $base" >&2
    missing=1
  fi

done

required=(
  "Accordion.astro"
  "AccordionItem.astro"
  "AccordionTrigger.astro"
  "AccordionContent.astro"
  "Banner.astro"
  "BannerContent.astro"
  "BannerTitle.astro"
  "BannerDescription.astro"
  "SidebarMenu.astro"
  "SidebarMenuItem.astro"
  "SidebarMenuButton.astro"
)

for name in "${required[@]}"; do
  if [[ ! -f "$root/components/$name" ]]; then
    echo "Missing required component: $name" >&2
    missing=1
  fi

done

if [[ -d "$root/vue" ]]; then
  for file in "$root"/vue/*.vue; do
    if [[ ! -s "$file" ]]; then
      echo "Empty Vue island: $file" >&2
      missing=1
    fi
  done
fi

if [[ $missing -ne 0 ]]; then
  exit 1
fi

echo "Component library validation passed."
