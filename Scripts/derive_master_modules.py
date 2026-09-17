"""Derive game-ready modules from the supplied MASTER without changing that file."""
import bpy,math,json
from mathutils import Matrix,Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'SourceAssets'/'ModularMaster'; OUT.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene
bpy.data.objects['CONTROLS | Bay count 1, half dome 8, full dome 16']['Bay count']=16
bpy.data.objects['CUPOLA | Drop-in cap - seated Z 12.900'].location.z=12.9
scene.frame_set(scene.frame_current+1);bpy.context.view_layer.update()
D=8*math.cos(math.pi/16); L=16*math.sin(math.pi/16); W=L/2
mats={n:bpy.data.materials.new(n) for n in ['IvoryFrame','Brass','FloorLight','FloorDark','ConservatoryGlass']}
for n,c in {'IvoryFrame':(.65,.62,.51,1),'Brass':(.45,.28,.07,1),'FloorLight':(.5,.48,.40,1),'FloorDark':(.2,.25,.24,1),'ConservatoryGlass':(.3,.6,.65,.12)}.items():mats[n].diffuse_color=c
outscene=bpy.data.scenes.new('Game modules - editable derived copy'); cache={}; groups={'Dome':[],'Passage':[]}
deps=bpy.context.evaluated_depsgraph_get()
for inst in deps.object_instances:
 o=inst.object; parent=inst.parent.name if inst.parent else ''
 if o.type not in {'MESH','CURVE'} or not inst.is_instance:continue
 is_corr=o.name.startswith('Corridor |')
 if is_corr:
  # Dome portal frames own the end arches: passage supplies the linking shell.
  if 'automatic final' in parent:continue
  if not any(k in o.name for k in ['barrel longitudinal','side','floor','Floor','Base |']):continue
  group='Passage'; transform=Matrix.Translation((-11.2-L/2,0,0))@inst.matrix_world
 else:
  if not any(k in parent for k in ['PROCEDURAL REPEAT','CUPOLA']):continue
  angle=math.atan2(inst.matrix_world[1][0],inst.matrix_world[0][0])
  # Bake one source sector explicitly: do not depend on viewport driver evaluation.
  if 'CUPOLA' not in parent and abs(angle)>.01:continue
  group='Dome';transform=inst.matrix_world.copy()
 key=o.name
 if key not in cache:
  mesh=bpy.data.meshes.new_from_object(o,depsgraph=deps)
  mat='FloorLight' if any(k in key.lower() for k in ['base |','floor','foundation']) else 'Brass' if any(k in key.lower() for k in ['bead','finial','ring','rosette','roundel']) else 'IvoryFrame'
  mesh.materials.clear();mesh.materials.append(mats[mat]);cache[key]=mesh
 for bay in (range(16) if group=='Dome' and 'CUPOLA' not in parent else [0]):
  portal=bay in [0,8]
  if group=='Dome' and portal and 'Foundation' in parent:continue
  if group=='Dome' and portal and 'Tall windows' in parent and o.name.startswith('Window |') and not any(k in o.name for k in ['outer jamb','semicircular arch moulding','spandrel spiral']):continue
  obj=bpy.data.objects.new(o.name,cache[key]);outscene.collection.objects.link(obj)
  obj.matrix_world=(Matrix.Rotation(bay*math.tau/16,4,'Z')@transform) if group=='Dome' else transform
  groups[group].append(obj)
# Add watertight visual glazing surfaces, walkable floors and explicit socket datums.
bpy.context.window.scene=outscene
class Geo:
 def __init__(self):self.v=[];self.f=[];self.mi=[]
 def face(self,vs,mat):
  i=len(self.v);self.v.extend(vs);self.f.append(tuple(range(i,i+len(vs))));self.mi.append(list(mats).index(mat))
 def box(self,x,y,z,sx,sy,sz,mat):
  v=[(x+a*sx/2,y+b*sy/2,z+c*sz/2) for a,b,c in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
  for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]:self.face([v[i] for i in f],mat)
 def finish(self,group):
  me=bpy.data.meshes.new(group+' glazing and floor');me.from_pydata(self.v,[],self.f);me.update()
  for m in mats.values():me.materials.append(m)
  for p,i in zip(me.polygons,self.mi):p.material_index=i
  o=bpy.data.objects.new(me.name,me);outscene.collection.objects.link(o);groups[group].append(o)
