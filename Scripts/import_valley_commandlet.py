import unreal,runpy
from pathlib import Path
unreal.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
runpy.run_path(str(Path(__file__).with_name('apply_valley_settlements.py')),run_name='__main__')
