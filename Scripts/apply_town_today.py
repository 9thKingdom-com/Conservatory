"""Apply the authored town pass to the active map, preserving habitat and rockface."""
import unreal as u,sys,re,json,math,random,shutil,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
MAP=re.search(r'GameDefaultMap=(.+)',(ROOT/'Config/DefaultEngine.ini').read_text()).group(1).strip()
source=ROOT/'Content'/Path(MAP.removeprefix('/Game/')+'.umap');backup=ROOT/'Saved/Backups/TownToday'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True,exist_ok=True);shutil.copy2(source,backup/source.name)
world=u.EditorLoadingAndSavingUtils.load_map(MAP);assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem);lib=u.EditorAssetLibrary;at=u.AssetToolsHelpers.get_asset_tools();mel=u.MaterialEditingLibrary
BASE='/Game/Conservatory/Environment/TownToday';lib.make_directory(BASE)
palette=json.loads((ROOT/'SourceAssets/TownToday/palette.json').read_text());materials={}
for name,color in palette.items():
 path=BASE+'/M_'+name;mat=lib.load_asset(path) if lib.does_asset_exist(path) else at.create_asset('M_'+name,BASE,u.Material,u.MaterialFactoryNew());mel.delete_all_material_expressions(mat)
 def node(cls,**props):
  e=mel.create_material_expression(mat,cls)
  for k,v in props.items():e.set_editor_property(k,v)
  return e
 c=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*color,1))
 if name in ['Asphalt','Concrete','Wall','Brick','Roof']:
  pos=node(u.MaterialExpressionWorldPosition);n=node(u.MaterialExpressionNoise,scale=.24 if name=='Asphalt' else .06,quality=1,levels=1)
  mel.connect_material_expressions(pos,'',n,'Position');a=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(*[x*.86 for x in color],1));mix=node(u.MaterialExpressionLinearInterpolate)
  for e,p in [(a,'A'),(c,'B'),(n,'Alpha')]:mel.connect_material_expressions(e,'',mix,p)
  c=mix
 mel.connect_material_property(c,'',u.MaterialProperty.MP_BASE_COLOR)
 rough=.10 if name=='Glass' else .33 if name in ['Metal','Blue','Cream','Red','Green'] else .9
 r=node(u.MaterialExpressionConstant,r=rough);mel.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
 m=node(u.MaterialExpressionConstant,r=.8 if name=='Metal' else .25 if name in ['Blue','Red','Cream'] else 0);mel.connect_material_property(m,'',u.MaterialProperty.MP_METALLIC)
 mat.set_editor_property('two_sided',True)
 mel.recompile_material(mat);lib.save_loaded_asset(mat);materials[name]=mat
meshes={}
for file in sorted((ROOT/'SourceAssets/TownToday').glob('*.fbx')):
 task=u.AssetImportTask();task.filename=str(file);task.destination_path=BASE;task.destination_name=file.stem;task.automated=True;task.save=True;task.replace_existing=True
 opt=u.FbxImportUI();opt.import_mesh=True;opt.import_materials=False;opt.import_textures=False;opt.import_as_skeletal=False;opt.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
 opt.static_mesh_import_data.combine_meshes=True;opt.static_mesh_import_data.auto_generate_collision=False;opt.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=opt;at.import_asset_tasks([task])
 mesh=lib.load_asset(BASE+'/'+file.stem);assert mesh,file.stem
 for i,slot in enumerate(mesh.get_editor_property('static_materials')):
  n=re.sub(r'_\d{3}$','',str(slot.material_slot_name).split('.')[0])
  # Cottage derivatives retain the original environment material vocabulary.
  oldpath='/Game/Conservatory/Environment/Materials/M_'+n
  mat=lib.load_asset(oldpath) if file.stem.startswith('SM_CleanCottage') and lib.does_asset_exist(oldpath) else materials.get(n)
  if mat is None:mat=materials.get(n,materials['Wall'])
  mesh.set_material(i,mat)
 body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE);body.set_editor_property('double_sided_geometry',True)
 lib.save_loaded_asset(mesh);meshes[file.stem]=mesh
