import bpy
for n in ['Dome | fine meridian glazing bar.001','Dome | shared principal rib']:
 o=bpy.data.objects[n]; print(n,o.type)
 if o.type=='CURVE':
  for s in o.data.splines:print([(tuple(p.co)) for p in s.points][::max(1,len(s.points)//8)])
 else:
  vs=o.data.vertices
  for z in [6.2,8,10,12,12.9]:
   v=min(vs,key=lambda v:abs(v.co.z-z));print(tuple(v.co))
