# OpenAI Codex CLI and Skills

## Overview
Codex CLI is a terminal-based coding agent that can read, modify, and run code locally.
It supports structured instructions and reusable "skills" to automate workflows.

## Installation
Typical installs:
- npm: npm install -g @openai/codex
- Homebrew: brew install --cask codex

## CLI Capabilities
- Reads and edits files in the working directory
- Executes shell commands with approval modes
- Supports slash commands for workflows
- Supports context files and reusable instruction bundles

## Skills Concept
A skill is a small, reusable bundle that contains:
- Name and description
- Trigger conditions ("use when...")
- Step-by-step instructions
- Optional scripts or helpers

Skills are typically defined with a SKILL.md file and supporting assets.

## Typical Folder Layout
.codex/
  skills/
    my-skill/
      SKILL.md
      helper.py
      README.md

## SKILL.md Structure (Example)
name: my-skill
description: Use when user asks to refactor Python modules
triggers:
  - refactor
  - restructure
instructions:
  - Analyse module structure
  - Extract functions into separate files
  - Update imports

## Best Practices
- Be explicit about trigger conditions
- Keep instructions operational, not descriptive
- Include guardrails for destructive actions
- Prefer small, composable skills

## Integration Patterns
- Pair skills with MCP servers for tool access
- Use skills for repeated operational tasks (tests, linting, packaging, BPMN generation, etc.)
