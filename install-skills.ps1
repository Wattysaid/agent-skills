#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Installs agent-skills for Claude Code, Gemini Code Assist, and Codex.

.DESCRIPTION
    This installer copies skills to the appropriate location where AI coding assistants
    can discover and use them. Works with Claude Code, Gemini, and Codex.

.PARAMETER Target
    Installation target directory. Defaults to current directory's .codex/skills

.PARAMETER Global
    Install globally to user's home directory for all projects

.PARAMETER SkillsRepo
    Path to the agent-skills repository. Defaults to current directory

.EXAMPLE
    .\install-skills.ps1
    Installs skills to current directory's .codex/skills

.EXAMPLE
    .\install-skills.ps1 -Global
    Installs skills globally to ~/.codex/skills

.EXAMPLE
    .\install-skills.ps1 -Target "C:\MyProject\.codex\skills"
    Installs skills to specific directory
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Target,
    
    [Parameter(Mandatory=$false)]
    [switch]$Global,
    
    [Parameter(Mandatory=$false)]
    [string]$SkillsRepo = $PSScriptRoot
)

# ANSI color codes
$Green = "`e[32m"
$Blue = "`e[34m"
$Yellow = "`e[33m"
$Red = "`e[31m"
$Reset = "`e[0m"
$Bold = "`e[1m"

function Write-Success { param([string]$msg) Write-Host "${Green}✓${Reset} $msg" }
function Write-Info { param([string]$msg) Write-Host "${Blue}ℹ${Reset} $msg" }
function Write-Warning { param([string]$msg) Write-Host "${Yellow}⚠${Reset} $msg" }
function Write-Error { param([string]$msg) Write-Host "${Red}✗${Reset} $msg" }
function Write-Header { param([string]$msg) Write-Host "`n${Bold}${Blue}$msg${Reset}`n" }

Write-Header "🚀 Agent Skills Installer"

# Determine installation target
if ($Global) {
    $installPath = Join-Path $env:USERPROFILE ".codex" "skills"
    Write-Info "Installing globally to: $installPath"
} elseif ($Target) {
    $installPath = $Target
    Write-Info "Installing to custom location: $installPath"
} else {
    $installPath = Join-Path (Get-Location) ".codex" "skills"
    Write-Info "Installing to current project: $installPath"
}

# Verify source repository
if (-not (Test-Path (Join-Path $SkillsRepo "AGENT.md"))) {
    Write-Error "Cannot find AGENT.md in $SkillsRepo"
    Write-Error "Please run this script from the agent-skills repository or use -SkillsRepo parameter"
    exit 1
}

Write-Success "Found agent-skills repository at: $SkillsRepo"

# Create installation directory
if (-not (Test-Path $installPath)) {
    Write-Info "Creating directory: $installPath"
    New-Item -ItemType Directory -Path $installPath -Force | Out-Null
}

# Get list of skill directories (exclude specific directories)
$excludeDirs = @('.git', '.github', 'node_modules', '.vscode', '__pycache__')
$skillDirs = Get-ChildItem -Path $SkillsRepo -Directory | Where-Object {
    $_.Name -notin $excludeDirs -and ((Test-Path (Join-Path $_.FullName "SKILL.md")) -or (Test-Path (Join-Path $_.FullName "skill.md")))
}

if ($skillDirs.Count -eq 0) {
    Write-Error "No skills found in $SkillsRepo"
    exit 1
}

Write-Info "Found $($skillDirs.Count) skills to install"
Write-Host ""

# Copy each skill
$installed = 0
$skipped = 0

foreach ($skillDir in $skillDirs) {
    $skillName = $skillDir.Name
    $sourcePath = $skillDir.FullName
    $destPath = Join-Path $installPath $skillName
    
    try {
        # Check if skill already exists
        if (Test-Path $destPath) {
            Write-Warning "Skill '$skillName' already exists, updating..."
            Remove-Item -Path $destPath -Recurse -Force
        }
        
        # Copy skill directory
        Copy-Item -Path $sourcePath -Destination $destPath -Recurse -Force
        Write-Success "Installed: $skillName"
        $installed++
    }
    catch {
        Write-Error "Failed to install '$skillName': $_"
        $skipped++
    }
}

# Copy AGENT.md to the skills directory root
try {
    Copy-Item -Path (Join-Path $SkillsRepo "AGENT.md") -Destination (Join-Path $installPath ".." "AGENT.md") -Force
    Write-Success "Copied AGENT.md configuration"
}
catch {
    Write-Warning "Could not copy AGENT.md: $_"
}

# Summary
Write-Header "📊 Installation Summary"
Write-Host "  ${Green}Installed:${Reset} $installed skills"
if ($skipped -gt 0) {
    Write-Host "  ${Yellow}Skipped:${Reset} $skipped skills"
}
Write-Host "  ${Blue}Location:${Reset} $installPath"
Write-Host ""

# Next steps
Write-Header "✨ Next Steps"
Write-Host "Your skills are now available to:"
Write-Host "  • ${Bold}Claude Code${Reset} - Will auto-detect skills in .codex/skills/"
Write-Host "  • ${Bold}Gemini Code Assist${Reset} - Will find skills via project context"
Write-Host "  • ${Bold}Codex${Reset} - Will discover skills from .codex/skills/"
Write-Host ""
Write-Host "To use a skill, simply mention its name or describe what you want to do."
Write-Host "Example: ${Bold}'Use the astro-developer skill to create a new blog'${Reset}"
Write-Host ""

# Verify installation
if ($installed -gt 0) {
    Write-Success "Installation complete! 🎉"
    exit 0
} else {
    Write-Error "Installation failed - no skills were installed"
    exit 1
}
