@echo off
REM Script for creating the Sokinox Simulator Installer
REM Uses binarycreator of Qt Installer Framework

REM Configuration variables
SET INSTALLER_NAME=SokinoxInstaller
SET VERSION=1.0.0

REM Clean old builds
if exist "%INSTALLER_NAME%.exe" del "%INSTALLER_NAME%.exe"

REM Create installer
echo Creation of the Sokinox Simulator installer...
"binarycreator.exe" ^
    --offline-only ^
    -c config\config.xml ^
    -p packages ^
    -v ^
    "%INSTALLER_NAME%_v%VERSION%.exe"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Installer successfully created : %INSTALLER_NAME%_v%VERSION%.exe
    echo.
) else (
    echo.
    echo Installer creation error
    echo.
)

pause