TAG='TownToday';allactors=actors.get_all_level_actors()
def state(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
protected={a.get_path_name():state(a) for a in allactors if a.get_actor_location().x<0 and not a.get_components_by_class(u.InstancedStaticMeshComponent)}
for a in allactors:
 if TAG in [str(t) for t in a.tags]:actors.destroy_actor(a)
created=[]
def place(name,label,x,y,z=None,yaw=0,pitch=0,roll=0,scale=(1,1,1)):
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x*100,y*100,(height(x,y)+.18 if z is None else z)*100),u.Rotator(pitch=pitch,yaw=yaw,roll=roll));a.set_actor_label(label);a.set_folder_path('03 Village/Town today');a.tags=[TAG]
 a.static_mesh_component.set_static_mesh(meshes[name]);a.set_actor_scale3d(u.Vector(*scale));created.append(a);return a
place('SM_TownRoads','Town — asphalt streets, pavements and fuel forecourt',0,0,0)
cleaned=0;removed=0;originals=[];candidates=[]
for a in actors.get_all_level_actors():
 label=a.get_actor_label()
 if label.startswith('Cottage_'):
  c=a.get_component_by_class(u.StaticMeshComponent);old=c.get_editor_property('static_mesh');n=old.get_name();match=re.search(r'(\d+)$',n)
  if match:
   originals.append({'actor':label,'mesh':old.get_path_name(),'hidden':a.is_hidden_ed()});c.set_static_mesh(meshes['SM_CleanCottage_'+match.group(1)]);cleaned+=1
  p=a.get_actor_location();candidates.append((math.hypot(p.x/100-180,p.y/100+16),a))
 for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
  keep=[];count=c.get_instance_count()
  for i in range(count):
   t=c.get_instance_transform(i,world_space=True);x,y=t.translation.x/100,t.translation.y/100
   if (94<x<310 and -90<y<104) or (60<x<332 and abs(y-8)<8):removed+=1
   else:keep.append(t)
  if len(keep)!=count:c.clear_instances();c.add_instances(keep,False,True)
# Replace one cottage with a recognisable small shop, retaining its actor for recovery.
assert candidates
oldshop=min(candidates,key=lambda q:q[0])[1];oldshop.set_actor_hidden_in_game(True);oldshop.set_is_temporarily_hidden_in_editor(True);oldshop.set_actor_enable_collision(False)
shop_z=max(height(x,y) for x in [174,186] for y in [-20.5,-11.5])+.28
place('SM_CornerShopDamaged','Valley Stores — broken display frontage',180,-16,shop_z)
fuel_z=max(height(x,y) for x in [112,128] for y in [-31,-23])+.27
place('SM_FuelShop','Valley Fuel — service shop',120,-27,fuel_z)
canopy_z=height(120,-10)+.23
place('SM_FuelCanopy','Valley Fuel — pump canopy',120,-10,canopy_z)
for x in [115,125]:place('SM_FuelPump','Valley Fuel — pump island',x,-10,height(x,-10)+.23)
place('SM_FuelSign','Valley Fuel — roadside sign',101,0,height(101,0)+.24)
# Terrain-fit concrete footings beneath shop and canopy support points.
cube=u.load_asset('/Engine/BasicShapes/Cube')
def footing(x,y,top,sx,sy,label):
 bottom=height(x,y)-.12;h=max(.12,top-bottom)
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x*100,y*100,(bottom+h/2)*100));a.set_actor_label(label);a.set_folder_path('03 Village/Town today');a.tags=[TAG];a.static_mesh_component.set_static_mesh(cube);a.static_mesh_component.set_material(0,materials['Concrete']);a.set_actor_scale3d(u.Vector(sx,sy,h));created.append(a)
for x in [112,128]:
 for y in [-13.4,-6.6]:footing(x,y,canopy_z,.48,.48,'Fuel canopy footing')
