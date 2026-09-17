import unreal as u,time,json
from pathlib import Path
root=Path(u.Paths.project_dir()); start=None; phase=0; points=[]
def tick(dt):
 global start,phase
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_Modular.L_Exterior_Modular')
 if not w: return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p: return
 pc=u.GameplayStatics.get_player_controller(w,0)
 if start is None:
  start=time.monotonic(); pc.set_ignore_look_input(True); p.set_actor_location(u.Vector(-14282,2490,4092),False,False); pc.set_control_rotation(u.Rotator(pitch=-25,yaw=-90,roll=0))
 t=time.monotonic()-start; pos=p.get_actor_location()
 if phase==0 and t>3:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(root/'Documentation'/'StairLanding.png').as_posix()+'"'); phase=1
 if phase==1 and t>4:
  if pos.y>1870: p.add_movement_input(u.Vector(0,-1,0),1,False)
  else: points.append({'direction':'stairs_to_corridor','z':pos.z,'passed':abs(pos.z-4090)<15}); phase=2
 elif phase==2:
  if pos.y<2460: p.add_movement_input(u.Vector(0,1,0),1,False)
  else: points.append({'direction':'corridor_to_stairs','z':pos.z,'passed':abs(pos.z-4090)<15}); phase=3
 if phase==3 or t>18:
  (root/'Documentation'/'LandingWalkTest.json').write_text(json.dumps({'crossings':points,'passed':len(points)==2 and all(r['passed'] for r in points)},indent=2))
  u.unregister_slate_post_tick_callback(handle); u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)


