"""Runtime movement, population, containment and animation checks plus screenshots."""
import unreal as u,time,json,math
from pathlib import Path
ROOT=Path(u.Paths.project_dir()); MAP='/Game/Conservatory/Maps/L_Exterior_WanderingBots'
placements=json.loads((ROOT/'Documentation/WanderingBots.json').read_text())['bots']
started=None; centers={}; origins={}; distances={}; shots=set(); errors=[]; samples={}
def tick(dt):
 global started
 w=u.find_object(None,MAP+'.L_Exterior_WanderingBots')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 bots=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot'))
 now=time.monotonic()
 if started is None:
  started=now
  pc=u.GameplayStatics.get_player_controller(w,0);pc.set_ignore_look_input(True)
  p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING)
 t=now-started
 if t>5:
  for b in bots:
   n=b.get_name();v=b.get_actor_location();pos=(v.x,v.y,v.z)
   if n not in origins:origins[n]=pos;distances[n]=0;samples[n]={'moving_samples':0,'grounded_samples':0,'min_z':v.z,'max_z':v.z}
   distances[n]=max(distances[n],math.dist(pos[:2],origins[n][:2]))
   s=samples[n];s['moving_samples']+=b.get_velocity().length()>10;s['grounded_samples']+=b.character_movement.is_moving_on_ground();s['min_z']=min(s['min_z'],v.z);s['max_z']=max(s['max_z'],v.z)
   s['mesh']=b.mesh.get_skinned_asset().get_path_name();s['last_position']=pos
   if n not in centers:centers[n]=min(placements,key=lambda item:math.dist(item['position'][:2],pos[:2]))
   center=centers[n];extent=b.get_editor_property('wander_extent')
   if abs(v.x-center['position'][0])>extent.x+5 or abs(v.y-center['position'][1])>extent.y+5:errors.append(n+' left wandering area')
 if t<2:
  p.set_actor_location(u.Vector(-8920,-3000,6470),False,False)
  u.GameplayStatics.get_player_controller(w,0).set_control_rotation(u.Rotator(pitch=-8,yaw=112,roll=0))
 if t>15 and 'outside' not in shots:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation/WanderingBotsOutside.png').as_posix()+'"');shots.add('outside')
 if 19<t<20:
  p.set_actor_location(u.Vector(-10800,-400,6500),False,False)
  u.GameplayStatics.get_player_controller(w,0).set_control_rotation(u.Rotator(pitch=-15,yaw=65,roll=0))
 if t>28 and 'inside' not in shots:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation/WanderingBotInside.png').as_posix()+'"');shots.add('inside')
 if t>40:
  result={'count':len(bots),'passed':len(bots)==11 and len(distances)==11 and all(d>70 for d in distances.values()) and not errors and all(s['moving_samples']>0 and s['grounded_samples']>0 and s['max_z']-s['min_z']<=25 for s in samples.values()),'max_displacement_cm':distances,'samples':samples,'errors':sorted(set(errors))}
  (ROOT/'Documentation/WanderingBotsRuntime.json').write_text(json.dumps(result,indent=2))
  u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,None,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)


