$habitatArguments = @'
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_Exterior_RobotVR -game -windowed -ResX=1280 -ResY=720 -nosplash -unattended -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/inspect_core_habitat.py').read())" -log=CoreHabitatRuntime.log
'@
$habitatProcess = Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $habitatArguments -WindowStyle Hidden -PassThru
Write-Output "Habitat test process: $($habitatProcess.Id)"
if (-not $habitatProcess.WaitForExit(200000)) {
    $habitatProcess.CloseMainWindow() | Out-Null
    if (-not $habitatProcess.WaitForExit(5000)) { Stop-Process -Id $habitatProcess.Id }
    Write-Output 'Test process closed at safety timeout.'
} else { Write-Output "Test process exited: $($habitatProcess.ExitCode)" }
