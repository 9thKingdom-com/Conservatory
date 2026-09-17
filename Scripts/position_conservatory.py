"""Place the enlarged conservatory on a supported hill-edge terrace in the library level."""
import unreal as u,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
MAP='/Game/Conservatory/Maps/L_Exterior_Modular'; CX=-10600; Z=6200; S=1.5
world=u.EditorLoadingAndSavingUtils.load_map(MAP); assert world
actors=u.get_editor_subsystem(u.EditorActorSubsystem)
for a in actors.get_all_level_actors():
 label=a.get_actor_label()
 if str(a.get_folder_path()).startswith('07 Hill-edge terrace'):
  actors.destroy_actor(a); continue
 if 'ConservatoryModule' in [str(t) for t in a.tags]:
  y=-1474.4*S if label.startswith('01') else 1474.4*S if label.startswith('03') else 0
  a.set_actor_location(u.Vector(CX,y,Z),False,False); a.set_actor_scale3d(u.Vector(S,S,S))
 if label=='Dome planter':
  y=(1 if a.get_actor_location().y>0 else -1)*1474.4*S
  a.set_actor_location(u.Vector(CX-300,y,6245),False,False); a.set_actor_scale3d(u.Vector(3,3,.9))
 if label=='Young white oak under dome':
  y=(1 if a.get_actor_location().y>0 else -1)*1474.4*S
  a.set_actor_location(u.Vector(CX-300,y,6290),False,False)
  mesh=a.get_component_by_class(u.StaticMeshComponent).get_editor_property('static_mesh')
  s=630/(mesh.get_bounds().box_extent.z*2); a.set_actor_scale3d(u.Vector(s,s,s))
 if isinstance(a,u.PlayerStart):
  a.set_actor_location(u.Vector(CX,0,6500),False,False); a.set_actor_rotation(u.Rotator(pitch=-5,yaw=0,roll=0),False)
  a.set_actor_label('Start — conservatory valley view')
 for c in a.get_components_by_class(u.HierarchicalInstancedStaticMeshComponent):
  keep=[]
  for i in range(c.get_instance_count()):
   t=c.get_instance_transform(i,world_space=True); x,y=t.translation.x/100,t.translation.y/100
   if -130<x<-83 and abs(y)<45: continue
   if -83<=x<135 and abs(y)<20 and 'Woodland' in label: continue
   keep.append(t)
  if len(keep)!=c.get_instance_count(): c.clear_instances(); c.add_instances(keep,False,True)
cube=u.load_asset('/Engine/BasicShapes/Cube')
stone=u.load_asset('/Game/Conservatory/Architecture/Materials/M_FloorLight')
metal=u.load_asset('/Game/Conservatory/Architecture/Materials/M_IvoryFrame')
glass=u.load_asset('/Game/Conservatory/Architecture/Materials/M_ConservatoryGlass')
def box(label,x,y,z,sx,sy,sz,mat=stone):
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x*100,y*100,z*100))
 a.set_actor_label(label); a.set_folder_path('07 Hill-edge terrace')
 a.static_mesh_component.set_static_mesh(cube); a.static_mesh_component.set_material(0,mat)
 a.set_actor_scale3d(u.Vector(sx,sy,sz)); return a
box('Terrace deck — 30 x 74 m',-106,0,61.7,30,74,.6)
for x in [-118,-106,-94]:
 for y in [-32,-16,0,16,32]:
  ground=height(x,y)-.5; top=61.4
  if top-ground>.25:
   box('Stone support pier',x,y,(ground+top)/2,1.8,1.8,top-ground)
   box('Pier footing',x,y,ground+.25,2.6,2.6,.5)
for y in [-32,-16,0,16,32]: box('Terrace cross-beam',-106,y,60.9,30,.65,1)
for y in range(-37,38,6): box('East glass balustrade post',-91,y,62.55,.065,.065,1.1,metal)
box('Clear valley-facing balustrade',-91,0,62.55,.025,74,1.1,glass)
for y in [-37,37]:
 for x in range(-121,-90,3): box('End balustrade post',x,y,62.57,.15,.15,1.14,metal)
 for z in [62.55,63.14]: box('End balustrade rail',-106,y,z,30,.12,.12,metal)
# The west edge meets the plateau; a broad landing makes the approach legible.
box('Hilltop approach landing',-124,0,61.87,6,8,.26)
assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
# Analytical check of the terrain sightline from the east glazing to village rooftops.
clearances=[]
for x in range(-94,211):
 line=64+(x+94)/(210+94)*(15-64)
 clearances.append(line-height(x,0))
report={'centre_cm':[CX,0,Z],'module_scale':S,'approx_footprint_m':[21.6,66],'terrace_m':[30,74],'floor_surface_cm':6242.75,'village_terrain_sightline_min_clearance_m':min(clearances)}
assert min(clearances)>0, 'Terrain obstructs village sightline'
(ROOT/'Documentation'/'HillEdgePlacement.json').write_text(json.dumps(report,indent=2))
print('HILL_EDGE_COMPLETE '+json.dumps(report),flush=True)


