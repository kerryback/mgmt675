# MGMT 675 Development Environment Installer for Windows (no Python libraries)
# Installs Python, Git for Windows, Claude Desktop, and Claude Code
# Supports both x64 and ARM64 architectures (auto-detected)

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
} else {
    $ArchLabel = "x64"
    $PythonUrl = "https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe"
    $PythonInstaller = "python-3.12.8-amd64.exe"
}

$ClaudeDesktopUrl = "https://downloads.claude.ai/releases/win32/ClaudeSetup.exe"

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

# Step 2: Install Git for Windows
Write-Status "Installing Git for Windows..."
if (-not (Test-CommandExists "git")) {
    Write-Status "  Downloading Git for Windows..."
    try {
        # Fetch latest release from GitHub API
        $GitRelease = Invoke-WebRequest -Uri "https://api.github.com/repos/git-for-windows/git/releases/latest" -UseBasicParsing | ConvertFrom-Json
        $GitAsset = $GitRelease.assets | Where-Object { $_.name -match "Git-.*-64-bit\.exe$" } | Select-Object -First 1
        $GitUrl = $GitAsset.browser_download_url
    } catch {
        # Fallback to a known stable version
        $GitUrl = "https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe"
    }
    $GitPath = "$TempDir\GitSetup.exe"
    Invoke-WebRequest -Uri $GitUrl -OutFile $GitPath

    Write-Status "  Running Git installer..."
    Start-Process -Wait -FilePath $GitPath -ArgumentList "/SILENT", "/NORESTART", "/COMPONENTS=icons,ext\reg\shellhere,assoc,assoc_sh"

    Refresh-Path
    if (Test-CommandExists "git") {
        Write-Success "Git for Windows installed: $(git --version 2>&1)"
    } else {
        Write-Success "Git for Windows installed (restart PowerShell to use)"
    }
} else {
    Write-Success "Git already installed: $(git --version 2>&1)"
}

# Step 3: Install Claude Desktop
Write-Status "Installing Claude Desktop..."
$ClaudeDesktopInstalled = $null -ne (
    Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName -like "*Claude*" -and $_.DisplayName -notlike "*Claude Code*" }
)
if (-not $ClaudeDesktopInstalled) {
    $ClaudePath = "$TempDir\ClaudeSetup.exe"

    Write-Status "  Downloading Claude Desktop..."
    Invoke-WebRequest -Uri $ClaudeDesktopUrl -OutFile $ClaudePath

    Write-Status "  Running Claude Desktop installer..."
    Start-Process -Wait -FilePath $ClaudePath -ArgumentList "/S"

    Write-Success "Claude Desktop installed"
} else {
    Write-Success "Claude Desktop already installed"
}

# Step 4: Install Claude Code (terminal)
Write-Status "Installing Claude Code (terminal)..."
if (-not (Test-CommandExists "claude")) {
    Write-Status "  Running Claude Code installer..."
    Invoke-RestMethod -Uri "https://claude.ai/install.ps1" | Invoke-Expression
    Refresh-Path
    if (Test-CommandExists "claude") {
        Write-Success "Claude Code installed: $(claude --version 2>&1)"
    } else {
        Write-Success "Claude Code installed (restart PowerShell to use 'claude' command)"
    }
} else {
    Write-Success "Claude Code already installed: $(claude --version 2>&1)"
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
if (Test-CommandExists "git") {
    Write-Success "  Git: $(git --version 2>&1)"
} else {
    Write-Warning "  Git: NOT FOUND (may need to restart PowerShell)"
    $AllGood = $false
}

# Check Claude Desktop
$ClaudeVerified = $null -ne (
    Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName -like "*Claude*" -and $_.DisplayName -notlike "*Claude Code*" }
)
if ($ClaudeVerified) {
    Write-Success "  Claude Desktop: installed"
} else {
    Write-Warning "  Claude Desktop: NOT FOUND"
    $AllGood = $false
}

# Check Claude Code CLI
if (Test-CommandExists "claude") {
    Write-Success "  Claude Code (terminal): $(claude --version 2>&1)"
} else {
    Write-Warning "  Claude Code (terminal): not yet in PATH (restart PowerShell)"
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
Write-Host "  1. Open Claude Desktop and sign in with your Anthropic account"
Write-Host "  2. Click the Code tab to start using Claude Code"
Write-Host "  3. Or open a terminal and type 'claude' to use Claude Code in the terminal"
Write-Host ""
Write-Host "Installed software:" -ForegroundColor Yellow
Write-Host "  - Python 3.12 ($ArchLabel)"
Write-Host "  - Git for Windows"
Write-Host "  - Claude Desktop"
Write-Host "  - Claude Code (terminal: 'claude' command)"
Write-Host ""
