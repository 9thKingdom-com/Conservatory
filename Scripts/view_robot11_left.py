import unreal as u,time,json,math,traceback
from pathlib import Path
R=Path(u.Paths.project_dir());start=time.monotonic();phase=0;mark=start;report={}
def tick(dt):
 global phase,mark
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 pc=u.GameplayStatics.get_player_controller(w,0);p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 now=time.monotonic()
 def finish():
  (R/'Documentation/Robot11LeftRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 try:
  if now-start>40:report['error']='timeout';finish();return
  if phase==0 and now-start>7:
   plan=json.loads((R/'Documentation/Robot11LeftMove.json').read_text());bots=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot'));bot=next(a for a in bots if a.get_editor_property('robot_id')==11)
   q=bot.get_actor_location();report['robot_runtime_position']=[q.x,q.y,q.z];report['near_saved_position']=(q-u.Vector(*plan['robot_position'])).length()<10
   upper=max(u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift')),key=lambda a:a.get_actor_location().z);v=upper.get_actor_location();yaw=upper.get_actor_rotation().yaw;ang=math.radians(yaw);f=u.Vector(math.cos(ang),math.sin(ang),0);side=u.Vector(-math.sin(ang),math.cos(ang),0)
   p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.character_movement.stop_movement_immediately();p.set_actor_location(v+f*790+side*65+u.Vector(0,0,160),False,True);pc.set_control_rotation(u.Rotator(pitch=-8,yaw=yaw+180,roll=0));phase=1;mark=now
  elif phase==1 and now-mark>4:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(R/'Documentation/Robot11Left.png').as_posix()+'"');phase=2;mark=now
  elif phase==2 and now-mark>2:finish()
 except Exception:report['error']=traceback.format_exc();finish()
handle=u.register_slate_post_tick_callback(tick)

