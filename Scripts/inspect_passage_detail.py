"""Current-map runtime passage photos; optional post-upgrade traversal checks."""
import unreal as u,time,re,json
from pathlib import Path
ROOT=Path(u.Paths.project_dir());MAP=re.search(r'GameDefaultMap=(.+)',(ROOT/'Config/DefaultEngine.ini').read_text()).group(1).strip()
before='-PassageBefore' in u.SystemLibrary.get_command_line();suffix='Before' if before else 'After'
views=[] if '-PassageWalkOnly' in u.SystemLibrary.get_command_line() else [('PassageExterior',-9880,0,6560,180,14),('PassageInterior',-10600,-410,6370,90,17),('PassageSideDetail',-10600,0,6390,0,14)]
stage=0;changed=0;shot=False;walk_origin=None;results={};leg=0
def tick(dt):
 global stage,changed,shot,walk_origin,leg
 w=u.find_object(None,MAP+'.'+MAP.rsplit('/',1)[-1])
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 if stage==len(views):
  if not changed:
   p.set_actor_enable_collision(True);p.character_movement.set_movement_mode(u.MovementMode.MOVE_WALKING);p.character_movement.stop_movement_immediately();p.set_actor_location(u.Vector(-10600,-650 if leg==0 else 650,6370),False,False);changed=now
  t=now-changed
  if t>2 and walk_origin is None:walk_origin=p.get_actor_location()
  if 2<t<6:p.add_movement_input(u.Vector(0,1 if leg==0 else -1,0),1,False)
  if t>6.4:
   pos=p.get_actor_location();distance=(pos.y-walk_origin.y)*(1 if leg==0 else -1);results['north' if leg==0 else 'south']={'distance_cm':distance,'grounded':p.character_movement.is_moving_on_ground(),'passed':distance>1100 and p.character_movement.is_moving_on_ground()}
   results['north' if leg==0 else 'south']['position']=str(pos)
   hit=u.SystemLibrary.capsule_trace_single(w,pos,pos+u.Vector(0,100 if leg==0 else -100,0),34,88,u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[p],u.DrawDebugTrace.NONE,True)
   results['north' if leg==0 else 'south']['sweep']=str(hit.to_tuple()) if hit else None
   leg+=1;changed=0;walk_origin=None
   if leg==2:
    results['passed']=all(v['passed'] for v in results.values());(ROOT/'Documentation/PassageDetailWalkTest.json').write_text(json.dumps(results,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
  return
 if not changed:
  name,x,y,z,yaw,pitch=views[stage];p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.character_movement.stop_movement_immediately();pc.set_ignore_look_input(True);p.set_actor_location(u.Vector(x,y,z),False,False);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0));changed=now
 if now-changed>8 and not shot:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1600x900 filename="'+(ROOT/'Documentation'/(views[stage][0]+suffix+'.png')).as_posix()+'"');shot=True
 if now-changed>11:
  stage+=1;changed=0;shot=False
  if stage==len(views) and before:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)





