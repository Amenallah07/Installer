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
    echo Le système d'authentification ne peut pas fonctionner.
    echo.
    echo Installation de Python requise pour continuer.
    pause
    exit /b 1
) 

REM Lance la page de login
python "scripts\Login.py"

echo L'application Chocolat a été lancée.
echo Vous pouvez fermer cette fenêtre.