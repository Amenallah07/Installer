@echo off
REM Script principal de lancement de l'application Chocolat
REM Équivalent Windows du script bashlauncher.sh

REM Définit le répertoire d'installation comme répertoire de travail
cd /d "%~dp0"

REM Configure les variables d'environnement nécessaires
call scripts\choco_env.bat

REM Vérifie si Python est installé
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé ou n'est pas dans le PATH.
    echo L'interface du simulateur ne sera pas disponible.
    
    REM Lance directement le simulateur et l'application sans l'interface graphique
    start "" "scripts\startsimulator.bat"
) else (
    REM Lance l'interface Python du simulateur
    start "" python "scripts\Simulator.py"
    
    REM Attendre que l'utilisateur configure le simulateur
    timeout /t 2 /nobreak >nul
    
    REM Lance le simulateur et l'application
    start "" "scripts\startsimulator.bat"
)

echo L'application Chocolat a été lancée.
echo Vous pouvez fermer cette fenêtre.