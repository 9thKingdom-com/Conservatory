import unreal as u, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
rows=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d()
 row=dict(name=a.get_name(),label=a.get_actor_label(),cls=a.get_class().get_name(),folder=str(a.get_folder_path()),pos=[p.x,p.y,p.z],rot=[r.pitch,r.yaw,r.roll],scale=[s.x,s.y,s.z])
 if row['cls']=='ServiceLift':
  d=a.get_editor_property('destination');row.update(destination=[d.x,d.y,d.z],yaw=a.get_editor_property('destination_yaw'))
 if isinstance(a,u.StaticMeshActor):
  m=a.static_mesh_component.static_mesh;row['mesh']=m.get_path_name() if m else None
 rows.append(row)
(root/'Documentation/LiftManualBaseline.json').write_text(json.dumps(rows,indent=2))
print('LIFT_AUDIT_DONE')
