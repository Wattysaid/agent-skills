#!/usr/bin/env python3
"""
Agent Skills Installer
Cross-platform installer for Claude Code, Gemini Code Assist, and Codex skills.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Tuple

# ANSI color codes
class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def success(msg: str) -> None:
    print(f"{Colors.GREEN}✓{Colors.RESET} {msg}")

def info(msg: str) -> None:
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {msg}")

def warning(msg: str) -> None:
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {msg}")

def error(msg: str) -> None:
    print(f"{Colors.RED}✗{Colors.RESET} {msg}")

def header(msg: str) -> None:
    print(f"\n{Colors.BOLD}{Colors.BLUE}{msg}{Colors.RESET}\n")

def find_skill_directories(skills_repo: Path) -> List[Path]:
    """Find all skill directories in the repository."""
    exclude_dirs = {'.git', '.github', 'node_modules', '.vscode', '__pycache__'}
    skill_dirs = []
    
    for item in skills_repo.iterdir():
        if not item.is_dir() or item.name in exclude_dirs:
            continue
        
        # Check if it's a skill directory (has SKILL.md or skill.md)
        if (item / 'SKILL.md').exists() or (item / 'skill.md').exists():
            skill_dirs.append(item)
    
    return sorted(skill_dirs, key=lambda x: x.name)

def install_skill(skill_path: Path, install_path: Path) -> bool:
    """Install a single skill."""
    skill_name = skill_path.name
    dest_path = install_path / skill_name
    
    try:
        # Check if skill already exists
        if dest_path.exists():
            warning(f"Skill '{skill_name}' already exists, updating...")
            shutil.rmtree(dest_path)
        
        # Copy skill directory
        shutil.copytree(skill_path, dest_path)
        success(f"Installed: {skill_name}")
        return True
    except Exception as e:
        error(f"Failed to install '{skill_name}': {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Install agent-skills for Claude Code, Gemini Code Assist, and Codex',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Install to current directory
  %(prog)s --global           # Install globally
  %(prog)s --target /path     # Install to specific directory
        """
    )
    
    parser.add_argument(
        '-g', '--global',
        action='store_true',
        dest='global_install',
        help='Install globally to ~/.codex/skills'
    )
    
    parser.add_argument(
        '-t', '--target',
        type=str,
        help='Install to specific directory'
    )
    
    parser.add_argument(
        '-s', '--skills-repo',
        type=str,
        default=None,
        help='Path to agent-skills repository (defaults to script directory)'
    )
    
    args = parser.parse_args()
    
    header("🚀 Agent Skills Installer")
    
    # Determine skills repository location
    if args.skills_repo:
        skills_repo = Path(args.skills_repo).resolve()
    else:
        skills_repo = Path(__file__).parent.resolve()
    
    # Verify source repository
    if not (skills_repo / 'AGENT.md').exists():
        error(f"Cannot find AGENT.md in {skills_repo}")
        error("Please run this script from the agent-skills repository or use --skills-repo option")
        sys.exit(1)
    
    success(f"Found agent-skills repository at: {skills_repo}")
    
    # Determine installation target
    if args.global_install:
        install_path = Path.home() / '.codex' / 'skills'
        info(f"Installing globally to: {install_path}")
    elif args.target:
        install_path = Path(args.target).resolve()
        info(f"Installing to custom location: {install_path}")
    else:
        install_path = Path.cwd() / '.codex' / 'skills'
        info(f"Installing to current project: {install_path}")
    
    # Create installation directory
    if not install_path.exists():
        info(f"Creating directory: {install_path}")
        install_path.mkdir(parents=True, exist_ok=True)
    
    # Find all skill directories
    skill_dirs = find_skill_directories(skills_repo)
    
    if not skill_dirs:
        error(f"No skills found in {skills_repo}")
        sys.exit(1)
    
    info(f"Found {len(skill_dirs)} skills to install")
    print()
    
    # Install each skill
    installed = 0
    skipped = 0
    
    for skill_path in skill_dirs:
        if install_skill(skill_path, install_path):
            installed += 1
        else:
            skipped += 1
    
    # Copy AGENT.md to the skills directory root
    try:
        agent_md_dest = install_path.parent / 'AGENT.md'
        shutil.copy2(skills_repo / 'AGENT.md', agent_md_dest)
        success("Copied AGENT.md configuration")
    except Exception as e:
        warning(f"Could not copy AGENT.md (this is optional): {e}")
    
    # Summary
    header("📊 Installation Summary")
    print(f"  {Colors.GREEN}Installed:{Colors.RESET} {installed} skills")
    if skipped > 0:
        print(f"  {Colors.YELLOW}Skipped:{Colors.RESET} {skipped} skills")
    print(f"  {Colors.BLUE}Location:{Colors.RESET} {install_path}")
    print()
    
    # Next steps
    header("✨ Next Steps")
    print("Your skills are now available to:")
    print(f"  • {Colors.BOLD}Claude Code{Colors.RESET} - Will auto-detect skills in .codex/skills/")
    print(f"  • {Colors.BOLD}Gemini Code Assist{Colors.RESET} - Will find skills via project context")
    print(f"  • {Colors.BOLD}Codex{Colors.RESET} - Will discover skills from .codex/skills/")
    print()
    print("To use a skill, simply mention its name or describe what you want to do.")
    print(f"Example: {Colors.BOLD}'Use the astro-developer skill to create a new blog'{Colors.RESET}")
    print()
    
    # Verify installation
    if installed > 0:
        success("Installation complete! 🎉")
        sys.exit(0)
    else:
        error("Installation failed - no skills were installed")
        sys.exit(1)

if __name__ == '__main__':
    main()
