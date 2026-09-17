"""Opt-in runtime collision, lift and stair checks with visual captures."""
import unreal as u, time, math, json
from pathlib import Path
ROOT=Path(u.Paths.project_dir()); start=None; phase=0; phase_start=0; index=0; results={}; origin=None; room_index=0
def capture(w,name):
 u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Saved'/'Screenshots'/(name+'.png')).as_posix()+'"')
def tick(dt):
 global start,phase,phase_start,index,origin,room_index
 try:
  w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_Modular.L_Exterior_Modular')
  if not w: return
  p=u.GameplayStatics.get_player_character(w,0)
  if not p: return
  pc=u.GameplayStatics.get_player_controller(w,0); now=time.monotonic()
  if start is None: start=now; phase_start=now; pc.set_ignore_look_input(True)
  elapsed=now-phase_start
  def next_phase(n):
   global phase,phase_start
   phase=n; phase_start=now
  def teleport(x,y,z,yaw=0,pitch=0):
   p.character_movement.stop_movement_immediately(); p.set_actor_location(u.Vector(x,y,z),False,False); pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0))
  if phase==0 and elapsed>5:
   top=json.loads((ROOT/'Documentation/ModularPlacement.json').read_text())['upper_lift_cm']; teleport(*top,180); next_phase(1)
  elif phase==1 and elapsed>2:
   lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'))
   upper=max(lifts,key=lambda a:a.get_actor_location().z)
   results['lift_down_accepted']=upper.travel(); next_phase(2)
  elif phase==2 and elapsed>2:
   pos=p.get_actor_location(); results['lift_down_arrived']=abs(pos.z-4090)<15 and abs(pos.x+15000)<30
   teleport(-14500,-2400,4092,90); next_phase(3)
  elif phase==3:
   if elapsed<3: p.add_movement_input(u.Vector(0,1,0),1,False)
   elif elapsed>4:
    pos=p.get_actor_location(); results['hall_walk_cm']=pos.y+2400; results['hall_walk_passed']=pos.y>-1450 and abs(pos.z-4090)<15
    capture(w,'BunkerHall'); next_phase(4)
  elif phase==4 and elapsed>2:
   teleport(-14980,-1830,4092,130,-5); next_phase(5)
  elif phase==5 and elapsed>3:
   capture(w,'SeedLaboratory'); next_phase(6)
  elif phase==6 and elapsed>2:
   teleport(-14090,2400,4092,166,-48); next_phase(7)
  elif phase==7 and elapsed>3:
   capture(w,'SpiralStair'); next_phase(71)
  elif phase==71 and elapsed>1:
   teleport(-14282,2500,4100,90); index=1; next_phase(8)
  elif phase==8 or phase==9:
   a=math.radians(index*11.25); target=u.Vector(-14500+218*math.cos(a),2500+218*math.sin(a),0)
   pos=p.get_actor_location(); delta=u.Vector(target.x-pos.x,target.y-pos.y,0); distance=delta.length()
   if distance<17:
    index+=1 if phase==8 else -1
    if index==49 and phase==8:
     results['stair_descent_z_cm']=pos.z; results['stair_descent_passed']=abs(pos.z-3490)<35
     index=47; next_phase(9)
    elif index<0 and phase==9:
     results['stair_ascent_z_cm']=pos.z; results['stair_ascent_passed']=abs(pos.z-4090)<35
     teleport(-14900,-1910,3492,132,-4); next_phase(10)
   else: p.add_movement_input(delta/distance,.48,False)
   if elapsed>40:
    results['stair_timeout_phase']=phase; results['stair_timeout_index']=index; results['stair_timeout_position']=[pos.x,pos.y,pos.z]
    teleport(-14900,-1910,3492,132,-4); next_phase(10)
  elif phase==10 and elapsed>4:
   capture(w,'WaterPumping'); next_phase(101)
  elif phase==101 and elapsed>1:
   teleport(-14100,-1900,3492,50,-5); next_phase(11)
  elif phase==11 and elapsed>4:
   capture(w,'OxygenRoom'); next_phase(111)
  elif phase==111 and elapsed>1:
   teleport(-15000,-2700,4092); next_phase(12)
  elif phase==12 and elapsed>2:
   lifts=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Habitat.ServiceLift'))
   lower=min(lifts,key=lambda a:a.get_actor_location().z); results['lift_up_accepted']=lower.travel(); next_phase(13)
  elif phase==13 and elapsed>2:
   pos=p.get_actor_location(); results['lift_up_arrived']=abs(pos.z-6333)<15 and abs(pos.x-json.loads((ROOT/'Documentation/ModularPlacement.json').read_text())['upper_lift_cm'][0])<30
   results['room_doorways']=[]; next_phase(14)
  elif phase==14:
   z=40 if room_index<6 else 34; local=room_index%6; direction=-1 if local%2==0 else 1; y=-15+(local//2)*15
   teleport(-14500+direction*230,y*100,z*100+90,180 if direction<0 else 0); next_phase(15)
  elif phase==15:
   direction=-1 if room_index%2==0 else 1; z=40 if room_index<6 else 34
   if elapsed<1.1: p.add_movement_input(u.Vector(direction,0,0),1,False)
   elif elapsed>1.6:
    pos=p.get_actor_location(); results['room_doorways'].append({'room_index':room_index,'passed':direction*(pos.x+14500)>500 and abs(pos.z-(z*100+90))<20})
    room_index+=1; next_phase(14 if room_index<12 else 16)
  elif phase==16:
   results['passed']=all(results.get(k,False) for k in ['lift_down_accepted','lift_down_arrived','hall_walk_passed','stair_descent_passed','stair_ascent_passed','lift_up_accepted','lift_up_arrived']) and all(r['passed'] for r in results['room_doorways'])
   (ROOT/'Documentation'/'BunkerWalkTest.json').write_text(json.dumps(results,indent=2)); print('BUNKER_TEST '+json.dumps(results),flush=True)
   u.unregister_slate_post_tick_callback(handle); u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
 except Exception as e:
  (ROOT/'Documentation'/'BunkerWalkTest.json').write_text(json.dumps({'error':repr(e),'partial':results},indent=2)); print('BUNKER_TEST_ERROR '+repr(e),flush=True)
  u.unregister_slate_post_tick_callback(handle)
handle=u.register_slate_post_tick_callback(tick)






