import unreal as u,json,datetime
from pathlib import Path
r=Path(u.Paths.project_dir()).resolve()
u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
a=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
rows=[]
for x in a:
 d=dict(name=x.get_name(),label=x.get_actor_label(),folder=str(x.get_folder_path()),cls=x.get_class().get_name(),transform=str(x.get_actor_transform()),tags=[str(t) for t in x.tags])
 if d['cls']=='Landscape':d['material']=x.get_editor_property('landscape_material').get_path_name()
 rows.append(d)
(r/'Documentation/RuralRemovalBaseline.json').write_text(json.dumps(rows,indent=2))
