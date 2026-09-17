"""Run in Blender background. Creates original reusable FBX assets and a landscape heightfield."""
import bpy, bmesh, math, random, sys, struct
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height, path_y, SEED
OUT=ROOT/'SourceAssets'/'Environment'; OUT.mkdir(parents=True,exist_ok=True)
random.seed(SEED)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
MATS=['Bark','Leaves','LeavesLight','Stone','Plaster','Roof','Timber','Glass','Grass','Earth','Birch','Ground']
materials={n:bpy.data.materials.new(n) for n in MATS}
class Mesh:
 def __init__(self): self.v=[]; self.f=[]; self.m=[]
 def face(self,vs,mat):
  i=len(self.v); self.v.extend(vs); self.f.append(tuple(range(i,i+len(vs)))); self.m.append(MATS.index(mat))
 def box(self,c,s,mat):
  x,y,z=c; a,b,d=[q/2 for q in s]
  v=[(x+i*a,y+j*b,z+k*d) for i,j,k in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
  for f in [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]: self.face([v[i] for i in f],mat)
 def tube(self,a,b,r1,r2,mat,n=7):
  a,b=Vector(a),Vector(b); direction=(b-a).normalized(); u=direction.cross(Vector((0,1,0))).normalized(); w=direction.cross(u)
  rings=[[p+r*(math.cos(i*math.tau/n)*u+math.sin(i*math.tau/n)*w) for i in range(n)] for p,r in [(a,r1),(b,r2)]]
  for i in range(n): self.face([rings[0][i],rings[0][(i+1)%n],rings[1][(i+1)%n],rings[1][i]],mat)
  self.face(list(reversed(rings[0])),mat); self.face(rings[1],mat)
 def leaf(self,c,size,mat):
  c=Vector(c); u=Vector((random.uniform(-1,1),random.uniform(-1,1),random.uniform(-.45,.65))).normalized()*size
  w=u.cross(Vector((0,0,1))).normalized()*size*.42
  self.face([c-u,c+w,c+Vector((0,0,size*.17))],mat)
  self.face([c+w,c+u,c+Vector((0,0,size*.17))],mat)
  self.face([c+u,c-w,c+Vector((0,0,size*.17))],mat)
  self.face([c-w,c-u,c+Vector((0,0,size*.17))],mat)
 def export(self,name,collision=None):
  bpy.ops.object.select_all(action='DESELECT')
  mesh=bpy.data.meshes.new(name); mesh.from_pydata(self.v,[],self.f); mesh.update()
  obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
  for n in MATS: mesh.materials.append(materials[n])
  for p,m in zip(mesh.polygons,self.m): p.material_index=m
  if name=='SM_DistantHills':
   bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.001); bm.to_mesh(mesh); bm.free()
   for p in mesh.polygons: p.use_smooth=True
  obj.select_set(True); bpy.context.view_layer.objects.active=obj
  if collision:
   cm=bpy.data.meshes.new('collision'); cm.from_pydata(collision.v,[],collision.f); cm.update()
   co=bpy.data.objects.new('UCX_'+name+'_00',cm); bpy.context.collection.objects.link(co); co.select_set(True)
  bpy.ops.export_scene.fbx(filepath=str(OUT/(name+'.fbx')),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},use_mesh_modifiers=True,add_leaf_bones=False)
  bpy.ops.object.delete(use_global=False)
  print('EXPORTED '+name,flush=True)
