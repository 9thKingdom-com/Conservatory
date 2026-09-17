"""Rebuild the revised robot into a separate Blender workbench and render it."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'SourceAssets/C17Refined';OUT.mkdir(parents=True,exist_ok=True)
(OUT/'References').mkdir(exist_ok=True)
for p in (ROOT/'SourceAssets/C17Detailed/References').glob('*.png'):shutil.copy2(p,OUT/'References'/p.name)
source=(ROOT/'Scripts/make_c17_detailed.py').read_text()
source=source.replace("OUT=ROOT/'SourceAssets/C17Detailed';DOC=ROOT/'Documentation/C17Detailed'", "OUT=ROOT/'SourceAssets/C17Refined';DOC=ROOT/'Documentation/C17Refined'")
source=source.replace("print('C17D_GEOMETRY'", "exec(compile((ROOT/'Scripts/refine_c17_shapes.py').read_text(),str(ROOT/'Scripts/refine_c17_shapes.py'),'exec'),globals())\nprint('C17D_GEOMETRY'")
source=source.replace('C17-Detailed-Reference.blend','C17-Refined-Reference.blend').replace('C17Detailed-','C17Refined-')
source=source.replace("scene.cycles.samples=48", "scene.cycles.samples=64")
source=source.replace("('Hero',(2.6,-4.5,2.25),2.23)","('Hero',(2.6,-4.5,2.05),2.23)")
source=source.replace("'body_height_m':1.805", "'body_height_m':1.795")
source=source.replace("'master_file':'C17-Refined-Reference.blend'", "'master_file':'C17-Refined-Reference.blend','revision':'Reference shape rebuild; compact head, longer forearms, sculpted armour, split guards. No exposed cables or hydraulics.'")
exec(compile(source,str(ROOT/'Scripts/make_c17_detailed.py'),'exec'),globals())
