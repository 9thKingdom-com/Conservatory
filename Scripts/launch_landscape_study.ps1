$studyArguments = @'
"C:\Users\ASUS TUF\Documents\1 conservatory\Conservatory.uproject" /Game/Conservatory/Maps/L_LandscapePaintStudy -nosplash -ExecCmds="py exec(open(r'C:/Users/ASUS TUF/Documents/1 conservatory/Scripts/open_landscape_study.py').read())" -log=LandscapeStudyEditor.log
'@
Start-Process -FilePath 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe' -ArgumentList $studyArguments -WindowStyle Hidden
