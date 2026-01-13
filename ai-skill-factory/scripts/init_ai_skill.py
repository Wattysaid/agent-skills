#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]+$")


def title_from_name(name: str) -> str:
    return name.replace("-", " ").title()


def read_template(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_template(template: str, context: dict[str, str]) -> str:
    for key, value in context.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template


def safe_write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def scaffold_skill(base_dir: Path, name: str, context: dict[str, str], resources: list[str], force: bool, templates_dir: Path) -> None:
    skill_dir = base_dir / name
    ensure_dir(skill_dir)

    template = read_template(templates_dir / "SKILL.md.tmpl")
    rendered = render_template(template, context)
    safe_write(skill_dir / "SKILL.md", rendered, force)

    for resource in resources:
        ensure_dir(skill_dir / resource)

    if context.get("agent") == "claude":
        claude_template = read_template(templates_dir / "CLAUDE.md.tmpl")
        rendered_claude = render_template(claude_template, context)
        safe_write(skill_dir / "CLAUDE.md", rendered_claude, force)


def parse_agents(value: str) -> list[str]:
    if value == "all":
        return ["codex", "claude", "gemini"]
    return [agent.strip() for agent in value.split(",") if agent.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize AI skill scaffolds for Codex/Claude/Gemini.")
    parser.add_argument("--name", required=True, help="Skill name, lowercase with hyphens.")
    parser.add_argument("--description", default="TODO: describe when and why to use this skill.")
    parser.add_argument("--triggers", required=True, help="Comma-separated list of triggers.")
    parser.add_argument("--goal", required=True, help="A brief description of the skill's goal.")
    parser.add_argument("--step1", default="TODO: Add step 1", help="First step of the skill.")
    parser.add_argument("--step2", default="TODO: Add step 2", help="Second step of the skill.")
    parser.add_argument("--step3", default="TODO: Add step 3", help="Third step of the skill.")
    parser.add_argument("--path", default="skills", help="Output directory.")
    parser.add_argument("--agent", default="codex", help="codex, claude, gemini, or all.")
    parser.add_argument(
        "--resources",
        default="",
        help="Comma-separated resource folders (scripts,references,assets).",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    if not NAME_RE.match(args.name):
        raise SystemExit("Skill name must match [a-z0-9-]+.")

    agents = parse_agents(args.agent)
    for agent in agents:
        if agent not in {"codex", "claude", "gemini"}:
            raise SystemExit(f"Unknown agent: {agent}")

    resources = [value.strip() for value in args.resources.split(",") if value.strip()]
    invalid_resources = [value for value in resources if value not in {"scripts", "references", "assets"}]
    if invalid_resources:
        raise SystemExit(f"Invalid resources: {', '.join(invalid_resources)}")

    base_dir = Path(args.path)
    templates_dir = Path(__file__).resolve().parent.parent / "assets" / "templates"

    context = {
        "skill_name": args.name,
        "skill_title": title_from_name(args.name),
        "skill_description": args.description,
        "skill_triggers": args.triggers,
        "skill_goal": args.goal,
        "step_1": args.step1,
        "step_2": args.step2,
        "step_3": args.step3,
        "agent": args.agent,
    }

    scaffold_skill(base_dir, args.name, context, resources, args.force, templates_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())