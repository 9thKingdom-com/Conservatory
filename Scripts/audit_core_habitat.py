import unreal as u,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
world=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
rows=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();c=a.get_component_by_class(u.StaticMeshComponent)
 rows.append(dict(name=a.get_name(),label=a.get_actor_label(),cls=a.get_class().get_name(),folder=str(a.get_folder_path()),tags=[str(t) for t in a.tags],transform=[p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z],mesh=c.static_mesh.get_path_name() if c and c.static_mesh else None))
(ROOT/'Documentation/CoreHabitat-Before.json').write_text(json.dumps(rows,indent=2))
print('CORE_HABITAT_AUDIT_COMPLETE',len(rows),flush=True)
