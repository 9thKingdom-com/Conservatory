import unreal as u,json
from pathlib import Path
R=Path(u.Paths.project_dir());w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR');rows=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 if a.get_class().get_name() not in ['VRSuitStation','RobotVRHub']:continue
 p=a.get_actor_location();d=dict(name=a.get_name(),cls=a.get_class().get_name(),pos=[p.x,p.y,p.z],yaw=a.get_actor_rotation().yaw)
 if d['cls']=='VRSuitStation':
  d['id']=a.robot_id;d['hub']=a.hub.get_name() if a.hub else None;p=a.get_editor_property('suit').get_world_location();d['suit_position']=[p.x,p.y,p.z]
 rows.append(d)
(R/'Documentation/ControlRoomBaseline.json').write_text(json.dumps(rows,indent=2))

