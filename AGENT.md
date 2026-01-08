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
<name>algorithmic-art</name>
<description>Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations.</description>
<location>project</location>
</skill>

<skill>
<name>astro-developer</name>
<description>Build and customize websites, blogs, and web applications using Astro. Use this skill when you need to scaffold Astro projects, select and apply starter templates or themes, implement layouts and components, configure content collections and routing, integrate CSS frameworks or JavaScript libraries, add UI framework integrations, create API endpoints, optimize and deploy builds, or troubleshoot Astro-specific issues. Includes working with Astro's theme library (blog, e-commerce, landing pages, portfolios, documentation) and adapting templates to project requirements.</description>
<location>project</location>
</skill>

<skill>
<name>brand-guidelines</name>
<description>Applies Anthropic's official brand colors and typography to any artifact that may benefit from having Anthropic's look-and-feel. Use when brand colors or style guidelines, visual formatting, or company design standards apply.</description>
<location>project</location>
</skill>

<skill>
<name>canvas-design</name>
<description>Create beautiful visual art in .png and .pdf documents using design philosophy. Use when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations.</description>
<location>project</location>
</skill>

<skill>
<name>dev-browser</name>
<description>Browser automation with persistent page state. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. Trigger phrases include "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into", or any browser interaction request.</description>
<location>project</location>
</skill>

<skill>
<name>doc-coauthoring</name>
<description>Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers.</description>
<location>project</location>
</skill>

<skill>
<name>docx</name>
<description>Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for creating new documents, modifying or editing content, working with tracked changes, adding comments, or any other document tasks.</description>
<location>project</location>
</skill>

<skill>
<name>frontend-design</name>
<description>Create distinctive, production-grade frontend interfaces with high design quality. Use when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.</description>
<location>project</location>
</skill>

<skill>
<name>gastown</name>
<description>Multi-agent orchestrator for Claude Code. Use when user mentions gastown, gas town, gt commands, bd commands, convoys, polecats, crew, rigs, slinging work, multi-agent coordination, beads, hooks, molecules, workflows, the witness, the mayor, the refinery, the deacon, dogs, escalation, or wants to run multiple AI agents on projects simultaneously. Handles installation, workspace setup, work tracking, agent lifecycle, crash recovery, and all gt/bd CLI operations.</description>
<location>project</location>
</skill>

<skill>
<name>internal-comms</name>
<description>A set of resources to help write all kinds of internal communications, using the formats that your company likes to use. Use whenever asked to write some sort of internal communications (status reports, leadership updates, 3P updates, company newsletters, FAQs, incident reports, project updates, etc.).</description>
<location>project</location>
</skill>

<skill>
<name>linkedin-article-generator</name>
<description>Generate leadership-style LinkedIn articles from a collection of topic and conversation files. Use when a user wants to draft a reflective LinkedIn post or long-form article based on notes, meeting transcripts or other documents. The skill reads all text files within a specified folder, synthesises the key points and produces a polished LinkedIn article using a distinctive tone of voice (observational, pragmatic and operator-credible) with second-order thinking and practical takeaways.</description>
<location>project</location>
</skill>

<skill>
<name>mcp-builder</name>
<description>Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).</description>
<location>project</location>
</skill>

<skill>
<name>pdf</name>
<description>Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.</description>
<location>project</location>
</skill>

<skill>
<name>pptx</name>
<description>Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for creating new presentations, modifying or editing content, working with layouts, adding comments or speaker notes, or any other presentation tasks.</description>
<location>project</location>
</skill>

<skill>
<name>process-architect-bpmn</name>
<description>Create BPMN process maps and analyses from transcripts, event logs, or connector data. Use when asked for process discovery, variants/bottlenecks, or BPMN outputs (Camunda 7/8, Mermaid, PlantUML, or generic BPMN XML).</description>
<location>project</location>
</skill>

<skill>
<name>process-mining-assistant</name>
<description>Perform an end-to-end process mining analysis via a command-line tool. Use when a user needs to load, clean and analyse event logs, discover process models, evaluate conformance and performance, or generate reports using PM4Py outside of a notebook.</description>
<location>project</location>
</skill>

<skill>
<name>skill-creator</name>
<description>Guide for creating effective skills. Use when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.</description>
<location>project</location>
</skill>

<skill>
<name>slack-gif-creator</name>
<description>Knowledge and utilities for creating animated GIFs optimized for Slack. Provides constraints, validation tools, and animation concepts. Use when users request animated GIFs for Slack like "make me a GIF of X doing Y for Slack."</description>
<location>project</location>
</skill>

<skill>
<name>theme-factory</name>
<description>Toolkit for styling artifacts with a theme. These artifacts can be slides, docs, reportings, HTML landing pages, etc. There are 10 pre-set themes with colors/fonts that you can apply to any artifact that has been creating, or can generate a new theme on-the-fly.</description>
<location>project</location>
</skill>

<skill>
<name>web-artifacts-builder</name>
<description>Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui). Use for complex artifacts requiring state management, routing, or shadcn/ui components - not for simple single-file HTML/JSX artifacts.</description>
<location>project</location>
</skill>

<skill>
<name>webapp-testing</name>
<description>Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.</description>
<location>project</location>
</skill>

<skill>
<name>xlsx</name>
<description>Comprehensive spreadsheet creation, editing, and analysis with support for formulas, formatting, data analysis, and visualization. When Claude needs to work with spreadsheets (.xlsx, .xlsm, .csv, .tsv, etc) for creating new spreadsheets with formulas and formatting, reading or analyzing data, modifying existing spreadsheets while preserving formulas, data analysis and visualization in spreadsheets, or recalculating formulas.</description>
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
