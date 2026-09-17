import unreal as u, json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
registry=u.AssetRegistryHelpers.get_asset_registry(); registry.scan_paths_synchronous(['/Game/Medieval_Environment'],True)
report=json.loads((root/'Documentation'/'LibraryFoliage.json').read_text())
for path in report['selected']:
 asset=u.load_asset(path)
 print('LIBRARY_ASSET '+path+' '+str(asset.get_class().get_name())+' '+str(asset.get_bounds())+' LODs='+str(asset.get_num_lods()),flush=True)
