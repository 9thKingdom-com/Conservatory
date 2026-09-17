import unreal as u,json
from pathlib import Path
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
out={'rotation_positional':str(u.Rotator(0,180,0)),'rotation_named':str(u.Rotator(pitch=0,yaw=180,roll=0))}
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 if a.get_class().get_name() in ['RobotVRHub','VRSuitStation'] or a.get_actor_label()=='Security monitor controls':
  out[a.get_actor_label()]={'rotation':str(a.get_actor_rotation()),'location':str(a.get_actor_location())}
Path(u.Paths.project_dir()+'Documentation/VRRoomAudit.json').write_text(json.dumps(out,indent=2))
