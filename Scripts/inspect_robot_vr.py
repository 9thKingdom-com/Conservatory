"""Saved-map integration checks: monitor, all ten physical suits, possession and AI resume."""
import unreal as u,time,json,math
from pathlib import Path
ROOT=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
start=None;stage=0;changed=0;index=0;human=None;before=None;robot_start=None;returned=None;checks=[];report={};shot=False
def xyz(v):return [v.x,v.y,v.z]
def tick(dt):
 global start,stage,changed,index,human,before,robot_start,returned,shot
 w=u.find_object(None,MAP+'.L_Exterior_RobotVR')
 if not w:return
 pc=u.GameplayStatics.get_player_controller(w,0)
 if not pc or not u.GameplayStatics.get_player_pawn(w,0):return
 hub=u.GameplayStatics.get_actor_of_class(w,u.load_class(None,'/Script/Conservatory.RobotVRHub'))
 if not hub:return
 suits=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.VRSuitStation')),key=lambda a:a.get_editor_property('robot_id'))
 now=time.monotonic()
 def photo(name):u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation'/(name+'.png')).as_posix()+'"')
 if start is None:
  start=now;changed=now;human=u.GameplayStatics.get_player_pawn(w,0);human.set_actor_location(u.Vector(-13470,1350,4090),False,False);pc.set_control_rotation(u.Rotator(pitch=7,yaw=0,roll=0))
  report['suit_ids']=[a.get_editor_property('robot_id') for a in suits]
  report['old_terminals']=len(u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.RobotTerminal')))
 t=now-changed
 if stage==0 and t>5:
  photo('KitchenSecurityMonitor');stage=9;changed=now
 elif stage==9 and t>1:
  report['monitor_open']=hub.open_monitor();stage=1;changed=now
 elif stage==1 and t>2:
  report['select_10']=hub.select_robot(10);stage=6;changed=now
 elif stage==6 and t>1:
  u.RenderingLibrary.export_render_target(w,hub.get_monitor_texture(),str(ROOT/'Documentation'),'RobotSecurityDisplay.png');hub.close_monitor();stage=2;changed=now
 elif stage==2:
  if index==10:
   human.set_actor_location(u.Vector(-13800,1500,4090),False,False);pc.set_control_rotation(u.Rotator(pitch=0,yaw=-65,roll=0));stage=7;changed=now;return
  loc=suits[index].get_actor_location();human.set_actor_location(loc+u.Vector(0,145,87),False,False);human.character_movement.stop_movement_immediately();pc.set_control_rotation(u.Rotator(pitch=-13,yaw=-90,roll=0));stage=3;changed=now
 elif stage==3 and t>.7:
  before=xyz(human.get_actor_location());ok=suits[index].wear_suit();pawn=u.GameplayStatics.get_player_pawn(w,0)
  row={'id':index+1,'wear_accepted':ok,'correct_robot':ok and pawn.get_editor_property('robot_id')==index+1}
  checks.append(row)
  if not ok:report['failed_station']=index+1;stage=8;changed=now;return
  robot_start=xyz(pawn.get_actor_location());stage=4;changed=now;shot=False
 elif stage==4:
  pawn=u.GameplayStatics.get_player_pawn(w,0)
  if t<1.5:pawn.add_movement_input(pawn.get_actor_forward_vector(),1,False);pawn.add_controller_yaw_input(.15)
  if index==2 and t>1 and not shot:photo('RobotVREyeView');shot=True
  if t>2:
   checks[-1]['moved_cm']=math.dist(robot_start,xyz(pawn.get_actor_location()));checks[-1]['human_stayed_cm']=math.dist(before,xyz(human.get_actor_location()))
   eyes=pawn.robot_eyes.get_world_location();capture=pawn.capture.get_world_location();checks[-1]['eye_feed_alignment_cm']=math.dist(xyz(eyes),xyz(capture))
   returned=pawn;checks[-1]['return_accepted']=hub.return_to_human();checks[-1]['returned_to_human']=u.GameplayStatics.get_player_pawn(w,0)==human;checks[-1]['return_position_error_cm']=math.dist(before,xyz(human.get_actor_location()));robot_start=xyz(returned.get_actor_location());stage=5;changed=now
 elif stage==5 and t>3:
  checks[-1]['ai_resumed']=returned.get_controller() is not None and returned.get_controller()!=pc
  checks[-1]['autonomous_movement_cm']=math.dist(robot_start,xyz(returned.get_actor_location()));index+=1;stage=2;changed=now
 elif stage==7 and t>3:photo('KitchenVRSuits');stage=8;changed=now
 elif stage==8 and t>2:
  report['pairings']=checks;report['passed']=report['suit_ids']==list(range(1,11)) and report['old_terminals']==0 and report.get('monitor_open') and report.get('select_10') and len(checks)==10 and all(r.get('correct_robot') and r.get('moved_cm',0)>50 and r.get('human_stayed_cm',999)<1 and r.get('returned_to_human') and r.get('return_position_error_cm',999)<1 and r.get('ai_resumed') and r.get('eye_feed_alignment_cm',999)<1 for r in checks)
  (ROOT/'Documentation/RobotVRRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)


