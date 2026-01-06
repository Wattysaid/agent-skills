#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f package.json ]]; then
  echo "Run this script from the root of an Astro project (where package.json exists)." >&2
  exit 1
fi

npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

cat <<'MSG'
Tailwind installed.
Next steps:
  - Update tailwind.config.js content paths for Astro.
  - Import your Tailwind CSS entry in a layout or global stylesheet.
MSG
