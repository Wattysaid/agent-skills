# Anthropic Claude Code Skills

## Overview
Claude Code supports structured agent guidance using:
- Skills (instruction bundles)
- Project context files (CLAUDE.md)
- Tool-aware agent workflows

## Skills Concept
A skill is a reusable capability that includes:
- When it should be used
- What steps to perform
- What tools or files it may access

Skills can be automatically or manually invoked based on relevance.

## CLAUDE.md
CLAUDE.md is a project-level instruction file that:
- Defines coding standards
- Describes project structure
- Lists preferred workflows

It is often used together with skills to steer agent behaviour.

## Example CLAUDE.md Sections
- Project overview
- Tech stack and conventions
- Build and test commands
- Deployment notes
- Security and compliance constraints

## Skill Folder Layout (Community Pattern)
.claude/
  skills/
    data-cleaning/
      SKILL.md
      pandas_helpers.py

## Best Practices
- Keep skills narrow and focused
- Avoid duplicating project-level rules
- Include example commands where possible
- Specify file paths explicitly

## Advanced Patterns
- Multi-skill orchestration by an external orchestrator agent
- Versioned skills (R1.00, R1.01, etc.)
- Skills mapped to value streams (finance, ops, marketing, BPMN, etc.)
