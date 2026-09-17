"""Close spacing between room modules without moving furniture or doorways."""
import unreal as u
MAP='/Game/Conservatory/Maps/L_Exterior_Modular'
FOLDER='08 Bunker/06 Structural joins'
def seal(world):
 actors=u.get_editor_subsystem(u.EditorActorSubsystem)
 for a in actors.get_all_level_actors():
  if str(a.get_folder_path())==FOLDER: actors.destroy_actor(a)
 cube=u.load_asset('/Engine/BasicShapes/Cube')
 wall=u.load_asset('/Game/Conservatory/Bunker/Materials/M_Wall')
 concrete=u.load_asset('/Game/Conservatory/Bunker/Materials/M_Concrete')
 def block(name,x,y,z,sx,sy,sz,mat):
  a=actors.spawn_actor_from_class(u.StaticMeshActor,u.Vector(x*100,y*100,z*100))
  a.set_actor_label(name); a.set_folder_path(FOLDER)
  a.static_mesh_component.set_static_mesh(cube); a.static_mesh_component.set_material(0,mat)
  a.static_mesh_component.set_collision_profile_name('BlockAll'); a.set_actor_scale3d(u.Vector(sx,sy,sz))
  return a
 # Rooms are 14 m deep on 15 m centres. Fill the 1 m service joints
 # through their entire depth, from below the floor to above the ceiling.
 for z in [34,40]:
  for x in [-154,-136]:
   for y in [-22.5,-7.5,7.5]:
    block('Solid room joint',x,y,z+1.7375,12.04,1.04,4.115,wall)
 # The lower hall previously looked above the room ceilings into the void.
 block('Utilities corridor ceiling',-145,-3,37.65,6,46,.25,concrete)
 if len([a for a in actors.get_all_level_actors() if str(a.get_folder_path())==FOLDER])!=13:
  raise RuntimeError('Incomplete structural joint pass')
if __name__=='__main__':
 world=u.EditorLoadingAndSavingUtils.load_map(MAP); assert world
 seal(world)
 assert u.EditorLoadingAndSavingUtils.save_map(world,MAP)
 print('BUNKER_JOINTS_SEALED: 12 full-depth joins and lower corridor ceiling')


