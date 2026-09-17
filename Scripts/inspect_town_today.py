"""Opt-in saved-map runtime inspection and photos; no gameplay changes saved."""
import unreal as u,time,re,json,sys,math
from pathlib import Path
ROOT=Path(u.Paths.project_dir());MAP=re.search(r'GameDefaultMap=(.+)',(ROOT/'Config/DefaultEngine.ini').read_text()).group(1).strip()
views=[('TownTodayOverview',8600,6700,5100,-32,-21),('TownTodayFuel',9700,1700,1510,-43,-3),('TownTodayCrash',19000,100,1170,-124,-2),('TownTodayStreet',14800,830,1110,0,0)]
sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
stage=0;changed=0;shot=False;walk_origin=None
def tick(dt):
 global stage,changed,shot,walk_origin
 w=u.find_object(None,MAP+'.'+MAP.rsplit('/',1)[-1])
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 if stage==len(views):
  if not changed:
   p.set_actor_enable_collision(True);p.character_movement.set_movement_mode(u.MovementMode.MOVE_WALKING);p.set_actor_location(u.Vector(14900,830,(height(149,8.3)+2)*100),False,False);changed=now
  t=now-changed
  if t>2 and walk_origin is None:walk_origin=p.get_actor_location()
  if 2<t<5:p.add_movement_input(u.Vector(1,0,0),1,False)
  if t>5.5:
   pos=p.get_actor_location();distance=math.hypot(pos.x-walk_origin.x,pos.y-walk_origin.y);grounded=p.character_movement.is_moving_on_ground()
   report={'walk_distance_cm':distance,'grounded':grounded,'passed':distance>400 and grounded,'map':MAP}
   (ROOT/'Documentation/TownTodayWalkTest.json').write_text(json.dumps(report,indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
  return
 if not changed:
  name,x,y,z,yaw,pitch=views[stage];p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.character_movement.stop_movement_immediately();pc.set_ignore_look_input(True)
  p.set_actor_location(u.Vector(x,y,z),False,False);pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=yaw,roll=0));changed=now
 if now-changed>10 and not shot:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1600x900 filename="'+(ROOT/'Documentation'/(views[stage][0]+'.png')).as_posix()+'"');shot=True
 if now-changed>13:
  stage+=1;changed=0;shot=False
handle=u.register_slate_post_tick_callback(tick)
