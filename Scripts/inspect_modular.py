import unreal as u,time,json
from pathlib import Path
root=Path(u.Paths.project_dir());phase=0;started=None;results={};origin=None
views=[('ModularExterior',-14800,-2900,6500,35,12),('ModularConnection',-11300,0,6400,0,14),('ModularInterior',-10600,1000,6340,-90,9)]
def tick(dt):
 global phase,started,origin
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_Modular.L_Exterior_Modular')
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 def move(x,y,z,yaw,pitch=0):
  p.character_movement.stop_movement_immediately();p.set_actor_location(u.Vector(x,y,z),False,False);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0))
 def advance(n):
  global phase,started
  phase=n;started=now
 if started is None:started=now;pc.set_ignore_look_input(True);move(-10600,-800,6340,90)
 t=now-started
 if phase==0 and t>3:origin=p.get_actor_location();advance(1)
 elif phase==1:
  if t<5:p.add_movement_input(u.Vector(0,1,0),1,False)
  elif t>6:
   pos=p.get_actor_location();results['two_connections_walk_cm']=pos.y-origin.y;results['floor_z_cm']=pos.z;results['connections_passed']=pos.y>850 and abs(pos.z-6333)<20;advance(2)
 elif 2<=phase<=7:
  i=(phase-2)//2
  if phase%2==0:
   _,x,y,z,yaw,pitch=views[i];move(x,y,z,yaw,pitch);advance(phase+1)
  elif t>4:
   u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(root/'Documentation'/(views[i][0]+'.png')).as_posix()+'"');advance(phase+1 if phase<7 else 8)
 elif phase==8 and t>1:
  lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));upper=max(lifts,key=lambda a:a.get_actor_location().z);pos=upper.get_actor_location();move(pos.x,pos.y,pos.z,180);advance(9)
 elif phase==9 and t>2:
  lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));upper=max(lifts,key=lambda a:a.get_actor_location().z);results['lift_down']=upper.travel();advance(10)
 elif phase==10 and t>2:
  results['bunker_arrival']=abs(p.get_actor_location().z-4090)<20
  lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));lower=min(lifts,key=lambda a:a.get_actor_location().z);results['lift_up']=lower.travel();advance(11)
 elif phase==11 and t>2:
  results['dome_arrival']=abs(p.get_actor_location().y-json.loads((root/'Documentation/ModularPlacement.json').read_text())['upper_lift_cm'][1])<30 and abs(p.get_actor_location().z-6333)<20;results['passed']=all(results[k] for k in ['connections_passed','lift_down','bunker_arrival','lift_up','dome_arrival'])
  (root/'Documentation/ModularWalkTest.json').write_text(json.dumps(results,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)

