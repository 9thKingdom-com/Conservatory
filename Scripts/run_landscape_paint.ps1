$studyArgs = @'
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_LandscapePaintStudy -nosplash -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/paint_landscape_study.py').read())" -log=LandscapePaintNative.log
'@
Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $studyArgs -WindowStyle Hidden
