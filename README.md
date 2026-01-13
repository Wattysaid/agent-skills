# Codex Skills

A small collection of Codex skills used by BusinessStrategyToolkit.com. Each skill bundles instructions, references, and optional scripts/assets to let Codex handle a specific workflow or toolchain.

## Quick Install

Install skills for Claude Code, Gemini Code Assist, and Codex:

**Windows (PowerShell):**
```powershell
.\install-skills.ps1
```

**macOS/Linux (Bash):**
```bash
chmod +x install-skills.sh && ./install-skills.sh
```

**Cross-Platform (Python):**
```bash
python install-skills.py
```

For more installation options (global install, custom locations, etc.), see [INSTALLER.md](INSTALLER.md).

## What's in this repo

| Skill | What it does | Path |
| --- | --- | --- |
| ai-skill-factory | Create new AI skills for Codex, Claude, and Gemini with proper structure and boilerplate. | `ai-skill-factory/` |
| algorithmic-art | Create algorithmic art using p5.js with seeded randomness and interactive parameter exploration. | `algorithmic-art/` |
| astro-developer | Build and customize Astro sites, templates, routing, integrations, deployment, and troubleshooting. | `astro-developer/` |
| brand-guidelines | Apply Anthropic's official brand colors and typography to artifacts for consistent look-and-feel. | `brand-guidelines/` |
| canvas-design | Create beautiful visual art in PNG and PDF documents using design philosophy. | `canvas-design/` |
| dev-browser | Browser automation with persistent page state for navigation, form filling, scraping, testing, and screenshots. | `dev-browser/` |
| doc-coauthoring | Structured workflow for co-authoring documentation, proposals, technical specs, and decision docs. | `doc-coauthoring/` |
| docx | Comprehensive document creation, editing, and analysis with tracked changes, comments, and formatting. | `docx/` |
| frontend-design | Create distinctive, production-grade frontend interfaces with high design quality. | `frontend-design/` |
| gastown | Multi-agent orchestrator for Claude Code with gt/bd workflow operations and recovery. | `gastown/` |
| internal-comms | Resources for writing internal communications using your company's formats. | `internal-comms/` |
| linkedin-article-generator | Generate leadership-style LinkedIn articles from topic and conversation files. | `linkedin-article-generator/` |
| mcp-builder | Create high-quality MCP servers that enable LLMs to interact with external services. | `mcp-builder/` |
| pdf | Comprehensive PDF manipulation for extracting text, creating documents, merging/splitting, and forms. | `pdf/` |
| pptx | Presentation creation, editing, and analysis for working with PowerPoint files. | `pptx/` |
| process-architect-bpmn | Create BPMN process maps and analyses from transcripts, event logs, or connector data. | `process-architect-bpmn/` |
| process-mining-assistant | End-to-end process mining analysis with event logs, process models, conformance, and performance. | `process-mining-assistant/` |
| skill-installer | Install agent-skills for Claude Code, Gemini Code Assist, and Codex to make them available. | `skill-installer/` |
| slack-gif-creator | Create animated GIFs optimized for Slack with constraints and validation tools. | `slack-gif-creator/` |
| theme-factory | Toolkit for styling artifacts with pre-set themes or custom generated themes. | `theme-factory/` |
| web-artifacts-builder | Create elaborate, multi-component claude.ai HTML artifacts with React, Tailwind, and shadcn/ui. | `web-artifacts-builder/` |
| webapp-testing | Toolkit for interacting with and testing local web applications using Playwright. | `webapp-testing/` |
| xlsx | Comprehensive spreadsheet creation, editing, and analysis with formulas, formatting, and visualization. | `xlsx/` |
| zai-cli | Z.AI CLI for vision analysis, web search, page reading, GitHub repo exploration, and MCP tools. | `zai-cli/` |
| business-skills | Index of business skills with routing guidance for the suite. | `business-skills/` |
| business-consultant | Cross-functional consulting analysis and recommendations for executive decision support. | `business-skills/business-consultant/` |
| strategy | Business strategy, competitive analysis, and growth options. | `business-skills/strategy/` |
| finance | Financial statements, budgeting, cash flow, and unit economics analysis. | `business-skills/finance/` |
| operations | Operational process design, capacity, service levels, and efficiency. | `business-skills/operations/` |
| marketing | Marketing strategy, positioning, campaigns, and metrics. | `business-skills/marketing/` |
| sales | Sales strategy, pipeline, outreach, and forecasting. | `business-skills/sales/` |
| customer-success | Customer onboarding, retention, account health, and churn reduction. | `business-skills/customer-success/` |
| leadership | Leadership decisions, org design, and team effectiveness. | `business-skills/leadership/` |
| hr | Hiring, performance, compensation, and people operations. | `business-skills/hr/` |
| pmo | Program management planning, tracking, governance, and delivery. | `business-skills/pmo/` |
| legal | Contract review, compliance, policy drafting, and risk assessment. | `business-skills/legal/` |

## Using a skill

After installation, your AI assistant will automatically discover and use skills:

1. **Mention a skill by name**: "Use the astro-developer skill to create a blog"
2. **Describe what you need**: "Help me create a PDF report" (auto-triggers pdf skill)
3. **Ask for specific workflows**: "I need to analyze process mining data" (loads process-mining-assistant)

Skills are loaded automatically based on your request - no manual importing needed!

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
