import unreal as u,json,shutil,datetime,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';BASE='/Game/Conservatory/Architecture/CoreHabitat'
backup=ROOT/'Saved/Backups/CoreHabitat'/('LiftFit-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
at=u.AssetToolsHelpers.get_asset_tools();lib=u.EditorAssetLibrary
task=u.AssetImportTask();task.filename=str(ROOT/'SourceAssets/CoreHabitat/SM_Core_Terrain.fbx');task.destination_path=BASE;task.destination_name='SM_Core_Terrain';task.automated=True;task.save=True;task.replace_existing=True
opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH;opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt;at.import_asset_tasks([task])
mesh=lib.load_asset(BASE+'/SM_Core_Terrain');mesh.set_material(0,lib.load_asset('/Game/Conservatory/Environment/Materials/M_Ground'));body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True);lib.save_loaded_asset(mesh)
w=u.EditorLoadingAndSavingUtils.load_map(MAP);actors=u.get_editor_subsystem(u.EditorActorSubsystem)
def transform_values(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():transform_values(a) for a in actors.get_all_level_actors() if 'CoreHabitat' not in [str(t) for t in a.tags]}
centre=next(a for a in actors.get_all_level_actors() if a.get_actor_label()=='Core habitat | Centre Floor')
delta=u.Vector(-11000-centre.get_actor_location().x,-centre.get_actor_location().y,0)
for a in actors.get_all_level_actors():
 if 'CoreHabitat' in [str(t) for t in a.tags]:a.set_actor_location(a.get_actor_location()+delta,False,False)
cleared={}
for a in actors.get_all_level_actors():
 for c in a.get_components_by_class(u.HierarchicalInstancedStaticMeshComponent):
  remove=[]
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,world_space=True);x=(t.translation.x+11000)/100;y=t.translation.y/100
   if math.hypot(x,y)<19 or any(math.hypot(x-xx,y-yy)<13 for xx,yy in [(46.63755,0),(-46.63755,0),(0,46.63755),(0,-46.63755)]) or (abs(x)<47 and abs(y)<3.3) or (abs(y)<47 and abs(x)<3.3):remove.append(i)
  if remove:c.remove_instances(remove);cleared[a.get_name()]=cleared.get(a.get_name(),0)+len(remove)
assert u.ExteriorTools.build_terrain_navigation()
unexpected=[a.get_name() for a in actors.get_all_level_actors() if a.get_name() in before and before[a.get_name()]!=transform_values(a)];assert not unexpected,unexpected
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
p=ROOT/'Documentation/CoreHabitatImport.json';report=json.loads(p.read_text());report['origin_cm']=[-11000,0,6230.95];report['lift_fit_shift_cm']=[-400,0,0];report['lift_fit_backup']=str(backup);report['navigation_rebuilt']=True;report['additional_foliage_clearance']=cleared;report['lift_and_other_actor_transform_changes']=unexpected;p.write_text(json.dumps(report,indent=2))
print('CORE_HABITAT_LIFT_FIT_SAVED',flush=True)
