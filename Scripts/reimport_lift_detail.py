import unreal as u,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];SRC=R/'Asset Chest/01 John Originals/LIFT-MASTER/UnrealExport';BASE='/Game/Conservatory/Architecture/LiftMaster';lib=u.EditorAssetLibrary
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
for kind in ['Solid','Glass']:
 name='SM_LiftMaster_'+kind;task=u.AssetImportTask();task.filename=str(SRC/(name+'.fbx'));task.destination_path=BASE;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=True
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;opt.static_mesh_import_data.normal_import_method=u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS;task.options=opt;u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=lib.load_asset(BASE+'/'+name)
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  key=str(slot.material_slot_name).split('.')[0];mat=lib.load_asset(BASE+'/M_'+key);assert mat,key;mesh.set_material(i,mat)
 settings=mesh.get_editor_property('nanite_settings');settings.enabled=False;mesh.set_editor_property('nanite_settings',settings)
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 assert lib.save_loaded_asset(mesh,only_if_is_dirty=False)
 print('DETAIL_REIMPORT',name,mesh.get_bounds())
print('LIFT_DETAIL_REIMPORT_SAVED')
