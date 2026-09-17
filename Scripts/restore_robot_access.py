import unreal as u,json,shutil,datetime,math
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve();MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR';sub=u.get_editor_subsystem(u.EditorActorSubsystem);w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world();assert w.get_path_name()==MAP+'.L_Exterior_RobotVR'
actors=sub.get_all_level_actors();bots=[a for a in actors if a.get_class().get_name()=='C17Robot'];suits=[a for a in actors if a.get_class().get_name()=='VRSuitStation'];assert len(bots)==11 and len(suits)==10
def xyz(p):return [p.x,p.y,p.z]
def tr(a):return xyz(a.get_actor_location())+[a.get_actor_rotation().pitch,a.get_actor_rotation().yaw,a.get_actor_rotation().roll]+xyz(a.get_actor_scale3d())
before={a.get_name():tr(a) for a in actors};land=next(a for a in actors if a.get_class().get_name()=='Landscape');ignore=[a for a in actors if a!=land];plans=[]
for a in bots:
 if a.robot_id==11:continue
 p=a.get_actor_location();hs=[]
 for i in range(9):
  dx=34*math.cos(i*math.pi/4) if i<8 else 0;dy=34*math.sin(i*math.pi/4) if i<8 else 0
  h=u.SystemLibrary.line_trace_single(w,u.Vector(p.x+dx,p.y+dy,100000),u.Vector(p.x+dx,p.y+dy,-100000),u.TraceTypeQuery.ECC_VISIBILITY,True,ignore,u.DrawDebugTrace.NONE);assert h.to_tuple()[0];hs.append(h.to_tuple()[5].z)
 plans.append((a,u.Vector(p.x,p.y,max(hs)+100)))
backup=R/'Saved/Backups/RobotAccess'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True);disk=R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap';shutil.copy2(disk,backup/'previous-disk.umap');assert u.EditorLoadingAndSavingUtils.save_map(w,MAP);shutil.copy2(disk,backup/'live-user-baseline.umap')
with u.ScopedEditorTransaction('Robot ground access and suit 11'):
 for a,p in plans:a.set_actor_location(p,False,True)
 source=next(a for a in suits if a.robot_id==1)
 s=sub.duplicate_actor(source,w,u.Vector(0,0,0));s.set_actor_location(u.Vector(-14150,1100,4003),False,True);s.set_actor_rotation(u.Rotator(pitch=0,yaw=0,roll=0),True);s.robot_id=11;s.set_actor_label('VR suit 11 - robot 11');s.set_folder_path('11 Kitchen VR/Numbered suits')
 label=next(a for a in actors if a.get_actor_label()=='VR suit 01 label');t=sub.duplicate_actor(label,w,u.Vector(0,0,0));t.set_actor_location(u.Vector(-14172,1100,4200),False,True);t.set_actor_rotation(u.Rotator(pitch=0,yaw=0,roll=0),True);t.set_actor_label('VR suit 11 label');t.get_component_by_class(u.TextRenderComponent).set_text('SUIT 11\nROBOT 11\n[F] WEAR')
assert not [a.get_name() for a in actors if a not in bots and tr(a)!=before[a.get_name()]]
assert u.ExteriorTools.build_terrain_navigation()
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
(R/'Documentation/RobotAccessRepair.json').write_text(json.dumps(dict(backup=str(backup),robots=[dict(id=a.robot_id,before=before[a.get_name()][:3],after=xyz(p)) for a,p in plans],station=xyz(s.get_actor_location()),navigation_rebuilt=True,terrain_unchanged=True,unrelated_transforms_preserved=True),indent=2))
u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(-13900,1550,4180),u.Rotator(pitch=-8,yaw=-120,roll=0));sub.set_selected_level_actors([s]);print('ROBOT_ACCESS_SAVED')
