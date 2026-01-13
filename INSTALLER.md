# Skills Installer

Cross-platform installer for agent-skills that works with Claude Code, Gemini Code Assist, and Codex.

## Quick Start

### Windows (PowerShell)
```powershell
.\install-skills.ps1
```

### macOS/Linux (Bash)
```bash
chmod +x install-skills.sh
./install-skills.sh
```

### Cross-Platform (Python)
```bash
python install-skills.py
```

## Installation Options

### Local Installation (Default)
Installs skills to the current project's `.codex/skills` directory:

```bash
# PowerShell
.\install-skills.ps1

# Bash
./install-skills.sh

# Python
python install-skills.py
```

### Global Installation
Installs skills to your user directory (`~/.codex/skills`) for all projects:

```bash
# PowerShell
.\install-skills.ps1 -Global

# Bash
./install-skills.sh --global

# Python
python install-skills.py --global
```

### Custom Location
Install to a specific directory:

```bash
# PowerShell
.\install-skills.ps1 -Target "C:\MyProject\.codex\skills"

# Bash
./install-skills.sh --target /path/to/project/.codex/skills

# Python
python install-skills.py --target /path/to/project/.codex/skills
```

## How It Works

The installer:

1. **Discovers all skills** in the agent-skills repository
2. **Creates the target directory** (`.codex/skills/` or custom path)
3. **Copies each skill directory** with all its files (SKILL.md, references/, scripts/, assets/)
4. **Copies AGENT.md** configuration to `.codex/AGENT.md`
5. **Verifies installation** and provides a summary

## AI Assistant Detection

Once installed, your skills are automatically discovered by:

### Claude Code
- Looks for skills in `.codex/skills/` directory
- Reads `AGENT.md` for skill catalog
- Auto-loads skills based on user requests

### Gemini Code Assist
- Discovers skills via project context
- Uses skill metadata for routing
- Activates skills when mentioned

### Codex
- Scans `.codex/skills/` directory
- Reads `SKILL.md` files for capabilities
- Loads skills on demand

## Using Skills

After installation, simply mention a skill by name or describe what you want to do:

```
"Use the astro-developer skill to create a new blog"
"Create a PDF report" (triggers pdf skill)
"Help me with process mining" (triggers process-mining-assistant skill)
"Make a presentation" (triggers pptx skill)
```

## Updating Skills

To update skills, simply run the installer again. It will:
- Detect existing skills
- Remove old versions
- Install updated versions

```bash
# Re-run any installer
.\install-skills.ps1  # PowerShell
./install-skills.sh   # Bash
python install-skills.py  # Python
```

## Troubleshooting

### Permission Denied (Bash/macOS/Linux)
Make the script executable:
```bash
chmod +x install-skills.sh
```

### Skills Not Detected
1. Verify installation location: Check that skills are in `.codex/skills/`
2. Check AGENT.md: Ensure it's in `.codex/AGENT.md`
3. Restart your AI assistant or IDE
4. Try mentioning a skill explicitly: "Load the docx skill"

### Installation Failed
- Ensure you have write permissions to the target directory
- Run with elevated permissions if needed (sudo/Administrator)
- Check that you're running from the agent-skills repository

## Advanced Options

### Install from Different Repository Location
```bash
# PowerShell
.\install-skills.ps1 -SkillsRepo "D:\other\agent-skills"

# Bash
./install-skills.sh --skills-repo /path/to/agent-skills

# Python
python install-skills.py --skills-repo /path/to/agent-skills
```

### Uninstall Skills
Simply delete the `.codex/skills` directory:

```bash
# PowerShell
Remove-Item -Recurse -Force .codex/skills

# Bash/Python
rm -rf .codex/skills
```

## Platform Support

| Platform | PowerShell | Bash | Python |
|----------|-----------|------|--------|
| Windows | ✅ | ✅ (WSL/Git Bash) | ✅ |
| macOS | ✅ | ✅ | ✅ |
| Linux | ✅ | ✅ | ✅ |

## What Gets Installed

Each skill directory includes:
- `SKILL.md` - Main skill instructions
- `references/` - Deep-dive documentation
- `scripts/` - Helper scripts and tools
- `assets/` - Templates and reusable components

Plus the configuration file:
- `AGENT.md` - Skill catalog and routing information

## Contributing

If you create new skills or update existing ones:
1. Add/update the skill directory
2. Update `AGENT.md` with skill entry
3. Run the installer to test
4. Submit a pull request

## License

See LICENSE.txt in individual skill directories.
