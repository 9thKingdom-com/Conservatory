import unreal as u,json
from pathlib import Path
R=Path(u.Paths.project_dir());w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();actors=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
out={'map':w.get_path_name(),'dirty':[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()],'bots':[]}
land=next(a for a in actors if a.get_class().get_name()=='Landscape')
out['height_doc']=str(getattr(land,'get_height_at_location',None).__doc__)
out['trace_doc']=str(u.SystemLibrary.line_trace_single.__doc__);out['hit_doc']=str(u.HitResult.__doc__)
for a in actors:
 if a.get_class().get_name()=='C17Robot':
  p=a.get_actor_location();hit=u.SystemLibrary.line_trace_single(w,u.Vector(p.x,p.y,100000),u.Vector(p.x,p.y,-100000),u.TraceTypeQuery.TRACE_TYPE_QUERY1,True,[x for x in actors if x!=land],u.DrawDebugTrace.NONE)
  out['bots'].append(dict(name=a.get_name(),label=a.get_actor_label(),pos=[p.x,p.y,p.z],id=a.get_editor_property('robot_id'),hit=str(hit),tuple=str(hit.to_tuple()) if hit else None))
(R/'Documentation/RobotGroundAudit.json').write_text(json.dumps(out,indent=2))
print('ROBOT_GROUND_AUDIT_DONE')
