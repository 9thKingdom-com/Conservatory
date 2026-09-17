import unreal as u,json,math,shutil,datetime
from pathlib import Path
R=Path(u.Paths.project_dir());MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';baseline=json.loads((R/'Documentation/Robot11LeftBaseline.json').read_text());w=u.EditorLoadingAndSavingUtils.load_map(MAP);sub=u.get_editor_subsystem(u.EditorActorSubsystem);actors=sub.get_all_level_actors()
def trans(a):
 p=a.get_actor_location();r=a.get_actor_rotation();s=a.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
before={a.get_name():trans(a) for a in actors}
assert len(actors)==baseline['count']
for row in baseline['actors']:assert all(abs(x-y)<.00001 for x,y in zip(before[row['name']],row['position']+row['rotation']+row['scale']))
bot=next(a for a in actors if a.get_class().get_name()=='C17Robot' and a.get_editor_property('robot_id')==11)
lift=next(a for a in actors if a.get_name()=='StaticMeshActor_1858');p=lift.get_actor_location();yaw=lift.get_actor_rotation().yaw;ang=math.radians(yaw);f=u.Vector(math.cos(ang),math.sin(ang),0);left=u.Vector(-math.sin(ang),math.cos(ang),0)
group=[a for a in actors if a==bot or a.get_actor_label().startswith('Robot 11 dock')];assert len(group)==13
old=bot.get_actor_location();target=p+f*40+left*270;target.z=old.z
# Check the supporting floor before preserving the dock's current height.
hit=u.SystemLibrary.line_trace_single(w,u.Vector(target.x,target.y,p.z+60),u.Vector(target.x,target.y,p.z-120),u.TraceTypeQuery.ECC_VISIBILITY,True,group,u.DrawDebugTrace.NONE)
assert hit and hit.to_tuple()[0],'No floor at requested dock position'
ground=hit.to_tuple()[5].z
oldhit=u.SystemLibrary.line_trace_single(w,u.Vector(old.x,old.y,p.z+60),u.Vector(old.x,old.y,p.z-120),u.TraceTypeQuery.ECC_VISIBILITY,True,group,u.DrawDebugTrace.NONE)
assert oldhit and oldhit.to_tuple()[0]
assert abs(ground-oldhit.to_tuple()[5].z)<2,'Support datum differs; inspect manually'
# Visibility traces hit the underlying Landscape here, not the deck mesh.
# Preserve the existing dock/deck elevation across this level area.
delta=math.radians(yaw-bot.get_actor_rotation().yaw)
backup=R/'Saved/Backups/Robot11Left'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True);shutil.copy2(R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
with u.ScopedEditorTransaction('Move robot 11 and charging dock left of lift'):
 for a in group:
  rel=a.get_actor_location()-old;q=u.Vector(rel.x*math.cos(delta)-rel.y*math.sin(delta),rel.x*math.sin(delta)+rel.y*math.cos(delta),rel.z)+target
  r=a.get_actor_rotation();r.yaw+=math.degrees(delta);a.modify();a.set_actor_location(q,False,True);a.set_actor_rotation(r,True)
unexpected=[a.get_name() for a in actors if a not in group and trans(a)!=before[a.get_name()]];assert not unexpected
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
report={'saved':True,'engine':u.SystemLibrary.get_engine_version(),'timestamp':datetime.datetime.now().isoformat(),'backup':str(backup),'robot_position':trans(bot)[:3],'underlying_landscape_z':ground,'left_convention':'Viewer left when facing entrance; lift local +Y','dock_side_gap_cm':73,'moved':[{'name':a.get_name(),'before':before[a.get_name()],'after':trans(a)} for a in group],'unrelated_transform_changes':unexpected,'actor_count':len(actors)}
(R/'Documentation/Robot11LeftMove.json').write_text(json.dumps(report,indent=2));print('ROBOT11_LEFT_SAVED')
