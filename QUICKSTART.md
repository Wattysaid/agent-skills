# Quick Start: Installing Agent Skills

## One-Line Install

### Windows
```powershell
cd agent-skills; .\install-skills.ps1
```

### macOS/Linux
```bash
cd agent-skills && chmod +x install-skills.sh && ./install-skills.sh
```

### Any Platform (Python)
```bash
cd agent-skills && python install-skills.py
```

## What Happens Next

After running the installer, you'll see:

```
🚀 Agent Skills Installer

ℹ Installing to current project: ./codex/skills
✓ Found agent-skills repository
✓ Installed: astro-developer
✓ Installed: dev-browser
... (25 skills total)
✓ Installation complete! 🎉
```

## Using Your Skills

Just mention them in conversation:

```
"Use astro-developer to create a blog"
"Help me create a PDF report"
"Analyze this spreadsheet"
"Make a presentation about Q4 results"
```

Your AI assistant will automatically load and use the appropriate skill!

## Global vs Local

**Local** (default): Skills available in current project only
```powershell
.\install-skills.ps1
```

**Global**: Skills available in all projects
```powershell
.\install-skills.ps1 -Global
```

## That's It!

You're ready to use all 25+ skills with Claude Code, Gemini, and Codex.

Need help? See [INSTALLER.md](INSTALLER.md) for detailed docs.
