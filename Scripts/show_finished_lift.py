import unreal as u,math
sub=u.get_editor_subsystem(u.EditorActorSubsystem)
lift=next(a for a in sub.get_all_level_actors() if a.get_actor_label()=='LIFT-MASTER | finished conservatory lift')
p=lift.get_actor_location();yaw=lift.get_actor_rotation().yaw;d=u.Vector(math.cos(math.radians(yaw)),math.sin(math.radians(yaw)),0)
u.EditorLevelLibrary.set_level_viewport_camera_info(p+d*650+u.Vector(0,0,270),u.Rotator(pitch=-4,yaw=yaw+180,roll=0))
sub.set_selected_level_actors([])
print('FINISHED_LIFT_READY_FOR_REVIEW')
