import bpy
from pathlib import Path
root=Path(__file__).resolve().parents[1]/'SourceAssets/C17'
for name in ['C17-Workbench.blend','C17-AnimationRig.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(root/name))
 for img in bpy.data.images:
  if img.name.startswith('T_C17_'):img.pack()
 bpy.ops.wm.save_as_mainfile(filepath=str(root/name))
