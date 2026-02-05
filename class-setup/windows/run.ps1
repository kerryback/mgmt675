# MGMT 675 Development Environment Installer for Windows
# This script installs Python, VS Code, Git, GitHub CLI, Node.js, Claude Code, Koyeb CLI, and Quarto
# Supports both x64 and ARM64 architectures (auto-detected)
# Run this script as Administrator

#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"
$ProgressPreference = 'SilentlyContinue'  # Speed up downloads

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Detect architecture
$Arch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture
$IsArm = $Arch -eq [System.Runtime.InteropServices.Architecture]::Arm64

if ($IsArm) {
    $ArchLabel = "ARM64"
    $PythonUrl = "https://www.python.org/ftp/python/3.12.8/python-3.12.8-arm64.exe"
    $PythonInstaller = "python-3.12.8-arm64.exe"
    $GhUrl = "https://github.com/cli/cli/releases/download/v2.65.0/gh_2.65.0_windows_arm64.msi"
    $GhInstaller = "gh_2.65.0_windows_arm64.msi"
    $NodeUrl = "https://nodejs.org/dist/v22.13.1/node-v22.13.1-arm64.msi"
    $NodeInstaller = "node-v22.13.1-arm64.msi"
    $VSCodeUrl = "https://update.code.visualstudio.com/latest/win32-arm64/stable"
    $VSCodeInstaller = "VSCodeSetup-arm64.exe"
    $KoyebUrl = "https://github.com/koyeb/koyeb-cli/releases/download/v5.9.0/koyeb-cli_5.9.0_windows_arm64.zip"
    $KoyebArchive = "koyeb-cli_5.9.0_windows_arm64.zip"
    $QuartoUrl = "https://github.com/quarto-dev/quarto-cli/releases/download/v1.6.42/quarto-1.6.42-win-arm64.msi"
    $QuartoInstaller = "quarto-1.6.42-win-arm64.msi"
} else {
    $ArchLabel = "x64"
    $PythonUrl = "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe"
    $PythonInstaller = "python-3.12.8-amd64.exe"
    $GhUrl = "https://github.com/cli/cli/releases/download/v2.65.0/gh_2.65.0_windows_amd64.msi"
    $GhInstaller = "gh_2.65.0_windows_amd64.msi"
    $NodeUrl = "https://nodejs.org/dist/v22.13.1/node-v22.13.1-x64.msi"
    $NodeInstaller = "node-v22.13.1-x64.msi"
    $VSCodeUrl = "https://update.code.visualstudio.com/latest/win32-x64/stable"
    $VSCodeInstaller = "VSCodeSetup-x64.exe"
    $KoyebUrl = "https://github.com/koyeb/koyeb-cli/releases/download/v5.9.0/koyeb-cli_5.9.0_windows_amd64.zip"
    $KoyebArchive = "koyeb-cli_5.9.0_windows_amd64.zip"
    $QuartoUrl = "https://github.com/quarto-dev/quarto-cli/releases/download/v1.6.42/quarto-1.6.42-win.msi"
    $QuartoInstaller = "quarto-1.6.42-win.msi"
}

# Git uses x64 for both (no native ARM build available, runs via emulation)
$GitUrl = "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe"
$GitInstaller = "Git-2.47.1-64-bit.exe"

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  MGMT 675 Development Environment Installer" -ForegroundColor Cyan
Write-Host "  for Windows ($ArchLabel)" -ForegroundColor Cyan
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

# Step 1: Install Python 3.12
Write-Status "Installing Python 3.12 ($ArchLabel)..."
$PythonInstalled = (Test-Path "C:\Program Files\Python312\python.exe") -or (Test-Path "C:\Program Files\Python312-arm64\python.exe")
if (-not $PythonInstalled) {
    $PythonPath = "$TempDir\$PythonInstaller"

    Write-Status "  Downloading Python 3.12 $ArchLabel..."
    Invoke-WebRequest -Uri $PythonUrl -OutFile $PythonPath

    Write-Status "  Running Python installer..."
    Start-Process -Wait -FilePath $PythonPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0"

    Refresh-Path
    Write-Success "Python 3.12 installed"
} else {
    Write-Success "Python 3.12 already installed"
}

