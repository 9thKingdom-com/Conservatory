import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
random.seed(73113);O=Path('C:/Users/ASUS TUF/Documents/1 conservatory/Asset Chest/01 John Originals/TREE-MASTER');sc=bpy.context.scene
assert Path(bpy.data.filepath)==O/'TREE-MASTER.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(O/'TREE-MASTER-Apple-Checkpoint.blend'),copy=True)
root=bpy.data.objects['TREE-MASTER | ground origin'];bark=bpy.data.materials['Bark | weathered warm grey']
def remove_collection_objects(name):
 for ob in list(bpy.data.collections[name].objects):bpy.data.objects.remove(ob,do_unlink=True)
remove_collection_objects('05 Blossom');remove_collection_objects('06 Orchard fruit')
for ob in list(bpy.data.objects):
 if ob.name.startswith(('Heartwood |','Trunk |','Ivy |')):bpy.data.objects.remove(ob,do_unlink=True)
# Compress the tall orchard form into a low, broad ancient olive silhouette.
def shape(v):
 v=v.copy();v.x*=1.06;v.y*=1.06;v.z=.43+(v.z-.43)*.71;return v
for ob in sc.objects:
 if ob.type=='MESH' and any(c.name[:2] in ['01','02','04','07'] for c in ob.users_collection):
  for v in ob.data.vertices:v.co=shape(v.co)
  ob.data.update()
def mesh(name,vs,fs,mat,col):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.data.collections[col].objects.link(o);o.parent=root;me.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 return o
def tube(name,pts,radii,segments=20):
 vs=[];fs=[]
 for i,c in enumerate(pts):
  c=Vector(c);t=i/(len(pts)-1);d=(Vector(pts[min(i+1,len(pts)-1)])-Vector(pts[max(0,i-1)])).normalized();u=d.cross(Vector((0,1,0)))
  if u.length<.01:u=d.cross(Vector((1,0,0)))
  u.normalize();v=d.cross(u)
  for j in range(segments):
   a=j*math.tau/segments;r=radii[i]*(1+.16*math.sin(a*5+t*8)+.07*math.cos(9*a-t*13));vs.append(c+(u*math.cos(a)+v*math.sin(a))*r)
  if i:
   for j in range(segments):b=(i-1)*segments;fs.append((b+j,b+(j+1)%segments,b+segments+(j+1)%segments,b+segments+j))
 fs.append(tuple(reversed(range(segments))));fs.append(tuple((len(pts)-1)*segments+j for j in range(segments)))
 o=mesh(name,vs,fs,bark,'01 Heartwood and limbs');s=o.modifiers.new('Rounded ancient growth','SUBSURF');s.levels=2;s.render_levels=2;d=o.modifiers.new('Weathered olive bark','DISPLACE');d.texture=bpy.data.textures['Bark | sculpted fissures'];d.strength=.105;d.mid_level=.5;d.texture_coords='GLOBAL';return o
# Interlocking living ribs surround a genuinely open hollow core.
for k in range(9):
 a=k*math.tau/9;pts=[];rads=[]
 for j in range(19):
  t=j/18;aa=a+.40*math.sin(t*5.5+k*.6)+.30*t;rad=1.08+.70*(1-t)**2+.22*math.sin(t*7+k);pts.append((rad*math.cos(aa)+.14*math.sin(t*5),rad*math.sin(aa),.43+t*4.3));rads.append((.38+.20*(1-t))*(1+.25*math.sin(t*10+k)))
 tube('Olive | hollow trunk living rib %02d'%k,pts,rads,24)
for k in range(11):
 a=k*math.tau/11+.2;z=random.uniform(.9,3.8);rad=1.2;pts=[];rads=[]
 for j in range(15):
  t=j/14;aa=a+t*.85;pts.append((rad*math.cos(aa),rad*math.sin(aa),z+.28*math.sin(t*math.pi)));rads.append(.15+.12*math.sin(t*math.pi))
 tube('Olive | twisted bridging burl %02d'%k,pts,rads,14)
# Scar lips leave dark real openings between lobes instead of painting hollow marks.
for k in range(6):
 a=-math.pi/2+(k-2.5)*.39;z=.95+k*.46;pts=[];rads=[]
 for j in range(25):
  t=j/24;ang=t*math.tau;rr=1.46+.10*math.sin(ang*3);pts.append((rr*math.cos(a)+.22*math.cos(ang),rr*math.sin(a),z+.43*math.sin(ang)));rads.append(.10+.035*math.sin(ang*4))
 tube('Olive | weathered hollow rim %02d'%k,pts,rads,12)
