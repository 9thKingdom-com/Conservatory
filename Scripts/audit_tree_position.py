import unreal as u,json,datetime
from pathlib import Path
R=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
w=u.EditorLoadingAndSavingUtils.load_map(MAP);rows=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d()
 row=dict(name=a.get_name(),label=a.get_actor_label(),cls=a.get_class().get_name(),pos=[p.x,p.y,p.z],rot=[r.pitch,r.yaw,r.roll],scale=[s.x,s.y,s.z])
 if isinstance(a,u.StaticMeshActor):
  m=a.static_mesh_component.static_mesh;row['mesh']=m.get_path_name() if m else None
  c,e=a.get_actor_bounds(False);row['bounds']=[[c.x,c.y,c.z],[e.x,e.y,e.z]]
 rows.append(row)
(R/'Documentation/TreePositionBaseline.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now().isoformat(),actors=rows),indent=2))
print('TREE_BASELINE_SAVED')
