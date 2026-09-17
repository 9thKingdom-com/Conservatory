import unreal as u,time,json,math,traceback
from pathlib import Path
R=Path(u.Paths.project_dir());started=time.monotonic();stage=0;mark=started;idx=0;rows=[];roam={};human=None;report={}
def xyz(p):return [p.x,p.y,p.z]
def tick(dt):
 global stage,mark,idx,human,begin,hpos
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 pc=u.GameplayStatics.get_player_controller(w,0)
 if not pc or not u.GameplayStatics.get_player_pawn(w,0):return
 now=u.GameplayStatics.get_time_seconds(w);t=now-mark
 def finish():
  report['suits']=rows;report['roaming']=roam
  report['passed']=len(rows)==11 and all(r.get('wear') and r.get('correct') and r.get('moved_cm',0)>100 and r.get('return') and r.get('human_error_cm',999)<2 for r in rows) and len(roam)==10 and all(r['distance_cm']>500 and r['grounded']>r['samples']*.9 for r in roam.values())
  (R/'Documentation/RobotAccessRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 try:
  if time.monotonic()-started>240:report['error']='timeout';finish();return
  bots=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot')),key=lambda a:a.robot_id)
  suits=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.VRSuitStation')),key=lambda a:a.robot_id)
  hub=u.GameplayStatics.get_actor_of_class(w,u.load_class(None,'/Script/Conservatory.RobotVRHub'))
  if stage==0 and now>5:
   human=u.GameplayStatics.get_player_pawn(w,0);report['suit_ids']=[s.robot_id for s in suits];stage=1
  elif stage==1:
   if idx==11:stage=5;mark=now;return
   s=suits[idx];v=s.get_actor_forward_vector();human.set_actor_location(s.get_actor_location()+v*145+u.Vector(0,0,87),False,True);human.character_movement.stop_movement_immediately();pc.set_control_rotation(u.Rotator(pitch=-13,yaw=s.get_actor_rotation().yaw+180,roll=0));stage=2;mark=now
  elif stage==2 and t>.8:
   if idx==10:u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(R/'Documentation/Suit11.png').as_posix()+'"')
   hpos=xyz(human.get_actor_location());ok=suits[idx].wear_suit();p=u.GameplayStatics.get_player_pawn(w,0);rows.append(dict(id=suits[idx].robot_id,wear=ok,correct=ok and p.robot_id==suits[idx].robot_id));begin=xyz(p.get_actor_location());stage=3;mark=now
   if not ok:stage=4
  elif stage==3:
   p=u.GameplayStatics.get_player_pawn(w,0)
   if t<2:p.add_movement_input(p.get_actor_forward_vector(),1,False)
   else:
    rows[-1]['moved_cm']=math.dist(begin[:2],xyz(p.get_actor_location())[:2]);rows[-1]['grounded']=p.character_movement.is_moving_on_ground();rows[-1]['return']=hub.return_to_human();rows[-1]['human_error_cm']=math.dist(hpos,xyz(human.get_actor_location()));stage=4;mark=now
  elif stage==4 and t>.3:idx+=1;stage=1
  elif stage==5:
   for b in bots[:10]:
    key=str(b.robot_id);p=xyz(b.get_actor_location())
    if key not in roam:roam[key]=dict(start=p,last=p,distance_cm=0,grounded=0,samples=0)
    r=roam[key];r['distance_cm']+=math.dist(p[:2],r['last'][:2]);r['last']=p;r['samples']+=1;r['grounded']+=b.character_movement.is_moving_on_ground()
   if t>35:finish()
 except Exception:report['error']=traceback.format_exc();finish()
handle=u.register_slate_post_tick_callback(tick)
