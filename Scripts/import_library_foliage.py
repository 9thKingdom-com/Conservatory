"""Copy the selected owned Epic cache assets and their local package dependencies.
Run with normal Python, not Unreal. Original package paths are retained.
"""
from pathlib import Path
import re, shutil, json
ROOT=Path(__file__).resolve().parents[1]
CACHE=Path(r'C:\ProgramData\Epic\EpicGamesLauncher\VaultCache\Medieval96a5ab5b99efV2\data\Content')
BASE='Medieval_Environment/Real_Landscape/Default/Meshes/'
NAMES=['Trees/SM_White_Oak_01','Trees/SM_White_Oak_02','Trees/SM_White_Oak_Young_01','Trees/SM_White_Oak_Sapling_01','Trees/SM_White_Oak_Sapling_02','Plants/SM_Grass_01','Plants/SM_Grass_01_Var01','Plants/SM_Grass_Long_01','Plants/SM_Fern_01','Plants/SM_Fern_01_Var01','Plants/SM_Plant_03']
todo=[BASE+n for n in NAMES]; seen=set(); copied=[]; missing=set()
while todo:
 name=todo.pop()
 if name in seen: continue
 seen.add(name); source=CACHE/(name+'.uasset')
 if not source.exists(): missing.add(name); continue
 data=source.read_bytes()
 todo.extend(s.decode('ascii')[6:] for s in re.findall(rb'/Game/[A-Za-z0-9_/]+',data))
 for suffix in ['.uasset','.uexp','.ubulk']:
  src=CACHE/(name+suffix)
  if not src.exists(): continue
  dst=ROOT/'Content'/(name+suffix); dst.parent.mkdir(parents=True,exist_ok=True)
  if dst.exists() and dst.read_bytes()!=src.read_bytes(): raise RuntimeError('Refusing to overwrite modified asset '+str(dst))
  shutil.copy2(src,dst); copied.append({'path':str(dst.relative_to(ROOT)).replace('\\','/'),'bytes':src.stat().st_size})
report={'source_pack':'Medieval Houses Modular Vol. 2','source_cache':str(CACHE),'selected':['/Game/'+BASE+n for n in NAMES],'files':copied,'unresolved_package_strings':sorted(missing)}
(ROOT/'Documentation'/'LibraryFoliage.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'copied_files':len(copied),'bytes':sum(f['bytes'] for f in copied),'unresolved':sorted(missing)},indent=2))
