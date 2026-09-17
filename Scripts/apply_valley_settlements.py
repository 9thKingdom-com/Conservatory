"""Run through Unreal Tools > Execute Python Script in the current RobotVR map."""
import unreal as u, json, math, sys, datetime, shutil, traceback, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';BASE='/Game/Conservatory/Environment/ValleySettlements';TAG='ValleySettlements'
actors=u.get_editor_subsystem(u.EditorActorSubsystem);lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();assert world.get_name()=='L_Exterior_RobotVR','Wrong active map'
layout=json.loads((ROOT/'SourceAssets/ValleySettlements/layout.json').read_text());buildings=layout['buildings']
backup=ROOT/'Saved/Backups/ValleySettlements'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True)
# Save the current editor state before taking the recovery copy.
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
shutil.copy2(ROOT/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
report={'backup':str(backup),'buildings':buildings,'removed':[],'created':[]}
def state(a):
 p=a.get_actor_location();r=a.get_actor_rotation();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll]
protected={a.get_path_name():state(a) for a in actors.get_all_level_actors() if 'CoreHabitat' in [str(t) for t in a.tags] or a.get_class().get_name() in ['C17Robot','ServiceLift']}
materials={}
for name,color in json.loads((ROOT/'SourceAssets/ValleySettlements/palette.json').read_text()).items():
 path=BASE+'/M_'+name;mat=lib.load_asset(path) if lib.does_asset_exist(path) else at.create_asset('M_'+name,BASE,u.Material,u.MaterialFactoryNew());mel.delete_all_material_expressions(mat)
 def node(cls,**props):
  e=mel.create_material_expression(mat,cls)
  for k,v in props.items():e.set_editor_property(k,v)
  return e
 c=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*color,1))
 if name not in ['Glass','Metal','Paper','Lime','Sage']:
  pos=node(u.MaterialExpressionWorldPosition);noise=node(u.MaterialExpressionNoise,scale=.055 if name not in ['Gravel','Stone'] else .17,quality=1,levels=2)
  mel.connect_material_expressions(pos,'',noise,'Position');dark=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*[v*(.94 if name in ['Lime','Sage'] else .85) for v in color],1));mix=node(u.MaterialExpressionLinearInterpolate)
  for e,pin in [(dark,'A'),(c,'B'),(noise,'Alpha')]:mel.connect_material_expressions(e,'',mix,pin)
  c=mix
 mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 rough=node(u.MaterialExpressionConstant,r=.13 if name=='Glass' else .38 if name in ['Metal','Roof'] else .84);mel.connect_material_property(rough,'',u.MaterialProperty.MP_ROUGHNESS)
 metal=node(u.MaterialExpressionConstant,r=.75 if name in ['Metal','Roof'] else 0);mel.connect_material_property(metal,'',u.MaterialProperty.MP_METALLIC)
 mat.set_editor_property('two_sided',True)
 if name=='Glass':
  mat.set_editor_property('blend_mode',u.BlendMode.BLEND_TRANSLUCENT)
  opacity=node(u.MaterialExpressionConstant,r=.18);mel.connect_material_property(opacity,'',u.MaterialProperty.MP_OPACITY)
 mel.recompile_material(mat);lib.save_loaded_asset(mat);materials[name]=mat
meshes={}
for file in sorted((ROOT/'SourceAssets/ValleySettlements').glob('*.fbx')):
 task=u.AssetImportTask();task.filename=str(file);task.destination_path=BASE;task.destination_name=file.stem;task.automated=True;task.save=True;task.replace_existing=True
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
 opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt;at.import_asset_tasks([task])
 mesh=lib.load_asset(BASE+'/'+file.stem);assert mesh
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):mesh.set_material(i,materials[re.sub(r'_\d{3}$','',str(slot.material_slot_name).split('.')[0])])
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 lib.save_loaded_asset(mesh);meshes[file.stem]=mesh
for a in list(actors.get_all_level_actors()):
 label=a.get_actor_label();tags=[str(t) for t in a.tags]
 if TAG in tags or 'TownToday' in tags or label.startswith('Cottage_') or label=='Village bell tower':
  report['removed'].append(label);actors.destroy_actor(a)
def spawn(cls,label,p,group='Infrastructure',yaw=0):
 a=actors.spawn_actor_from_class(cls,u.Vector(*[v*100 for v in p]),u.Rotator(pitch=0,yaw=yaw,roll=0));a.set_actor_label(label);a.set_folder_path('03 Village/Valley settlements/'+group);a.tags=[TAG];report['created'].append(label);return a
