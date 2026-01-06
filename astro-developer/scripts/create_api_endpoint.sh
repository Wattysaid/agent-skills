#!/usr/bin/env bash
set -euo pipefail

if [[ ${1:-} == "" ]]; then
  echo "Usage: $0 <endpoint-name>" >&2
  echo "Example: $0 subscribe" >&2
  exit 1
fi

endpoint_name="$1"

if [[ ! -f package.json ]]; then
  echo "Run this script from the root of an Astro project (where package.json exists)." >&2
  exit 1
fi

api_dir="src/pages/api"
endpoint_file="$api_dir/${endpoint_name}.ts"

mkdir -p "$api_dir"

if [[ -f "$endpoint_file" ]]; then
  echo "Endpoint already exists at $endpoint_file" >&2
  exit 1
fi

cat <<'ENDPOINT' > "$endpoint_file"
import type { APIRoute } from "astro";

export const GET: APIRoute = async () => {
  return new Response(JSON.stringify({ status: "ok" }), {
    headers: { "Content-Type": "application/json" },
  });
};

export const POST: APIRoute = async ({ request }) => {
  const data = await request.json();
  return new Response(JSON.stringify({ status: "ok", data }), {
    headers: { "Content-Type": "application/json" },
  });
};
ENDPOINT

echo "Created endpoint at $endpoint_file"
