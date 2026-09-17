$valleyArguments = @'
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_Exterior_RobotVR -game -windowed -ResX=1280 -ResY=720 -nosplash -unattended -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/inspect_valley_settlements.py').read())" -log=ValleyRuntime.log
'@
$valleyProcess = Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $valleyArguments -WindowStyle Hidden -PassThru
Write-Output "Valley test process: $($valleyProcess.Id)"
if (-not $valleyProcess.WaitForExit(310000)) {
    $valleyProcess.CloseMainWindow() | Out-Null
    if (-not $valleyProcess.WaitForExit(5000)) { Stop-Process -Id $valleyProcess.Id }
    Write-Output 'Test process closed at safety timeout.'
} else { Write-Output "Test process exited: $($valleyProcess.ExitCode)" }
