import unreal as u,time,json,math,traceback
from pathlib import Path
R=Path(u.Paths.project_dir());start=time.monotonic();rows={};last_sample=0;photo=False

def xyz(p):return [p.x,p.y,p.z]
def tick(dt):
 global last_sample,photo
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 pc=u.GameplayStatics.get_player_controller(w,0)
 if not pc:return
 t=u.GameplayStatics.get_time_seconds(w)
 def finish(error=None):
  passed=len(rows)==11 and all(r['inside_failures']==0 and r['destination_failures']==0 and r['grounded']/max(1,r['samples'])>.95 and (r['distance_cm']>1000 if k!='11' else r['distance_cm']<10) for k,r in rows.items())
  (R/'Documentation/RobotRuralRuntime.json').write_text(json.dumps(dict(passed=passed,error=error,duration_seconds=t,robots=rows),indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 try:
  if time.monotonic()-start>150:finish('timeout');return
  if t<5 or t-last_sample<.2:return
  last_sample=t
  bots=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot'))
  for b in bots:
   p=xyz(b.get_actor_location());key=str(b.robot_id)
   if key not in rows:rows[key]=dict(start=p,last=p,distance_cm=0,grounded=0,samples=0,inside_failures=0,destination_failures=0,destinations=[])
   r=rows[key];r['distance_cm']+=math.dist(p[:2],r['last'][:2]);r['last']=p;r['samples']+=1;r['grounded']+=b.character_movement.is_moving_on_ground()
   if b.robot_id!=11:
    r['inside_failures']+=not b.is_inside_wander_bounds(b.get_actor_location())
    dest=b.get_wander_destination();d=xyz(dest)
    if any(v!=0 for v in d):
     r['destination_failures']+=not b.is_inside_wander_bounds(dest)
     if d not in r['destinations']:r['destinations'].append(d)
  if not photo and t>15:
   b=next(b for b in bots if b.robot_id==3);p=u.GameplayStatics.get_player_pawn(w,0);p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.set_actor_location(b.get_actor_location()+u.Vector(-700,-700,400),False,True);pc.set_control_rotation(u.Rotator(pitch=-18,yaw=45,roll=0));photo=True
  if photo and t>17 and photo is True:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(R/'Documentation/RobotRuralGrounded.png').as_posix()+'"');photo='done'
  if t>75:finish()
 except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick)
