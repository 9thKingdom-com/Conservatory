$arguments = @"
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_Exterior_RobotVR -game -windowed -ResX=1280 -ResY=720 -nosplash -unattended -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/verify_heavy_nav_mesh_runtime.py').read())" -log=HeavyNavMeshRuntime.log
"@
$process = Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $arguments -WindowStyle Hidden -PassThru
Write-Output "Runtime test process: $($process.Id)"
if (-not $process.WaitForExit(310000)) {
    $process.CloseMainWindow() | Out-Null
    if (-not $process.WaitForExit(15000)) { Stop-Process -Id $process.Id -Force }
    Write-Output 'Runtime test closed at safety timeout.'
} else { Write-Output "Runtime test exited: $($process.ExitCode)" }
