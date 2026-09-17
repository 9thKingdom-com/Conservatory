@echo off
start "Kitchen Robot VR" "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" "%~dp0Conservatory.uproject" /Game/Conservatory/Maps/L_Exterior_RobotVR -game -windowed -ResX=1600 -ResY=900 -nosplash -RobotVRShowcase
