# Codex Skills

A small collection of Codex skills used by BusinessStrategyToolkit.com. Each skill bundles instructions, references, and optional scripts/assets to let Codex handle a specific workflow or toolchain.

## What's in this repo

| Skill | What it does | Path |
| --- | --- | --- |
| astro-developer | Build and customize Astro sites, templates, routing, integrations, deployment, and troubleshooting. | `astro-developer/` |
| dev-browser | Browser automation with persistent page state for navigation, form filling, scraping, testing, and screenshots. | `dev-browser/` |
| gastown | Multi-agent orchestrator for Claude Code with gt/bd workflow operations and recovery. | `gastown/` |
| zai-cli | Z.AI CLI for vision analysis, web search, page reading, GitHub repo exploration, and MCP tools. | `zai-cli/` |

## Using a skill

1. Place this repo at `.codex/skills` in your project.
2. In your prompt, mention the skill name (e.g. `astro-developer`) or ask for something that clearly matches its description.
3. Codex loads `SKILL.md` from the skill directory and follows its workflow.

## Skill structure

A typical skill directory looks like this:

```
my-skill/
  SKILL.md
  references/
  scripts/
  assets/
```

- `SKILL.md` defines the name, description, and operating rules.
- `references/` holds deep-dive docs that the skill can load on demand.
- `scripts/` contains helper scripts (preferred over retyping long steps).
- `assets/` stores templates and reusable UI/UX snippets.

## Contributing

- Keep skills focused and actionable.
- Put long-form guidance in `references/` to keep `SKILL.md` short.
- Prefer scripts/assets when they prevent repetitive instructions.

## Notes

- `dev-browser/` includes a local Node toolchain; follow its `SKILL.md` for setup and run modes.
- `zai-cli/` requires `Z_AI_API_KEY` to be set before use.
