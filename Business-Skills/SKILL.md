---
name: business-skills
description: Index of business skills in this folder. Use to select the right skill for a task and understand each skill’s role and trigger.
---

# Business Skills Index

## Document control
- Version: R1.00
- Status: Approved (agent-ready Markdown with canonical capability map block)
- Last updated: 2026-01-06
- Change log:
  - R1.00: Added agent-parsable capability map (IDs + canonical YAML) and a scan-friendly capability matrix, without removing or rewriting any original content.

## Identity
You are the business-skills orchestrator. Your job is to pick the right skill, route work, and ensure the team has enough context to deliver confident recommendations.

## Core principle
Start with the most relevant skill, but use `business-consultant` whenever the scope is unclear or required context is missing.

## Modes
- Discovery: gather baseline context and clarify objectives.
- Analysis: evaluate data, diagnose gaps, quantify impact.
- Recommendation: propose options and trade-offs with risks.
- Execution support: provide templates, cadence, and tracking.

## Startup flow
- Check the target skill’s `memory-context.md`.
- If it has only the template and intake questions, route to `business-consultant` to gather baseline facts.
- Append answers to each relevant `memory-context.md` before executing the targeted task.

## Memory update policy
- Store only reusable facts, constraints, metrics, and decisions.
- Note unknowns explicitly and capture proxy data if needed.
- Tag related skills to enable handoffs.

## Memory context
- Read `memory-context.md` to seed company-wide facts before starting discovery.
- Append new org-level context after intake or major decisions.

## Skills and roles
- `business-consultant`: Cross-functional discovery, diagnostics, and executive-ready recommendations. Use for ambiguous problems, multi-function decisions, or missing context.
- `strategy`: Strategic planning, market analysis, and growth options. Use for direction, portfolio choices, or competitive positioning.
- `finance`: Financial performance, budgeting, cash flow, and unit economics. Use for runway, margins, forecasts, or investment decisions.
- `operations`: Process design, capacity planning, and delivery performance. Use for efficiency, quality, and execution bottlenecks.
- `marketing`: Positioning, campaigns, and acquisition metrics. Use for GTM, demand generation, and brand alignment.
- `sales`: Pipeline, forecasting, and sales execution. Use for revenue targets, deal health, and conversion improvement.
- `customer-success`: Onboarding, retention, and expansion. Use for churn reduction, health scoring, and renewals.
- `leadership`: Org design, alignment, and culture. Use for management effectiveness and change leadership.
- `hr`: Hiring, performance, and people programs. Use for talent strategy and workforce planning.
- `pmo`: Program governance, planning, and delivery cadence. Use for portfolio tracking and risk management.
- `legal`: Contract review and compliance risk. Use for governance, policy, and legal exposure.

## When to start with business-consultant
- The request spans multiple functions or is poorly scoped.
- Required context is missing in `memory-context.md`.
- The user asks for executive-level guidance or a diagnostic.

## Routing guidance
- Use the skill closest to the user’s ask, then pull in complementary skills using handoff references.
- If a skill lacks baseline context, route intake through `business-consultant` first.
- For targeted asks (e.g., SEO), gather minimum viable facts before providing recommendations.

## References
- Use `references/suite-governance.md` for maintenance and consistency checks.
- Use `references/suite-routing.md` for routing patterns and examples.

## Verification checklist
- Confirm objective, audience level, and decision owner.
- State assumptions and data gaps explicitly.
- Validate key metrics and time windows.
- Identify risks, dependencies, and constraints.
- End with clear next steps and owners.

## Skill locations
- `business-consultant/SKILL.md`
- `strategy/SKILL.md`
- `finance/SKILL.md`
- `operations/SKILL.md`
- `marketing/SKILL.md`
- `sales/SKILL.md`
- `customer-success/SKILL.md`
- `leadership/SKILL.md`
- `hr/SKILL.md`
- `pmo/SKILL.md`
- `legal/SKILL.md`

## Org chart
```
Business Skills
├── business-consultant (orchestrator)
│   ├── strategy
│   ├── finance
│   ├── operations
│   ├── marketing
│   ├── sales
│   ├── customer-success
│   ├── leadership
│   ├── hr
│   ├── pmo
│   └── legal
```

## Typical business org chart
```
CEO
├── Strategy
├── Finance
├── Operations
│   ├── PMO
│   └── Customer Success
├── Marketing
├── Sales
├── HR
└── Legal
```

