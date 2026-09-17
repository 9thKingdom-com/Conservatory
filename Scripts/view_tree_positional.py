import unreal as u,time,json,math,traceback
from pathlib import Path
R=Path(u.Paths.project_dir());start=time.monotonic();mark=start;phase=0;report={};plan=json.loads((R/'Documentation/TreePositionalImport.json').read_text());center=u.Vector(*plan['position'])
def tick(dt):
 global phase,mark
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0);pc=u.GameplayStatics.get_player_controller(w,0)
 if not p:return
 now=time.monotonic();t=now-mark
 def nextphase():
  global phase,mark
  phase+=1;mark=now
 def finish():
  (R/'Documentation/TreePositionalRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 try:
  if now-start>55:report['error']='timeout';finish();return
  if phase==0 and t>8:
   p.character_movement.stop_movement_immediately();p.set_actor_location(center+u.Vector(0,-860,100),False,True);p.character_movement.set_movement_mode(u.MovementMode.MOVE_WALKING);nextphase()
  elif phase==1:
   if t<2.0:p.add_movement_input(u.Vector(0,1,0),1,False)
   elif t>2.5:
    q=p.get_actor_location();report['planter_walk_block_distance_cm']=math.hypot(q.x-center.x,q.y-center.y);report['floor_standing_z']=q.z;report['planter_blocks_entry']=640<report['planter_walk_block_distance_cm']<730
    p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.character_movement.stop_movement_immediately();p.set_actor_location(center+u.Vector(900,0,100),False,True)
    blocked=[]
    for j in range(1,73):
     a=j*math.tau/72;dest=center+u.Vector(900*math.cos(a),900*math.sin(a),100);p.set_actor_location(dest,True,False)
     if (p.get_actor_location()-dest).length()>2:blocked.append(j)
    report['capsule_ring_radius_cm']=900;report['ring_blocked_segments']=blocked
    p.set_actor_location(center+u.Vector(-1250,-350,180),False,True);pc.set_control_rotation(u.Rotator(pitch=12,yaw=15.64,roll=0));nextphase()
  elif phase==2 and t>5:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1400x900 filename="'+(R/'Documentation/TreePositionalUnreal.png').as_posix()+'"');nextphase()
  elif phase==3 and t>2:
   report['passed']=report['planter_blocks_entry'] and not report['ring_blocked_segments'];finish()
 except Exception:report['error']=traceback.format_exc();finish()
handle=u.register_slate_post_tick_callback(tick)
