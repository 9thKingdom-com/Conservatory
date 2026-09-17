"""Opt-in standalone validation with automatic exit; never modifies the saved map."""
import unreal as u,time,json,math,traceback
from pathlib import Path
ROOT=Path(u.Paths.project_dir());phase=0;started=None;phase_start=None;checks=[];origin=None;report={};directions=[(1,0),(0,1),(-1,0),(0,-1)]
def tick(dt):
 global phase,started,phase_start,origin
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 def quit():
  report['tested_origin_cm']=[-11000,0,6230.95];report['tested_at_unix']=time.time();(ROOT/'Documentation/CoreHabitatRuntime.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 def advance(n):
  global phase,phase_start
  phase=n;phase_start=now
  (ROOT/'Saved/CoreHabitatTestProgress.json').write_text(json.dumps({'phase':phase,'elapsed':now-started,'walkways':checks}))
 def move(x,y,z,yaw,pitch=0):
  p.character_movement.stop_movement_immediately();p.set_actor_location(u.Vector(x,y,z),False,False);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0))
 def photo(name):u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation'/(name+'.png')).as_posix()+'"')
 try:
  if started is None:started=now;phase_start=now;pc.set_ignore_look_input(True)
  if now-started>145:report['error']='Timeout';quit();return
  t=now-phase_start
  if phase==0 and t>8:advance(1)
  elif 1<=phase<=8:
   i=(phase-1)//2;dx,dy=directions[i]
   if phase%2:
    p.character_movement.set_movement_mode(u.MovementMode.MOVE_WALKING);move(-11000+dx*1400,dy*1400+(100 if i==2 else 0),6340,math.degrees(math.atan2(dy,dx)));origin=p.get_actor_location();advance(phase+1)
   elif t<10:p.add_movement_input(u.Vector(dx,dy,0),1,False)
   elif t>11:
    pos=p.get_actor_location();travel=(pos.x-origin.x)*dx+(pos.y-origin.y)*dy;checks.append({'direction':i,'travel_cm':travel,'capsule_z':pos.z,'passed':travel>3300 and abs(pos.z-6331)<25});advance(phase+1)
  elif phase==9:
   lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));upper=max(lifts,key=lambda a:a.get_actor_location().z);v=upper.get_actor_location();move(v.x,v.y,v.z,0);advance(10)
  elif phase==10 and t>1:
   lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));report['lift_down']=max(lifts,key=lambda a:a.get_actor_location().z).travel();advance(11)
  elif phase==11 and t>2:
   report['bunker_arrival']=p.get_actor_location().z<4500;lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));report['lift_up']=min(lifts,key=lambda a:a.get_actor_location().z).travel();advance(12)
  elif phase==12 and t>2:
   report['habitat_arrival']=abs(p.get_actor_location().z-6331)<25;p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);move(-20400,-11500,15800,49,-27);advance(13)
  elif phase==13 and t>5:photo('CoreHabitatOverview');advance(14)
  elif phase==14 and t>2:move(-10600,500,6370,0,10);advance(15)
  elif phase==15 and t>4:photo('CoreHabitatInterior');advance(16)
  elif phase==16 and t>2:move(-8200,-950,6900,25,-8);advance(17)
  elif phase==17 and t>4:photo('CoreHabitatWalkway');advance(18)
  elif phase==18 and t>2:
   move(-10900,700,6590,135,-8);advance(19)
  elif phase==19 and t>4:photo('CoreHabitatLift');advance(20)
  elif phase==20 and t>2:
   report['walkways']=checks;report['passed']=all(c['passed'] for c in checks) and all(report.get(k,False) for k in ['lift_down','lift_up','bunker_arrival','habitat_arrival']);quit()
 except Exception:
  report['error']=traceback.format_exc();quit()
handle=u.register_slate_post_tick_callback(tick)
