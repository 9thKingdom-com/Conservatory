"""Windowed, automatically exiting visual review of the saved Landscape study."""
import unreal as u,time,json
from pathlib import Path
root=Path(u.Paths.project_dir());start=time.monotonic();stage=0
views=[('RuralClearedOverview',(80,-250,270),40,-35)]
def tick(dt):
 global stage,start
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0);pc=u.GameplayStatics.get_player_controller(w,0)
 if not p or not pc:return
 t=time.monotonic()-start
 if stage>=len(views)*2:
  if t>2:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
  return
 name,pos,yaw,pitch=views[stage//2]
 if stage%2==0:
  p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);pc.set_ignore_look_input(True)
  p.set_actor_location(u.Vector(*[v*100 for v in pos]),False,True);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0));stage+=1;start=time.monotonic()
 elif t>12:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1600x900 filename="'+(root/'Documentation'/(name+'.png')).as_posix()+'"');stage+=1;start=time.monotonic()
handle=u.register_slate_post_tick_callback(tick)

