import unreal as u,json
from pathlib import Path
mesh=u.EditorAssetLibrary.load_asset('/Game/Conservatory/Architecture/LiftMaster/SM_LiftMaster_Solid')
n=mesh.get_editor_property('nanite_settings');print('BEFORE_NANITE',n)
n.enabled=False;mesh.set_editor_property('nanite_settings',n)
sub=u.get_editor_subsystem(u.StaticMeshEditorSubsystem);settings=sub.get_lod_build_settings(mesh,0);print('BUILD_SETTINGS',settings)
settings.use_mikk_t_space=False;settings.recompute_normals=True;settings.recompute_tangents=True;sub.set_lod_build_settings(mesh,0,settings)
assert u.EditorAssetLibrary.save_loaded_asset(mesh,only_if_is_dirty=False)
print('LIFT_DETAIL_SAVED')
