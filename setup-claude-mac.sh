#!/bin/bash
# Setup script for MGMT 675 students - Mac/Linux
# Configures Claude Code to use the course LiteLLM proxy

echo "Setting up Claude Code for MGMT 675..."

# Ensure ~/.local/bin is on PATH (needed for claude CLI)
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    export PATH="$HOME/.local/bin:$PATH"
    echo "Added ~/.local/bin to PATH in ~/.zshrc"
fi

CLAUDE_DIR="$HOME/.claude"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"

# Create .claude directory if it doesn't exist
if [ ! -d "$CLAUDE_DIR" ]; then
    mkdir -p "$CLAUDE_DIR"
    echo "Created .claude directory"
fi

# Check if settings.json exists
if [ -f "$SETTINGS_FILE" ]; then
    echo "Found existing settings.json"
    echo "Creating backup at $SETTINGS_FILE.backup"
    cp "$SETTINGS_FILE" "$SETTINGS_FILE.backup"
fi

# Create the settings.json file
cat > "$SETTINGS_FILE" << 'EOF'
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://litellm-kerrybackapps-cd4f3edf.koyeb.app",
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-mgmt675-2026",
    "ANTHROPIC_API_KEY": "",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "course-model",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "course-model",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "course-model",
    "CLAUDE_CODE_SUBAGENT_MODEL": "course-model"
  }
}
EOF

echo ""
echo "Setup complete! Claude Code is now configured for MGMT 675."
echo ""
echo "Your settings file: $SETTINGS_FILE"
echo ""
read -p "Press Enter to continue..."
