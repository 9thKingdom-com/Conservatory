"""Upgrade the saved exterior without regenerating architecture or terrain.
Saves L_Exterior_Modular; L_Exterior remains the original procedural version.
"""
import unreal as u, random, sys, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height,path_y
BASE='/Game/Medieval_Environment/Real_Landscape/Default/Meshes/'
MAP='/Game/Conservatory/Maps/L_Exterior_Modular'
u.AssetRegistryHelpers.get_asset_registry().scan_paths_synchronous(['/Game/Medieval_Environment'],True)
world=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior')
assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
rules={'SM_Oak_1':('Trees/SM_White_Oak_01',1600),'SM_Oak_2':('Trees/SM_White_Oak_02',1400),'SM_Oak_3':('Trees/SM_White_Oak_01',1750),'SM_Oak_4':('Trees/SM_White_Oak_02',1300),'SM_Birch_1':('Trees/SM_White_Oak_Young_01',450),'SM_Birch_2':('Trees/SM_White_Oak_02',1100),'SM_Grass_1':('Plants/SM_Grass_01',40),'SM_Grass_2':('Plants/SM_Grass_01_Var01',40),'SM_Grass_3':('Plants/SM_Grass_Long_01',50),'SM_Fern':('Plants/SM_Fern_01',75)}
cache={}; report=[]
def load(name):
 if name in cache: return cache[name]
 mesh=u.load_asset(BASE+name); assert isinstance(mesh,u.StaticMesh),name
 for slot in mesh.get_editor_property('static_materials'):
  mat=slot.material_interface
  while isinstance(mat,u.MaterialInstanceConstant): mat=mat.get_editor_property('parent')
  if isinstance(mat,u.Material) and not mat.get_editor_property('used_with_instanced_static_meshes'):
   mat.set_editor_property('used_with_instanced_static_meshes',True)
   u.MaterialEditingLibrary.recompile_material(mat); u.EditorAssetLibrary.save_loaded_asset(mat)
 cache[name]=mesh; return mesh
for a in actors.get_all_level_actors():
 for c in a.get_components_by_class(u.HierarchicalInstancedStaticMeshComponent):
  old=c.get_editor_property('static_mesh')
  if not old or old.get_name() not in rules: continue
  name,target=rules[old.get_name()]; new=load(name); bounds=new.get_bounds()
  factor=target/(bounds.box_extent.z*2); bottom=max(0,bounds.origin.z-bounds.box_extent.z)
  transforms=[]
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,world_space=True)
   t.scale3d=u.Vector(t.scale3d.x*factor,t.scale3d.y*factor,t.scale3d.z*factor)
   t.translation=u.Vector(t.translation.x,t.translation.y,t.translation.z-bottom*t.scale3d.z)
   transforms.append(t)
  c.clear_instances(); c.set_static_mesh(new); c.add_instances(transforms,False,True)
  tree='Trees/' in name
  if not tree: c.set_cull_distances(13000,20000)
  a.set_actor_label(('Woodland ' if tree else 'Ground cover ')+new.get_name()+' | '+str(len(transforms)))
  report.append({'old':old.get_name(),'new':new.get_path_name(),'instances':len(transforms),'height_target_cm':target,'lods':new.get_num_lods()})
 # Replace the two small conservatory trees with a suitably sized real young oak.
 if a.get_actor_label()=='Young tree under dome':
  c=a.get_component_by_class(u.StaticMeshComponent); tree=load('Trees/SM_White_Oak_Young_01')
  c.set_static_mesh(tree); s=420/(tree.get_bounds().box_extent.z*2); a.set_actor_scale3d(u.Vector(s,s,s))
  a.set_actor_label('Young white oak under dome')

# Denser, shorter ground cover around the inspection area, avoiding buildings and track ruts.
random.seed(580203); additions=[]; meadow=load('Plants/SM_Grass_01_Var01')
for i in range(24000):
 x=random.uniform(-290,-85); y=random.uniform(-130,130)
 if abs(x+175)<10 and abs(y)<25: continue
 if -148<x<230 and abs(y-path_y(x))<1.7: continue
 if (x+105)**2+(y+20)**2<2.5**2: continue
 s=random.uniform(.85,1.4)
 additions.append(u.Transform(location=u.Vector(x*100,y*100,height(x,y)*100),rotation=u.Rotator(pitch=0,yaw=random.uniform(0,360),roll=0),scale=u.Vector(s,s,s)))
a=u.ExteriorTools.create_instances(meadow,additions,'Meadow grass — library assets',False)
a.get_component_by_class(u.HierarchicalInstancedStaticMeshComponent).set_cull_distances(10000,17000)
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
(ROOT/'Documentation'/'FoliageUpgrade.json').write_text(json.dumps({'map':MAP,'replacements':report,'additional_meadow_instances':len(additions)},indent=2))
print('FOLIAGE_UPGRADE_COMPLETE '+json.dumps(report),flush=True)


