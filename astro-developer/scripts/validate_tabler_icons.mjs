#!/usr/bin/env node
import fs from "fs";
import path from "path";

const ICON_JSON_CANDIDATES = [
  "node_modules/@iconify-json/tabler/icons.json",
  "node_modules/@tabler/icons/icons.json",
  "node_modules/@tabler/icons-react/icons.json",
  "node_modules/@tabler/icons-webfont/icons.json",
];

const DEFAULT_ALL_OUTPUT =
  ".codex/skills/astro-developer/references/tabler-icons.txt";
const DEFAULT_CURATED_OUTPUT =
  ".codex/skills/astro-developer/references/tabler-icons-curated.txt";
const DEFAULT_TABLER_ICONS_DIR = "tabler-icons/icons";

function parseArgs(argv) {
  const args = {
    input: null,
    allOutput: DEFAULT_ALL_OUTPUT,
    curatedOutput: DEFAULT_CURATED_OUTPUT,
    sourceDir: null,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--input") {
      args.input = argv[i + 1];
      i += 1;
    } else if (arg === "--source-dir") {
      args.sourceDir = argv[i + 1];
      i += 1;
    } else if (arg === "--all-output") {
      args.allOutput = argv[i + 1];
      i += 1;
    } else if (arg === "--curated-output") {
      args.curatedOutput = argv[i + 1];
      i += 1;
    }
  }
  return args;
}

function loadIconsJson() {
  for (const candidate of ICON_JSON_CANDIDATES) {
    if (fs.existsSync(candidate)) {
      const data = JSON.parse(fs.readFileSync(candidate, "utf-8"));
      return { sourcePath: candidate, data };
    }
  }
  return { sourcePath: null, data: null };
}

function loadFromIconsDir(iconsDir) {
  if (!iconsDir || !fs.existsSync(iconsDir)) return null;
  const entries = fs.readdirSync(iconsDir, { withFileTypes: true });
  const names = entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(".svg"))
    .map((entry) => entry.name.replace(/\.svg$/, ""));
  if (!names.length) return null;
  return { sourcePath: iconsDir, icons: names };
}

function extractIconNames(data) {
  if (Array.isArray(data)) {
    if (data.length === 0) return [];
    if (typeof data[0] === "string") return data;
    if (typeof data[0] === "object") {
      return data.map((item) => item.name).filter(Boolean);
    }
  }
  if (data && typeof data === "object") {
    if (data.icons && typeof data.icons === "object") {
      return Object.keys(data.icons);
    }
    if (Array.isArray(data.icons)) {
      return extractIconNames(data.icons);
    }
  }
  return [];
}

function toKebab(value) {
  return value
    .replace(/([a-z0-9])([A-Z])/g, "$1-$2")
    .replace(/_/g, "-")
    .toLowerCase();
}

function normalizeCandidate(value) {
  const trimmed = value.trim();
  if (!trimmed) return [];

  const candidates = [];
  if (trimmed.startsWith("Icon") && trimmed.length > 4) {
    candidates.push(trimmed.slice(4));
  }

  candidates.push(trimmed);

  const cleaned = trimmed
    .toLowerCase()
    .replace(/^tabler:/, "")
    .replace(/^tabler-icon-/, "")
    .replace(/^tabler-/, "")
    .replace(/^icon-/, "");

  candidates.push(cleaned);

  const normalized = candidates.map((item) => toKebab(item));
  const unique = [];
  for (const item of normalized) {
    if (item && !unique.includes(item)) unique.push(item);
  }
  return unique;
}

function parseInputList(inputPath) {
  const raw = fs.readFileSync(inputPath, "utf-8");
  return raw
    .split(/[\n,]+/)
    .map((part) => part.trim())
    .filter(Boolean);
}

function levenshtein(a, b) {
  const matrix = Array.from({ length: a.length + 1 }, () => []);
  for (let i = 0; i <= a.length; i += 1) matrix[i][0] = i;
  for (let j = 0; j <= b.length; j += 1) matrix[0][j] = j;

  for (let i = 1; i <= a.length; i += 1) {
    for (let j = 1; j <= b.length; j += 1) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1,
        matrix[i][j - 1] + 1,
        matrix[i - 1][j - 1] + cost
      );
    }
  }
  return matrix[a.length][b.length];
}

function bestMatch(target, candidates) {
  let best = null;
  let bestScore = -1;
  for (const candidate of candidates) {
    const distance = levenshtein(target, candidate);
    const maxLen = Math.max(target.length, candidate.length) || 1;
    const score = 1 - distance / maxLen;
    if (score > bestScore) {
      bestScore = score;
      best = candidate;
    }
  }
  return { match: best, score: bestScore };
}

function ensureDir(filePath) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const sourceDir =
    args.sourceDir || (fs.existsSync(DEFAULT_TABLER_ICONS_DIR) ? DEFAULT_TABLER_ICONS_DIR : null);
  const fromDir = loadFromIconsDir(sourceDir);
  const { sourcePath, data } = fromDir ? { sourcePath: fromDir.sourcePath, data: null } : loadIconsJson();
  const dirIcons = fromDir ? fromDir.icons : null;

  if (!sourcePath) {
    console.error(
      "Could not find Tabler icons data. Provide --source-dir to a cloned tabler-icons/icons folder, or install @iconify-json/tabler or a @tabler/icons package."
    );
    process.exit(1);
  }

  const icons = dirIcons || extractIconNames(data);
  if (!icons.length) {
    console.error("No icons found in icons.json");
    process.exit(1);
  }

  const validIcons = Array.from(new Set(icons.map((name) => toKebab(name)))).sort();

  ensureDir(args.allOutput);
  fs.writeFileSync(args.allOutput, `${validIcons.join("\n")}\n`, "utf-8");

  if (!args.input) {
    console.log(`Wrote ${validIcons.length} valid icons to ${args.allOutput}`);
    return;
  }

  const requested = parseInputList(args.input);
  const curated = [];
  const replacements = [];

  for (const item of requested) {
    let matched = null;
    for (const candidate of normalizeCandidate(item)) {
      if (validIcons.includes(candidate)) {
        matched = candidate;
        break;
      }
    }

    if (!matched) {
      const { match, score } = bestMatch(toKebab(item), validIcons);
      if (!match || score < 0.6) {
        console.error(`No close match found for: ${item}`);
        process.exit(1);
      }
      matched = match;
    }

    if (matched !== toKebab(item)) {
      replacements.push({ original: item, replacement: matched });
    }

    curated.push(matched);
  }

  const curatedUnique = Array.from(new Set(curated));
  ensureDir(args.curatedOutput);
  fs.writeFileSync(args.curatedOutput, `${curatedUnique.join("\n")}\n`, "utf-8");

  if (replacements.length) {
    console.log("Replacements applied:");
    for (const entry of replacements) {
      console.log(`  ${entry.original} -> ${entry.replacement}`);
    }
  }

  console.log(
    `Wrote ${curatedUnique.length} curated icons to ${args.curatedOutput} and ` +
      `${validIcons.length} total icons to ${args.allOutput} (source: ${sourcePath}).`
  );
}

main();
