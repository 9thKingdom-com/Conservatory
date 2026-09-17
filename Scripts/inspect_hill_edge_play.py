"""Run game with -LibraryInspection to verify the enlarged site without rebuilding modules."""
import unreal as u,json,time
from pathlib import Path
ROOT=Path(u.Paths.project_dir()); started=None; stage=0; origin=None; report={}
def capture(world,name):
 path=(ROOT/'Saved'/'Screenshots'/(name+'.png')).as_posix()
 u.SystemLibrary.execute_console_command(world,'HighResShot 1280x720 filename="'+path+'"')
def tick(dt):
 global started,stage,origin,handle
 try:
  world=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_Modular.L_Exterior_Modular')
  if not world: return
  pawn=u.GameplayStatics.get_player_character(world,0)
  if not pawn: return
  pc=u.GameplayStatics.get_player_controller(world,0)
  if started is None:
   started=time.monotonic(); pc.set_ignore_look_input(True); pc.set_control_rotation(u.Rotator(pitch=0,yaw=90,roll=0))
  t=time.monotonic()-started
  if t>4 and stage==0: origin=pawn.get_actor_location(); stage=1
  if 4<t<9: pawn.add_movement_input(u.Vector(0,1,0),1,False)
  if t>10 and stage==1:
   p=pawn.get_actor_location(); distance=((p.x-origin.x)**2+(p.y-origin.y)**2)**.5
   report.update({'walk_distance_cm':distance,'capsule_z_cm':p.z,'passed':distance>1200 and abs(p.z-6333)<25})
   pawn.set_actor_location(u.Vector(-10100,0,6380),False,False); pc.set_control_rotation(u.Rotator(pitch=-9,yaw=0,roll=0)); stage=2
  if t>15 and stage==2: capture(world,'VillageFromConservatory'); stage=3
  if t>19 and stage==3:
   pawn.set_actor_location(u.Vector(-15700,-2600,6500),False,False); pc.set_control_rotation(u.Rotator(pitch=5,yaw=27,roll=0)); stage=4
  if t>24 and stage==4: capture(world,'EnlargedConservatory'); stage=5
  if t>28 and stage==5:
   pawn.set_actor_location(u.Vector(-18000,-5200,6500),False,False); pc.set_control_rotation(u.Rotator(pitch=0,yaw=-75,roll=0)); stage=6
  if t>33 and stage==6: capture(world,'LibraryWoodland'); stage=7
  if t>37 and stage==7:
   (ROOT/'Documentation'/'HillEdgeWalkTest.json').write_text(json.dumps(report,indent=2))
   print('LIBRARY_PLAY_TEST '+json.dumps(report),flush=True)
   u.unregister_slate_post_tick_callback(handle); stage=8
   u.SystemLibrary.quit_game(world,pc,u.QuitPreference.QUIT,False)
 except Exception as exc:
  print('LIBRARY_PLAY_ERROR '+repr(exc),flush=True)
  u.unregister_slate_post_tick_callback(handle)
handle=u.register_slate_post_tick_callback(tick)


