# MGMT 675 Development Environment Installer for Windows ARM64
# This script installs Python, VS Code, Git, GitHub CLI, Node.js, and Claude Code
# Run this script as Administrator

#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"
$ProgressPreference = 'SilentlyContinue'  # Speed up downloads

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  MGMT 675 Development Environment Installer" -ForegroundColor Cyan
Write-Host "  for Windows ARM64" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Create temp directory for downloads
$TempDir = "$env:TEMP\mgmt675-setup"
if (Test-Path $TempDir) {
    Remove-Item -Recurse -Force $TempDir
}
New-Item -ItemType Directory -Force -Path $TempDir | Out-Null

function Write-Status {
    param([string]$Message)
    Write-Host "[*] $Message" -ForegroundColor White
}

function Write-Success {
    param([string]$Message)
    Write-Host "[+] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[!] $Message" -ForegroundColor Yellow
}

function Test-CommandExists {
    param([string]$Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

function Refresh-Path {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

# Step 1: Install Python 3.12 (ARM64)
Write-Status "Installing Python 3.12 (ARM64)..."
$PythonInstalled = Test-Path "C:\Program Files\Python312-arm64\python.exe" -or (Test-Path "C:\Program Files\Python312\python.exe")
if (-not $PythonInstalled) {
    $PythonUrl = "https://www.python.org/ftp/python/3.12.8/python-3.12.8-arm64.exe"
    $PythonInstaller = "$TempDir\python-3.12.8-arm64.exe"

    Write-Status "  Downloading Python 3.12 ARM64..."
    Invoke-WebRequest -Uri $PythonUrl -OutFile $PythonInstaller

    Write-Status "  Running Python installer..."
    Start-Process -Wait -FilePath $PythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0"

    Refresh-Path
    Write-Success "Python 3.12 installed"
} else {
    Write-Success "Python 3.12 already installed"
}

# Step 2: Install Git (x64 works on ARM via emulation - no native ARM build available)
Write-Status "Installing Git..."
$GitInstalled = Test-CommandExists "git"
if (-not $GitInstalled) {
    $GitUrl = "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe"
    $GitInstaller = "$TempDir\Git-2.47.1-64-bit.exe"

    Write-Status "  Downloading Git..."
    Invoke-WebRequest -Uri $GitUrl -OutFile $GitInstaller

    Write-Status "  Running Git installer..."
    Start-Process -Wait -FilePath $GitInstaller -ArgumentList "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"

    Refresh-Path
    Write-Success "Git installed"
} else {
    Write-Success "Git already installed"
}

# Step 3: Install GitHub CLI (ARM64)
Write-Status "Installing GitHub CLI..."
Refresh-Path
$GhInstalled = Test-CommandExists "gh"
if (-not $GhInstalled) {
    $GhUrl = "https://github.com/cli/cli/releases/download/v2.65.0/gh_2.65.0_windows_arm64.msi"
    $GhInstaller = "$TempDir\gh_2.65.0_windows_arm64.msi"

    Write-Status "  Downloading GitHub CLI ARM64..."
    Invoke-WebRequest -Uri $GhUrl -OutFile $GhInstaller

    Write-Status "  Running GitHub CLI installer..."
    Start-Process -Wait msiexec -ArgumentList "/i", "`"$GhInstaller`"", "/quiet", "/norestart"

    Refresh-Path
    Write-Success "GitHub CLI installed"
} else {
    Write-Success "GitHub CLI already installed"
}

# Step 4: Install Node.js (ARM64)
Write-Status "Installing Node.js (ARM64)..."
Refresh-Path
$NodeInstalled = Test-CommandExists "node"
if (-not $NodeInstalled) {
    $NodeUrl = "https://nodejs.org/dist/v22.13.1/node-v22.13.1-arm64.msi"
    $NodeInstaller = "$TempDir\node-v22.13.1-arm64.msi"

    Write-Status "  Downloading Node.js ARM64..."
    Invoke-WebRequest -Uri $NodeUrl -OutFile $NodeInstaller

    Write-Status "  Running Node.js installer..."
    Start-Process -Wait msiexec -ArgumentList "/i", "`"$NodeInstaller`"", "/quiet", "/norestart"

    Refresh-Path
    Write-Success "Node.js installed"
} else {
    Write-Success "Node.js already installed"
}

# Step 5: Install VS Code (ARM64)
Write-Status "Installing VS Code (ARM64)..."
$VSCodeInstalled = Test-Path "C:\Program Files\Microsoft VS Code\Code.exe"
if (-not $VSCodeInstalled) {
    $VSCodeUrl = "https://update.code.visualstudio.com/latest/win32-arm64/stable"
    $VSCodeInstaller = "$TempDir\VSCodeSetup-arm64.exe"

    Write-Status "  Downloading VS Code ARM64..."
    Invoke-WebRequest -Uri $VSCodeUrl -OutFile $VSCodeInstaller

    Write-Status "  Running VS Code installer..."
    Start-Process -Wait -FilePath $VSCodeInstaller -ArgumentList "/VERYSILENT", "/NORESTART", "/MERGETASKS=!runcode,addcontextmenufiles,addcontextmenufolders,addtopath"

    Refresh-Path
    Write-Success "VS Code installed"
} else {
    Write-Success "VS Code already installed"
}

# Step 6: Install Claude Code
Write-Status "Installing Claude Code..."
Refresh-Path
$ClaudeInstalled = Test-CommandExists "claude"
if (-not $ClaudeInstalled) {
    Write-Status "  Running npm install..."
    npm install -g @anthropic-ai/claude-code
    Refresh-Path
    Write-Success "Claude Code installed"
} else {
    Write-Success "Claude Code already installed"
}

# Step 7: Install VS Code extensions
Write-Status "Installing VS Code extensions..."
Refresh-Path
$CodePath = "C:\Program Files\Microsoft VS Code\bin\code.cmd"
if (Test-Path $CodePath) {
    $ExtensionsFile = Join-Path $ScriptDir "config\extensions.txt"
    if (Test-Path $ExtensionsFile) {
        Get-Content $ExtensionsFile | Where-Object { $_ -and $_ -notmatch "^#" } | ForEach-Object {
            $ext = $_.Trim()
            if ($ext) {
                Write-Status "  Installing extension: $ext"
                & $CodePath --install-extension $ext --force 2>$null
            }
        }
        Write-Success "VS Code extensions installed"
    } else {
        Write-Warning "Extensions file not found"
    }
} else {
    Write-Warning "VS Code CLI not found. Please install extensions manually."
}

# Step 8: Install Claude skills
Write-Status "Installing Claude skills..."
$SkillsSource = Join-Path $ScriptDir "skills"
$SkillsDest = "$env:USERPROFILE\.claude\skills"
if (Test-Path $SkillsSource) {
    New-Item -ItemType Directory -Force -Path $SkillsDest | Out-Null
    Copy-Item -Recurse -Force "$SkillsSource\*" $SkillsDest
    Write-Success "Claude skills installed to $SkillsDest"
} else {
    Write-Warning "Skills folder not found"
}

# Cleanup
Write-Status "Cleaning up temporary files..."
Remove-Item -Recurse -Force $TempDir -ErrorAction SilentlyContinue
Write-Success "Cleanup complete"

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Close and reopen PowerShell or Command Prompt"
Write-Host "  2. Run 'gh auth login' to authenticate with GitHub"
Write-Host "  3. Run 'claude' to start Claude Code and authenticate"
Write-Host ""
Write-Host "Installed software:" -ForegroundColor Yellow
Write-Host "  - Python 3.12 (ARM64)"
Write-Host "  - Git"
Write-Host "  - GitHub CLI (ARM64)"
Write-Host "  - Node.js (ARM64)"
Write-Host "  - VS Code (ARM64)"
Write-Host "  - Claude Code"
Write-Host ""