def car(name,label,x,y,yaw,z=None):
 angle=math.radians(yaw);dx,dy=math.cos(angle),math.sin(angle)
 slope=(height(x+dx,y+dy)-height(x-dx,y-dy))/2
 return place(name,label,x,y,height(x,y)+.22 if z is None else z,yaw,math.degrees(math.atan(slope)) if z is None else 0)
car('SM_OldSedan','Abandoned blue sedan — stopped in main street',161,9.8,9)
car('SM_OldEstate','Abandoned estate — opposite lane',247,6.3,178)
car('SM_OldEstate','Estate left beside fuel pump',113.2,-10,90)
car('SM_OldSedan','Blue sedan waiting at forecourt exit',132,-2,67)
car('SM_OldSedan','Abandoned sedan — cross street',226.7,44,-87)
def apron(x,y):
 t=max(0,min(1,(y+11.5)/13.65));return shop_z*(1-t)+(height(x,2.15)+.29)*t
crash_pitch=math.degrees(math.atan((apron(182.8,-10.9)-apron(182.8,-8.9))/2))
place('SM_CrashedSedan','Crashed red sedan — nose inside broken shopfront',182.8,-9.90,apron(182.8,-9.9)+.025,-90,crash_pitch)
place('SM_CrashDebris','Shopfront — local brick and glass debris',182.8,-10.25,apron(182.8,-10.25)+.02,pitch=crash_pitch)
# Skid marks approach the shop from the nearby lane.
for x in [182.05,183.50]:
 for j in range(5):
  y=-1.5-j*1.35
  a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x*100,y*100,(apron(x,y)+.012)*100),u.Rotator(pitch=0,yaw=0,roll=crash_pitch));a.set_actor_label('Short braking mark');a.tags=[TAG];a.set_folder_path('03 Village/Town today');a.static_mesh_component.set_static_mesh(cube);a.static_mesh_component.set_material(0,materials['Rubber']);a.static_mesh_component.set_editor_property('cast_shadow',False);a.set_actor_scale3d(u.Vector(.13,1.15,.008));a.set_actor_enable_collision(False);created.append(a)
for x in [145,175,205,240,275,299]:
 place('SM_StreetLamp','Main street — unlit lamp',x,14.0,height(x,14)+.29)
for x in [157,198,266]:
 place('SM_StreetBench','Main street bench',x,14.0,height(x,14)+.29,yaw=180)
 place('SM_StreetBin','Main street litter bin',x+1.5,14.1,height(x+1.5,14.1)+.29)
# Open visibility within the town: reduce the former dense low valley blanket.
fog_before=[]
for a in actors.get_all_level_actors():
 if isinstance(a,u.ExponentialHeightFog):
  c=a.get_component_by_class(u.ExponentialHeightFogComponent);fog_before.append({'actor':a.get_actor_label(),'density':c.get_editor_property('fog_density')});c.set_editor_property('fog_density',.018)
after={a.get_path_name():state(a) for a in actors.get_all_level_actors() if a.get_path_name() in protected};assert after==protected,'Protected habitat transform changed'
assert len([a for a in actors.get_all_level_actors() if 'TerraceRockface' in [str(t) for t in a.tags]])==46,'Rockface layer missing'
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
report={'map':MAP,'backup':str(backup/source.name),'actors_added':len(created),'cleaned_cottages':cleaned,'town_vegetation_instances_removed':removed,'cars':6,'fuel_pumps':2,'replaced_cottage':oldshop.get_actor_label(),'protected_transforms_preserved':True,'rockface_actors_preserved':46,'previous_fog':fog_before,'shop_z_m':shop_z,'source':'SourceAssets/TownToday/Town-Today.blend','original_cottages':originals}
(ROOT/'Documentation/TownToday.json').write_text(json.dumps(report,indent=2));print('TOWN_APPLIED '+json.dumps(report),flush=True)
