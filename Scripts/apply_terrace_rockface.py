"""Add only the tagged rockface layer to the current default map. Rerunnable."""
import unreal as u, sys, re, json, random, math, shutil, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
MAP=re.search(r'GameDefaultMap=(.+)',(ROOT/'Config/DefaultEngine.ini').read_text()).group(1).strip()
# Keep a filesystem snapshot before saving the edited map.
src=ROOT/'Content'/Path(MAP.removeprefix('/Game/')+'.umap')
backup=ROOT/'Saved/Backups/TerraceRockface'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
backup.mkdir(parents=True,exist_ok=True); shutil.copy2(src,backup/src.name)
world=u.EditorLoadingAndSavingUtils.load_map(MAP); assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem); lib=u.EditorAssetLibrary; at=u.AssetToolsHelpers.get_asset_tools(); mel=u.MaterialEditingLibrary
BASE='/Game/Conservatory/Environment/TerraceRockface';lib.make_directory(BASE)
path=BASE+'/M_WeatheredLimestone'; mat=lib.load_asset(path) if lib.does_asset_exist(path) else at.create_asset('M_WeatheredLimestone',BASE,u.Material,u.MaterialFactoryNew())
mel.delete_all_material_expressions(mat)
def node(cls,**props):
 e=mel.create_material_expression(mat,cls)
 for k,v in props.items():e.set_editor_property(k,v)
 return e
pos=node(u.MaterialExpressionWorldPosition)
n=node(u.MaterialExpressionNoise,scale=.002,quality=1,levels=2)
mel.connect_material_expressions(pos,'',n,'Position')
a=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(.23,.22,.19,1)); b=node(u.MaterialExpressionConstant3Vector,constant=u.LinearColor(.32,.31,.27,1))
mix=node(u.MaterialExpressionLinearInterpolate)
for e,p in [(a,'A'),(b,'B'),(n,'Alpha')]:mel.connect_material_expressions(e,'',mix,p)
mel.connect_material_property(mix,'',u.MaterialProperty.MP_BASE_COLOR)
r=node(u.MaterialExpressionConstant,r=.91);mel.connect_material_property(r,'',u.MaterialProperty.MP_ROUGHNESS)
mel.recompile_material(mat);lib.save_loaded_asset(mat)
meshes={}
for file in sorted((ROOT/'SourceAssets/TerraceRockface').glob('*.fbx')):
 task=u.AssetImportTask();task.filename=str(file);task.destination_path=BASE;task.destination_name=file.stem;task.automated=True;task.save=True;task.replace_existing=True
 options=u.FbxImportUI();options.import_mesh=True;options.import_materials=False;options.import_textures=False;options.import_as_skeletal=False;options.mesh_type_to_import=u.FBXImportType.FBXIT_STATIC_MESH
 options.static_mesh_import_data.combine_meshes=True;options.static_mesh_import_data.auto_generate_collision=False;options.static_mesh_import_data.generate_lightmap_u_vs=False;task.options=options;at.import_asset_tasks([task])
 mesh=lib.load_asset(BASE+'/'+file.stem);assert mesh
 mesh.set_material(0,mat);body=mesh.get_editor_property('body_setup');body.set_editor_property('collision_trace_flag',u.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
 lib.save_loaded_asset(mesh);meshes[file.stem]=mesh
def state(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d()
 return [a.get_actor_label(),p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
TAG='TerraceRockface'; old=actors.get_all_level_actors(); unchanged={a.get_path_name():state(a) for a in old if TAG not in [str(t) for t in a.tags]}
for a in old:
 if TAG in [str(t) for t in a.tags]:actors.destroy_actor(a)
created=[]
def place(name,label,x,y,z,scale=(1,1,1),yaw=0):
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x*100,y*100,z*100),u.Rotator(pitch=0,yaw=yaw,roll=0));a.set_actor_label(label);a.set_folder_path('07 Hill-edge terrace/Rockface');a.tags=[TAG]
 a.static_mesh_component.set_static_mesh(meshes[name]);a.set_actor_scale3d(u.Vector(*scale));created.append(a);return a
bed=place('SM_TerraceBedrock','Weathered limestone — fitted terrace rockface',-91,0,0)
random.seed(90926)
for i in range(45):
 y=random.uniform(-42,42);x=random.uniform(-81,-74);s=random.uniform(.45,1.25)
 place('SM_TerraceStone_'+str(i%3+1),'Rockface toe stone %02d'%i,x,y,height(x,y)-.15,(s,s*random.uniform(.75,1.2),s),random.uniform(0,360))
# All existing transforms, including lift, robots, modules and circulation, remain untouched.
after={a.get_path_name():state(a) for a in actors.get_all_level_actors() if TAG not in [str(t) for t in a.tags]}
assert unchanged==after,'An existing actor changed'
origin,extent=bed.get_actor_bounds(False)
assert origin.z+extent.z<6140,'Rockface projects into terrace floor'
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
report={'map':MAP,'actors_added':len(created),'existing_actor_transforms_preserved':True,'rockface_top_cm':origin.z+extent.z,'terrace_deck_bottom_cm':6140,'backup':str(backup/src.name),'source':'SourceAssets/TerraceRockface/Terrace-Rockface.blend'}
(ROOT/'Documentation/TerraceRockface.json').write_text(json.dumps(report,indent=2));print('ROCKFACE_APPLIED '+json.dumps(report),flush=True)
