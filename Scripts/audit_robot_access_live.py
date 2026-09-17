import unreal as u,json
from pathlib import Path
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
rows=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 c=a.get_class().get_name()
 if c in ['C17Robot','VRSuitStation','RobotVRHub','NavMeshBoundsVolume','RecastNavMesh'] or 'VR suit' in a.get_actor_label():
  p=a.get_actor_location();r=a.get_actor_rotation();row=dict(name=a.get_name(),label=a.get_actor_label(),cls=c,pos=[p.x,p.y,p.z],yaw=r.yaw)
  for k in ['robot_id','patrol_enabled','wander_enabled','terrain_wander','wander_speed','hub']:
   try:
    v=a.get_editor_property(k);row[k]=v.get_name() if isinstance(v,u.Object) else v
   except:pass
  rows.append(row)
Path(u.Paths.project_dir()+'Documentation/RobotAccessBaseline.json').write_text(json.dumps(dict(world=w.get_path_name(),dirty=[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()],actors=rows),indent=2))
print('ROBOT_ACCESS_AUDITED')
