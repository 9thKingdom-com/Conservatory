import unreal as u,json
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();lib=u.EditorAssetLibrary
# Save only our unused material experiment, keeping it out of the applied map.
unused=lib.load_asset('/Game/Conservatory/Environment/CityRoadDraft/M_CityRoadDraft');lib.save_loaded_asset(unused)
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(28500,-4000,85000),u.Rotator(pitch=-89.9,yaw=90,roll=0))
print('CITY_EDITOR_VIEW_READY')
