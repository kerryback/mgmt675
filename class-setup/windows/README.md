# Windows Installation Instructions

## Quick Start (Recommended)

1. **Open PowerShell as Administrator**
   - Press `Win + X` and select "Windows PowerShell (Admin)" or "Terminal (Admin)"

2. **Navigate to this directory**
   ```powershell
   cd path\to\class-setup\windows
   ```

3. **Run the bootstrap script**
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\run.ps1
   ```

## Alternative Method (If Above Fails)

If you get an error about the script not being signed, use this method:

1. **Unblock the script files**
   ```powershell
   Unblock-File -Path .\install.ps1
   Unblock-File -Path .\run.ps1
   ```

2. **Set execution policy temporarily**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   ```

3. **Run the installer**
   ```powershell
   .\install.ps1
   ```

## Manual Copy-Paste Method (Most Reliable)

If both methods above fail, you can run the installer directly by copying the entire script content into PowerShell:

1. Open PowerShell as Administrator
2. Run this command to unblock and execute:
   ```powershell
   Get-Content .\install.ps1 | Out-String | Invoke-Expression
   ```

## What Gets Installed

This installer will install the following software:
- Python 3.12 (with pip)
- Git for Windows
- GitHub CLI
- Node.js (with npm)
- Visual Studio Code
- Claude Code (via npm)
- Koyeb CLI
- VS Code extensions (from config/extensions.txt)
- Claude skills (to ~/.claude/skills)

## Requirements

- Windows 10 or later (x64 or ARM64)
- Administrator privileges
- Internet connection

## Troubleshooting

### "Running scripts is disabled on this system"
This means your execution policy is too restrictive. Use the bootstrap script with the `-ExecutionPolicy Bypass` flag.

### "File is not digitally signed"
This is because the script isn't signed. Use the `Unblock-File` command or the bootstrap script which handles this automatically.

### "Access denied"
Make sure you're running PowerShell as Administrator.

### Tools not found after installation
Close and reopen PowerShell to refresh the PATH environment variable.

## Post-Installation

After installation completes:

1. **Close and reopen PowerShell** (to refresh PATH)
2. **Authenticate with GitHub**:
   ```powershell
   gh auth login
   ```
3. **Authenticate with Koyeb**:
   ```powershell
   koyeb login
   ```

### Using Claude Code

Claude Code is an AI coding assistant integrated into VS Code.

1. Open VS Code
2. Click the Claude icon in the sidebar (or press `Ctrl+Shift+P` and type "Claude")
3. On first launch, you'll be prompted to authenticate with your Anthropic account
4. Follow the browser prompts to sign in or create an account
5. Once authenticated, you can chat with Claude in the sidebar panel

### Using GitHub Copilot

GitHub Copilot is an AI coding assistant that provides code completions directly in VS Code.

1. Open VS Code
2. Click the Copilot icon in the sidebar (or press `Ctrl+Shift+I`)
3. Sign in with your GitHub account when prompted
4. GitHub Copilot Free provides 2,000 code completions and 50 chat messages per month

Once signed in, Copilot will automatically suggest code as you type. Press `Tab` to accept a suggestion.

## Support

If you continue to have issues, please report them to the course instructor.
