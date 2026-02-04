# MGMT 675 Development Environment Setup

This package installs the development environment for MGMT 675.

## Requirements

Before you begin, ensure you have:

- **Internet connection** - The installer downloads software (~500 MB)
- **Disk space** - At least 3 GB of free disk space
- **Administrator access** - Required to install software

## What Gets Installed

- **Python 3.12** - Programming language
- **VS Code** - Code editor
- **Git** - Version control
- **GitHub CLI** - Command-line interface for GitHub
- **Node.js** - JavaScript runtime (required for Claude Code)
- **Claude Code** - AI coding assistant
- **Koyeb CLI** - Command-line interface for Koyeb serverless platform

### VS Code Extensions

- Python
- Jupyter
- Claude Code
- GitHub Copilot
- LaTeX Workshop
- Quarto

### Claude Skills

Pre-configured skills for working with:
- Excel spreadsheets (xlsx)
- Word documents (docx)
- PowerPoint presentations (pptx)

## Installation Instructions

### Windows

1. **Extract the zip file** to a folder on your computer (e.g., your Downloads folder)

2. **Open PowerShell as Administrator**
   - Press `Win + X` and select "Windows Terminal (Admin)" or "PowerShell (Admin)"
   - Or search for PowerShell, right-click, and select "Run as administrator"

3. **Navigate to the extracted folder** (the folder containing `install.ps1`)
   ```powershell
   cd "C:\Users\YourName\Downloads\class-setup-windows"
   ```
   Replace `YourName` with your Windows username and adjust the path if you extracted elsewhere.

4. **Enable script execution** (if needed)
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

5. **Run the installer**
   ```powershell
   .\install.ps1
   ```

6. **Wait for installation to complete** (this may take several minutes)

### macOS

1. **Extract the zip file** to a folder on your computer (e.g., your Downloads folder)
   - Double-click the zip file to extract it

2. **Open Terminal**
   - Press `Cmd + Space`, type "Terminal", and press Enter

3. **Navigate to the extracted folder** (the folder containing `install.sh`)
   ```bash
   cd ~/Downloads/class-setup-mac
   ```
   Adjust the path if you extracted elsewhere.

4. **Make the script executable**
   ```bash
   chmod +x install.sh
   ```

5. **Run the installer**
   ```bash
   ./install.sh
   ```

6. **Wait for installation to complete** (this may take several minutes)

## Post-Installation Steps

### 1. Authenticate with GitHub

Open a new terminal/PowerShell window and run:

```bash
gh auth login
```

Follow the prompts to authenticate with your GitHub account.

### 2. Sign in to Claude Code

Claude Code is an AI coding assistant integrated into VS Code.

1. Open VS Code
2. Click the Claude icon in the sidebar (or press `Ctrl+Shift+P` on Windows, `Cmd+Shift+P` on Mac and type "Claude")
3. On first launch, you'll be prompted to authenticate with your Anthropic account
4. Follow the browser prompts to sign in or create an account (free)
5. Once authenticated, you can chat with Claude in the sidebar panel

### 3. Sign in to GitHub Copilot

GitHub Copilot provides AI-powered code completions directly in VS Code.

1. Open VS Code
2. Click the Copilot icon in the sidebar (or press `Ctrl+Shift+I` on Windows, `Cmd+Shift+I` on Mac)
3. Sign in with your GitHub account when prompted
4. GitHub Copilot Free provides 2,000 code completions and 50 chat messages per month

Once signed in, Copilot will automatically suggest code as you type. Press `Tab` to accept a suggestion.

### 4. Authenticate with Koyeb

Run the Koyeb CLI to authenticate:

```bash
koyeb login
```

This will open a browser window to authenticate with your Koyeb account.

## Troubleshooting

### "Script execution is disabled" (Windows)

Run this command in PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Command not found" after installation

Close and reopen your terminal/PowerShell window to refresh the PATH.

### Python not recognized (Windows)

If `python` is not recognized after installation:

1. Close and reopen PowerShell
2. If still not working, manually add Python to your PATH:
   - Press `Win + I` to open Settings
   - Search for "environment variables"
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Add `C:\Program Files\Python312` and `C:\Program Files\Python312\Scripts`
   - Click OK to save and restart PowerShell

### VS Code extensions not installing

Open VS Code and install extensions manually:
1. Press `Ctrl+Shift+X` (Windows) or `Cmd+Shift+X` (Mac)
2. Search for each extension and click Install

### Permission denied (macOS)

Make sure the script is executable:
```bash
chmod +x install.sh
```

## Need Help?

Contact your instructor if you encounter any issues during installation.
