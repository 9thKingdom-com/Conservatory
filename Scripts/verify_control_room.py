import unreal as u,time,json,math,traceback
from pathlib import Path
R=Path(u.Paths.project_dir());started=time.monotonic();stage=0;idx=0;mark=0;rows=[];report={};human=None

def xyz(v):return [v.x,v.y,v.z]
def tick(dt):
 global stage,idx,mark,human,before,robot_start
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 pc=u.GameplayStatics.get_player_controller(w,0)
 if not pc:return
 now=u.GameplayStatics.get_time_seconds(w);t=now-mark
 def finish(error=None):
  report.update(error=error,suits=rows,passed=len(rows)==11 and all(r.get('wear') and r.get('correct') and r.get('returned') and r.get('return_error',999)<1 for r in rows))
  (R/'Documentation/ControlRoomRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 try:
  if time.monotonic()-started>150:finish('timeout');return
  suits=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.VRSuitStation')),key=lambda s:s.robot_id)
  hub=u.GameplayStatics.get_actor_of_class(w,u.load_class(None,'/Script/Conservatory.RobotVRHub'))
  if stage==0 and now>5:human=u.GameplayStatics.get_player_pawn(w,0);stage=1
  elif stage==1:
   if idx==len(suits):
    s=suits[3];human.set_actor_location(s.get_actor_location()+s.get_actor_forward_vector()*60+u.Vector(0,0,87),False,True);pc.set_control_rotation(u.Rotator(pitch=0,yaw=s.get_actor_rotation().yaw+180,roll=0));stage=4;mark=now;return
   s=suits[idx];p=s.get_actor_location()+s.get_actor_forward_vector()*60+u.Vector(0,0,87);human.set_actor_location(p,False,True);human.character_movement.stop_movement_immediately();pc.set_control_rotation(u.Rotator(pitch=0,yaw=s.get_actor_rotation().yaw+180,roll=0));stage=2;mark=now
  elif stage==2 and t>1:
   s=suits[idx];eye=pc.player_camera_manager.get_camera_location();target=s.get_actor_location()+u.Vector(0,0,120);hit=u.SystemLibrary.line_trace_single(w,eye,target,u.TraceTypeQuery.ECC_VISIBILITY,False,[human],u.DrawDebugTrace.NONE);block=hit.to_tuple()[9] if hit and hit.to_tuple()[0] else None
   before=xyz(human.get_actor_location());row=dict(id=s.robot_id,position=before,can_use=s.can_use(),blocking_actor=str(block),eye=xyz(eye),target=xyz(target));rows.append(row)
   if idx==3:u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(R/'Documentation/ControlRoomSuitTest.png').as_posix()+'"')
   row['wear']=s.wear_suit();row['correct']=row['wear'] and u.GameplayStatics.get_player_pawn(w,0).robot_id==s.robot_id
   if row['wear']:robot_start=xyz(u.GameplayStatics.get_player_pawn(w,0).get_actor_location());stage=3;mark=now
   else:idx+=1;stage=1
  elif stage==3:
   if t<1:u.GameplayStatics.get_player_pawn(w,0).add_movement_input(u.GameplayStatics.get_player_pawn(w,0).get_actor_forward_vector(),1,False)
   else:
    rows[-1]['robot_moved_cm']=math.dist(robot_start,xyz(u.GameplayStatics.get_player_pawn(w,0).get_actor_location()));rows[-1]['returned']=hub.return_to_human();rows[-1]['return_error']=math.dist(before,xyz(u.GameplayStatics.get_player_pawn(w,0).get_actor_location()));idx+=1;stage=1
  elif stage==4 and t>1:
   (R/'Documentation/ControlRoomFReady.json').write_text(json.dumps(dict(ready=True,can_use=suits[3].can_use(),robot=4)));stage=5;mark=now
  elif stage==5:
   pawn=u.GameplayStatics.get_player_pawn(w,0)
   if pawn!=human:
    report['physical_f_correct_robot']=pawn.robot_id==4;stage=6;mark=now
  elif stage==6:
   if u.GameplayStatics.get_player_pawn(w,0)==human:report['physical_r_return']=True;finish()
 except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick)



