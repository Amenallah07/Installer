@echo off
REM Script pour changer le mot de passe Sokinox
REM Usage: change_password.bat <nouveau_mot_de_passe>

echo ================================
echo   SOKINOX - Changement MDP
echo ================================
echo.

if "%1"=="" (
    echo Usage: change_password.bat ^<nouveau_mot_de_passe^>
    echo.
    echo Exemples:
    echo   change_password.bat mon_nouveau_mdp_2025
    echo   change_password.bat sokinox2026
    echo.
    pause
    exit /b 1
)

REM Aller dans le répertoire des scripts
cd /d "%~dp0scripts"

REM Vérifier que Python est disponible
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python pour continuer
    pause
    exit /b 1
)

REM Exécuter le changement de mot de passe
echo Changement du mot de passe en cours...
echo.
python AuthManager.py "%1"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================
    echo   CHANGEMENT REUSSI !
    echo ================================
    echo Le nouveau mot de passe sera effectif
    echo au prochain démarrage de l'application.
    echo.
    echo Fichier de configuration: %%LOCALAPPDATA%%\Sokinox\auth.json
    echo.
) else (
    echo.
    echo ================================
    echo   ERREUR !
    echo ================================
    echo Le changement de mot de passe a échoué.
    echo Vérifiez que l'application n'est pas en cours d'exécution.
    echo.
)

pause