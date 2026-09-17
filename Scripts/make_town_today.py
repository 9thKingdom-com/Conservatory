"""Original small-town dressing kit; run in Blender background. Metre units."""
import bpy, math, random, sys, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Scripts'))
from layout import height
OUT=ROOT/'SourceAssets/TownToday';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
palette={'Asphalt':(.055,.061,.065),'Concrete':(.38,.37,.33),'PaintWhite':(.72,.70,.62),'Rubber':(.012,.014,.016),'Metal':(.28,.30,.31),'Glass':(.028,.065,.080),'Red':(.25,.035,.024),'Blue':(.035,.10,.16),'Cream':(.48,.42,.28),'Green':(.06,.13,.105),'Wall':(.56,.51,.41),'Brick':(.29,.13,.075),'Roof':(.12,.13,.14),'Lamp':(.78,.75,.59),'TailLight':(.38,.015,.008),'Black':(.018,.022,.023),'Paper':(.65,.62,.50)}
mats={}
for n,c in palette.items():
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);mats[n]=m
parts=[]
def material(obj,name):obj.data.materials.append(mats[name]);parts.append(obj);return obj
def box(c,s,mat,bevel=.02):
 bpy.ops.mesh.primitive_cube_add(size=1,location=c);o=bpy.context.object;o.scale=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Manufactured edges','BEVEL');mod.width=bevel;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 return material(o,mat)
def face(v,mat):
 me=bpy.data.meshes.new('surface');me.from_pydata(v,[],[tuple(range(len(v)))]);me.update();o=bpy.data.objects.new('surface',me);bpy.context.collection.objects.link(o);return material(o,mat)
def tube(a,b,r,mat,vertices=12):
 a,b=Vector(a),Vector(b);d=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=d.length,location=(a+b)/2);o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return material(o,mat)
def text(body,c,size,mat,rot=(math.pi/2,0,0)):
 cu=bpy.data.curves.new(body,'FONT');cu.body=body;cu.size=size;cu.align_x='CENTER';cu.extrude=.002
 o=bpy.data.objects.new(body,cu);bpy.context.collection.objects.link(o);o.location=c;o.rotation_euler=rot
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False);return material(o,mat)
def export(name):
 global parts
 bpy.ops.object.select_all(action='DESELECT')
 for o in parts:o.select_set(True)
 bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 uv=o.data.uv_layers.new(name='SurfaceUV')
 for p in o.data.polygons:
  axes=sorted(range(3),key=lambda k:abs(p.normal[k]))[:2]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
 bpy.ops.export_scene.fbx(filepath=str(OUT/(name+'.fbx')),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},add_leaf_bones=False,mesh_smooth_type='FACE')
 o.hide_set(True);parts=[];return o

# All site geometry uses world coordinates; Blender Y is negated for Unreal.
def quad_world(v,mat):return face([(x,-y,z) for x,y,z in reversed(v)],mat)
def patch(x0,x1,y0,y1,mat,dz=.08,step=2):
 nx=max(1,math.ceil((x1-x0)/step));ny=max(1,math.ceil((y1-y0)/step))
 for i in range(nx):
  for j in range(ny):
   xa=x0+(x1-x0)*i/nx;xb=x0+(x1-x0)*(i+1)/nx;ya=y0+(y1-y0)*j/ny;yb=y0+(y1-y0)*(j+1)/ny
   quad_world([(x,y,height(x,y)+dz) for x,y in [(xa,ya),(xb,ya),(xb,yb),(xa,yb)]],mat)
patch(65,325,4.4,11.6,'Asphalt',.16)
patch(221.4,228.6,-82,96,'Asphalt',.165)
for y in [2.15,11.7]:
 for xa,xb in [(135,220.9),(229.1,302)]:patch(xa,xb,y,y+2.1,'Concrete',.29)
for x in [219.1,228.7]:
 for ya,yb in [(-76,1.6),(14.2,91)]:patch(x,x+2.1,ya,yb,'Concrete',.30)
for x in range(70,323,6):
 if abs(x-225)>6:patch(x,x+2.8,7.94,8.06,'PaintWhite',.18,1)
for y in range(-78,94,6):
 if abs(y-8)>7:patch(224.94,225.06,y,y+2.8,'PaintWhite',.185,1)
for y in [4.66,11.24]:
 for xa,xb in [(65,221.35),(228.65,325)]:patch(xa,xb,y,y+.10,'PaintWhite',.18)
for y in [-.5,16]:
 for x in [222,223,224,225,226,227]:patch(x,x+.5,y,y+2,'PaintWhite',.195,1)
