import unreal as u,json,shutil,datetime,math
from pathlib import Path
R=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();assert w.get_path_name()==MAP+'.L_Exterior_RobotVR'
sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=sub.get_all_level_actors();bots=[a for a in actors if a.get_class().get_name()=='C17Robot' and 1<=a.get_editor_property('robot_id')<=10];assert len(bots)==10
land=next(a for a in actors if a.get_class().get_name()=='Landscape');ignore=[a for a in actors if a!=land]
def trans(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():trans(a) for a in actors};plans=[]
for a in bots:
 p=a.get_actor_location();heights=[]
 for dx,dy in [(0,0)]+[(34*math.cos(i*math.pi/4),34*math.sin(i*math.pi/4)) for i in range(8)]:
  hit=u.SystemLibrary.line_trace_single(w,u.Vector(p.x+dx,p.y+dy,100000),u.Vector(p.x+dx,p.y+dy,-100000),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE)
  assert hit and hit.to_tuple()[0],a.get_actor_label();heights.append(hit.to_tuple()[5].z)
 target=max(heights)+100
 plans.append((a,u.Vector(p.x,p.y,target),dict(robot=a.get_editor_property('robot_id'),before=[p.x,p.y,p.z],after=[p.x,p.y,target],terrain_z=heights[0],minimum_foot_clearance_cm=4)))
backup=R/'Saved/Backups/RobotGround'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True)
source=R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap';shutil.copy2(source,backup/'previous-disk.umap')
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
shutil.copy2(source,backup/'live-user-baseline.umap')
with u.ScopedEditorTransaction('Place outdoor robots above current Landscape'):
 for a,p,row in plans:a.modify();a.set_actor_location(p,False,True)
unexpected=[a.get_name() for a in actors if a not in bots and trans(a)!=before[a.get_name()]];assert not unexpected,unexpected
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
report=dict(timestamp=datetime.datetime.now().isoformat(),engine=u.SystemLibrary.get_engine_version(),backup=str(backup),robots=[row for a,p,row in plans],unrelated_changes=unexpected,actor_count=len(actors),saved=True,dirty_maps=[p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
(R/'Documentation/RobotGroundRepair.json').write_text(json.dumps(report,indent=2))
print('ROBOT_GROUND_REPAIR_SAVED')
