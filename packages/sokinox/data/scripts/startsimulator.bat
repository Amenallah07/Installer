@echo off
REM -----------------------------------------------------------------------------
REM Script: startsimulator.bat
REM Equivalent Windows launcher for Qt cross-compiled app with simulator
REM -----------------------------------------------------------------------------

REM Get script directory
set SCRIPT_DIR=%~dp0

REM Go to script directory
cd /d "%SCRIPT_DIR%"

REM Step 1: Set environment variables
call choco_env.bat

REM Step 2: Launch simulator Python script
start "" python "%SCRIPT_DIR%Simulator.py"

REM Step 3: Go to bin and launch simulator.exe and GUI
cd /d "%SCRIPT_DIR%..\bin"
start "" simulator.exe
start "" ChocolatPanel_release.exe

REM Step 4: Wait for user input before shutting down
echo.
echo Press any key to terminate the simulator and panel...
pause >nul

REM Step 5: Kill the launched processes (only the most recent ones)
taskkill /F /IM simulator.exe /T
taskkill /F /IM ChocolatPanel_release.exe /T

REM Optionally: Also kill python if needed
REM taskkill /F /IM python.exe /T
