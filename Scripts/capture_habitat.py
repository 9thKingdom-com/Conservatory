"""Capture settled runtime views, keeping camera changes after screenshot rendering."""
import unreal as u,time
from pathlib import Path
ROOT=Path(u.Paths.project_dir()); index=0; changed=0; captured=False
views=[
 ('SpiralStair',-14090,2400,4092,166,-48),
 ('WaterPumping',-14950,-1900,3492,130,-4),
 ('OxygenRoom',-14030,-1930,3492,48,-4),
 ('LibraryStudy',-14040,-1940,4092,44,-3),
 ('SleepingQuarters',-14960,-440,4092,135,-5),
 ('ServiceLift',-10620,-420,6335,180,0),
 ('VillageFromConservatory',-10100,0,6380,0,-9),
 ('SeedLaboratory',-14980,-1830,4092,130,-5),
]
if '-StairPhoto' in u.SystemLibrary.get_command_line(): views=views[:1]
if '-LiftPhoto' in u.SystemLibrary.get_command_line(): views=[v for v in views if v[0]=='ServiceLift']
if '-JointPhoto' in u.SystemLibrary.get_command_line(): views=[('SealedRoomJoints',-14500,-750,3492,180,8)]
def tick(dt):
 global index,changed,captured
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_Modular.L_Exterior_Modular')
 if not w: return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p: return
 pc=u.GameplayStatics.get_player_controller(w,0); now=time.monotonic()
 if not changed:
  name,x,y,z,yaw,pitch=views[index]
  pc.set_ignore_look_input(True); p.character_movement.stop_movement_immediately(); p.set_actor_location(u.Vector(x,y,z),False,False)
  pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0)); changed=now
 if now-changed>4 and not captured:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Saved'/'Screenshots'/(views[index][0]+'.png')).as_posix()+'"'); captured=True
 if now-changed>5.5:
  index+=1; changed=0; captured=False
  if index==len(views):
   u.unregister_slate_post_tick_callback(handle); u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)


