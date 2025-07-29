@echo off

REM Sets installation directory as working directory
cd /d "%~dp0"

REM Set the necessary environment variables
call scripts\choco_env.bat

REM Checks if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in the PATH.
    echo The authentication system cannot function.
    echo.
    echo Python installation required to continue.
    pause
    exit /b 1
) 

REM Launch Login page
start /B pythonw "scripts\Login.pyw"

echo The Sokinox Simulator has been launched.
echo You can close this window.
