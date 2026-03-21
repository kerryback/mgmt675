#!/bin/bash
# MGMT 675 Development Environment Installer for macOS
# Installs Python, Claude Desktop, Claude Code, and Claude skills

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

# Step 3: Install Python packages
print_status "Installing Python packages..."
pip3 install --no-warn-script-location -q \
    numpy pandas matplotlib statsmodels scikit-learn \
    pandas-datareader yfinance requests cvxpy 2>/dev/null
print_success "Python packages installed"

# Step 4: Install Claude Desktop
print_status "Installing Claude Desktop..."
if [[ -d "/Applications/Claude.app" ]]; then
    print_success "Claude Desktop already installed"
else
    brew install --cask claude
    print_success "Claude Desktop installed"
fi

# Step 5: Install Claude Code (terminal)
print_status "Installing Claude Code (terminal)..."
if command_exists claude; then
    print_success "Claude Code already installed: $(claude --version 2>&1)"
else
    curl -fsSL https://claude.ai/install.sh | bash
    # Reload PATH
    export PATH="$HOME/.local/bin:$PATH"
    if command_exists claude; then
        print_success "Claude Code installed: $(claude --version 2>&1)"
    else
        print_success "Claude Code installed (open a new terminal to use 'claude' command)"
    fi
fi

# Verification
echo ""
echo "=============================================="
echo "  Verifying Installation"
echo "=============================================="
echo ""

ALL_GOOD=true

print_status "Checking installed versions..."

# Check Python
if command_exists python3; then
    print_success "  Python: $(python3 --version 2>&1)"
else
    print_warning "  Python: NOT FOUND"
    ALL_GOOD=false
fi

# Check Claude Desktop
if [[ -d "/Applications/Claude.app" ]]; then
    print_success "  Claude Desktop: installed"
else
    print_warning "  Claude Desktop: NOT FOUND"
    ALL_GOOD=false
fi

# Check Claude Code CLI
if command_exists claude; then
    print_success "  Claude Code (terminal): $(claude --version 2>&1)"
else
    print_warning "  Claude Code (terminal): not yet in PATH (open a new terminal)"
fi

echo ""
if [ "$ALL_GOOD" = true ]; then
    echo "=============================================="
    echo "  Installation Complete!"
    echo "=============================================="
else
    echo "=============================================="
    echo "  Installation Complete (with warnings)"
    echo "=============================================="
    echo ""
    echo "Some components may not be available until you"
    echo "open a new terminal window."
fi
echo ""
echo "Next steps:"
echo "  1. Open Claude Desktop and sign in with your Anthropic account"
echo "  2. Click the Code tab to start using Claude Code"
echo "  3. Or open a terminal and type 'claude' to use Claude Code in the terminal"
echo ""
echo "Installed software:"
echo "  - Python 3.12"
echo "  - Claude Desktop"
echo "  - Claude Code (terminal)"
echo ""
