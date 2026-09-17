import unreal as u, json, shutil, datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1]
lib=u.EditorAssetLibrary
base='/Game/Conservatory/Architecture/CoreHabitat'
ivory=lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterIvoryFrame')
brass=lib.load_asset('/Game/Conservatory/Architecture/ModularMaster/M_MasterBrass')
assert ivory and brass
backup=root/'Saved/Backups/HabitatIvory'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
backup.mkdir(parents=True)
changed=[]
for path in lib.list_assets(base,recursive=False):
    asset=lib.load_asset(path)
    if not isinstance(asset,u.StaticMesh): continue
    slots=asset.get_editor_property('static_materials')
    if not any(str(s.material_slot_name)=='HabitatFrame' for s in slots): continue
    disk=root/'Content'/Path(path.split('.')[0].removeprefix('/Game/')+'.uasset')
    shutil.copy2(disk,backup/disk.name)
    for i,s in enumerate(slots):
        if str(s.material_slot_name)=='HabitatFrame': asset.set_material(i,ivory)
    assert lib.save_loaded_asset(asset,only_if_is_dirty=False)
    changed.append(asset.get_path_name())
for mat in [ivory,brass]:
    u.MaterialEditingLibrary.set_material_usage(mat,u.MaterialUsage.MATUSAGE_NANITE)
    u.MaterialEditingLibrary.recompile_material(mat)
    assert lib.save_loaded_asset(mat,only_if_is_dirty=False)
(root/'Documentation/HabitatIvory.json').write_text(json.dumps({'changed_meshes':changed,'ivory_material':ivory.get_path_name(),'brass_material':brass.get_path_name(),'backup':str(backup)},indent=2))
print('HABITAT_IVORY_RESTORED',len(changed))