for variant in range(6):
 random.seed(SEED+variant); m=Mesh(); birch=variant>=4; H=random.uniform(14,19) if not birch else random.uniform(17,22)
 bark='Birch' if birch else 'Bark'; radius=.20 if birch else .42
 m.tube((0,0,-.3),(.4,.15,H),radius,.045,bark,12)
 for root in range(7):
  a=root*math.tau/7; m.tube((math.cos(a)*1.2,math.sin(a)*1.2,-.15),(0,0,1.1),.12,radius*.65,bark)
 for j in range(38):
  z=random.uniform(H*.30,H*.91); ang=j*2.4; spread=(1-z/H)*7+1.3
  tip=Vector((math.cos(ang)*spread,math.sin(ang)*spread,z+random.uniform(.4,2)))
  base=Vector((.3*z/H,.1,z-1)); mid=base.lerp(tip,.65)+Vector((0,0,.45))
  m.tube(base,mid,radius*.30,.04,bark); m.tube(mid,tip,.04,.012,bark,5)
  for twig in range(3):
   end=tip+Vector((random.uniform(-1.3,1.3),random.uniform(-1.3,1.3),random.uniform(-.4,1.2)))
   m.tube(mid,end,.025,.006,bark,4)
   for k in range(28):
    off=Vector((random.gauss(0,.70),random.gauss(0,.70),random.gauss(0,.48)))
    m.leaf(end+off,random.uniform(.16,.29) if birch else random.uniform(.22,.40),'LeavesLight' if random.random()<.23 else 'Leaves')
 col=Mesh(); col.tube((0,0,0),(.2,.1,H*.6),radius,radius*.55,'Bark',8)
 m.export('SM_Birch_'+str(variant-3) if birch else 'SM_Oak_'+str(variant+1),col)
for variant in range(3):
 random.seed(59+variant); m=Mesh()
 for i in range(80):
  x,y=random.uniform(-.9,.9),random.uniform(-.9,.9); h=random.uniform(.18,.7); w=random.uniform(.015,.035)
  a=random.random()*math.tau; dx,dy=math.cos(a)*w,math.sin(a)*w
  m.face([(x-dx,y-dy,0),(x+dx,y+dy,0),(x+dx*.3+.12,y+dy*.3,h*.65),(x+.17,y,h)],'Grass')
 m.export('SM_Grass_'+str(variant+1))
m=Mesh()
for i in range(16):
 a=i*2.4; length=random.uniform(.6,1.3); tip=Vector((math.cos(a)*length,math.sin(a)*length,.6)); base=Vector((0,0,0))
 m.tube(base,tip,.013,.002,'Grass',4)
 for j in range(1,10):
  c=base.lerp(tip,j/11); w=(1-j/11)*.28
  for sign in [-1,1]:
   t=c+Vector((math.cos(a+sign*1.2)*w,math.sin(a+sign*1.2)*w,.08))
   m.face([c,c+Vector((.035,.035,.06)),t],'Leaves')
m.export('SM_Fern')
for variant in range(3):
 m=Mesh(); bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1)
 obj=bpy.context.object
 for v in obj.data.vertices:
  v.co*=random.uniform(.8,1.15); v.co.x*=1.5; v.co.y*=1.1; v.co.z*=.7; v.co.z+=.35
 for p in obj.data.polygons: m.face([obj.data.vertices[i].co.copy() for i in p.vertices],'Stone')
 bpy.data.objects.remove(obj,do_unlink=True); m.export('SM_Rock_'+str(variant+1))
