@echo off
REM Script qui configure les variables d'environnement pour la communication UDP CAN
REM Équivalent Windows du script choco_env.sh

SET MCC_CAN_DEV_2=vcan0
SET MCC_CAN_DEV_3=vcan0
SET MCC_CAN_DEV_4=vcan0
SET MCC_CAN_DEV_5=vcan0

REM Variables supplémentaires spécifiques à l'environnement Windows
SET MCC_QT_QUICK_DEV=1
SET MCC_NO_PUC=1
SET MCC_STINA=1

REM Ce paramètre permet d'afficher un curseur sur l'application (utile pour le débogage)
REM SET MCC_USE_CURSOR=1