# Short streets give both residential rows actual frontage.
for y in [-35,57]:
 patch(140,292,y-2.7,y+2.7,'Asphalt',.17)
 for side in [-1,1]:patch(140,292,y+side*3.1-.45,y+side*3.1+.45,'Concrete',.25)
# Station apron and driveways follow the ground without floating corners.
patch(100,136,-35,4.3,'Concrete',.23)
for x in [103,133]:patch(x-2,x+2,-1,7,'Asphalt',.245)
for x in [105,109,113,117,121,125,129]:patch(x,x+.10,-33,-29,'PaintWhite',.25,1)
# Graded shop forecourt connects the raised threshold to the main street pavement.
shop_z=max(height(x,y) for x in [174,186] for y in [-20.5,-11.5])+.28
def apron(x,y):
 t=max(0,min(1,(y+11.5)/13.65));return shop_z*(1-t)+(height(x,2.15)+.29)*t
for i in range(16):
 for j in range(15):
  xa=172+i;xb=xa+1;ya=-11.5+j*.91;yb=ya+.91
  quad_world([(x,y,apron(x,y)) for x,y in [(xa,ya),(xb,ya),(xb,yb),(xa,yb)]],'Concrete')
# Drives follow the actual deterministic cottage placement and front-door orientation.
random.seed(5802)
for row,yy in enumerate([-53,-16,37,76]):
 for col in range(5 if row<3 else 3):
  x=150+col*30+random.uniform(-4,4);y=yy+random.uniform(-5,5);yaw=random.uniform(-8,8)+(180 if row%2 else 0)
  variant=(row+col)%4;length=9+variant
  door=y+(1 if row%2==0 else -1)*(length/2+.5);road=-35 if row<2 else 57
  patch(x-1.4,x+1.4,min(door,road),max(door,road),'Concrete',.22,1)
export('SM_TownRoads')

# Detailed older four-door cars, front along +X.
def car(name,color,wagon=False,crashed=False):
 body=box((0,0,.72),(4.45,1.77,.66),color,.16)
 # Actual wheel arch openings in the body.
 for x in [-1.35,1.35]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.405,depth=2.2,location=(x,0,.39),rotation=(math.pi/2,0,0));cut=bpy.context.object
  bpy.context.view_layer.objects.active=body;mod=body.modifiers.new('Wheel arch','BOOLEAN');mod.object=cut;mod.operation='DIFFERENCE';bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 box((-.10,0,.44),(3.25,1.6,.17),'Black',.035)
 # Trapezoidal cabin with glazing fitted to the frame.
 rear=-1.65 if wagon else -1.05
 v=[(rear-.25,-.80,1.02),(1.17,-.80,1.02),(.60,-.65,1.58),(rear,-.65,1.58)]
 for side in [-1,1]:
  vv=[(x,y*side,z) for x,y,z in v];face(vv,color)
  face([(rear+.05,-.806*side,1.10),(.03,-.806*side,1.10),(.03,-.674*side,1.51),(rear+.07,-.674*side,1.51)],'Glass')
  face([(.11,-.806*side,1.10),(1.03,-.806*side,1.10),(.56,-.674*side,1.51),(.11,-.674*side,1.51)],'Glass')
  tube((.065,-.805*side,1.05),(.065,-.666*side,1.57),.028,'Black')
  for x in [-.85,.52]:
   box((x,side*.899,.96),(.16,.024,.035),'Metal',.009)
   tube((x+.18,side*.897,.56),(x+.18,side*.897,1.02),.006,'Black',6)
  tube((-1.95,side*.89,.66),(1.95,side*.89,.66),.025,'Black')
  box((.9,side*.98,1.07),(.18,.18,.105),color,.045)
 face([(1.17,-.80,1.035),(1.17,.80,1.035),(.60,.65,1.58),(.60,-.65,1.58)],'Glass')
 face([(rear-.25,-.80,1.035),(rear,-.65,1.58),(rear,.65,1.58),(rear-.25,.80,1.035)],'Glass')
 box(((rear+.6)/2,0,1.59),(.6-rear+.08,1.34,.065),color,.05)
 for side in [-1,1]:
  tube((1.17,side*.80,1.03),(.60,side*.65,1.58),.036,color)
  tube((rear-.25,side*.80,1.03),(rear,side*.65,1.58),.04,color)
 for x in [-1.35,1.35]:
  for y in [-.9,.9]:
   bpy.ops.mesh.primitive_torus_add(major_radius=.26,minor_radius=.10,major_segments=32,minor_segments=12,location=(x,y,.37),rotation=(math.pi/2,0,0));material(bpy.context.object,'Rubber')
   tube((x,y-.08,.37),(x,y+.08,.37),.205,'Metal',24)
   for k in range(8):
    a=k*math.tau/8;tube((x,y*1.10,.37),(x+.17*math.cos(a),y*1.10,.37+.17*math.sin(a)),.018,'Black',6)
 for end in [-1,1]:
  box((end*2.22,0,.57),(.12,1.72,.14),'Black',.04)
  box((end*2.287,0,.72),(.016,.48,.12),'PaintWhite',.004)
  for side in [-1,1]:box((end*2.23,side*.61,.91),(.055,.40,.17),'Lamp' if end>0 else 'TailLight',.025)
 box((2.24,0,.91),(.025,.62,.16),'Black',.01)
 for y in [-.24,-.12,0,.12,.24]:box((2.26,y,.91),(.03,.022,.13),'Metal',.002)
 for y in [-.32,.32]:tube((1.09,y,1.10),(.95,y+.22,1.24),.009,'Black',6)
 if crashed:
  for o in parts:
   bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.select_set(False)
   for p in o.data.vertices:
    if p.co.x>1.48:
     q=p.co.x-1.48;p.co.x=1.48+q*.50;p.co.z+=q*.19*math.sin(p.co.y*9+q*7)
  # Fractured windshield lines, confined to the windshield plane.
  for y in [-.35,-.12,.18,.40]:tube((.87,y,1.32),(.66,y+.12,1.52),.008,'PaintWhite',6)
 export(name)
