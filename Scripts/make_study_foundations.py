import bpy,bmesh,json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'SourceAssets/LandscapePaintStudy';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'SourceAssets/ValleySettlements/Valley-Settlements.blend'))
b=bpy.data.objects['SM_Valley_Infrastructure'];data=json.loads((root/'SourceAssets/ValleySettlements/layout.json').read_text())['buildings']
bm=bmesh.new();bm.from_mesh(b.data);remove=[]
for f in bm.faces:
 n=b.data.materials[f.material_index].name.split('.')[0];c=f.calc_center_median();x,y=c.x,-c.y
 if n in ['Asphalt','Soil']:remove.append(f)
 elif n=='Gravel':
  keep=False
  for a in data:
   s=1 if a['yaw']==0 else -1;t=(y-a['y'])*s
   if abs(x-a['x'])<3.7 and a['d']/2-.1<t<a['d']/2+13:keep=True;break
  if not keep:remove.append(f)
bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(b.data);bm.free()
bpy.ops.object.select_all(action='DESELECT');b.select_set(True);bpy.context.view_layer.objects.active=b
bpy.ops.export_scene.fbx(filepath=str(out/'SM_Study_Foundations.fbx'),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},add_leaf_bones=False,mesh_smooth_type='FACE')
print('REMOVED_SURFACE_FACES',len(remove))
