#!/usr/bin/env bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

# Helper functions
success() { echo -e "${GREEN}✓${RESET} $1"; }
info() { echo -e "${BLUE}ℹ${RESET} $1"; }
warning() { echo -e "${YELLOW}⚠${RESET} $1"; }
error() { echo -e "${RED}✗${RESET} $1"; }
header() { echo -e "\n${BOLD}${BLUE}$1${RESET}\n"; }

# Parse arguments
GLOBAL=false
TARGET=""
SKILLS_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--global)
            GLOBAL=true
            shift
            ;;
        -t|--target)
            TARGET="$2"
            shift 2
            ;;
        -s|--skills-repo)
            SKILLS_REPO="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Install agent-skills for Claude Code, Gemini Code Assist, and Codex"
            echo ""
            echo "Options:"
            echo "  -g, --global          Install globally to ~/.codex/skills"
            echo "  -t, --target DIR      Install to specific directory"
            echo "  -s, --skills-repo DIR Path to agent-skills repository"
            echo "  -h, --help            Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Install to current directory"
            echo "  $0 --global           # Install globally"
            echo "  $0 --target /path     # Install to specific directory"
            exit 0
            ;;
        *)
            error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

header "🚀 Agent Skills Installer"

# Determine installation target
if [ "$GLOBAL" = true ]; then
    INSTALL_PATH="$HOME/.codex/skills"
    info "Installing globally to: $INSTALL_PATH"
elif [ -n "$TARGET" ]; then
    INSTALL_PATH="$TARGET"
    info "Installing to custom location: $INSTALL_PATH"
else
    INSTALL_PATH="$(pwd)/.codex/skills"
    info "Installing to current project: $INSTALL_PATH"
fi

# Verify source repository
if [ ! -f "$SKILLS_REPO/AGENT.md" ]; then
    error "Cannot find AGENT.md in $SKILLS_REPO"
    error "Please run this script from the agent-skills repository or use --skills-repo option"
    exit 1
fi

success "Found agent-skills repository at: $SKILLS_REPO"

# Create installation directory
if [ ! -d "$INSTALL_PATH" ]; then
    info "Creating directory: $INSTALL_PATH"
    mkdir -p "$INSTALL_PATH"
fi

# Get list of skill directories
EXCLUDE_DIRS=(".git" ".github" "node_modules" ".vscode" "__pycache__")
SKILL_DIRS=()

for dir in "$SKILLS_REPO"/*/; do
    dir_name=$(basename "$dir")
    
    # Skip excluded directories
    skip=false
    for exclude in "${EXCLUDE_DIRS[@]}"; do
        if [ "$dir_name" = "$exclude" ]; then
            skip=true
            break
        fi
    done
    
    if [ "$skip" = true ]; then
        continue
    fi
    
    # Check if it's a skill directory
    if [ -f "$dir/SKILL.md" ] || [ -f "$dir/skill.md" ]; then
        SKILL_DIRS+=("$dir")
    fi
done

if [ ${#SKILL_DIRS[@]} -eq 0 ]; then
    error "No skills found in $SKILLS_REPO"
    exit 1
fi

info "Found ${#SKILL_DIRS[@]} skills to install"
echo ""

# Copy each skill
INSTALLED=0
SKIPPED=0

for skill_path in "${SKILL_DIRS[@]}"; do
    skill_name=$(basename "$skill_path")
    dest_path="$INSTALL_PATH/$skill_name"
    
    # Check if skill already exists
    if [ -d "$dest_path" ]; then
        warning "Skill '$skill_name' already exists, updating..."
        rm -rf "$dest_path"
    fi
    
    # Copy skill directory
    if cp -r "$skill_path" "$dest_path"; then
        success "Installed: $skill_name"
        ((INSTALLED++))
    else
        error "Failed to install '$skill_name'"
        ((SKIPPED++))
    fi
done

# Copy AGENT.md to the skills directory root
if cp "$SKILLS_REPO/AGENT.md" "$(dirname "$INSTALL_PATH")/AGENT.md" 2>/dev/null; then
    success "Copied AGENT.md configuration"
else
    warning "Could not copy AGENT.md (this is optional)"
fi

# Summary
header "📊 Installation Summary"
echo -e "  ${GREEN}Installed:${RESET} $INSTALLED skills"
if [ $SKIPPED -gt 0 ]; then
    echo -e "  ${YELLOW}Skipped:${RESET} $SKIPPED skills"
fi
echo -e "  ${BLUE}Location:${RESET} $INSTALL_PATH"
echo ""

# Next steps
header "✨ Next Steps"
echo "Your skills are now available to:"
echo -e "  • ${BOLD}Claude Code${RESET} - Will auto-detect skills in .codex/skills/"
echo -e "  • ${BOLD}Gemini Code Assist${RESET} - Will find skills via project context"
echo -e "  • ${BOLD}Codex${RESET} - Will discover skills from .codex/skills/"
echo ""
echo "To use a skill, simply mention its name or describe what you want to do."
echo -e "Example: ${BOLD}'Use the astro-developer skill to create a new blog'${RESET}"
echo ""

# Verify installation
if [ $INSTALLED -gt 0 ]; then
    success "Installation complete! 🎉"
    exit 0
else
    error "Installation failed - no skills were installed"
    exit 1
fi
