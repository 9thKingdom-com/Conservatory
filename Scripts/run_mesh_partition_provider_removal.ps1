$arguments = @"
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_Exterior_RobotVR -nosplash -unattended -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/remove_mesh_partition_providers.py').read())" -log=MeshPartitionFix-ProviderRemoval.log
"@
$process = Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $arguments -WindowStyle Hidden -PassThru
Write-Output "Provider removal process: $($process.Id)"
if (-not $process.WaitForExit(600000)) {
    $process.CloseMainWindow() | Out-Null
    if (-not $process.WaitForExit(15000)) { Stop-Process -Id $process.Id -Force }
    Write-Output 'Provider removal process closed at safety timeout.'
} else { Write-Output "Provider removal process exited: $($process.ExitCode)" }