# Narrow lanceolate blades, with silver undersides and dark olive upper faces.
leafm=[]
for i,(upper,lower) in enumerate([((.065,.105,.038),(.25,.29,.205)),((.10,.145,.059),(.34,.37,.27)),((.14,.185,.078),(.39,.41,.31))]):
 m=bpy.data.materials.new('Olive foliage | silver underside %d'%i);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');g=n.new('ShaderNodeNewGeometry');mix=n.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(*upper,1);mix.inputs[2].default_value=(*lower,1);l.new(g.outputs['Backfacing'],mix.inputs[0]);l.new(mix.outputs[0],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.63;p.inputs['Specular IOR Level'].default_value=.22;leafm.append(m)
old=bpy.data.objects['Canopy | individually folded leaves'];data=old.data;vs=[];fs=[];inds=[];centers=[]
for b in range(0,len(data.vertices),15):
 base=data.vertices[b+1].co.copy();tip=data.vertices[b+13].co.copy();d=(tip-base);side=(data.vertices[b+8].co-data.vertices[b+6].co).normalized();normal=side.cross(d.normalized());centers.append(base)
 for rep in range(3):
  shift=side*(rep-1)*random.uniform(.025,.12)+Vector((0,0,random.uniform(-.08,.08)));start=len(vs);length=d.length*random.uniform(.66,.96);axis=d.normalized();width=random.uniform(.017,.033)
  for t,w,h in [(0,0,0),(.25,.8,.015),(.55,1,.025),(.82,.62,.01),(1,0,-.02)]:
   for s in [-1,0,1]:vs.append(base+shift+axis*(length*t)+side*(width*w*s)+normal*(h-abs(s)*.014*w))
  for j in range(4):
   for q in range(2):fs.append((start+j*3+q,start+j*3+q+1,start+(j+1)*3+q+1,start+(j+1)*3+q));inds.append(random.randrange(3))
new=bpy.data.meshes.new('Olive | 60000 narrow blades');new.from_pydata(vs,[],fs);new.update()
for m in leafm:new.materials.append(m)
for p,i in zip(new.polygons,inds):p.material_index=i;p.use_smooth=True
old.data=new;old.name='Olive | narrow silver green canopy'
# Modest olive clusters, replacing the conspicuous apples.
m=bpy.data.materials.new('Olives | green to purple');m.diffuse_color=(.065,.09,.015,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.08,.105,.022,1);p.inputs['Roughness'].default_value=.3
vs=[];fs=[]
for c in random.sample(centers,240):
 c=c+Vector((0,0,-.09));b=len(vs)
 for i in range(9):
  ph=math.pi*i/8
  for j in range(10):a=j*math.tau/10;vs.append(c+Vector((.027*math.sin(ph)*math.cos(a),.027*math.sin(ph)*math.sin(a),.042*math.cos(ph))))
 for i in range(8):
  for j in range(10):fs.append((b+i*10+j,b+i*10+(j+1)%10,b+(i+1)*10+(j+1)%10,b+(i+1)*10+j))
mesh('Olive | small fruit clusters',vs,fs,m,'06 Orchard fruit')
remove_collection_objects('99 Reference')
for i,name in enumerate(['olive-tree2.jpg','olive-tree1.jpg','tree3-oldest-4000.jpeg']):
 im=bpy.data.images.load(str(Path('C:/Users/ASUS TUF/Downloads')/name));im.pack();o=bpy.data.objects.new('REFERENCE | '+name,None);bpy.data.collections['99 Reference'].objects.link(o);o.empty_display_type='IMAGE';o.data=im;o.empty_display_size=8;o.location=(-16-i*9,4,5);o.rotation_euler=(math.pi/2,0,0);o.hide_render=True
sc.name='TREE-MASTER | ancient olive';root.name='OLIVE TREE MASTER | ground origin'
cam=bpy.data.objects['CAM | Hero'];cam.location=(12,-25,9);cam.rotation_euler=(Vector((0,0,4.6))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=48;sc.camera=cam
cam=bpy.data.objects['CAM | Root detail'];cam.location=(5,-9,4);cam.rotation_euler=(Vector((0,0,2.2))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=49
for t in bpy.data.texts:
 if t.name.startswith('START HERE'):t.clear();t.write('TREE-MASTER — ancient olive revision\nOlive species replaces the apple direction by John\'s request. Hollow interlocking trunk ribs, narrow silver-backed foliage and small olives. Planter retained. References packed separately. Blender review master only; no Unreal import.\n')
sc.render.filepath='//OLIVE-TREE-Hero.png';bpy.ops.wm.save_as_mainfile(filepath=str(O/'TREE-MASTER.blend'));print('OLIVE_CONVERSION_SAVED')
