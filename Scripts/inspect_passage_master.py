"""Read and render the master corridor without saving the reference file."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
deps=bpy.context.evaluated_depsgraph_get();report=[]
out=bpy.data.scenes.new('Corridor reference inspection');cache={};points=[]
for inst in deps.object_instances:
 o=inst.object
 if not inst.is_instance or not o.name.startswith('Corridor |') or o.type not in ['MESH','CURVE']:continue
 me=bpy.data.meshes.new_from_object(o,depsgraph=deps)
 item={'name':o.name,'parent':inst.parent.name if inst.parent else '', 'matrix':[list(r) for r in inst.matrix_world],'vertices':len(me.vertices),'polygons':len(me.polygons)}
 report.append(item)
 if o.name not in cache:cache[o.name]=me
 obj=bpy.data.objects.new(o.name,me);out.collection.objects.link(obj);obj.matrix_world=inst.matrix_world.copy()
 points.extend(obj.matrix_world@Vector(c) for c in obj.bound_box)
(ROOT/'Documentation/PassageMasterInspection.json').write_text(json.dumps(report,indent=2))
assert points,'No evaluated corridor instances'
lo=Vector([min(p[k] for p in points) for k in range(3)]);hi=Vector([max(p[k] for p in points) for k in range(3)]);target=(lo+hi)/2
bpy.context.window.scene=out
data=bpy.data.cameras.new('Reference camera');cam=bpy.data.objects.new('Reference camera',data);out.collection.objects.link(cam);cam.location=target+Vector((9,-12,7));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=max(hi-lo)*1.6;out.camera=cam
out.render.engine='BLENDER_WORKBENCH';out.render.resolution_x=1500;out.render.resolution_y=1100;out.render.resolution_percentage=100
out.display.shading.light='STUDIO';out.display.shading.color_type='MATERIAL';out.display.shading.show_cavity=True;out.display.shading.show_shadows=True
out.render.filepath=str(ROOT/'Documentation/PassageMasterReference.png');bpy.ops.render.render(write_still=True)
print(json.dumps({'instances':len(report),'unique':sorted(set(i['name'] for i in report)),'bounds':[list(lo),list(hi)]}),flush=True)
