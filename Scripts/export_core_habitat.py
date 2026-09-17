"""Export approved editable assembly through a temporary scene; never alter source meshes."""
import bpy,math,json,os
import sys
from pathlib import Path
from mathutils import Matrix
ROOT=Path(r'C:\Users\ASUS TUF\Documents\1 conservatory');OUT=ROOT/'SourceAssets/CoreHabitat';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'Scripts'))
from habitat_mesh_finish import finish
source=bpy.data.scenes['ASSEMBLY | Five domes - editable']
exports=bpy.data.scenes.new('TEMP | Core habitat export');bpy.context.window.scene=exports
materials={n:bpy.data.materials.get(n) or bpy.data.materials.new(n) for n in ['HabitatFrame','HabitatBrass','HabitatFloor','HabitatGlass']}
spec={'source':bpy.data.filepath,'meshes':{},'actors':[],'origin_cm':[-11000,0,6230.95]}

def export(name,items,kind='frame'):
 objs=[]
 for mesh,transform,mat in items:
  m=mesh.copy();m.transform(transform);m.materials.clear();m.materials.append(materials[mat])
  for p in m.polygons:p.material_index=0
  if mat=='HabitatFrame':
   m.materials.append(materials['HabitatBrass']);finish(m,1)
  o=bpy.data.objects.new(name,m);exports.collection.objects.link(o);objs.append(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in objs:o.select_set(True)
 bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.join();o=bpy.context.object;o.name=name
 bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 bpy.ops.export_scene.fbx(filepath=str(OUT/(name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,bake_space_transform=False,add_leaf_bones=False,mesh_smooth_type='FACE',use_mesh_modifiers=True)
 spec['meshes'][name]={'kind':kind,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons)}
 bpy.data.objects.remove(o,do_unlink=True)
 print('EXPORTED',name,flush=True)

def single(name,objname,kind='frame',mat='HabitatFrame'):
 export(name,[(source.objects[objname].data,Matrix.Identity(4),mat)],kind)

for size,label in [('Small','East'),('Large','Centre')]:
 for portal,bay in [(False,2),(True,9 if size=='Small' else 1)]:
  on=f'{label} | Bay {bay:02d}'+(' | OPEN CONNECTION' if portal else '')
  single(f'SM_Core_{size}_'+('Portal' if portal else 'Bay'),on)
 cap=[(o.data,Matrix.Identity(4),'HabitatBrass' if int(o.name.rsplit(' ',1)[1]) in [1,2,19,20,21] else 'HabitatFrame') for o in source.objects if o.name.startswith(label+' | Cap ')]
 export('SM_Core_'+size+'_Cap',cap)
 single('SM_Core_'+size+'_Floor',label+' | Floor datum','floor','HabitatFloor')

walk=[o for o in source.objects if o.name.startswith('East | Section ') or o.name.startswith('East | Midpoint |')]
floor=lambda o:any(t in o.name for t in ['foundation slab','PASSAGE-FLOOR','side plinth'])
export('SM_Core_WalkwayFrame',[(o.data,Matrix.Identity(4),'HabitatFrame') for o in walk if not floor(o)])
export('SM_Core_WalkwayFloor',[(o.data,Matrix.Identity(4),'HabitatFloor') for o in walk if floor(o)],'floor')

class Glass:
 def __init__(self):self.v=[];self.f=[]
 def face(self,vs):
  k=len(self.v);self.v.extend(vs);self.f.append(tuple(range(k,k+len(vs))))
 def mesh(self,name):
  m=bpy.data.meshes.new(name);m.from_pydata(self.v,[],self.f);m.update();return m

for size,count,scale,portals in [('Small',16,1,{8}),('Large',24,1.5,{0,6,12,18})]:
 g=Glass();step=math.tau/count;radius=11.3675*scale;half=radius*math.tan(step/2)
 for bay in range(count):
  ang=bay*step
  def tr(y,z):return(radius*math.cos(ang)-y*math.sin(ang),radius*math.sin(ang)+y*math.cos(ang),z)
  if bay not in portals:g.face([tr(-half,.118),tr(half,.118),tr(half,8.47),tr(-half,8.47)])
  else:
   width=1.94
   for j in range(40):
    y0=-half+2*half*j/40;y1=-half+2*half*(j+1)/40
    def lower(y):return .118 if abs(y)>width else 5.94+math.sqrt(max(0,width*width-y*y))
    # Keep all geometry outside the connecting arch's clear opening.
    if abs(y0)>width and abs(y1)>width:g.face([tr(y0,.118),tr(y1,.118),tr(y1,8.47),tr(y0,8.47)])
    else:g.face([tr(y0,max(lower(y0),5.94)),tr(y1,max(lower(y1),5.94)),tr(y1,8.47),tr(y0,8.47)])
 profile=[(11.49,8.49),(11.32,10.43),(10.79,12.30),(9.92,14.00),(8.77,15.44),(7.37,16.57),(5.82,17.34),(4.72,17.63)]
 profile=[(r*scale,8.5+(z-8.5)*scale) for r,z in profile]
 for (r,z),(rr,zz) in zip(profile,profile[1:]):
  for i in range(192):
   a=i*math.tau/192;b=(i+1)*math.tau/192;g.face([(r*math.cos(a),r*math.sin(a),z),(r*math.cos(b),r*math.sin(b),z),(rr*math.cos(b),rr*math.sin(b),zz),(rr*math.cos(a),rr*math.sin(a),zz)])
 # Existing cap: lower moulded skirt followed by its rounded roof.
 capprofile=[(4.72,17.63),(4.80,18.20)]+[(4.38*math.cos(j*math.pi/32),18.20+2.68*math.sin(j*math.pi/32)) for j in range(17)]
 capprofile=[(r*scale,8.5+(z-8.5)*scale) for r,z in capprofile]
 for (r,z),(rr,zz) in zip(capprofile,capprofile[1:]):
  for i in range(96):
   a=i*math.tau/96;b=(i+1)*math.tau/96;g.face([(r*math.cos(a),r*math.sin(a),z),(r*math.cos(b),r*math.sin(b),z),(rr*math.cos(b),rr*math.sin(b),zz),(rr*math.cos(a),rr*math.sin(a),zz)])
 export('SM_Core_'+size+'_Glass',[(g.mesh(size+' glass'),Matrix.Identity(4),'HabitatGlass')],'glass')
g=Glass();x0=17.05125;x1=35.27005
for side in [-1,1]:g.face([(x0,side*2.12,.118),(x1,side*2.12,.118),(x1,side*2.12,5.94),(x0,side*2.12,5.94)])
for i in range(48):
 a=i*math.pi/48;b=(i+1)*math.pi/48;g.face([(x,2.02*math.cos(t),5.94+2.02*math.sin(t)) for x,t in [(x0,a),(x1,a),(x1,b),(x0,b)]])
export('SM_Core_WalkwayGlass',[(g.mesh('walk glass'),Matrix.Identity(4),'HabitatGlass')],'glass')

dist=46.63755
for label,count,size,pos,portals,glassrot in [('Centre',24,'Large',[0,0,0],{0,6,12,18},0),('East',16,'Small',[dist,0,0],{8},0),('North',16,'Small',[0,dist,0],{12},90),('West',16,'Small',[-dist,0,0],{0},180),('South',16,'Small',[0,-dist,0],{4},270)]:
 for i in range(count):spec['actors'].append(dict(label=label+' bay '+str(i+1),mesh='SM_Core_'+size+('_Portal' if i in portals else '_Bay'),position=pos,yaw=i*360/count))
 for kind in ['Cap','Floor','Glass']:spec['actors'].append(dict(label=label+' '+kind,mesh='SM_Core_'+size+'_'+kind,position=pos,yaw=glassrot if kind=='Glass' else 0))
for label,angle in [('East',0),('North',90),('West',180),('South',270)]:
 for kind in ['Frame','Floor','Glass']:spec['actors'].append(dict(label=label+' walkway '+kind,mesh='SM_Core_Walkway'+kind,position=[0,0,0],yaw=angle))
(OUT/'CoreHabitat.json').write_text(json.dumps(spec,indent=2))
bpy.context.window.scene=source;bpy.data.scenes.remove(exports)
print('CORE_HABITAT_EXPORT_COMPLETE',len(spec['meshes']),flush=True)