def mesh_actor(mesh,label,p,group='Infrastructure',yaw=0):
 a=spawn(u.StaticMeshActor,label,p,group,yaw);a.static_mesh_component.set_static_mesh(mesh);return a
mesh_actor(meshes['SM_Valley_Infrastructure'],'Valley roads, foundations, approaches and farm fields',(0,0,0))
for b in buildings:
 a=mesh_actor(meshes[b['mesh']],b['id']+' | '+b['kind']+' | explorable',(b['x'],b['y'],b['z']),b['group'],b['yaw']);a.tags=[TAG,'ExplorableBuilding',b['id']]
 for i,p in enumerate(b['clue_anchors']):
  anchor=spawn(u.TargetPoint,b['id']+' | future clue %d'%(i+1),p,b['group']+'/Discovery anchors');anchor.tags=[TAG,'FutureClueAnchor',b['id']]
 light=spawn(u.PointLight,b['id']+' | interior daylight fill',(b['x'],b['y'],b['z']+2.7),b['group']+'/Daylight')
 c=light.point_light_component;c.set_editor_property('intensity_units',u.LightUnits.LUMENS);c.set_intensity(80);c.set_attenuation_radius(700);c.set_cast_shadows(True);c.set_light_color(u.LinearColor(1,.89,.73,1))
# Keep familiar street props in credible roadside positions; all old closed buildings go.
old='/Game/Conservatory/Environment/TownToday/'
for name,x,y,yaw in [('SM_OldSedan',162,9.8,0),('SM_OldEstate',252,6.2,180)]:
 path=old+name
 if lib.does_asset_exist(path):mesh_actor(lib.load_asset(path),'Vehicle left in road',(x,y,height(x,y)+.2),yaw=yaw)
for x in [145,180,210,250,288,318]:
 for name,y in [('SM_StreetLamp',13),('SM_StreetBench',16)]:
  if lib.does_asset_exist(old+name):mesh_actor(lib.load_asset(old+name),'Main street '+name,(x,y,height(x,y)+.16))
def segment_distance(x,y,a,b):
 dx=b[0]-a[0];dy=b[1]-a[1];t=max(0,min(1,((x-a[0])*dx+(y-a[1])*dy)/(dx*dx+dy*dy)))
 return math.hypot(x-a[0]-t*dx,y-a[1]-t*dy)
def clear_at(x,y,pad):
 for b in buildings:
  if abs(x-b['x'])<b['w']/2+pad and abs(y-b['y'])<b['d']/2+pad:return True
  if abs(x-b['x'])<2+pad and min(b['y'],b['y']+(1 if b['yaw']==0 else -1)*(b['d']/2+13))<y<max(b['y'],b['y']+(1 if b['yaw']==0 else -1)*(b['d']/2+13)):return True
 for r in layout['roads']:
  if any(segment_distance(x,y,a,b)<r['width']/2+pad for a,b in zip(r['points'],r['points'][1:])):return True
 for cx,cy in [(105,-215),(450,32)]:
  if cx-30<x<cx+40 and cy-80<y<cy-30:return True
 return False
removed=0
for a in actors.get_all_level_actors():
 for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
  name=c.static_mesh.get_name() if c.static_mesh else '';pad=6 if any(k in name.lower() for k in ['oak','birch','tree']) else 1.2
  keep=[];count=c.get_instance_count()
  for i in range(count):
   t=c.get_instance_transform(i,world_space=True)
   if clear_at(t.translation.x/100,t.translation.y/100,pad):removed+=1
   else:keep.append(t)
  if len(keep)!=count:c.clear_instances();c.add_instances(keep,False,True)
report['foliage_instances_cleared']=removed
for a in actors.get_all_level_actors():
 if a.get_path_name() in protected:assert state(a)==protected[a.get_path_name()],a.get_actor_label()
report['protected_actors_unchanged']=len(protected)
report['navigation_rebuilt']=u.ExteriorTools.build_terrain_navigation()
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
report['saved_map']=MAP
(ROOT/'Documentation/ValleySettlementsImport.json').write_text(json.dumps(report,indent=2))
u.EditorLevelLibrary.set_level_viewport_camera_info(u.Vector(9000,-12000,8500),u.Rotator(pitch=-25,yaw=45,roll=0))
print('VALLEY_SETTLEMENTS_APPLIED',len(buildings))