## Complementary skill mapping
- Strategy ↔ Finance: investment models, ROI gates, portfolio trade-offs.
- Strategy ↔ Operations: capability requirements, feasibility, delivery constraints.
- Marketing ↔ Sales: ICP, messaging, pipeline conversion, enablement.
- Sales ↔ Customer Success: handoffs, renewals, expansion plans.
- Operations ↔ PMO: execution cadence, dependencies, risk tracking.
- Leadership ↔ HR: org design, capability gaps, retention risks.

## Business capabilities map
Use this to understand where each skill fits and what to ask for.

### Agent-parsable canonical map (do not edit keys)
- Purpose: give agents a consistent structure for retrieval and comparison across domains.
- Conventions:
  - IDs are stable: `STR-01`, `FIN-01`, etc.
  - Lists are semicolon-separated in tables; YAML uses arrays.
  - When adding new entries, maintain the same fields: `processes`, `people_roles`, `technology`.

```yaml
capability_map:
  version: "R1.00"
  fields:
    - domain
    - capability_id
    - capability_name
    - processes
    - people_roles
    - technology
  domains:
    - domain: Strategy
      capabilities:
        - capability_id: STR-01
          capability_name: Strategic planning and portfolio
          processes: [market sizing, option evaluation, portfolio reviews]
          people_roles: [strategy lead, business analyst]
          technology: [BI/analytics, market research tools]
        - capability_id: STR-02
          capability_name: Competitive positioning
          processes: [competitive analysis, differentiation, pricing strategy]
          people_roles: [strategy lead, product marketing partner]
          technology: [competitive intel, pricing tools]

    - domain: Finance
      capabilities:
        - capability_id: FIN-01
          capability_name: FP&A
          processes: [budgeting, forecasting, variance review]
          people_roles: [FP&A analyst, finance manager]
          technology: [ERP, planning tools, BI]
        - capability_id: FIN-02
          capability_name: Cash and capital management
          processes: [cash flow monitoring, runway analysis, capital allocation]
          people_roles: [finance director, controller]
          technology: [treasury tools, banking portals]

    - domain: Operations
      capabilities:
        - capability_id: OPS-01
          capability_name: Service delivery
          processes: [SLA management, quality control, capacity planning]
          people_roles: [operations manager, service lead]
          technology: [ERP, workflow tools, ticketing]
        - capability_id: OPS-02
          capability_name: Process improvement
          processes: [bottleneck analysis, SOPs, continuous improvement]
          people_roles: [ops excellence lead, process owner]
          technology: [process mining, workflow automation]

    - domain: Marketing
      capabilities:
        - capability_id: MKT-01
          capability_name: Demand generation
          processes: [campaign planning, channel optimization, attribution]
          people_roles: [growth marketer, demand gen lead]
          technology: [marketing automation, analytics, ad platforms]
        - capability_id: MKT-02
          capability_name: Brand and messaging
          processes: [positioning, content strategy, asset production]
          people_roles: [brand manager, content lead]
          technology: [CMS, DAM, design tools]

    - domain: Sales
      capabilities:
        - capability_id: SAL-01
          capability_name: Revenue execution
          processes: [pipeline management, forecasting, deal reviews]
          people_roles: [sales manager, account executive]
          technology: [CRM, sales engagement, CPQ]
        - capability_id: SAL-02
          capability_name: Enterprise selling
          processes: [account planning, multi-stakeholder sales, negotiation]
          people_roles: [enterprise AE, sales engineer]
          technology: [CRM, proposal tools, contract management]

    - domain: Customer Success
      capabilities:
        - capability_id: CS-01
          capability_name: Retention and expansion
          processes: [health scoring, renewals, expansion plays]
          people_roles: [CSM, renewal manager]
          technology: [CS platform, CRM, product analytics]
        - capability_id: CS-02
          capability_name: Onboarding
          processes: [time-to-value planning, enablement, adoption]
          people_roles: [onboarding specialist, solutions lead]
          technology: [LMS, in-app guidance, knowledge base]

    - domain: Leadership
      capabilities:
        - capability_id: LDR-01
          capability_name: Org design and alignment
          processes: [decision rights, OKR alignment, comms cadence]
          people_roles: [COO/CEO, functional leaders]
          technology: [OKR tools, collaboration suites]
        - capability_id: LDR-02
          capability_name: Culture and performance
          processes: [performance reviews, engagement programs]
          people_roles: [people leader, HR partner]
          technology: [HRIS, survey tools]

    - domain: HR
      capabilities:
        - capability_id: HR-01
          capability_name: Talent acquisition
          processes: [hiring pipeline, interview process, onboarding]
          people_roles: [recruiter, hiring manager]
          technology: [ATS, HRIS]
        - capability_id: HR-02
          capability_name: Performance and rewards
          processes: [calibration, compensation reviews, development plans]
          people_roles: [HRBP, compensation analyst]
          technology: [HRIS, comp planning tools]

    - domain: PMO
      capabilities:
        - capability_id: PMO-01
          capability_name: Program governance
          processes: [portfolio intake, RAID, reporting cadence]
          people_roles: [PMO lead, program manager]
          technology: [project management tools, dashboards]
        - capability_id: PMO-02
          capability_name: Delivery coordination
          processes: [dependency tracking, milestone management]
          people_roles: [program manager, delivery lead]
          technology: [project management, workflow tools]

    - domain: Legal
      capabilities:
        - capability_id: LEG-01
          capability_name: Contract management
          processes: [review, redlines, approvals]
          people_roles: [legal counsel, contracts manager]
          technology: [CLM, e-signature]
        - capability_id: LEG-02
          capability_name: Compliance and risk
          processes: [policy management, audit readiness]
          people_roles: [compliance officer, legal ops]
          technology: [GRC tools, document management]
```

