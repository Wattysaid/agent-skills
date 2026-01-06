# Tabler Icon Usage

Use Tabler icons with the `tabler:` prefix and validate icon names before running dev or build.

## Do

- Use names like `tabler:arrow-up-right`.
- Run the validator before `npm run dev` or `npm run build`.
- Keep the curated icon list updated in `src/config/tabler-icons.txt`.

## Do Not

- Do not invent icon names.
- Do not use other icon prefixes unless intentionally configured.

## Validation

Use the validation script to correct and record icon names:

```bash
node scripts/validate-tabler-icons.mjs --source-dir /path/to/tabler-icons/icons
```

If `--source-dir` is not provided, the script falls back to `node_modules/@iconify-json/tabler` if installed.