for variant in range(4):
 m=Mesh(); W=7+variant*.8; L=9+variant; H=4.4 if variant!=2 else 6.4
 m.box((0,0,.4),(W+.3,L+.3,.8),'Stone'); m.box((0,0,H/2),(W,L,H),'Plaster')
 # Gable roof with thickness, fascia, weathered standing seams and chimney.
 peak=H+W*.42
 for side in [-1,1]:
  m.face([(side*(W/2+.5),-L/2-.5,H),(side*(W/2+.5),L/2+.5,H),(0,L/2+.5,peak),(0,-L/2-.5,peak)],'Roof')
  for yy in [-L/2-.51,L/2+.51]: m.tube((side*(W/2+.5),yy,H),(0,yy,peak),.09,.09,'Timber',4)
 for yy in [-L/2,L/2]: m.face([(-W/2,yy,H),(W/2,yy,H),(0,yy,peak)],'Plaster')
 for side in [-1,1]:
  for yy in [-L*.28,0,L*.28]:
   for zz in ([2.3,4.8] if H>6 else [2.2]):
    m.box((side*(W/2+.035),yy,zz),(.07,1.15,1.5),'Timber'); m.box((side*(W/2+.08),yy,zz),(.03,.94,1.30),'Glass')
    m.box((side*(W/2+.10),yy,zz),(.05,.055,1.3),'Timber'); m.box((side*(W/2+.10),yy,zz),(.05,1,.05),'Timber')
    m.box((side*(W/2+.12),yy,zz-.8),(.32,1.4,.12),'Stone')
    if random.random()<.40:
     m.box((side*(W/2+.15),yy,zz-.2),(.07,1.3,.17),'Timber'); m.box((side*(W/2+.15),yy,zz+.35),(.07,1.3,.12),'Timber')
 m.box((0,-L/2-.05,1.15),(1.15,.12,2.3),'Timber')
 m.box((0,-L/2-.65,.10),(1.9,1.2,.2),'Stone')
 m.box((W*.23,L*.22,peak-.4),(.75,.8,2.4),'Stone'); m.box((W*.23,L*.22,peak+.83),(.95,1,.16),'Stone')
 # Unmaintained gutters and creeping vine stems/leaves on the facade.
 for side in [-1,1]: m.tube((side*W/2,-L/2,H-.1),(side*W/2,L/2,H-.1),.075,.075,'Timber')
 for j in range(180):
  z=random.uniform(.1,H); yy=-L/2+.6+math.sin(z*1.3)*.5+random.gauss(0,.42)
  m.leaf((W/2+.16,yy,z),random.uniform(.09,.20),'Leaves')
 col=Mesh(); col.box((0,0,H/2),(W,L,H),'Stone'); m.export('SM_Cottage_'+str(variant+1),col)
m=Mesh(); m.box((0,0,4),(5,5,8),'Stone'); m.box((0,0,8.7),(4.5,4.5,1.4),'Plaster')
for side in [-1,1]:
 m.box((side*2.27,0,8.7),(.05,1,1.1),'Glass')
for a in range(4):
 ang=a*math.pi/2; ang2=(a+1)*math.pi/2
 m.face([(3*math.cos(ang),3*math.sin(ang),9.4),(3*math.cos(ang2),3*math.sin(ang2),9.4),(0,0,13)],'Roof')
col=Mesh(); col.box((0,0,4),(5,5,8),'Stone'); m.export('SM_BellTower',col)
m=Mesh(); m.box((0,0,.5),(2.1,.48,1),'Stone'); m.export('SM_Wall')
m=Mesh(); m.tube((0,0,.3),(4,0,.45),.3,.24,'Bark',10); m.export('SM_FallenLog')
# Track follows terrain; discontinuous grass later softens the edges.
m=Mesh()
for i in range(360):
 x=-140+i; xn=x+1
 for side in [-1,1]:
  y=path_y(x); yn=path_y(xn)
  inner=side*.55; outer=side*1.3
  vs=[(x,y+inner,height(x,y+inner)+.045),(xn,yn+inner,height(xn,yn+inner)+.045),(xn,yn+outer,height(xn,yn+outer)+.045),(x,y+outer,height(x,y+outer)+.045)]
  m.face(vs if side>0 else list(reversed(vs)),'Earth')
m.export('SM_OldTrack')
m=Mesh()
def ridge(r,a):
 x,y=r*math.cos(a),r*math.sin(a)
 t=min(1,max(0,(r-590)/500)); t=t*t*(3-2*t)
 h=-15*(1-t)+(40+35*math.sin(a*3+.4)**2+65*math.sin(a*7+r*.001)**2+30*math.sin(r*.003))*t
 return (x,y,h)
for ring in range(30):
 r=590+ring*120; rn=r+120
 for j in range(256):
  a=j*math.tau/256; an=(j+1)*math.tau/256
  m.face([ridge(r,a),ridge(rn,a),ridge(rn,an),ridge(r,an)],'Ground')
m.export('SM_DistantHills')
with open(OUT/'Hill.r16','wb') as f:
 for y in range(505):
  for x in range(505): f.write(struct.pack('<H',round(32768+height(-630+x*2.5,-630+y*2.5)*128)))
print('ASSETS_COMPLETE',flush=True)