### Capability matrix (scan view)
| Domain | Capability ID | Capability | Processes | People | Technology |
|---|---|---|---|---|---|
| Strategy | STR-01 | Strategic planning and portfolio | market sizing; option evaluation; portfolio reviews | strategy lead; business analyst | BI/analytics; market research tools |
| Strategy | STR-02 | Competitive positioning | competitive analysis; differentiation; pricing strategy | strategy lead; product marketing partner | competitive intel; pricing tools |
| Finance | FIN-01 | FP&A | budgeting; forecasting; variance review | FP&A analyst; finance manager | ERP; planning tools; BI |
| Finance | FIN-02 | Cash and capital management | cash flow monitoring; runway analysis; capital allocation | finance director; controller | treasury tools; banking portals |
| Operations | OPS-01 | Service delivery | SLA management; quality control; capacity planning | operations manager; service lead | ERP; workflow tools; ticketing |
| Operations | OPS-02 | Process improvement | bottleneck analysis; SOPs; continuous improvement | ops excellence lead; process owner | process mining; workflow automation |
| Marketing | MKT-01 | Demand generation | campaign planning; channel optimization; attribution | growth marketer; demand gen lead | marketing automation; analytics; ad platforms |
| Marketing | MKT-02 | Brand and messaging | positioning; content strategy; asset production | brand manager; content lead | CMS; DAM; design tools |
| Sales | SAL-01 | Revenue execution | pipeline management; forecasting; deal reviews | sales manager; account executive | CRM; sales engagement; CPQ |
| Sales | SAL-02 | Enterprise selling | account planning; multi-stakeholder sales; negotiation | enterprise AE; sales engineer | CRM; proposal tools; contract management |
| Customer Success | CS-01 | Retention and expansion | health scoring; renewals; expansion plays | CSM; renewal manager | CS platform; CRM; product analytics |
| Customer Success | CS-02 | Onboarding | time-to-value planning; enablement; adoption | onboarding specialist; solutions lead | LMS; in-app guidance; knowledge base |
| Leadership | LDR-01 | Org design and alignment | decision rights; OKR alignment; comms cadence | COO/CEO; functional leaders | OKR tools; collaboration suites |
| Leadership | LDR-02 | Culture and performance | performance reviews; engagement programs | people leader; HR partner | HRIS; survey tools |
| HR | HR-01 | Talent acquisition | hiring pipeline; interview process; onboarding | recruiter; hiring manager | ATS; HRIS |
| HR | HR-02 | Performance and rewards | calibration; compensation reviews; development plans | HRBP; compensation analyst | HRIS; comp planning tools |
| PMO | PMO-01 | Program governance | portfolio intake; RAID; reporting cadence | PMO lead; program manager | project management tools; dashboards |
| PMO | PMO-02 | Delivery coordination | dependency tracking; milestone management | program manager; delivery lead | project management; workflow tools |
| Legal | LEG-01 | Contract management | review; redlines; approvals | legal counsel; contracts manager | CLM; e-signature |
| Legal | LEG-02 | Compliance and risk | policy management; audit readiness | compliance officer; legal ops | GRC tools; document management |
