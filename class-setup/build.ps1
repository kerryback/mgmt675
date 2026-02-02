# Build script to create platform-specific zip packages
# Run from the class-setup directory

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $ScriptDir "dist"

Write-Host "Building class setup packages..." -ForegroundColor Cyan

# Create output directory
if (Test-Path $OutputDir) {
    Remove-Item -Recurse -Force $OutputDir
}
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

# Function to build a platform package
function Build-Package {
    param(
        [string]$Platform,
        [string]$PlatformDir
    )

    Write-Host "Building $Platform package..." -ForegroundColor Yellow

    $TempDir = Join-Path $env:TEMP "class-setup-build-$Platform"
    $PackageName = "class-setup-$Platform"
    $PackageDir = Join-Path $TempDir $PackageName

    # Clean temp directory
    if (Test-Path $TempDir) {
        Remove-Item -Recurse -Force $TempDir
    }
    New-Item -ItemType Directory -Force -Path $PackageDir | Out-Null

    # Copy platform-specific files
    $PlatformPath = Join-Path $ScriptDir $PlatformDir
    if (Test-Path $PlatformPath) {
        Copy-Item -Recurse "$PlatformPath\*" $PackageDir
    }

    # Copy shared files
    $SharedPath = Join-Path $ScriptDir "shared"
    Copy-Item -Recurse (Join-Path $SharedPath "config") $PackageDir
    Copy-Item -Recurse (Join-Path $SharedPath "skills") $PackageDir
    Copy-Item (Join-Path $SharedPath "README.md") $PackageDir

    # Create zip file
    $ZipPath = Join-Path $OutputDir "$PackageName.zip"
    Compress-Archive -Path $PackageDir -DestinationPath $ZipPath -Force

    # Get file size
    $Size = (Get-Item $ZipPath).Length / 1MB
    Write-Host "  Created: $PackageName.zip ($([math]::Round($Size, 2)) MB)" -ForegroundColor Green

    # Cleanup temp
    Remove-Item -Recurse -Force $TempDir
}

# Build each platform package
Build-Package -Platform "mac" -PlatformDir "mac"
Build-Package -Platform "windows-x64" -PlatformDir "windows-x64"
Build-Package -Platform "windows-arm" -PlatformDir "windows-arm"

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host "Packages are in: $OutputDir" -ForegroundColor Cyan
Write-Host ""

# List output files
Get-ChildItem $OutputDir | ForEach-Object {
    $Size = $_.Length / 1MB
    Write-Host "  $($_.Name) - $([math]::Round($Size, 2)) MB"
}
