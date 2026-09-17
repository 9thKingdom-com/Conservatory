import unreal as u,json
from pathlib import Path
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();sub=u.get_editor_subsystem(u.EditorActorSubsystem);n=next(a for a in sub.get_all_level_actors() if a.get_class().get_name()=='RecastNavMesh')
old=str(n.get_actor_transform());n.set_actor_location(u.Vector(0,0,0),False,True);n.set_actor_rotation(u.Rotator(pitch=0,yaw=0,roll=0),True);n.set_actor_scale3d(u.Vector(1,1,1));assert u.ExteriorTools.build_terrain_navigation();assert u.EditorLoadingAndSavingUtils.save_map(w,'/Game/Conservatory/Maps/L_Exterior_RobotVR')
Path(u.Paths.project_dir()+'Documentation/NavigationTransformRepair.json').write_text(json.dumps(dict(before=old,after=str(n.get_actor_transform()),rebuilt=True),indent=2))