# Step 2: Install Git (x64 for both architectures)
Write-Status "Installing Git..."
$GitInstalled = Test-CommandExists "git"
if (-not $GitInstalled) {
    $GitPath = "$TempDir\$GitInstaller"

    Write-Status "  Downloading Git..."
    Invoke-WebRequest -Uri $GitUrl -OutFile $GitPath

    Write-Status "  Running Git installer..."
    Start-Process -Wait -FilePath $GitPath -ArgumentList "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS"

    Refresh-Path
    Write-Success "Git installed"
} else {
    Write-Success "Git already installed"
}

# Step 3: Install GitHub CLI
Write-Status "Installing GitHub CLI ($ArchLabel)..."
Refresh-Path
$GhInstalled = Test-CommandExists "gh"
if (-not $GhInstalled) {
    $GhPath = "$TempDir\$GhInstaller"

    Write-Status "  Downloading GitHub CLI $ArchLabel..."
    Invoke-WebRequest -Uri $GhUrl -OutFile $GhPath

    Write-Status "  Running GitHub CLI installer..."
    Start-Process -Wait msiexec -ArgumentList "/i", "`"$GhPath`"", "/quiet", "/norestart"

    Refresh-Path
    Write-Success "GitHub CLI installed"
} else {
    Write-Success "GitHub CLI already installed"
}

# Step 4: Install Node.js
Write-Status "Installing Node.js ($ArchLabel)..."
Refresh-Path
$NodeInstalled = Test-CommandExists "node"
if (-not $NodeInstalled) {
    $NodePath = "$TempDir\$NodeInstaller"

    Write-Status "  Downloading Node.js $ArchLabel..."
    Invoke-WebRequest -Uri $NodeUrl -OutFile $NodePath

    Write-Status "  Running Node.js installer..."
    Start-Process -Wait msiexec -ArgumentList "/i", "`"$NodePath`"", "/quiet", "/norestart"

    Refresh-Path
    Write-Success "Node.js installed"
} else {
    Write-Success "Node.js already installed"
}

