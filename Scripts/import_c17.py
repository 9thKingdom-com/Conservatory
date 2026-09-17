"""Import C17 skeletal mesh and seven animations with shared skeleton and UE-native materials."""
import unreal as u,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'SourceAssets/C17';BASE='/Game/Conservatory/Robots/C17';lib=u.EditorAssetLibrary;lib.make_directory(BASE);at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary
u.SystemLibrary.execute_console_command(None,'Interchange.FeatureFlags.Import.FBX 0')
colors={'Ochre':(.60,.34,.035),'Graphite':(.075,.09,.095),'Steel':(.30,.33,.32),'Rubber':(.015,.02,.021),'Sensor':(.012,.035,.045),'Ivory':(.78,.76,.61),'Amber':(1,.49,.06)}
materials={}
for name,col in colors.items():
 path=BASE+'/M_C17_'+name
 if lib.does_asset_exist(path):m=lib.load_asset(path)
 else:
  m=at.create_asset('M_C17_'+name,BASE,u.Material,u.MaterialFactoryNew());m.set_editor_property('used_with_skeletal_mesh',True)
  if name in ['Ochre','Graphite','Steel']:
   t=u.AssetImportTask();t.filename=str(SRC/('T_C17_'+name+'.png'));t.destination_path=BASE;t.automated=True;t.save=True;at.import_asset_tasks([t]);tex=lib.load_asset(BASE+'/T_C17_'+name)
   c=mel.create_material_expression(m,u.MaterialExpressionTextureSample);c.set_editor_property('texture',tex)
  else:
   c=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector);c.set_editor_property('constant',u.LinearColor(*col,1))
  mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
  for value,prop in [(.65 if name in ['Ochre','Graphite','Steel'] else .05,u.MaterialProperty.MP_METALLIC),(.32 if name=='Sensor' else .58,u.MaterialProperty.MP_ROUGHNESS)]:
   e=mel.create_material_expression(m,u.MaterialExpressionConstant);e.set_editor_property('r',value);mel.connect_material_property(e,'',prop)
  if name=='Amber':mel.connect_material_property(c,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
  mel.recompile_material(m);lib.save_loaded_asset(m)
 materials[name]=m
opts=u.FbxImportUI();opts.import_mesh=True;opts.import_as_skeletal=True;opts.mesh_type_to_import=u.FBXImportType.FBXIT_SKELETAL_MESH;opts.import_animations=False;opts.import_materials=False;opts.import_textures=False;opts.create_physics_asset=True;opts.automated_import_should_detect_type=False
opts.skeletal_mesh_import_data.set_editor_property('normal_import_method',u.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS)
opts.skeletal_mesh_import_data.set_editor_property('force_front_x_axis',True)
opts.skeletal_mesh_import_data.set_editor_property('import_uniform_scale',100.0)
t=u.AssetImportTask();t.filename=str(SRC/'SK_C17.fbx');t.destination_path=BASE;t.destination_name='SK_C17';t.automated=True;t.replace_existing=True;t.replace_existing_settings=True;t.save=True;t.options=opts;at.import_asset_tasks([t]);mesh=lib.load_asset(BASE+'/SK_C17');assert isinstance(mesh,u.SkeletalMesh),t.imported_object_paths
slots=mesh.get_editor_property('materials')
for i,slot in enumerate(slots):
 name=str(slot.material_slot_name).replace('C17_','');assert name in materials,name;slot.set_editor_property('material_interface',materials[name]);slots[i]=slot
mesh.set_editor_property('materials',slots);lib.save_loaded_asset(mesh);skeleton=mesh.get_editor_property('skeleton');lib.save_loaded_asset(skeleton,False)
physics=mesh.get_editor_property('physics_asset')
if physics:lib.save_loaded_asset(physics,False)
manifest=json.loads((SRC/'C17_Manifest.json').read_text());animations={}
for clip in manifest['animations']:
 opts=u.FbxImportUI();opts.import_mesh=False;opts.import_as_skeletal=True;opts.mesh_type_to_import=u.FBXImportType.FBXIT_ANIMATION;opts.import_animations=True;opts.import_materials=False;opts.import_textures=False;opts.skeleton=skeleton;opts.automated_import_should_detect_type=False;opts.anim_sequence_import_data.set_editor_property('force_front_x_axis',True);opts.anim_sequence_import_data.set_editor_property('import_uniform_scale',100.0)
 t=u.AssetImportTask();t.filename=str(SRC/('A_C17_'+clip+'.fbx'));t.destination_path=BASE;t.destination_name='A_C17_'+clip;t.automated=True;t.replace_existing=True;t.replace_existing_settings=True;t.save=True;t.options=opts;at.import_asset_tasks([t])
 candidates=[lib.load_asset(p) for p in t.imported_object_paths];anim=next((a for a in candidates if isinstance(a,u.AnimSequence)),None);assert anim,t.imported_object_paths
 desired=BASE+'/A_C17_'+clip
 if anim.get_path_name().split('.')[0]!=desired:assert lib.rename_asset(anim.get_path_name(),desired)
 animations[clip]=desired
bounds=mesh.get_bounds();report={'mesh':mesh.get_path_name(),'skeleton':skeleton.get_path_name(),'animations':animations,'bounds_origin_cm':list(bounds.origin.to_tuple()),'bounds_extent_cm':list(bounds.box_extent.to_tuple()),'imported':True}
(ROOT/'Documentation/C17/Import.json').write_text(json.dumps(report,indent=2));print('C17_IMPORTED',flush=True)





