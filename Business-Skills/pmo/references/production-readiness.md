# Production Readiness Checklist

## Structure and metadata
- SKILL.md frontmatter uses name/description only.
- Skill folder name matches the name field.
- Descriptions include clear trigger keywords and scope.

## Progressive disclosure
- Keep SKILL.md concise; push detail into references.
- Use references for frameworks, templates, data needs.
- Avoid duplicate information between files.

## Quality and safety
- Ensure quality-standards.md is referenced.
- Add clarifying questions when inputs are missing.
- Maintain memory-context.md with useful facts only.

## Scripts
- Use python3 shebang and simple CLI args.
- Validate scripts with at least one test run.
- Avoid hardcoded secrets or external dependencies.

## Cross-skill alignment
- Ensure complementary skills are listed.
- Add handoff and common-project references.
- Keep KPI/OKR definitions consistent.

## Packaging
- Validate skill folder with skills-ref (if available).
- Package with package_skill.py when distributing.
- Re-test scripts after any change.
