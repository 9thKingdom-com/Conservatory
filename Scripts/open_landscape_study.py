import unreal as u,re
from pathlib import Path
root=Path(u.Paths.project_dir());base='/Game/Conservatory/Environment/LandscapePaintStudy';lib=u.EditorAssetLibrary
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();assert w.get_name()=='L_LandscapePaintStudy'
task=u.AssetImportTask();task.filename=str(root/'SourceAssets/LandscapePaintStudy/SM_Study_Foundations.fbx');task.destination_path=base;task.automated=True;task.save=True;task.replace_existing=True
o=u.FbxImportUI();o.import_mesh=True;o.import_materials=False;o.import_textures=False;o.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;o.static_mesh_import_data.combine_meshes=True;o.static_mesh_import_data.auto_generate_collision=False;task.options=o
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=lib.load_asset(base+'/SM_Study_Foundations')
for i,s in enumerate(mesh.get_editor_property('static_materials')):mesh.set_material(i,lib.load_asset('/Game/Conservatory/Environment/ValleySettlements/M_'+re.sub(r'_\d{3}$','',str(s.material_slot_name).split('.')[0])))
body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True);lib.save_loaded_asset(mesh)
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 if a.get_actor_label()=='Valley roads, foundations, approaches and farm fields':a.static_mesh_component.set_static_mesh(mesh);a.set_actor_label('Study | retained foundations and approaches')
u.EditorLoadingAndSavingUtils.save_map(w,'/Game/Conservatory/Maps/L_LandscapePaintStudy')
u.EditorLevelLibrary.set_level_viewport_camera_info(u.Vector(16000,-6500,5000),u.Rotator(pitch=-32,yaw=35,roll=0))
