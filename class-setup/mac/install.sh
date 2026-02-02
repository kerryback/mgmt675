#!/bin/bash
# MGMT 675 Development Environment Installer for macOS
# This script installs Python, VS Code, Git, GitHub CLI, Node.js, and Claude Code

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=============================================="
echo "  MGMT 675 Development Environment Installer"
echo "  for macOS"
echo "=============================================="
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to print status
print_status() {
    echo "[*] $1"
}

print_success() {
    echo "[+] $1"
}

print_warning() {
    echo "[!] $1"
}

# Check if running on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "Error: This script is for macOS only."
    exit 1
fi

# Step 1: Install Homebrew if not present
print_status "Checking for Homebrew..."
if ! command_exists brew; then
    print_status "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    fi
    print_success "Homebrew installed"
else
    print_success "Homebrew already installed"
fi

# Step 2: Install Python 3.12
print_status "Installing Python 3.12..."
if brew list python@3.12 &>/dev/null; then
    print_success "Python 3.12 already installed"
else
    brew install python@3.12
    print_success "Python 3.12 installed"
fi

# Step 3: Install Git
print_status "Installing Git..."
if brew list git &>/dev/null; then
    print_success "Git already installed"
else
    brew install git
    print_success "Git installed"
fi

# Step 4: Install GitHub CLI
print_status "Installing GitHub CLI..."
if brew list gh &>/dev/null; then
    print_success "GitHub CLI already installed"
else
    brew install gh
    print_success "GitHub CLI installed"
fi

# Step 5: Install Node.js
print_status "Installing Node.js..."
if brew list node &>/dev/null; then
    print_success "Node.js already installed"
else
    brew install node
    print_success "Node.js installed"
fi

# Step 6: Install VS Code
print_status "Installing VS Code..."
if [[ -d "/Applications/Visual Studio Code.app" ]]; then
    print_success "VS Code already installed"
else
    brew install --cask visual-studio-code
    print_success "VS Code installed"
fi

# Step 7: Install Claude Code
print_status "Installing Claude Code..."
if command_exists claude; then
    print_success "Claude Code already installed"
else
    npm install -g @anthropic-ai/claude-code
    print_success "Claude Code installed"
fi

# Step 8: Install VS Code extensions
print_status "Installing VS Code extensions..."
if command_exists code; then
    while IFS= read -r ext || [[ -n "$ext" ]]; do
        if [[ -n "$ext" && ! "$ext" =~ ^# ]]; then
            print_status "  Installing extension: $ext"
            code --install-extension "$ext" --force 2>/dev/null || print_warning "  Could not install $ext"
        fi
    done < "$SCRIPT_DIR/config/extensions.txt"
    print_success "VS Code extensions installed"
else
    print_warning "VS Code CLI not found. Please install extensions manually."
fi

# Step 9: Install Claude skills
print_status "Installing Claude skills..."
SKILLS_DEST="$HOME/.claude/skills"
mkdir -p "$SKILLS_DEST"
if [[ -d "$SCRIPT_DIR/skills" ]]; then
    cp -r "$SCRIPT_DIR/skills/"* "$SKILLS_DEST/" 2>/dev/null || true
    print_success "Claude skills installed to $SKILLS_DEST"
else
    print_warning "Skills folder not found"
fi

echo ""
echo "=============================================="
echo "  Installation Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "  1. Open a new terminal window"
echo "  2. Run 'gh auth login' to authenticate with GitHub"
echo "  3. Run 'claude' to start Claude Code and authenticate"
echo ""
echo "Installed software:"
echo "  - Python $(python3 --version 2>/dev/null | cut -d' ' -f2 || echo 'check version')"
echo "  - Git $(git --version 2>/dev/null | cut -d' ' -f3 || echo 'check version')"
echo "  - GitHub CLI $(gh --version 2>/dev/null | head -1 | cut -d' ' -f3 || echo 'check version')"
echo "  - Node.js $(node --version 2>/dev/null || echo 'check version')"
echo "  - VS Code"
echo "  - Claude Code"
echo ""
