import unreal as u,time,json,math
from pathlib import Path
ROOT=Path(u.Paths.project_dir());data=json.loads((ROOT/'Documentation/C17/Placement.json').read_text());stage=-1;started=None;bots=[];origins=[];report={'clips':{}};clips=['Idle','Walk','CarryWalk','Lift','ShelfPick','Chop','BreakStone']
def tick(dt):
 global stage,started,bots,origins
 w=u.find_object(None,data['map']+'.'+data['map'].rsplit('/',1)[-1])
 if not w:return
 p=u.GameplayStatics.get_player_character(w,0)
 if not p:return
 pc=u.GameplayStatics.get_player_controller(w,0);now=time.monotonic()
 def photo(name):u.SystemLibrary.execute_console_command(w,'HighResShot 1280x720 filename="'+(ROOT/'Documentation/C17'/(name+'.png')).as_posix()+'"')
 if started is None:
  p.set_actor_enable_collision(False);p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING)
  bots=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot'));origins=[b.get_actor_location() for b in bots];started=now;return
 t=now-started
 if stage==-1 and t>10:
  distances=[(b.get_actor_location()-o).length() for b,o in zip(bots,origins)];report['patrol_distance_cm']=distances;report['robot_positions_cm']=[[b.get_actor_location().x,b.get_actor_location().y,b.get_actor_location().z] for b in bots];report['patrol_passed']=len(bots)==2 and all(d>100 for d in distances)
  for b in bots:b.set_editor_property('patrol_enabled',False);b.character_movement.stop_movement_immediately()
  b=bots[0];c=b.get_component_by_class(u.SkeletalMeshComponent);v=c.get_socket_location('camera_mount')-c.get_socket_location('head');fw=b.get_actor_forward_vector();report['sensor_facing_dot_actor_forward']=(v.x*fw.x+v.y*fw.y+v.z*fw.z)/v.length();b.set_actor_rotation(u.Rotator(pitch=0,yaw=0,roll=0),False);pos=b.get_actor_location();p.character_movement.stop_movement_immediately();p.set_actor_location(pos+u.Vector(320,-235,15),False,False);pc.set_control_rotation(u.Rotator(pitch=-4,yaw=144,roll=0));b.play_work_animation('Idle');stage=0;started=now
 elif 0<=stage<14:
  b=bots[0];clip=clips[stage//2];c=b.get_component_by_class(u.SkeletalMeshComponent)
  if stage%2==0:
   report['clips'][clip]={'accepted':b.play_work_animation(clip)};stage+=1;started=now
  elif t>(.20 if clip in ['Walk','CarryWalk'] else 1.0):
   pos=b.get_actor_location();head=c.get_socket_location('head');hand=c.get_socket_location('hand_r');ankle=c.get_socket_location('foot_r');d=(head-pos).length()
   report['clips'][clip].update({'head_distance_from_actor_cm':d,'head_z_above_capsule_base_cm':head.z-(pos.z-76),'hand_r_cm':[hand.x-pos.x,hand.y-pos.y,hand.z-pos.z],'scale_and_pose_valid':15<d<180,'bone_count':c.get_num_bones()})
   report['clips'][clip]['hand_pose_changes']=clip=='Idle' or sum((a-b)**2 for a,b in zip(report['clips'][clip]['hand_r_cm'],report['clips']['Idle']['hand_r_cm']))>4
   photo('UE_'+clip);stage+=1;started=now
 elif stage==14 and t>2:
  p.set_actor_location(u.Vector(-13500,960,4090),False,False);pc.set_control_rotation(u.Rotator(pitch=-5,yaw=39,roll=0));stage=15;started=now
 elif stage==15 and t>3:
  photo('UE_Workstation');report['passed']=report['patrol_passed'] and all(c['accepted'] and c['scale_and_pose_valid'] and c['hand_pose_changes'] for c in report['clips'].values());(ROOT/'Documentation/C17/RuntimeValidation.json').write_text(json.dumps(report,indent=2));stage=16;started=now
 elif stage==16 and t>2:
  u.unregister_slate_post_tick_callback(handle);u.SystemLibrary.quit_game(w,pc,u.QuitPreference.QUIT,False)
handle=u.register_slate_post_tick_callback(tick)





