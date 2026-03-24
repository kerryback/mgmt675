@echo off
REM MGMT 675 Development Environment Installer (no Python libraries)
REM Double-click to run. A permission prompt will appear -- click Yes.

echo ================================================
echo   MGMT 675 Development Environment Installer
echo ================================================
echo.

REM Self-elevate: if not already admin, re-launch with UAC prompt
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting administrator privileges...
    echo A User Account Control prompt will appear. Click Yes to continue.
    echo.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo Starting installer...
echo.

REM Run the PowerShell installer script
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%~dp0run2.ps1"

if %errorLevel% neq 0 (
    echo.
    echo ================================================
    echo   Installation Failed
    echo ================================================
    echo.
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Installation Complete
echo ================================================
echo.
echo Please close and reopen PowerShell or Command Prompt
echo to use the newly installed tools.
echo.
pause
