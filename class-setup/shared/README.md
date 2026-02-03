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

### VS Code Extensions

- Python
- Jupyter
- Claude Code
- LaTeX Workshop
- Quarto

### Claude Skills

Pre-configured skills for working with:
- Excel spreadsheets (xlsx)
- Word documents (docx)
- PowerPoint presentations (pptx)
- Rice Data Portal database

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

### 2. Authenticate with Claude

Run Claude Code for the first time:

```bash
claude
```

This will:
1. Open a browser window to the Anthropic website
2. Prompt you to sign in or create an Anthropic account (free)
3. Ask you to authorize Claude Code to use your account

After authorizing, return to your terminal. Claude Code is now ready to use in VS Code.

### 3. Set up your Rice Data Portal token (if using database skills)

Create a `.env` file in your project folder with your Rice Data Portal access token:

```
RICE_ACCESS_TOKEN=your_token_here
```

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
