# Google Gemini CLI Extensions and Skills Patterns

## Overview
Gemini CLI currently supports extensions and plugins rather than formalised "skills",
but the community is converging on skill-like patterns.

## Extension Concept
An extension typically provides:
- Custom commands
- API integrations
- Contextual tooling

## Community Skill Patterns
Although not formally standardised, community approaches include:
- Instruction manifests (AGENTS.md, GEMINI.md)
- Folder-based rule discovery
- Cross-agent compatible SKILL.md files

## Suggested Skill-Compatible Layout
.gemini/
  extensions/
    my-extension/
      manifest.json
      index.ts

.skills/
  my-skill/
    SKILL.md

## Portability Strategy
To support Gemini CLI alongside Codex and Claude:
- Keep SKILL.md agent-agnostic
- Externalise tool calls into scripts
- Use adapters per CLI

## Use Cases
- DevOps automation
- Code review checks
- Data pipeline scaffolding
- Process mining ingestion