car('SM_OldSedan','Blue')
car('SM_OldEstate','Cream',True)
car('SM_CrashedSedan','Red',False,True)

# Petrol station shop: front faces Blender -Y / Unreal +Y.
box((0,0,1.75),(16,8,3.5),'Wall',.07);box((0,0,3.58),(16.5,8.5,.30),'Roof',.06)
box((0,-4.06,2.95),(16.2,.20,.65),'Green',.025)
text('VALLEY FUEL',(0,-4.18,2.76),.48,'PaintWhite')
for x in [-5,-2,3,6]:
 box((x,-4.065,1.65),(2.5,.06,1.8),'Glass',.025)
 for xx in [x-1.25,x+1.25]:box((xx,-4.105,1.65),(.055,.07,1.9),'Metal',.004)
box((.45,-4.09,1.20),(1.3,.07,2.35),'Glass',.015);box((1.05,-4.15,1.15),(.04,.08,.45),'Metal',.01)
box((0,0,-.30),(16.4,8.4,.60),'Concrete',.02)
export('SM_FuelShop')
box((0,0,4.65),(22,10,.42),'PaintWhite',.06)
box((0,-5.025,4.63),(22,.09,.46),'Green',.015)
box((0,-5.08,4.43),(22,.10,.08),'Red',.005)
text('VALLEY FUEL',(0,-5.09,4.52),.35,'PaintWhite')
for x in [-8,8]:
 for y in [-3.4,3.4]:box((x,y,2.27),(.24,.24,4.54),'Metal',.015)
for x in [-5,5]:box((x,0,4.41),(2,.45,.05),'Lamp',.015)
export('SM_FuelCanopy')
box((0,0,.13),(1.35,2.8,.26),'Concrete',.12)
box((0,0,.76),(.60,.65,1.28),'Green',.06)
box((0,0,1.48),(.86,.68,.52),'PaintWhite',.065)
for y in [-.351,.351]:
 box((0,y,1.51),(.61,.025,.22),'Black',.012)
 text('00.00',(0,-.373,1.49),.115,'PaintWhite')
 text('UNLEADED',(0,-.374,1.30),.071,'Black')
 for x in [-.20,0,.20]:box((x,y,1.18),(.09,.023,.07),'Black',.01)
for side in [-1,1]:
 pts=[(side*.43,0,1.55),(side*.70,0,1.30),(side*.79,0,.40),(side*.60,0,.30),(side*.49,0,.95)]
 for a,b in zip(pts,pts[1:]):tube(a,b,.026,'Rubber')
 tube((side*.49,0,.95),(side*.49,0,1.18),.045,'Black');tube((side*.49,0,1.18),(side*.36,0,1.29),.020,'Metal')
export('SM_FuelPump')
box((0,0,2.2),(.22,.22,4.4),'Metal',.01);box((0,0,4.4),(3,.35,1.5),'Green',.04)
text('FUEL',(0,-.19,4.53),.47,'PaintWhite');text('95   DIESEL',(0,-.19,4.03),.24,'PaintWhite')
export('SM_FuelSign')

