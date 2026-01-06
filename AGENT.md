# AGENTS

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Read the skill file directly: Use read_file to load `.codex/skills/<skill-name>/skill.md` or `.codex/skills/<skill-name>/SKILL.md`
- The skill content contains detailed instructions on how to complete the task
- Skills include references to additional resources in their references/, scripts/, and assets/ subdirectories
- Load referenced files from `.codex/skills/<skill-name>/references/` as needed for specific subtasks

Usage notes:
- Only use skills listed in <available_skills> below
- Do not reload a skill that is already loaded in your context
- Read only the references you need for the current task to stay focused
- Each skill invocation is stateless - you may need to reload skill content in new conversations
</usage>

<available_skills>

<skill>
<name>astro-developer</name>
<description>Build and customize websites, blogs, and web applications using Astro. Use this skill when you need to scaffold Astro projects, select and apply starter templates or themes, implement layouts and components, configure content collections and routing, integrate CSS frameworks or JavaScript libraries, add UI framework integrations, create API endpoints, optimize and deploy builds, or troubleshoot Astro-specific issues. Includes working with Astro's theme library (blog, e-commerce, landing pages, portfolios, documentation) and adapting templates to project requirements.</description>
<location>project</location>
</skill>

<skill>
<name>dev-browser</name>
<description>Browser automation with persistent page state. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. Trigger phrases include "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into", or any browser interaction request.</description>
<location>project</location>
</skill>

<skill>
<name>gastown</name>
<description>Multi-agent orchestrator for Claude Code. Use when user mentions gastown, gas town, gt commands, bd commands, convoys, polecats, crew, rigs, slinging work, multi-agent coordination, beads, hooks, molecules, workflows, the witness, the mayor, the refinery, the deacon, dogs, escalation, or wants to run multiple AI agents on projects simultaneously. Handles installation, workspace setup, work tracking, agent lifecycle, crash recovery, and all gt/bd CLI operations.</description>
<location>project</location>
</skill>

<skill>
<name>zai-cli</name>
<description>Z.AI CLI providing: Vision (image/video analysis, OCR, UI-to-code, error diagnosis with GLM-4.6V), Search (real-time web search with domain/recency filtering), Reader (web page to markdown extraction), Repo (GitHub code search and reading via ZRead), Tools (MCP tool discovery and raw calls), and Code (TypeScript tool chaining). Use for visual content analysis, web search, page reading, or GitHub exploration. Requires Z_AI_API_KEY.</description>
<location>project</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
