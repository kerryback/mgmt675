# Bootstrap script to run the MGMT 675 installer
# This script unblocks and runs install.ps1
# Usage: powershell -ExecutionPolicy Bypass -File .\run.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallerPath = Join-Path $ScriptDir "install.ps1"

Write-Host "MGMT 675 Development Environment Installer Bootstrap" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator." -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "  1. Close this PowerShell window" -ForegroundColor Yellow
    Write-Host "  2. Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host "  3. Navigate back to this directory" -ForegroundColor Yellow
    Write-Host "  4. Run: powershell -ExecutionPolicy Bypass -File .\run.ps1" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if installer exists
if (-not (Test-Path $InstallerPath)) {
    Write-Host "ERROR: Installer not found at: $InstallerPath" -ForegroundColor Red
    exit 1
}

Write-Host "[*] Unblocking installer script..." -ForegroundColor White
try {
    Unblock-File -Path $InstallerPath -ErrorAction SilentlyContinue
    Write-Host "[+] Installer script unblocked" -ForegroundColor Green
} catch {
    Write-Host "[!] Could not unblock file (this is OK, continuing anyway)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[*] Starting installer..." -ForegroundColor White
Write-Host ""

# Run the installer with bypass execution policy
try {
    & $InstallerPath
} catch {
    Write-Host ""
    Write-Host "ERROR: Installer failed with error:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Please see README.md for alternative installation methods." -ForegroundColor Yellow
    exit 1
}