# Corner shop with a real opening for the crash rather than a car buried in solid wall.
box((0,0,-.30),(12.3,9.3,.6),'Concrete',.02)
box((0,4.4,1.55),(12,.20,3.1),'Brick',.02)
for x in [-5.9,5.9]:box((x,0,1.55),(.20,9,3.1),'Brick',.02)
box((0,0,4.75),(12,9,3.3),'Wall',.035)
box((0,-4.52,2.9),(12.2,.22,.55),'Green',.015)
text('VALLEY STORES',(0,-4.65,2.75),.45,'PaintWhite')
for x in [-5.3,-1.7,5.5]:box((x,-4.45,1.30),(.5,.24,2.60),'Brick',.01)
box((-3.5,-4.47,1.50),(3.0,.045,1.85),'Glass',.008)
box((-.4,-4.47,1.28),(1.55,.05,2.45),'Glass',.01)
box((0,0,.03),(12,9,.09),'Concrete',.005)
# Interior shelves are visible through the broken right display window.
for y in [0,2.8]:
 for z in [.55,1.1,1.65]:box((2,y,z),(4,.5,.07),'Metal',.01)
for x in [-4,-1.3,1.3,4]:
 box((x,-4.535,4.80),(1.25,.045,1.55),'Glass',.008)
 box((x,-4.58,4.80),(.045,.045,1.55),'PaintWhite',.003)
 box((x,-4.60,4.00),(1.45,.32,.10),'Concrete',.01)
for side in [-1,1]:
 face([(-6.4,side*4.8,6.42),(6.4,side*4.8,6.42),(6.4,0,8.7),(-6.4,0,8.7)],'Roof')
 face([(side*6,-4.5,6.4),(side*6,4.5,6.4),(side*6,0,8.7)],'Wall')
box((4,2,8.1),(.6,.7,2),'Brick',.02)
export('SM_CornerShopDamaged')

# A few street furnishings, deliberately ordinary and intact.
tube((0,0,0),(0,0,6),.075,'Metal');tube((0,0,6),(0,-1,6.25),.065,'Metal');box((0,-1.1,6.23),(.35,.65,.14),'Roof',.04);box((0,-1.1,6.15),(.26,.5,.035),'Lamp',.01)
export('SM_StreetLamp')
for z in [.10,.28,.46,.64]:box((0,0,z),(.48,.45,.16),'Green',.02)
box((0,0,.76),(.54,.50,.10),'Black',.035);export('SM_StreetBin')
for x in [-.70,.70]:
 box((x,0,.24),(.07,.48,.48),'Metal',.01)
for y in [-.16,0,.16]:box((0,y,.50),(1.8,.13,.06),'Cream',.012)
for z in [.74,.92]:box((0,.22,z),(1.8,.06,.13),'Cream',.012)
export('SM_StreetBench')
random.seed(922)
for i in range(22):
 x=random.uniform(-1.7,1.7);y=random.uniform(-1.0,1.0)
 o=box((x,y,random.uniform(.025,.09)),(random.uniform(.07,.24),random.uniform(.07,.16),random.uniform(.04,.12)),'Brick',.008);o.rotation_euler.z=random.random()*math.tau
for i in range(18):
 x=random.uniform(-1.5,1.5);y=random.uniform(-1,1)
 face([(x,y,.025),(x+.10,y+.03,.025),(x+.03,y+.17,.027)],'Glass')
export('SM_CrashDebris')

# Remove baked-in vegetation from derivative cottage meshes; retain originals.
for k in range(1,5):
 bpy.ops.object.select_all(action='DESELECT');bpy.ops.import_scene.fbx(filepath=str(ROOT/'SourceAssets/Environment'/('SM_Cottage_'+str(k)+'.fbx')))
 imported=list(bpy.context.selected_objects);parts=[]
 for o in imported:
  if o.type!='MESH' or o.name.startswith('UCX_'):bpy.data.objects.remove(o,do_unlink=True);continue
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data)
  foliage=[i for i,m in enumerate(o.data.materials) if m and m.name.split('.')[0] in ['Leaves','LeavesLight','Grass']]
  bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index in foliage],context='FACES');bm.to_mesh(o.data);bm.free();parts.append(o)
 export('SM_CleanCottage_'+str(k))
for o in bpy.context.scene.objects:o.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Town-Today.blend'))
(OUT/'palette.json').write_text(json.dumps(palette,indent=2))
print('TOWN_SOURCE_COMPLETE',flush=True)
