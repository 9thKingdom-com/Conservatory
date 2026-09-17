"""Park unit 11 on a compact contact dock beside the upper lift, clear of its entry."""
import unreal as u,json
from pathlib import Path
ROOT=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_TerrainRobots'
w=u.EditorLoadingAndSavingUtils.load_map(MAP);actors=u.get_editor_subsystem(u.EditorActorSubsystem);lib=u.EditorAssetLibrary
folder='10 Wandering Mannequins/Indoor charging dock'
for a in actors.get_all_level_actors():
 if str(a.get_folder_path())==folder:actors.destroy_actor(a)
robot=next(a for a in actors.get_all_level_actors() if a.get_class().get_name()=='C17Robot' and a.get_editor_property('robot_id')==11)
x,y,z=-11480,1161.05,6242.75
mats={'green':lib.load_asset('/Game/Conservatory/Architecture/OrnateLift/M_LiftEnamel'),'brass':lib.load_asset('/Game/Conservatory/Architecture/OrnateLift/M_AgedBrass'),'dark':lib.load_asset('/Game/Conservatory/Robots/C17/M_C17_Graphite'),'steel':lib.load_asset('/Game/Conservatory/Robots/C17/M_C17_Steel')}
cube=lib.load_asset('/Engine/BasicShapes/Cube')
def box(name,dx,dy,dz,sx,sy,sz,mat):
 a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x+dx,y+dy,z+dz));a.set_actor_label('Robot 11 dock - '+name);a.set_folder_path(folder)
 a.static_mesh_component.set_static_mesh(cube);a.static_mesh_component.set_material(0,mats[mat]);a.set_actor_scale3d(u.Vector(sx/100,sy/100,sz/100));return a
box('low steel plinth',0,0,2,120,100,4,'steel')
box('non-slip standing pad',5,0,4.5,103,89,1,'dark')
for dy in [-42,42]:box('edge inlay',5,dy,5.1,100,1.5,.25,'brass')
for dy in [-17,17]:box('foot charging contact',2,dy,5.3,30,8,.5,'brass')
box('rear charging pedestal',-49,0,73,18,64,142,'green')
box('pedestal face',-39.5,0,86,1,52,110,'dark')
for dy in [-14,14]:box('back contact',-35,dy,100,8,8,12,'brass')
box('status panel',-38,0,134,2,43,16,'steel')
a=actors.spawn_actor_from_class(u.TextRenderActor,u.Vector(x-36.5,y,z+134));a.set_actor_label('Robot 11 dock identity');a.set_folder_path(folder)
c=a.get_component_by_class(u.TextRenderComponent);c.set_text('ROBOT 11\nCHARGING DOCK');c.set_world_size(3.5);c.set_horizontal_alignment(u.HorizTextAligment.EHTA_CENTER);c.set_vertical_alignment(u.VerticalTextAligment.EVRTA_TEXT_CENTER);c.set_text_render_color(u.Color(25,42,35,255))
robot.set_actor_label('Indoor robot 11 - charging dock')
robot.set_editor_property('patrol_enabled',False);robot.set_editor_property('wander_enabled',False);robot.set_editor_property('terrain_wander',False)
robot.set_actor_location(u.Vector(x+5,y,z+5.6+98),False,True);robot.set_actor_rotation(u.Rotator(0,0,0),False)
assert u.ExteriorTools.build_terrain_navigation()
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
(ROOT/'Documentation/IndoorRobotDock.json').write_text(json.dumps({'map':MAP,'robot_id':11,'pad_center':[x,y,z],'robot_position':[x+5,y,z+103.6],'pad_size_cm':[120,100,5.6],'lift_side_gap_cm':75,'scope':'Physical charging dock and stationary idle robot; battery simulation is future work.'},indent=2))


