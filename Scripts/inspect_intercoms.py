import unreal as u,time,json,math
from pathlib import Path
root=Path(u.Paths.project_dir());data=json.loads((root/'Documentation/IntercomStations.json').read_text());started=None;index=0;phase=0;results=[]
def tick(dt):
 global started,index,phase
 w=u.find_object(None,data['map']+'.'+data['map'].rsplit('/',1)[-1])
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 stations=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.IntercomStation'))
 if index>=len(data['stations']):
  (root/'Documentation/IntercomStationTest.json').write_text(json.dumps({'count':len(stations),'passed':len(stations)==len(results) and all(r['opened'] and r['far_rejected'] for r in results),'results':results},indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False);return
 spec=data['stations'][index];a=next(s for s in stations if s.get_editor_property('area_name')==spec['area']);x,y,z=spec['position_cm'];yaw=spec['yaw'];r=math.radians(yaw)
 if phase==0:
  p.character_movement.stop_movement_immediately();p.set_actor_location(u.Vector(x+math.cos(r)*130,y+math.sin(r)*130,z-65),False,False);pc.set_control_rotation(u.Rotator(pitch=0,yaw=yaw+180,roll=0));started=now;phase=1
 elif phase==1 and now-started>1.2:
  if index in [0,12]:u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(root/'Documentation'/('IntercomRoom.png' if index==0 else 'IntercomDome.png')).as_posix()+'"')
  started=now;phase=2
 elif phase==2 and now-started>.3:
  opened=a.interact()
  if opened:p.get_component_by_class(u.load_class(None,'/Script/Conservatory.CidcoreIntercom')).toggle()
  p.set_actor_location(u.Vector(x+math.cos(r)*400,y+math.sin(r)*400,z-65),False,False)
  far=not a.interact();results.append({'area':spec['area'],'opened':opened,'far_rejected':far});index+=1;phase=0
handle=u.register_slate_post_tick_callback(tick)
