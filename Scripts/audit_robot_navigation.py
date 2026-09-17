import unreal as u,json
from pathlib import Path
w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();a=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors();rows=[]
for b in a:
 if b.get_class().get_name()!='C17Robot':continue
 p=b.get_actor_location();q=u.NavigationSystemV1.project_point_to_navigation(w,p,None,None,query_extent=u.Vector(300,300,300));r=dict(id=b.robot_id,position=str(p),projected=str(q));rows.append(r)
Path(u.Paths.project_dir()+'Documentation/RobotNavigationAudit.json').write_text(json.dumps(rows,indent=2))
