$arguments = @"
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_Exterior_RobotVR -game -windowed -ResX=1280 -ResY=720 -nosplash -unattended -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/verify_robot_streaming_fix.py').read())" -log=RobotStreamingFix-Runtime.log
"@
$process = Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $arguments -WindowStyle Hidden -PassThru
Write-Output "Runtime verification process: $($process.Id)"
if (-not $process.WaitForExit(310000)) {
    $process.CloseMainWindow() | Out-Null
    if (-not $process.WaitForExit(15000)) { Stop-Process -Id $process.Id -Force }
    Write-Output 'Runtime verification closed at safety timeout.'
} else { Write-Output "Runtime verification exited: $($process.ExitCode)" }