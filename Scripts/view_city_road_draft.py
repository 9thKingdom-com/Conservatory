import unreal as u,time,json
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();start=time.monotonic();phase=0;mark=start
def tick(dt):
 global phase,mark
 w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR');now=time.monotonic()
 if not w:return
 pc=u.GameplayStatics.get_player_controller(w,0);p=u.GameplayStatics.get_player_character(w,0)
 if not pc or not p:return
 if now-start>40:u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False);return
 if phase==0 and now-start>7:
  p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING);p.character_movement.stop_movement_immediately();p.set_actor_location(u.Vector(28500,-4000,85000),False,True);pc.set_control_rotation(u.Rotator(pitch=-89.9,yaw=90,roll=0));phase=1;mark=now
 elif phase==1 and now-mark>5:
  u.SystemLibrary.execute_console_command(w,'HighResShot 1400x1400 filename="'+(R/'Documentation/CityRoadDraftUnreal.png').as_posix()+'"');phase=2;mark=now
 elif phase==2 and now-mark>2:
  land=next(a for a in u.GameplayStatics.get_all_actors_of_class(w,u.Landscape));mat=land.get_editor_property('landscape_material');(R/'Documentation/CityRoadDraftRuntime.json').write_text(json.dumps(dict(saved_material=mat.get_path_name(),reopened=True,render_captured=True),indent=2));u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)

