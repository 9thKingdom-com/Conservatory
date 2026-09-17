import unreal as u,time
from pathlib import Path
ROOT=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';start=None;shots=set()
def tick(dt):
 global start
 w=u.find_object(None,MAP+'.L_Exterior_RobotVR')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 if start is None:start=now
 t=now-start
 p.character_movement.stop_movement_immediately();p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING)
 if t<17:
  p.set_actor_location(u.Vector(-13470,1350,4090),False,False);pc.set_control_rotation(u.Rotator(pitch=7,yaw=0,roll=0))
 else:
  p.set_actor_location(u.Vector(-13650,1500,4090),False,False);pc.set_control_rotation(u.Rotator(pitch=0,yaw=-90,roll=0))
 for moment,name in [(10,'KitchenSecurityMonitor'),(25,'KitchenVRSuits')]:
  if t>moment and name not in shots:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation'/(name+'.png')).as_posix()+'"');shots.add(name)
 if t>32:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)
