---
name: skill-installer
description: Install agent-skills for Claude Code, Gemini Code Assist, and Codex
version: "1.0.0"
author: "GitHub Copilot"
---

# Skill Installer

## Purpose
- **Use when:** You need to install agent-skills to make them available to AI assistants
- **Goal:** To install skills to the correct location where Claude Code, Gemini Code Assist, and Codex can discover them

## Triggers
- "Install skills"
- "Set up agent skills"
- "How do I install these skills?"
- "Make skills available to Claude/Gemini/Codex"
- "Configure skills"

## Workflow

### 1. Choose Installation Method
Select the appropriate installer based on the user's platform:
- **Windows**: Use `install-skills.ps1` (PowerShell)
- **macOS/Linux**: Use `install-skills.sh` (Bash)
- **Cross-platform**: Use `install-skills.py` (Python)

### 2. Determine Installation Scope
Ask the user where they want to install:
- **Local** (default): Current project's `.codex/skills/`
- **Global**: User's home directory `~/.codex/skills/`
- **Custom**: Specific directory path

### 3. Run the Installer

#### PowerShell (Windows)
```powershell
# Local installation
.\install-skills.ps1

# Global installation
.\install-skills.ps1 -Global

# Custom location
.\install-skills.ps1 -Target "C:\MyProject\.codex\skills"
```

#### Bash (macOS/Linux)
```bash
# Make executable (first time only)
chmod +x install-skills.sh

# Local installation
./install-skills.sh

# Global installation
./install-skills.sh --global

# Custom location
./install-skills.sh --target /path/to/project/.codex/skills
```

#### Python (Cross-platform)
```bash
# Local installation
python install-skills.py

# Global installation
python install-skills.py --global

# Custom location
python install-skills.py --target /path/to/project/.codex/skills
```

### 4. Verify Installation
The installer will:
1. Find all skill directories in the repository
2. Copy each skill with all its files
3. Copy AGENT.md configuration
4. Display installation summary
5. Provide next steps

### 5. Test Skills
After installation, test by:
- Mentioning a skill by name
- Describing a task that matches a skill
- Verifying the AI assistant loads the skill

## What Gets Installed

The installer copies:
- All skill directories with `SKILL.md` files
- Each skill's complete structure:
  - `SKILL.md` - Main instructions
  - `references/` - Documentation
  - `scripts/` - Helper scripts
  - `assets/` - Templates and components
- `AGENT.md` - Skill catalog configuration

## Installation Locations

### Local Installation
```
your-project/
  .codex/
    AGENT.md
    skills/
      astro-developer/
      dev-browser/
      docx/
      ... (all other skills)
```

### Global Installation
```
~/.codex/
  AGENT.md
  skills/
    astro-developer/
    dev-browser/
    docx/
    ... (all other skills)
```

## AI Assistant Detection

After installation, skills are automatically discovered:

### Claude Code
- Scans `.codex/skills/` directory
- Reads `AGENT.md` for skill catalog
- Loads skills based on user requests
- Uses `<available_skills>` section for routing

### Gemini Code Assist
- Discovers skills via project context
- Uses skill metadata for capability matching
- Activates skills when mentioned or needed

### Codex
- Looks for `.codex/skills/` directory
- Reads individual `SKILL.md` files
- Loads skills on demand based on description matching

## Updating Skills

To update installed skills:
1. Pull latest changes from agent-skills repository
2. Run the installer again (same command)
3. Installer will detect existing skills and update them

```bash
# Example update workflow
cd agent-skills
git pull
.\install-skills.ps1  # or ./install-skills.sh or python install-skills.py
```

## Troubleshooting

### Skills Not Detected
1. **Verify installation path**: Check `.codex/skills/` exists
2. **Check AGENT.md**: Ensure `.codex/AGENT.md` is present
3. **Restart IDE**: Close and reopen your editor
4. **Explicit loading**: Try "Load the [skill-name] skill"

### Permission Issues
- **Windows**: Run PowerShell as Administrator if needed
- **macOS/Linux**: Use `sudo` if installing to protected directories
- **Alternative**: Use local installation (no permissions needed)

### Installer Errors
- **"AGENT.md not found"**: Run from agent-skills directory
- **"No skills found"**: Check repository structure
- **Copy failures**: Ensure write permissions on target directory

## Examples

### Example 1: First-time Installation
```powershell
# User wants to install skills locally
cd d:\GitHub\agent-skills
.\install-skills.ps1

# Output:
# 🚀 Agent Skills Installer
# ℹ Installing to current project: D:\GitHub\myproject\.codex\skills
# ✓ Found agent-skills repository at: D:\GitHub\agent-skills
# ✓ Installed: astro-developer
# ✓ Installed: dev-browser
# ... (all skills)
# ✓ Installation complete! 🎉
```

### Example 2: Global Installation
```bash
# User wants skills available to all projects
cd ~/projects/agent-skills
./install-skills.sh --global

# Skills installed to ~/.codex/skills/
# Available to all projects automatically
```

### Example 3: Custom Location
```python
# User has specific project structure
cd /projects/agent-skills
python install-skills.py --target /projects/my-app/.codex/skills

# Skills installed exactly where needed
```

## Safety & Guardrails

### File Safety
- Installer creates directories if they don't exist
- Existing skills are backed up before overwrite (by deletion then copy)
- No files outside target directory are modified

### Validation
- Verifies AGENT.md exists before starting
- Checks each skill has SKILL.md file
- Confirms write permissions before copying
- Provides detailed error messages

### Rollback
To uninstall/rollback:
```bash
# Remove skills directory
rm -rf .codex/skills

# Or on Windows
Remove-Item -Recurse -Force .codex/skills
```

## Platform Support

| Platform | PowerShell | Bash | Python |
|----------|-----------|------|--------|
| Windows 11/10 | ✅ Primary | ✅ WSL/Git Bash | ✅ |
| macOS | ✅ | ✅ Primary | ✅ |
| Linux | ✅ | ✅ Primary | ✅ |

## Related Files

- `install-skills.ps1` - PowerShell installer (Windows)
- `install-skills.sh` - Bash installer (macOS/Linux)
- `install-skills.py` - Python installer (cross-platform)
- `INSTALLER.md` - Detailed installation guide
- `AGENT.md` - Skill catalog configuration
- `README.md` - Quick start guide

## Best Practices

1. **Use local installation for project-specific skills**
   - Keeps skills with project
   - Easy to version control
   - Portable across machines

2. **Use global installation for personal workflows**
   - Available to all projects
   - Consistent experience
   - One-time setup

3. **Update regularly**
   - Pull latest agent-skills
   - Re-run installer
   - Test key skills

4. **Verify after installation**
   - Check directory structure
   - Try loading a skill
   - Confirm AI assistant recognizes skills

## Notes

- First installation may take 10-30 seconds depending on skill count
- Updates are faster (only changed files)
- Global installation requires write permissions to home directory
- Skills work offline once installed (except those requiring API keys)
