import bpy,math,ast,json
from pathlib import Path
from mathutils import Vector
ROOT=Path('C:/Users/ASUS TUF/Documents/1 conservatory');OUT=ROOT/'Asset Chest/01 John Originals/LIFT-MASTER'
assert Path(bpy.data.filepath).name=='LIFT-MASTER.blend'
cols={c.name:c for c in bpy.context.scene.collection.children};root=bpy.data.objects['LIFT_MASTER | floor origin | front -Y']
green=bpy.data.materials['01 | Deep bottle-green enamel'];brass=bpy.data.materials['02 | Aged warm brass'];edge=bpy.data.materials['03 | Polished brass beads'];patina=bpy.data.materials['04 | Dark bronze recesses']
tree=ast.parse((ROOT/'Scripts/build_lift_master.py').read_text());functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name not in ['camera','area','text']];exec(compile(ast.Module(body=functions,type_ignores=[]),'<lift_helpers>','exec'))
box('Entrance | solid green arched tympanum',(0,-1.10,3.015),(2.13,.095,.30),green,b=.006)
# Embossed leaf fans in each spandrel and around post capitals.
for side in [-1,1]:
 for i in range(3):
  leaf('Spandrel | layered acanthus leaf',(side*.83,-1.17,2.96),(side*(.69-i*.075),-1.17,3.12+i*.012),.042)
 for zz in [.53,.83,2.66,2.91]:
  leaf('Stile | sculpted leaf',(side*1.016,-1.161,zz-.09),(side*(1.016-.07),-1.161,zz+.07),.044)
 for y in [-1.04,1.04]:
  for i in range(8):
   a=i*math.tau/8
   # leaf is built flat at front of shaft then rotated around the shaft centre
   before=set(bpy.data.objects)
   leaf('Capital | acanthus petal',(0,-.105,3.04),(0,-.14,3.18),.05)
   for o in set(bpy.data.objects)-before:o.rotation_euler.z=a;o.location.x=side*1.18;o.location.y=y
# S-curved openwork on the exterior side panels.
for side in [-1,1]:
 for yc in [-.53,.53]:
  before=set(bpy.data.objects)
  scroll('Side | lower paired volute',yc-.12,0,.70,.16,1.32,1,math.pi/2)
  scroll('Side | lower counter-volute',yc+.10,0,.63,.13,1.24,-1,-math.pi/2)
  leaf('Side | climbing leaf',(yc-.18,0,.52),(yc+.05,0,.85),.065)
  scroll('Side | upper arch curl',yc-.15,0,2.91,.15,1.20,1,0)
  scroll('Side | upper counter curl',yc+.13,0,2.91,.14,1.20,-1,0)
  curve('Side | long arch frame',[(yc+.36*math.cos(a),0,2.47+.53*math.sin(a)) for a in [i*math.pi/64 for i in range(65)]],.01,brass)
  for o in set(bpy.data.objects)-before:o.rotation_euler.z=math.pi/2;o.location.x=side*1.16
for side in [-1,1]:
 scroll('Crown | apex scroll',side*.10,-.015,4.19,.09,1.16,side,math.pi)
 leaf('Crown | apex leaf',(side*.17,-.016,4.115),(side*.07,-.016,4.29),.042)
# Narrower view, near the reference's frontal perspective.
sc=bpy.context.scene;cam=bpy.data.objects['CAM | Hero three-quarter'];cam.location=(4.35,-10.8,4.50);cam.rotation_euler=(Vector((0,0,2.28))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=69;sc.camera=cam
for screen in bpy.data.screens:
 for ar in screen.areas:
  if ar.type=='VIEW_3D':
   ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.region_3d.view_camera_zoom=8;ar.spaces.active.shading.type='MATERIAL'
root['opening_width_m']=1.515;root['opening_height_m']=2.657
sc.render.resolution_x=1000;sc.render.resolution_y=1250;sc.cycles.samples=64
prefs=bpy.context.preferences.addons['cycles'].preferences
for device_type in ['OPTIX','CUDA','HIP']:
 try:
  prefs.compute_device_type=device_type;prefs.get_devices()
  gpu=[d for d in prefs.devices if d.type!='CPU']
  if gpu:
   for d in prefs.devices:d.use=d.type!='CPU'
   sc.cycles.device='GPU';break
 except Exception:pass
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'LIFT-MASTER.blend'))
print('LIVE_REFINEMENT_SAVED',len(root.children))
