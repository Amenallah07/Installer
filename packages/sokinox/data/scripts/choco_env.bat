@echo off
REM Script to configure environment variables for UDP CAN communication
REM Windows equivalent of choco_env.sh script, I am not sure if its useful or not

SET MCC_CAN_DEV_1=vcan0
SET MCC_CAN_DEV_2=vcan0
SET MCC_CAN_DEV_3=vcan0
SET MCC_CAN_DEV_4=vcan0
SET MCC_CAN_DEV_5=vcan0

REM Additional variables specific to the Windows environment
SET MCC_QT_QUICK_DEV=1
SET MCC_NO_PUC=1
SET MCC_STINA=1

REM This parameter displays a cursor on the application (useful for debugging).
REM SET MCC_USE_CURSOR=1
