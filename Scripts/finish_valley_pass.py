import unreal as u,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1];base='/Game/Conservatory/Environment/ValleySettlements';lib=u.EditorAssetLibrary
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 if 'ValleySettlements' in [str(t) for t in a.tags] and isinstance(a,u.PointLight):
  c=a.point_light_component;c.set_editor_property('intensity_units',u.LightUnits.LUMENS);c.set_intensity(80);c.set_attenuation_radius(700);c.set_cast_shadows(True)
# Reduce coarse colour variation in pale render; preserve a subtle material surface.
for name in ['Lime','Sage']:
 mat=lib.load_asset(base+'/M_'+name)
 # Material rebuilding is isolated from all existing environment materials.
 u.MaterialEditingLibrary.delete_all_material_expressions(mat)
 color=json.loads((root/'SourceAssets/ValleySettlements/palette.json').read_text())[name]
 c=u.MaterialEditingLibrary.create_material_expression(mat,u.MaterialExpressionConstant3Vector);c.constant=u.LinearColor(*color,1)
 u.MaterialEditingLibrary.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 r=u.MaterialEditingLibrary.create_material_expression(mat,u.MaterialExpressionConstant);r.r=.86;u.MaterialEditingLibrary.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
 u.MaterialEditingLibrary.recompile_material(mat);lib.save_loaded_asset(mat)
name='SM_Valley_Infrastructure';task=u.AssetImportTask();task.filename=str(root/'SourceAssets/ValleySettlements'/(name+'.fbx'));task.destination_path=base;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=True
opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt
u.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task]);mesh=lib.load_asset(base+'/'+name)
for i,s in enumerate(mesh.get_editor_property('static_materials')):mesh.set_material(i,lib.load_asset(base+'/M_'+re.sub(r'_\d{3}$','',str(s.material_slot_name).split('.')[0])))
body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True);lib.save_loaded_asset(mesh)
u.ExteriorTools.build_terrain_navigation();assert u.EditorLoadingAndSavingUtils.save_map(w,'/Game/Conservatory/Maps/L_Exterior_RobotVR')
print('VALLEY_APPROACH_AND_LIGHTING_FINISH_SAVED')
