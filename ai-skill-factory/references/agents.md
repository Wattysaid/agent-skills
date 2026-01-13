# Agent Notes

This document provides a brief overview of how to create skills that are compatible with different AI agents.

## The Agnostic Skill
The `ai-skill-factory` now generates a single, agent-agnostic skill that can be used with Codex, Claude, and Gemini. This is achieved by using a common `SKILL.md` file format and externalizing agent-specific logic.

## `SKILL.md`
The `SKILL.md` file is the core of the skill. It defines the skill's name, description, triggers, and instructions. It also includes sections for safety and examples.

## Agent-Specific Files
- **Claude:** For Claude, a `CLAUDE.md` file can be generated. This file provides project-specific context to the agent.
- **Gemini:** For Gemini, a `GEMINI_manifest.json.tmpl` is provided as a placeholder for a Gemini extension.

## Best Practices
- **Keep skills small and focused.**
- **Use explicit triggers.**
- **Externalize complex logic into scripts.**
- **Always include safety guardrails.**