import bpy,math,json
from mathutils import Vector
for name in ['B | SOURCE Window bay','B | SOURCE Roof sector','B | SOURCE Foundation bay','B | SOURCE Cupola']:
 c=bpy.data.collections[name]; print(name)
 for o in c.objects:
  if any(k in o.name.lower() for k in ['floor','rib','sill','glaz','spring','cupola']):
   pts=[o.matrix_world@Vector(v) for v in o.bound_box]; lo=[min(p[k] for p in pts) for k in range(3)];hi=[max(p[k] for p in pts) for k in range(3)]
   print(o.name, [round(v,3) for v in lo],[round(v,3) for v in hi])
