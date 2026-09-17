import unreal as u,json,shutil,datetime,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';BASE='/Game/Conservatory/Architecture/CoreHabitat';spec=json.loads((ROOT/'SourceAssets/CoreHabitat/CoreHabitat.json').read_text())
backup=ROOT/'Saved/Backups/CoreHabitat'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True,exist_ok=True)
shutil.copy2(ROOT/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary;lib.make_directory(BASE)
def solid(name,color,metal,rough):
 path=BASE+'/M_'+name
 if lib.does_asset_exist(path):return lib.load_asset(path)
 m=at.create_asset('M_'+name,BASE,u.Material,u.MaterialFactoryNew())
 c=mel.create_material_expression(m,u.MaterialExpressionConstant3Vector);c.constant=u.LinearColor(*color,1);mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 for val,prop in [(metal,u.MaterialProperty.MP_METALLIC),(rough,u.MaterialProperty.MP_ROUGHNESS)]:
  e=mel.create_material_expression(m,u.MaterialExpressionConstant);e.r=val;mel.connect_material_property(e,'',prop)
 mel.recompile_material(m);lib.save_loaded_asset(m);return m
mats={'HabitatFrame':lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterIvoryFrame'),'HabitatBrass':lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterBrass'),'HabitatFloor':lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterFloorLight'),'HabitatGlass':lib.load_asset('/Game/Conservatory/Architecture/PassageDetail/M_PassageConservatoryGlass'),'HabitatGround':lib.load_asset('/Game/Conservatory/Environment/Materials/M_Ground')}
assert all(mats.values()),'Missing existing materials'
for key in ['HabitatFrame','HabitatBrass']:
 mel.set_material_usage(mats[key],u.MaterialUsage.MATUSAGE_NANITE)
 mel.recompile_material(mats[key]);lib.save_loaded_asset(mats[key],only_if_is_dirty=False)
meshes={}
for name,info in spec['meshes'].items():
 task=u.AssetImportTask();task.filename=str(ROOT/'SourceAssets/CoreHabitat'/(name+'.fbx'));task.destination_path=BASE;task.destination_name=name;task.automated=True;task.save=True;task.replace_existing=True
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
 opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt;at.import_asset_tasks([task]);mesh=lib.load_asset(BASE+'/'+name);assert mesh,name
 for i,s in enumerate(mesh.get_editor_property('static_materials')):
  key=str(s.material_slot_name).split('.')[0];assert key in mats,key;mesh.set_material(i,mats[key])
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 if info['kind']=='frame':
  settings=mesh.get_editor_property('nanite_settings');settings.enabled=True;mesh.set_editor_property('nanite_settings',settings)
 lib.save_loaded_asset(mesh);meshes[name]=mesh;print('CORE_IMPORTED',name,flush=True)
world=u.EditorLoadingAndSavingUtils.load_map(MAP);assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
def state(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();c=a.get_component_by_class(u.StaticMeshComponent)
 return dict(label=a.get_actor_label(),transform=[p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z],mesh=c.static_mesh.get_path_name() if c and c.static_mesh else None)
before={a.get_name():state(a) for a in actors.get_all_level_actors()};removed=[]
for a in actors.get_all_level_actors():
 if 'ConservatoryModule' in [str(t) for t in a.tags] or 'CoreHabitat' in [str(t) for t in a.tags] or str(a.get_folder_path()).startswith('07 Hill-edge terrace'):
  removed.append(a.get_name());actors.destroy_actor(a)
for item in spec['actors']:
 xyz=[spec['origin_cm'][i]+item['position'][i]*100 for i in range(3)]
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(*xyz),u.Rotator(pitch=0,yaw=item['yaw'],roll=0));a.set_actor_label('Core habitat | '+item['label']);a.set_folder_path('06 Conservatory/Core habitat');a.tags=['CoreHabitat']
 c=a.static_mesh_component;c.set_static_mesh(meshes[item['mesh']]);c.set_mobility(u.ComponentMobility.STATIC)
 if spec['meshes'][item['mesh']]['kind']=='frame':c.set_collision_enabled(u.CollisionEnabled.NO_COLLISION)
 else:c.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS)
# Clear only foliage instances that physically intersect the new habitat footprint.
cleared={}
for a in actors.get_all_level_actors():
 for c in a.get_components_by_class(u.HierarchicalInstancedStaticMeshComponent):
  remove=[]
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,world_space=True);x=(t.translation.x-spec['origin_cm'][0])/100;y=(t.translation.y-spec['origin_cm'][1])/100
   inside=math.hypot(x,y)<19 or any(math.hypot(x-xx,y-yy)<13 for xx,yy in [(46.63755,0),(-46.63755,0),(0,46.63755),(0,-46.63755)]) or (abs(x)<47 and abs(y)<3.3) or (abs(y)<47 and abs(x)<3.3)
   if inside:remove.append(i)
  if remove:c.remove_instances(remove);cleared[a.get_name()]=cleared.get(a.get_name(),0)+len(remove)
after={a.get_name():state(a) for a in actors.get_all_level_actors()}
unexpected={k:[v,after.get(k)] for k,v in before.items() if k not in removed and after.get(k)!=v};assert not unexpected,str(unexpected)
assert u.ExteriorTools.build_terrain_navigation()
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
report={'map':MAP,'backup':str(backup),'removed_architecture_and_old_terrace':removed,'new_actors':len(spec['actors']),'unrelated_actor_changes':unexpected,'foliage_instances_cleared_inside_habitat':cleared,'floor_z_cm':6242.75,'origin_cm':spec['origin_cm'],'status':'Imported and saved; runtime checks pending.'}
(ROOT/'Documentation/CoreHabitatImport.json').write_text(json.dumps(report,indent=2));print('CORE_HABITAT_APPLIED',flush=True)

