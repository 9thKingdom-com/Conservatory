import unreal as u,time,json
from pathlib import Path
ROOT=Path(u.Paths.project_dir());start=None;origin=None;phase=0
def tick(dt):
 global start,origin,phase
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR');p=u.GameplayStatics.get_player_character(w,0) if w else None
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 if start is None:
  start=now;p.set_actor_location(u.Vector(-12000,100,6340),False,False);p.character_movement.stop_movement_immediately();pc.set_control_rotation(u.Rotator(pitch=0,yaw=180,roll=0));origin=p.get_actor_location()
 t=now-start
 if phase==0:
  if t<11:p.add_movement_input(u.Vector(-1,0,0),1,False)
  else:
   pos=p.get_actor_location();path=ROOT/'Documentation/CoreHabitatRuntime.json';report=json.loads(path.read_text());check={'direction':2,'travel_cm':origin.x-pos.x,'capsule_z':pos.z,'lateral_offset_cm':100,'passed':origin.x-pos.x>3300 and abs(pos.z-6333)<25,'note':'One metre to the side of the retained outdoor robot 01; no robot edits.'};report['west_centreline_initial_test']=report['walkways'][2];report['walkways'][2]=check;report['passed']=all(c['passed'] for c in report['walkways']) and all(report.get(k) for k in ['lift_down','lift_up','bunker_arrival','habitat_arrival']);path.write_text(json.dumps(report,indent=2))
   p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.character_movement.stop_movement_immediately();p.set_actor_location(u.Vector(-10900,700,6590),False,False);pc.set_control_rotation(u.Rotator(pitch=-8,yaw=135,roll=0));phase=1;start=now
 elif phase==1 and t>4:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation/CoreHabitatLift.png').as_posix()+'"');phase=2;start=now
 elif phase==2 and t>2:
  u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)
