import unreal as u,json,math
from pathlib import Path
R=Path(u.Paths.project_dir());w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR');aa=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors();l=next(a for a in aa if a.get_name()=='StaticMeshActor_1858');p=l.get_actor_location();ang=math.radians(l.get_actor_rotation().yaw);f=u.Vector(math.cos(ang),math.sin(ang),0);left=u.Vector(-math.sin(ang),math.cos(ang),0);ignore=[a for a in aa if a.get_actor_label().startswith('Robot 11 dock') or a.get_class().get_name()=='C17Robot'];rows=[]
for x,y in [(x,y) for x in [40,140,240,340] for y in [240,280,320]]:
 q=p+f*x+left*y;h=u.SystemLibrary.line_trace_single(w,q+u.Vector(0,0,60),q-u.Vector(0,0,150),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE);rows.append([x,y,str(h.to_tuple())])
(R/'Documentation/Robot11FloorChecks.json').write_text(json.dumps(rows,indent=2))
