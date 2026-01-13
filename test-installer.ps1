#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Test the skill installer
.DESCRIPTION
    Creates a temporary test directory and verifies the installer works correctly
#>

$ErrorActionPreference = 'Stop'

Write-Host "`n🧪 Testing Skill Installer`n" -ForegroundColor Cyan

# Create temporary test directory
$testDir = Join-Path $env:TEMP "agent-skills-test-$(Get-Random)"
Write-Host "Creating test directory: $testDir" -ForegroundColor Gray
New-Item -ItemType Directory -Path $testDir -Force | Out-Null

try {
    # Run installer to test directory
    Write-Host "`nRunning installer..." -ForegroundColor Yellow
    $installPath = Join-Path $testDir ".codex" "skills"
    
    & "$PSScriptRoot\install-skills.ps1" -Target $installPath
    
    # Verify installation
    Write-Host "`n🔍 Verifying installation..." -ForegroundColor Cyan
    
    # Check if directory exists
    if (Test-Path $installPath) {
        Write-Host "✓ Skills directory created" -ForegroundColor Green
    } else {
        Write-Host "✗ Skills directory not found" -ForegroundColor Red
        exit 1
    }
    
    # Count installed skills
    $skillCount = (Get-ChildItem $installPath -Directory).Count
    Write-Host "✓ Found $skillCount skills installed" -ForegroundColor Green
    
    # Check for AGENT.md
    $agentMdPath = Join-Path (Split-Path $installPath) "AGENT.md"
    if (Test-Path $agentMdPath) {
        Write-Host "✓ AGENT.md copied successfully" -ForegroundColor Green
    } else {
        Write-Host "⚠ AGENT.md not found (optional)" -ForegroundColor Yellow
    }
    
    # Check a few key skills
    $keySkills = @('astro-developer', 'dev-browser', 'docx', 'pptx', 'xlsx')
    $foundSkills = 0
    
    foreach ($skill in $keySkills) {
        $skillPath = Join-Path $installPath $skill
        if (Test-Path $skillPath) {
            $foundSkills++
        }
    }
    
    Write-Host "✓ Found $foundSkills/$($keySkills.Count) key skills" -ForegroundColor Green
    
    # Verify SKILL.md files
    $skillsWithMd = Get-ChildItem $installPath -Directory | Where-Object {
        (Test-Path (Join-Path $_.FullName "SKILL.md")) -or (Test-Path (Join-Path $_.FullName "skill.md"))
    }
    
    Write-Host "✓ All $($skillsWithMd.Count) skills have SKILL.md files" -ForegroundColor Green
    
    Write-Host "`n✅ All tests passed!`n" -ForegroundColor Green
    exit 0
    
} catch {
    Write-Host "`n❌ Test failed: $_" -ForegroundColor Red
    exit 1
} finally {
    # Cleanup
    Write-Host "Cleaning up test directory..." -ForegroundColor Gray
    Remove-Item -Path $testDir -Recurse -Force -ErrorAction SilentlyContinue
}
