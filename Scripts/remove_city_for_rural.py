import unreal as u,json,datetime,shutil
from pathlib import Path
R=Path(u.Paths.project_dir()).resolve(); MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
w=u.EditorLoadingAndSavingUtils.load_map(MAP); sub=u.get_editor_subsystem(u.EditorActorSubsystem)
a=list(sub.get_all_level_actors())
def tr(x):
 p=x.get_actor_location();r=x.get_actor_rotation();s=x.get_actor_scale3d();return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
targets=[x for x in a if str(x.get_folder_path()).startswith(('03 Village','City draft/Town hall positional'))]
keep={x.get_name():tr(x) for x in a if x not in targets}
land=next(x for x in a if x.get_class().get_name()=='Landscape')
assert land.get_editor_property('landscape_material').get_path_name()=='/Game/Conservatory/Environment/CityRoadDraft/M_CityRoadDraft_v1.M_CityRoadDraft_v1'
backup=R/'Saved/Backups/RuralRemoval'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S');backup.mkdir(parents=True)
shutil.copy2(R/'Content/Conservatory/Maps/L_Exterior_RobotVR.umap',backup/'L_Exterior_RobotVR.umap')
removed=[dict(name=x.get_name(),label=x.get_actor_label(),folder=str(x.get_folder_path())) for x in targets]
for x in reversed(targets):assert sub.destroy_actor(x)
land.set_editor_property('landscape_material',u.load_asset('/Game/Conservatory/Environment/Materials/M_Ground'))
assert keep=={x.get_name():tr(x) for x in sub.get_all_level_actors()}
assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
w=u.EditorLoadingAndSavingUtils.load_map(MAP)
a=list(sub.get_all_level_actors());assert keep=={x.get_name():tr(x) for x in a}
land=next(x for x in a if x.get_class().get_name()=='Landscape');assert land.get_editor_property('landscape_material').get_name()=='M_Ground'
(R/'Documentation/RuralRemovalResult.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now().isoformat(),engine=u.SystemLibrary.get_engine_version(),backup=str(backup),removed=removed,remaining_actors=len(a),remaining_transforms_preserved=True,saved_and_reopened=True,landscape_material=land.get_editor_property('landscape_material').get_path_name()),indent=2))
