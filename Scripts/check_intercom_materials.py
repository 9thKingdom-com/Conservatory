import unreal as u,json
from pathlib import Path
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_Modular')
a=next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name()=='IntercomStation')
Path(u.Paths.project_dir(),'Saved/StationMaterials.json').write_text(json.dumps([(c.get_name(),c.get_material(0).get_path_name() if c.get_material(0) else None) for c in a.get_components_by_class(u.StaticMeshComponent)],indent=2))
