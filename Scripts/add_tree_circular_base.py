import bpy,bmesh,math,json,datetime
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory');O=R/'Asset Chest/01 John Originals/TREE-MASTER'
assert Path(bpy.data.filepath)==O/'TREE-MASTER.blend'
if bpy.context.object and bpy.context.object.mode!='OBJECT':bpy.ops.object.mode_set(mode='OBJECT')
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
bpy.ops.wm.save_as_mainfile(filepath=str(O/('TREE-MASTER-PreCircularBase-'+stamp+'.blend')),copy=True)
old=bpy.data.collections['08 Planter'];old.name='98 Archived original planter';old.hide_render=True;old.hide_viewport=True
col=bpy.data.collections.new('08 Circular limestone planter');bpy.context.scene.collection.children.link(col)
root=bpy.data.objects.get('OLIVE TREE MASTER | ground origin')
def mat(name,color,rough=.7,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 return m
stone=mat('Circular base | pale warm limestone',(.56,.50,.39));recess=mat('Circular base | recessed limestone',(.43,.385,.30));brass=bpy.data.materials['Planter | aged brass'];soil=bpy.data.materials['Soil | cultivated earth']
for m in [stone,recess]:
 nt=m.node_tree;p=nt.nodes.get('Principled BSDF');n=nt.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=17;n.inputs['Detail'].default_value=3;b=nt.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.18;b.inputs['Distance'].default_value=.018;nt.links.new(n.outputs['Fac'],b.inputs['Height']);nt.links.new(b.outputs['Normal'],p.inputs['Normal'])
def mesh(name,vs,fs,material,bevel=0):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();ob=bpy.data.objects.new(name,me);col.objects.link(ob);ob.parent=root;me.materials.append(material)
 if bevel:
  mod=ob.modifiers.new('Soft dressed stone edges','BEVEL');mod.width=bevel;mod.segments=2
 return ob
def arc(name,ri,ro,z,h,material,a0=0,a1=math.tau,segments=256,bevel=0):
 vs=[];fs=[];n=segments+1
 for r,zz in [(ri,z),(ro,z),(ro,z+h),(ri,z+h)]:vs.extend([(r*math.cos(a0+(a1-a0)*j/segments),r*math.sin(a0+(a1-a0)*j/segments),zz) for j in range(n)])
 for k in range(4):
  for j in range(segments):fs.append((k*n+j,k*n+j+1,((k+1)%4)*n+j+1,((k+1)%4)*n+j))
 fs.extend([(0,n,2*n,3*n),(n-1,4*n-1,3*n-1,2*n-1)])
 ob=mesh(name,vs,fs,material,bevel)
 for p in ob.data.polygons:p.use_smooth=(p.index<3*segments and p.index>=segments) or p.index>=3*segments and p.index<4*segments
 return ob
arc('Circular base | continuous inner retaining wall',5.94,6.12,.15,.49,recess)
for i in range(16):
 a0=i*math.tau/16+.001;a1=(i+1)*math.tau/16-.001
 for label,ri,ro,z,h in [('lower plinth',5.91,6.39,0,.12),('stepped foot',5.94,6.31,.12,.10),('lower moulding',5.96,6.245,.22,.065),('upper moulding',5.94,6.245,.625,.065),('coping',5.86,6.34,.69,.11)]:
  arc('Circular base | %s %02d'%(label,i+1),ri,ro,z,h,stone,a0,a1,16,.012)
 arc('Circular base | inset panel %02d'%(i+1),6.10,6.16,.30,.30,recess,a0+.018,a1-.018,16,.008)
 # Narrow raised frame around each curved recessed panel.
 for z in [.29,.59]:arc('Circular base | panel border %02d'%(i+1),6.14,6.195,z,.018,stone,a0+.015,a1-.015,16,.004)
 a=i*math.tau/16
 arc('Circular base | pilaster %02d'%(i+1),5.9,6.29,.21,.49,stone,a-.024,a+.024,5,.014)
 arc('Circular base | pilaster cap %02d'%(i+1),5.84,6.38,.69,.15,stone,a-.031,a+.031,5,.012)
# Four slightly raised cartouches echo the reference's central panel while keeping a circular footprint.
for i in range(4):
 a=-math.pi/2+i*math.pi/2
 arc('Circular base | raised cartouche %02d'%(i+1),5.88,6.26,.27,.65,stone,a-.18,a+.18,32,.018)
 arc('Circular base | cartouche inset %02d'%(i+1),6.26,6.28,.39,.40,recess,a-.15,a+.15,24,.008)
 arc('Circular base | cartouche crown %02d'%(i+1),5.82,6.38,.92,.09,stone,a-.195,a+.195,32,.012)
 # Restrained compass medallion, no unrequested inscription.
 center=Vector((6.295*math.cos(a),6.295*math.sin(a),.61));t=Vector((-math.sin(a),math.cos(a),0));up=Vector((0,0,1));radial=Vector((math.cos(a),math.sin(a),0));vs=[];fs=[]
 for j in range(64):
  q=j*math.tau/64
  for r in [.108,.119]:vs.append(center+t*(math.cos(q)*r)+up*(math.sin(q)*r))
 for j in range(64):fs.append((2*j,2*j+1,2*((j+1)%64)+1,2*((j+1)%64)))
 for j in range(8):
  q=j*math.tau/8;idx=len(vs);length=.16 if j%2==0 else .10;vs.extend([center+radial*.005,center+t*(math.cos(q-.22)*.035)+up*(math.sin(q-.22)*.035),center+t*(math.cos(q)*length)+up*(math.sin(q)*length),center+t*(math.cos(q+.22)*.035)+up*(math.sin(q+.22)*.035)]);fs.append(tuple(range(idx,idx+4)))
 mesh('Circular base | compass %02d'%(i+1),vs,fs,brass)
arc('Circular base | cultivated soil',.001,5.955,.04,.43,soil)
# Reveal the asset for assembly review, retaining the sculptable wood as a separate mesh.
for o in bpy.context.scene.objects:
 if any(c.name[:2] in ['01','04','06','07','08'] for c in o.users_collection):o.hide_set(False)
bpy.ops.object.select_all(action='DESELECT');wood=bpy.data.objects['OLIVE | SCULPT trunk roots branches'];wood.select_set(True);bpy.context.view_layer.objects.active=wood
for s in bpy.data.screens:
 for ar in s.areas:
  if ar.type=='VIEW_3D':
   sp=ar.spaces.active;sp.shading.type='MATERIAL';sp.overlay.show_overlays=False;sp.region_3d.view_perspective='PERSP';sp.region_3d.view_location=(0,0,4);sp.region_3d.view_distance=24;sp.region_3d.view_rotation=Vector((12,-22,10)).to_track_quat('Z','Y')
im=bpy.data.images.load('C:/Users/ASUS TUF/Downloads/tree2-base.png',check_existing=True);im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(O/'TREE-MASTER.blend'))
(O/'CircularBaseReport.json').write_text(json.dumps(dict(backup='TREE-MASTER-PreCircularBase-'+stamp+'.blend',outer_diameter_m=12.78,wall_height_m=.8,cartouche_height_m=1.01,tree_mesh_preserved=True,old_planter_archived=True,status='Positional source revision; refinement by John later'),indent=2))
print('CIRCULAR_BASE_SAVED',len(col.objects))
