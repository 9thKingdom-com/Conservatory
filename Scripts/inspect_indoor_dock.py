import unreal as u,time,json,math
from pathlib import Path
ROOT=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_TerrainRobots'
start=None;origin=None;shot=False;stage=0;result={}
def tick(dt):
 global start,origin,shot,stage
 w=u.find_object(None,MAP+'.L_Exterior_TerrainRobots')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 bots=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot'))
 robot=next(b for b in bots if b.get_editor_property('robot_id')==11)
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 if start is None:
  start=now;p.set_actor_location(u.Vector(-10900,1370,6350),False,False);pc.set_control_rotation(u.Rotator(pitch=1,yaw=183,roll=0))
 t=now-start
 if t>3 and origin is None:origin=robot.get_actor_location()
 if t>10 and not shot:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation/IndoorRobotChargingDock.png').as_posix()+'"');shot=True
 if t>13 and stage==0:
  p.set_actor_location(u.Vector(-11270,1411.05,6340),False,False);stage=1
 if stage==1:
  if p.get_actor_location().x>-11580:p.add_movement_input(u.Vector(-1,0,0),.5,False)
  else:
   result['lift_entry_clear']=p.character_movement.is_moving_on_ground();stage=2
 if t>20:
  result.update({'count':len(bots),'stationary_drift_cm':math.dist([origin.x,origin.y,origin.z],[robot.get_actor_location().x,robot.get_actor_location().y,robot.get_actor_location().z]),'grounded':robot.character_movement.is_moving_on_ground(),'patrol_enabled':robot.get_editor_property('patrol_enabled')})
  result['passed']=len(bots)==11 and result['stationary_drift_cm']<1 and result['grounded'] and not result['patrol_enabled'] and result.get('lift_entry_clear',False)
  (ROOT/'Documentation/IndoorRobotDockRuntime.json').write_text(json.dumps(result,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)

