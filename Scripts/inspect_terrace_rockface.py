"""Opt-in runtime photographs of the saved rockface, without saving gameplay changes."""
import unreal as u,time,re
from pathlib import Path
ROOT=Path(u.Paths.project_dir()); MAP=re.search(r'GameDefaultMap=(.+)',(ROOT/'Config/DefaultEngine.ini').read_text()).group(1).strip()
views=[('TerraceRockface',-4800,-7700,7200,143,-9),('TerraceRockfaceDetail',-6800,-2200,5750,166,7)]
stage=0; changed=0;shot=False
def tick(dt):
 global stage,changed,shot
 w=u.find_object(None,MAP+'.'+MAP.rsplit('/',1)[-1])
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 if not changed:
  name,x,y,z,yaw,pitch=views[stage]
  p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.character_movement.stop_movement_immediately();pc.set_ignore_look_input(True)
  p.set_actor_location(u.Vector(x,y,z),False,False);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0));changed=now
 if now-changed>12 and not shot:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1600x900 filename="'+(ROOT/'Documentation'/(views[stage][0]+'.png')).as_posix()+'"');shot=True
 if now-changed>15:
  stage+=1;changed=0;shot=False
  if stage==len(views):
   u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)
