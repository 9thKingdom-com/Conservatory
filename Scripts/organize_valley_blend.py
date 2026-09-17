"""Make the original kit and the complete placement layout separately editable."""
import bpy,json,math
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'SourceAssets/ValleySettlements'
bpy.ops.wm.open_mainfile(filepath=str(out/'Valley-Settlements.blend'))
kit=bpy.context.scene;kit.name='KIT | Original rural buildings'
mesh_objects={o.name:o for o in kit.objects if o.type=='MESH'}
layout=json.loads((out/'layout.json').read_text());scene=bpy.data.scenes.new('LAYOUT | Town hamlets and farms')
for b in layout['buildings']:
 source=mesh_objects[b['mesh']];o=bpy.data.objects.new(b['id']+' | '+b['group']+' | '+b['kind'],source.data);scene.collection.objects.link(o)
 o.location=(b['x'],-b['y'],b['z']);o.rotation_euler.z=-math.radians(b['yaw'])
 o['building_id']=b['id'];o['interior_access']='Open 1.8m doorway; centre route to rear room';o['future_clue_anchors']=json.dumps(b['clue_anchors'])
infra=mesh_objects['SM_Valley_Infrastructure'];scene.collection.objects.link(infra);kit.collection.objects.unlink(infra)
for i,o in enumerate(kit.objects):o.location=(i*22,0,0)
bpy.context.window.scene=scene
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Valley-Settlements.blend'))
print('VALLEY_EDITABLE_LAYOUT_SAVED')
