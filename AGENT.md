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

<skill>
<name>business-skills</name>
<description>Index of business skills in this folder. Use to select the right skill for a task and understand each skill’s role and trigger.</description>
<location>project</location>
</skill>

<skill>
<name>business-consultant</name>
<description>Provide structured business consulting analysis, diagnostics, and recommendations across strategy, finance, operations, sales, and marketing. Use for consulting-style problem solving, executive summaries, or decision support.</description>
<location>project</location>
</skill>

<skill>
<name>strategy</name>
<description>Develop business strategy, competitive analysis, and growth options. Use for strategic planning, market analysis, or portfolio decisions.</description>
<location>project</location>
</skill>

<skill>
<name>finance</name>
<description>Analyze financial statements, budgets, cash flow, unit economics, and financial risks. Use for finance/accounting questions, financial performance reviews, forecasts, or budgeting tasks.</description>
<location>project</location>
</skill>

<skill>
<name>operations</name>
<description>Improve operational processes, capacity, service levels, and efficiency. Use for workflows, process design, operational KPIs, or execution issues.</description>
<location>project</location>
</skill>

<skill>
<name>marketing</name>
<description>Plan and evaluate marketing strategy, positioning, campaigns, and metrics. Use for marketing, brand, growth, acquisition, or go-to-market tasks.</description>
<location>project</location>
</skill>

<skill>
<name>sales</name>
<description>Build sales strategy, pipelines, outreach, and forecasting. Use for sales process design, revenue targets, pipeline health, or deal management tasks.</description>
<location>project</location>
</skill>

<skill>
<name>customer-success</name>
<description>Improve customer onboarding, retention, and account health. Use for customer success strategy, churn reduction, QBRs, or customer lifecycle tasks.</description>
<location>project</location>
</skill>

<skill>
<name>leadership</name>
<description>Support leadership decisions, org design, and team effectiveness. Use for management, culture, org change, or leadership communication tasks.</description>
<location>project</location>
</skill>

<skill>
<name>hr</name>
<description>Support HR and people operations work such as hiring, performance, compensation, and policies. Use for HR processes, employee relations, or org health tasks.</description>
<location>project</location>
</skill>

<skill>
<name>pmo</name>
<description>Support project and program management: planning, tracking, governance, and delivery. Use for PMO reporting, roadmaps, risk logs, or execution cadence tasks.</description>
<location>project</location>
</skill>

<skill>
<name>legal</name>
<description>Assist with legal/compliance workflows such as contract reviews, policy drafting, and risk assessment. Use for legal questions, compliance checks, or governance tasks.</description>
<location>project</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
