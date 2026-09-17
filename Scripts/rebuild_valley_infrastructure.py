"""Rebuild only the infrastructure export and update its editable Blender object."""
from pathlib import Path
p=Path(__file__).with_name('make_valley_settlements.py');s=p.read_text()
line=next(l for l in s.splitlines() if l.startswith('for kind,w,d,finish in [('))
s=s.replace(line,'pass # Existing building assets remain unchanged')
s=s.replace("bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Valley-Settlements.blend'))",'pass # Update the organised source below')
exec(compile(s,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
import bpy
out=p.parents[1]/'SourceAssets/ValleySettlements'
bpy.ops.wm.open_mainfile(filepath=str(out/'Valley-Settlements.blend'))
old=bpy.data.objects.get('SM_Valley_Infrastructure');scene=bpy.data.scenes['LAYOUT | Town hamlets and farms'];bpy.context.window.scene=scene
if old:bpy.data.objects.remove(old,do_unlink=True)
bpy.ops.import_scene.fbx(filepath=str(out/'SM_Valley_Infrastructure.fbx'))
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Valley-Settlements.blend'))
