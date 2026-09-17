import bpy
from pathlib import Path
root=Path('C:/Users/ASUS TUF/Documents/1 conservatory/SourceAssets/OrnateLift')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for part in ['Crowned','Bunker']:
 bpy.ops.import_scene.fbx(filepath=str(root/('SM_OrnateLift_'+part+'.fbx')))
 for o in bpy.context.selected_objects:
  if part=='Bunker':o.location.y+=4
for m in bpy.data.materials:
 if m.name.startswith('Brass'):m.diffuse_color=(.48,.30,.1,1)
 elif m.name.startswith('LiftEnamel'):m.diffuse_color=(.025,.075,.07,1)
 elif m.name.startswith('ConservatoryGlass'):m.diffuse_color=(.5,.7,.65,.15)
 elif m.name.startswith('FloorLight'):m.diffuse_color=(.52,.47,.34,1)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Ornate-Service-Lift.blend'))