g=Geo()
for i in range(96):
 a=i*math.tau/96;b=(i+1)*math.tau/96;r=8.16
 g.face([(0,0,.59),(r*math.cos(a),r*math.sin(a),.59),(r*math.cos(b),r*math.sin(b),.59)],'FloorLight')
 g.face([(r*math.cos(a),r*math.sin(a),.42),(r*math.cos(b),r*math.sin(b),.42),(r*math.cos(b),r*math.sin(b),.59),(r*math.cos(a),r*math.sin(a),.59)],'FloorLight')
for x in range(-8,8):
 for y in range(-8,8):
  if (abs(x+.5)+.5)**2+(abs(y+.5)+.5)**2<8.05**2:g.box(x+.5,y+.5,.6,.99,.99,.02,'FloorLight' if (x+y)%2 else 'FloorDark')
for bay in range(16):
 angle=bay*math.tau/16
 def tr(x,y,z):return (x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),z)
 if bay not in [0,8]:g.face([tr(D,-W,.61),tr(D,W,.61),tr(D,W,6.2),tr(D,-W,6.2)],'ConservatoryGlass')
 else:
  for j in range(24):
   y0=-W+j*2*W/24;y1=-W+(j+1)*2*W/24
   h0=4.35+math.sqrt(max(0,W*W-y0*y0));h1=4.35+math.sqrt(max(0,W*W-y1*y1))
   g.face([tr(D,y0,h0),tr(D,y1,h1),tr(D,y1,6.2),tr(D,y0,6.2)],'ConservatoryGlass')
 for j in range(16):
  t0=j*math.acos(.15)/16;t1=(j+1)*math.acos(.15)/16
  for k in range(4):
   a=angle-math.pi/16+k*math.tau/64;b=a+math.tau/64
   g.face([(8*math.cos(t)*math.cos(q),8*math.cos(t)*math.sin(q),6.2+6.7/math.sqrt(1-.15**2)*math.sin(t)) for q,t in [(a,t0),(b,t0),(b,t1),(a,t1)]],'ConservatoryGlass')
# Cupola windows and small roof.
for i in range(32):
 a=i*math.tau/32;b=(i+1)*math.tau/32
 g.face([(1.2*math.cos(q),1.2*math.sin(q),z) for q,z in [(a,13.1),(b,13.1),(b,14.1),(a,14.1)]],'ConservatoryGlass')
 for j in range(8):
  t=j*math.pi/16;v=(j+1)*math.pi/16
  g.face([(1.2*math.cos(p)*math.cos(q),1.2*math.cos(p)*math.sin(q),14.14+.72*math.sin(p)) for q,p in [(a,t),(b,t),(b,v),(a,v)]],'ConservatoryGlass')
g.finish('Dome')
g=Geo();g.box(0,0,.51,L,W*2+.25,.2,'FloorLight')
for side in [-1,1]:g.face([(-L/2,side*W,.61),(L/2,side*W,.61),(L/2,side*W,4.35),(-L/2,side*W,4.35)],'ConservatoryGlass')
for j in range(32):
 a=j*math.pi/32;b=(j+1)*math.pi/32
 g.face([(x,W*math.cos(t),4.35+W*math.sin(t)) for x,t in [(-L/2,a),(L/2,a),(L/2,b),(-L/2,b)]],'ConservatoryGlass')
g.finish('Passage')
for group,objs in groups.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();obj=bpy.context.object
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');obj.name='SM_Master_'+group
 uv=obj.data.uv_layers.new(name='SurfaceUV')
 for p in obj.data.polygons:
  axes=sorted(range(3),key=lambda k:abs(p.normal[k]))[:2]
  for li in p.loop_indices:
   v=obj.data.vertices[obj.data.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
 bpy.ops.export_scene.fbx(filepath=str(OUT/(obj.name+'.fbx')),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},add_leaf_bones=False,mesh_smooth_type='FACE')
 print('EXPORTED',obj.name,len(obj.data.polygons),flush=True)
 obj.hide_set(True)
for o in outscene.objects:o.hide_set(False)
bpy.data.objects['SM_Master_Passage'].location.x=12
# Preserve an editable derivative, not the supplied master.
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Conservatory-GameModules.blend'))
(ROOT/'Documentation'/'MasterSockets.json').write_text(json.dumps({'units':'metres, before uniform game scale 1.5','dome_radius':8,'floor_z':.61,'passage_length':L,'column_width':L,'clear_width':L-.4,'spring_z':4.35,'dome_sockets':[{'position':[s*D,0,.61],'yaw':0 if s>0 else 180} for s in [1,-1]],'passage_sockets':[{'position':[s*L/2,0,.61],'yaw':0 if s>0 else 180} for s in [1,-1]]},indent=2))
