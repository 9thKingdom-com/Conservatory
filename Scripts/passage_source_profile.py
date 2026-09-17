import bpy,json
from mathutils import Vector
for n in ['Corridor | barrel longitudinal glazing bar','Corridor | barrel longitudinal glazing bar.003','Corridor | intermediate barrel hoop','Corridor | longitudinal entablature','Corridor | side plinth moulding','Corridor | walking surface paving','Corridor | foundation slab','Corridor | open transverse arch']:
 o=bpy.data.objects[n];e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=bpy.data.meshes.new_from_object(e,depsgraph=bpy.context.evaluated_depsgraph_get());vs=[v.co for v in me.vertices];print(n, 'min',[min(v[k] for v in vs) for k in range(3)],'max',[max(v[k] for v in vs) for k in range(3)])
