$reviewArgs = @'
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_LandscapePaintStudy -game -windowed -ResX=1280 -ResY=720 -nosplash -unattended -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/inspect_landscape_paint.py').read())" -log=LandscapePaintReview.log
'@
$reviewProcess=Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $reviewArgs -WindowStyle Hidden -PassThru
if(-not $reviewProcess.WaitForExit(180000)) { Stop-Process -Id $reviewProcess.Id; Write-Output 'Review timed out.' } else { Write-Output "Review exit code: $($reviewProcess.ExitCode)" }
