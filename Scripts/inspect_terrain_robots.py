"""Exercise saved full-terrain routes and measure animation on the actual moving actors."""
import unreal as u,time,json,math,statistics
from pathlib import Path
ROOT=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_TerrainRobots'
start=None;last_sample=0;rows={};previous={};shots=set()
def vec(v):return [v.x,v.y,v.z]
def tick(dt):
 global start,last_sample
 w=u.find_object(None,MAP+'.L_Exterior_TerrainRobots')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 now=time.monotonic()
 if start is None:
  start=now;p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING)
 t=now-start
 bots=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot'))
 if t>5 and now-last_sample>.08:
  last_sample=now
  for b in bots:
   rid=b.get_editor_property('robot_id');pos=vec(b.get_actor_location());vel=b.get_velocity();speed=math.hypot(vel.x,vel.y)
   foot=vec(b.mesh.get_socket_location('foot_l'));local=u.MathLibrary.inverse_transform_location(b.mesh.get_world_transform(),u.Vector(*foot))
   if rid not in rows:rows[rid]={'start':pos,'distance_cm':0,'max_displacement_cm':0,'grounded':0,'samples':0,'moving_samples':0,'foot_positions':[],'stance_slip_cm_s':[],'destinations':[]}
   r=rows[rid];r['samples']+=1;r['grounded']+=b.character_movement.is_moving_on_ground();r['moving_samples']+=speed>20
   r['max_displacement_cm']=max(r['max_displacement_cm'],math.dist(pos,r['start']));r['end']=pos
   dest=vec(b.get_wander_destination())
   if dest!=[0,0,0] and dest not in r['destinations']:r['destinations'].append(dest)
   if rid in previous:
    old=previous[rid];r['distance_cm']+=math.dist(pos,old['pos'])
    if speed>100 and local.z<13 and old['z']<13 and now-old['time']<.3:
     r['stance_slip_cm_s'].append(math.dist(foot[:2],old['foot'][:2])/(now-old['time']))
   previous[rid]={'pos':pos,'foot':foot,'time':now,'z':local.z}
   if speed>100:r['foot_positions'].append([local.x,local.y,local.z])
 # Follow the town robot from a readable side angle; its movement is never modified.
 target=next((b for b in bots if b.get_editor_property('robot_id')==3),None)
 if target and 5<t<24:
  loc=target.get_actor_location();p.set_actor_location(loc+u.Vector(-320,-480,170),False,False)
  pc=u.GameplayStatics.get_player_controller(w,0);pc.set_control_rotation(u.Rotator(pitch=-12,yaw=56,roll=0))
 for moment,name in [(15,'TerrainRobotStrideA'),(15.4,'TerrainRobotStrideB')]:
  if t>moment and name not in shots:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation'/(name+'.png')).as_posix()+'"');shots.add(name)
 if t>90:
  for rid,r in rows.items():
   feet=r.pop('foot_positions');slip=r.pop('stance_slip_cm_s')
   r['foot_fore_aft_range_cm']=max((v[1] for v in feet),default=0)-min((v[1] for v in feet),default=0)
   r['median_stance_slip_cm_s']=statistics.median(slip) if slip else None
   r['stance_samples']=len(slip)
  result={'count':len(bots),'passed':len(rows)==11 and all(((r['max_displacement_cm']>1000 and r['foot_fore_aft_range_cm']>30) if rid!=11 else r['max_displacement_cm']<1) and r['grounded']/r['samples']>.95 for rid,r in rows.items()),'robots':rows}
  (ROOT/'Documentation/TerrainRobotsRuntime.json').write_text(json.dumps(result,indent=2))
  u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,None,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)

