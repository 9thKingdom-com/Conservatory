import bpy,math,json
from mathutils import Vector
s=bpy.context.scene
bpy.data.objects['CONTROLS | Bay count 1, half dome 8, full dome 16']['Bay count']=16
bpy.data.objects['CUPOLA | Drop-in cap - seated Z 12.900'].location.z=12.9
s.frame_set(s.frame_current+1);bpy.context.view_layer.update()
for c in bpy.data.collections:
 if 'SOURCE' in c.name:
  print(c.name,[(o.name, tuple(round(v,3) for v in o.location)) for o in list(c.objects)[:6]])
print('INSTANCE SAMPLE')
for i,inst in enumerate(bpy.context.evaluated_depsgraph_get().object_instances):
 if i<12:print(inst.object.name,inst.parent.name if inst.parent else '',list(inst.matrix_world.translation))
camdata=bpy.data.cameras.new('Inspection');cam=bpy.data.objects.new('Inspection',camdata);s.collection.objects.link(cam)
cam.location=(29,-35,24);cam.rotation_euler=(Vector((3,0,5))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=38;s.camera=cam
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=1400;s.render.resolution_y=1000;s.render.resolution_percentage=100
s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True
s.render.filepath='C:/Users/ASUS TUF/Documents/1 conservatory/Documentation/MasterReference.png';bpy.ops.render.render(write_still=True)
