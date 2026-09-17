import unreal as u,time,json
from pathlib import Path
root=Path(u.Paths.project_dir());info=json.loads((root/'Documentation/OrnateLift.json').read_text());path=info['map'];start=None;phase=0;report={}
def tick(dt):
 global start,phase
 w=u.find_object(None,path+'.'+path.rsplit('/',1)[-1])
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic();x,y,z=info['upper_cm']
 def advance(n):
  global phase,start
  phase=n;start=now
 if start is None:
  start=now;pc.set_ignore_look_input(True);p.set_actor_location(u.Vector(x+650,y-130,z+90),False,False);pc.set_control_rotation(u.Rotator(pitch=7,yaw=169,roll=0))
 t=now-start
 if phase==0 and t>4:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(root/'Documentation/OrnateLift.png').as_posix()+'"');advance(1)
 elif phase==1 and t>1 and '-LiftPhotoOnly' in u.SystemLibrary.get_command_line():
  u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 elif phase==1 and t>1:
  p.set_actor_location(u.Vector(x+330,y,z+92),False,False);pc.set_control_rotation(u.Rotator(pitch=0,yaw=180,roll=0));advance(2)
 elif phase==2:
  if p.get_actor_location().x>x+10:p.add_movement_input(u.Vector(-1,0,0),.5,False)
  else:report['walk_into_cabin']=abs(p.get_actor_location().z-(z+90))<20;advance(3)
  if t>6:report['walk_into_cabin']=False;advance(3)
 elif phase==3 and t>1:
  lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));report['down_accepted']=max(lifts,key=lambda a:a.get_actor_location().z).travel();advance(4)
 elif phase==4 and t>2:
  report['lower_arrival']=abs(p.get_actor_location().z-4090)<20;pc.set_control_rotation(u.Rotator(pitch=0,yaw=0,roll=0));advance(5)
 elif phase==5:
  if t<1.7:p.add_movement_input(u.Vector(1,0,0),.5,False)
  elif t>2:report['walk_out_lower']=p.get_actor_location().x>-14750;advance(6)
 elif phase==6:
  if p.get_actor_location().x>-14995:p.add_movement_input(u.Vector(-1,0,0),.5,False)
  else:advance(7)
  if t>5:advance(7)
 elif phase==7 and t>1:
  lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'));report['up_accepted']=min(lifts,key=lambda a:a.get_actor_location().z).travel();advance(8)
 elif phase==8 and t>2:
  report['upper_arrival']=abs(p.get_actor_location().x-x)<30 and abs(p.get_actor_location().z-(z+90))<20;report['passed']=all(report.values());(root/'Documentation/OrnateLiftTest.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)

