import unreal as u,time,json,math,traceback
from pathlib import Path
ROOT=Path(u.Paths.project_dir());phase=0;start=time.monotonic();phase_start=start;report={}
def tick(dt):
 global phase,phase_start
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic();t=now-phase_start
 lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));upper=max(lifts,key=lambda a:a.get_actor_location().z);lower=min(lifts,key=lambda a:a.get_actor_location().z)
 v=upper.get_actor_location();yaw=upper.get_actor_rotation().yaw;d=u.Vector(math.cos(math.radians(yaw)),math.sin(math.radians(yaw)),0)
 def advance():
  global phase,phase_start
  phase+=1;phase_start=now
 def quit():
  (ROOT/'Documentation/LiftMasterRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 def move(v,yaw,pitch=0):
  p.character_movement.stop_movement_immediately();p.set_actor_location(v,False,False);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0))
 try:
  if now-start>65:report['error']='timeout';quit();return
  if phase==0 and t>7:
   move(v+d*480,yaw+180);advance()
  elif phase==1:
   if t<1.15:p.add_movement_input(d*-1,1,False)
   elif t>1.5:
    report['walk_into_lift_distance_cm']=(p.get_actor_location()-v).length();report['down']=upper.travel();advance()
  elif phase==2 and t>2:
   report['bunker_arrival']=(p.get_actor_location()-lower.get_actor_location()).length()<60;report['up']=lower.travel();advance()
  elif phase==3 and t>2:
   report['upper_arrival']=(p.get_actor_location()-v).length()<60;advance()
  elif phase==4:
   if t<1.4:p.add_movement_input(d,1,False)
   elif t>1.8:
    report['walk_out_distance_cm']=(p.get_actor_location()-v).length();report['floor_z']=p.get_actor_location().z
    p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);move(v+d*650+u.Vector(0,0,180),yaw+180,-8);advance()
  elif phase==5 and t>3:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation/LiftMasterUnreal.png').as_posix()+'"');advance()
  elif phase==6 and t>2:
   report['passed']=all(report.get(k,False) for k in ['down','up','bunker_arrival','upper_arrival']) and report['walk_out_distance_cm']>300 and abs(report['floor_z']-6331)<35;quit()
 except Exception:report['error']=traceback.format_exc();quit()
handle=u.register_slate_post_tick_callback(tick)

