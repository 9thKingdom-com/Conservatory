import unreal as u,json
from pathlib import Path
root=Path(u.Paths.project_dir());world=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_Modular')
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
 if 'ConservatoryModule' in [str(t) for t in a.tags]:
  y=a.get_actor_location().y;a.set_actor_label('01 South dome - master frame' if y<0 else '03 North dome - master frame' if y>0 else '02 Short passage - master bay')
for part in ['Dome','Passage']:
 m=u.load_asset('/Game/Conservatory/Architecture/ModularMaster/SM_Master_'+part)
 for name in ['Attach_PositiveX','Attach_NegativeX']:
  keep=m.find_socket(name);assert keep
  while m.find_socket(name):m.remove_socket(m.find_socket(name))
  m.add_socket(keep)
 u.EditorAssetLibrary.save_loaded_asset(m)
assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Conservatory/Maps/L_Exterior_Modular')
b=json.loads((root/'Documentation/BunkerLayout.json').read_text());b['lift_top_cm']=json.loads((root/'Documentation/ModularPlacement.json').read_text())['upper_lift_cm'];(root/'Documentation/BunkerLayout.json').write_text(json.dumps(b,indent=2))

