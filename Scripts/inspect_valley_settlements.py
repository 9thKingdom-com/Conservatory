"""Standalone collision traversal of every building, plus in-game review views."""
import unreal as u,time,json,math,traceback,sys
from pathlib import Path
ROOT=Path(u.Paths.project_dir());buildings=json.loads((ROOT/'SourceAssets/ValleySettlements/layout.json').read_text())['buildings']
sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
started=None;phase='wait';phase_start=0;index=0;origin=None;checks=[];views=[];report={};nav_result=None
def tick(dt):
 global started,phase,phase_start,index,origin,views,nav_result
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 def quit():
  report.update(buildings=checks,passed=len(checks)==28 and all(c['passed'] for c in checks),tested_at_unix=time.time())
  (ROOT/'Documentation/ValleySettlementsRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 def advance(s):
  global phase,phase_start
  phase=s;phase_start=now
  (ROOT/'Saved/ValleyTestProgress.json').write_text(json.dumps({'phase':phase,'building':index,'checks':checks}))
 def move(pos,yaw,pitch=0):
  p.character_movement.stop_movement_immediately();p.set_actor_location(u.Vector(*[v*100 for v in pos]),False,True);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0))
 try:
  if started is None:
   started=now;phase_start=now;pc.set_ignore_look_input(True);p.character_movement.max_walk_speed=400
  if now-started>290:report['error']='Timeout';quit();return
  t=now-phase_start
  if phase=='wait' and t>8:advance('place')
  elif phase=='place':
   b=buildings[index];sgn=1 if b['yaw']==0 else -1;x=b['x'];y=b['y']+sgn*(b['d']/2+13.8)
   p.set_actor_enable_collision(True);p.character_movement.set_movement_mode(u.MovementMode.MOVE_WALKING);move([x,y,height(x,y)+1.12],-90 if b['yaw']==0 else 90);advance('settle')
  elif phase=='settle' and t>.65:
   origin=p.get_actor_location();b=buildings[index]
   try:
    path=u.NavigationSystemV1.find_path_to_location_synchronously(w,origin,u.Vector(*[v*100 for v in b['rear']]))
    nav_result=bool(path and path.is_valid() and not path.is_partial())
   except Exception as e:nav_result=str(e)
   advance('walk')
  elif phase=='walk':
   b=buildings[index];sgn=1 if b['yaw']==0 else -1;pos=p.get_actor_location();target=b['rear'][1]*100;distance=(pos.y-target)*sgn
   if t<7.5 and distance>25:p.add_movement_input(u.Vector(0,-sgn,0),1,False)
   else:
    p.character_movement.stop_movement_immediately()
    checks.append({'id':b['id'],'kind':b['kind'],'travel_cm':(origin.y-pos.y)*sgn,'distance_to_rear_cm':abs(pos.y-target),'capsule_z':pos.z,'floor_z':b['z']*100,'navigation_path':nav_result,'passed':abs(pos.y-target)<80 and 50<pos.z-b['z']*100<150})
    index+=1
    if index<len(buildings):advance('place')
    else:
     report['collision_enabled']=True
     views=[('ValleyTownOverview',(105,-110,64),48,-22),('ValleyTownStreet',(223,9,8.9),-53,0),('ValleyCottageInterior',(155,-52,buildings[0]['z']+1.0),-125,-5),('ValleyNorthHamlet',(325,122,31),60,-23),('ValleyFarm',(102,-191,29),-73,-23)]
     index=0;p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);advance('view')
  elif phase=='view':
   name,pos,yaw,pitch=views[index];move(pos,yaw,pitch);advance('photo')
  elif phase=='photo' and t>4:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1600x900 filename="'+(ROOT/'Documentation'/(views[index][0]+'.png')).as_posix()+'"');advance('next_view')
  elif phase=='next_view' and t>1.5:
   index+=1
   if index<len(views):advance('view')
   else:quit()
 except Exception:report['error']=traceback.format_exc();quit()
handle=u.register_slate_post_tick_callback(tick)
