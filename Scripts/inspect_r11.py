"""Opt-in saved-map R11 camera, task pause and possession regression."""
import unreal as u, time, json
from pathlib import Path
start=None
stage=0
report={}
def tick(dt):
 global start,stage,body,robot,hub,phase,status,position
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 pc=u.GameplayStatics.get_player_controller(w,0)
 if not pc or not u.GameplayStatics.get_player_pawn(w,0):return
 if start is None:
  start=time.monotonic()
  body=u.GameplayStatics.get_player_pawn(w,0)
  body.set_actor_location(u.Vector(-13470,1350,4090),False,False)
  pc.set_control_rotation(u.Rotator(pitch=7,yaw=0,roll=0))
  hub=u.GameplayStatics.get_actor_of_class(w,u.load_class(None,'/Script/Conservatory.RobotVRHub'))
  robot=next(a for a in u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot')) if a.robot_id==11)
 t=time.monotonic()-start
 if stage==0 and t>4:
  report['select_r11']=hub.select_robot(11)
  report['monitor_open']=hub.open_monitor()
  report['task_assigned']=robot.submit_task('collect timber')
  phase=robot.get_task_phase();status=robot.get_task_status()
  report['task_status']=status
  position=body.get_actor_location()
  report['enter']=hub.enter_robot(11)
  report['correct_pawn']=u.GameplayStatics.get_player_pawn(w,0)==robot
  stage=1
 elif stage==1 and t>7:
  report['task_paused']=robot.get_task_phase()==phase and robot.get_task_status()==status
  report['feed_exists']=robot.get_feed() is not None
  report['returned']=hub.return_to_human() and u.GameplayStatics.get_player_pawn(w,0)==body
  report['body_return_error']=body.get_actor_location().distance(position)
  stage=2
 elif stage==2 and t>8:
  report['ai_restored']=robot.get_controller() is not None and robot.get_controller()!=pc
  report['task_retained']=robot.get_task_phase()==phase
  report['passed']=all(report[k] for k in ['select_r11','monitor_open','task_assigned','enter','correct_pawn','task_paused','feed_exists','returned','ai_restored','task_retained']) and report['body_return_error']<1
  (Path(u.Paths.project_dir())/'Documentation/R11Runtime.json').write_text(json.dumps(report,indent=2))
  u.unregister_slate_post_tick_callback(handle)
  u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)