# Step 5: Install VS Code
Write-Status "Installing VS Code ($ArchLabel)..."
$VSCodeInstalled = Test-Path "C:\Program Files\Microsoft VS Code\Code.exe"
if (-not $VSCodeInstalled) {
    $VSCodePath = "$TempDir\$VSCodeInstaller"

    Write-Status "  Downloading VS Code $ArchLabel..."
    Invoke-WebRequest -Uri $VSCodeUrl -OutFile $VSCodePath

    Write-Status "  Running VS Code installer..."
    Start-Process -Wait -FilePath $VSCodePath -ArgumentList "/VERYSILENT", "/NORESTART", "/MERGETASKS=!runcode,addcontextmenufiles,addcontextmenufolders,addtopath"

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

# Step 7: Install Koyeb CLI
Write-Status "Installing Koyeb CLI ($ArchLabel)..."
Refresh-Path
$KoyebInstalled = Test-CommandExists "koyeb"
if (-not $KoyebInstalled) {
    $KoyebPath = "$TempDir\$KoyebArchive"
    $KoyebExtract = "$TempDir\koyeb"
    $KoyebDest = "C:\Program Files\Koyeb"

    Write-Status "  Downloading Koyeb CLI $ArchLabel..."
    Invoke-WebRequest -Uri $KoyebUrl -OutFile $KoyebPath

    Write-Status "  Extracting Koyeb CLI..."
    Expand-Archive -Path $KoyebPath -DestinationPath $KoyebExtract -Force

    Write-Status "  Installing Koyeb CLI..."
    New-Item -ItemType Directory -Force -Path $KoyebDest | Out-Null
    Copy-Item "$KoyebExtract\koyeb.exe" "$KoyebDest\koyeb.exe" -Force

    # Add to system PATH
    $CurrentPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($CurrentPath -notlike "*$KoyebDest*") {
        [System.Environment]::SetEnvironmentVariable("Path", "$CurrentPath;$KoyebDest", "Machine")
    }

    Refresh-Path
    Write-Success "Koyeb CLI installed"
} else {
    Write-Success "Koyeb CLI already installed"
}

# Step 8: Install Quarto
Write-Status "Installing Quarto ($ArchLabel)..."
Refresh-Path
$QuartoInstalled = Test-CommandExists "quarto"
if (-not $QuartoInstalled) {
    $QuartoPath = "$TempDir\$QuartoInstaller"

    Write-Status "  Downloading Quarto $ArchLabel..."
    Invoke-WebRequest -Uri $QuartoUrl -OutFile $QuartoPath

    Write-Status "  Running Quarto installer..."
    Start-Process -Wait msiexec -ArgumentList "/i", "`"$QuartoPath`"", "/quiet", "/norestart"

    Refresh-Path
    Write-Success "Quarto installed"
} else {
    Write-Success "Quarto already installed"
}

# Step 9: Install TinyTeX (LaTeX distribution for LaTeX Workshop)
Write-Status "Installing TinyTeX..."
Refresh-Path
$TinyTexInstalled = Test-Path "$env:APPDATA\TinyTeX\bin\windows\tlmgr.bat"
if (-not $TinyTexInstalled) {
    Write-Status "  Running quarto install tinytex..."
    quarto install tinytex --no-prompt
    Refresh-Path
    Write-Success "TinyTeX installed"
} else {
    Write-Success "TinyTeX already installed"
}

# Step 10: Install VS Code extensions
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

# Step 11: Install Claude skills
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

# Verification
Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  Verifying Installation" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

Refresh-Path
$AllGood = $true

Write-Status "Checking installed versions..."

# Check Python
try {
    $PyVersion = python --version 2>&1
    Write-Success "  Python: $PyVersion"
} catch {
    Write-Warning "  Python: NOT FOUND (may need to restart PowerShell)"
    $AllGood = $false
}

# Check Git
try {
    $GitVersion = git --version 2>&1
    Write-Success "  Git: $GitVersion"
} catch {
    Write-Warning "  Git: NOT FOUND"
    $AllGood = $false
}

# Check Node
try {
    $NodeVersion = node --version 2>&1
    Write-Success "  Node.js: $NodeVersion"
} catch {
    Write-Warning "  Node.js: NOT FOUND"
    $AllGood = $false
}

# Check GitHub CLI
try {
    $GhVersion = gh --version 2>&1 | Select-Object -First 1
    Write-Success "  GitHub CLI: $GhVersion"
} catch {
    Write-Warning "  GitHub CLI: NOT FOUND"
    $AllGood = $false
}

# Check Claude
try {
    $ClaudeVersion = claude --version 2>&1
    Write-Success "  Claude Code: $ClaudeVersion"
} catch {
    Write-Warning "  Claude Code: NOT FOUND"
    $AllGood = $false
}

# Check Koyeb
try {
    $KoyebVersion = koyeb version 2>&1
    Write-Success "  Koyeb CLI: $KoyebVersion"
} catch {
    Write-Warning "  Koyeb CLI: NOT FOUND"
    $AllGood = $false
}

# Check Quarto
try {
    $QuartoVersion = quarto --version 2>&1
    Write-Success "  Quarto: $QuartoVersion"
} catch {
    Write-Warning "  Quarto: NOT FOUND"
    $AllGood = $false
}

# Check TinyTeX
if (Test-Path "$env:APPDATA\TinyTeX\bin\windows\tlmgr.bat") {
    Write-Success "  TinyTeX: installed"
} else {
    Write-Warning "  TinyTeX: NOT FOUND"
    $AllGood = $false
}

Write-Host ""
if ($AllGood) {
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "  Installation Complete!" -ForegroundColor Green
    Write-Host "==============================================" -ForegroundColor Cyan
} else {
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host "  Installation Complete (with warnings)" -ForegroundColor Yellow
    Write-Host "==============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Some components may not be available until you" -ForegroundColor Yellow
    Write-Host "close and reopen PowerShell." -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Close and reopen PowerShell or Command Prompt"
Write-Host "  2. Run 'gh auth login' to authenticate with GitHub"
Write-Host "  3. Run 'claude' to start Claude Code and authenticate"
Write-Host "  4. Run 'koyeb login' to authenticate with Koyeb"
Write-Host ""
Write-Host "Installed software:" -ForegroundColor Yellow
Write-Host "  - Python 3.12 ($ArchLabel)"
Write-Host "  - Git"
Write-Host "  - GitHub CLI ($ArchLabel)"
Write-Host "  - Node.js ($ArchLabel)"
Write-Host "  - VS Code ($ArchLabel)"
Write-Host "  - Claude Code"
Write-Host "  - Koyeb CLI ($ArchLabel)"
Write-Host "  - Quarto ($ArchLabel)"
Write-Host "  - TinyTeX (LaTeX)"
Write-Host ""
