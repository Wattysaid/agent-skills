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

content_dir="src/content"
config_file="$content_dir/config.ts"
posts_dir="$content_dir/posts"

mkdir -p "$posts_dir"

if [[ -f "$config_file" && $force -ne 1 ]]; then
  echo "Content config already exists at $config_file. Use --force to overwrite." >&2
  exit 1
fi

cat <<'CONFIG' > "$config_file"
import { defineCollection, z } from "astro:content";

const posts = defineCollection({
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.date(),
  }),
});

export const collections = { posts };
CONFIG

echo "Initialized content collection at $config_file"
