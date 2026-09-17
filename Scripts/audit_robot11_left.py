import unreal as u,json
from pathlib import Path
R=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
w=u.EditorLoadingAndSavingUtils.load_map(MAP);sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=sub.get_all_level_actors()
rows=[]
for a in actors:
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d()
 row={'name':a.get_name(),'label':a.get_actor_label(),'class':a.get_class().get_name(),'position':[p.x,p.y,p.z],'rotation':[r.pitch,r.yaw,r.roll],'scale':[s.x,s.y,s.z]}
 if row['class']=='C17Robot':row['robot_id']=a.get_editor_property('robot_id')
 if row['class']=='ServiceLift':
  d=a.get_editor_property('destination');row['destination']=[d.x,d.y,d.z]
 if isinstance(a,u.StaticMeshActor):
  m=a.static_mesh_component.static_mesh;row['mesh']=m.get_path_name() if m else None
 if 'lift' in row['label'].lower() or 'dock' in row['label'].lower() or row.get('robot_id')==11:
  center,extent=a.get_actor_bounds(False);row['bounds']={'center':[center.x,center.y,center.z],'extent':[extent.x,extent.y,extent.z]}
 rows.append(row)
(R/'Documentation/Robot11LeftBaseline.json').write_text(json.dumps({'actors':rows,'map':MAP,'count':len(rows)},indent=2))
print('ROBOT11_AUDIT_COMPLETE')
