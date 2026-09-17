import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory');O=R/'Asset Chest/01 John Originals/TREE-MASTER';O.mkdir(parents=True,exist_ok=True)
random.seed(130926)
bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.name='TREE-MASTER | ancient orchard tree';sc.unit_settings.system='METRIC'
cols={}
for n in ['01 Heartwood and limbs','02 Surface roots','03 Bark relief','04 Canopy leaves','05 Blossom','06 Orchard fruit','07 Understory','08 Planter','90 Studio','99 Reference']:
 c=bpy.data.collections.new(n);sc.collection.children.link(c);cols[n]=c
root=bpy.data.objects.new('TREE-MASTER | ground origin',None);sc.collection.objects.link(root)
def mesh(name,verts,faces,mat,col):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);cols[col].objects.link(ob);ob.parent=root
 for m in (mat if isinstance(mat,list) else [mat]):me.materials.append(m)
 for p in me.polygons:p.use_smooth=True
 return ob
def material(name,c,rough=.5,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal;return m
bark=material('Bark | weathered warm grey',(.20,.14,.082),.89)
n=bark.node_tree.nodes;l=bark.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=7;tex.inputs['Detail'].default_value=6;tex.inputs['Roughness'].default_value=.8
coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(4,4,.48);l.new(coord.outputs['Object'],mapping.inputs[0]);l.new(mapping.outputs[0],tex.inputs[0]);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.2;r.color_ramp.elements[0].color=(.038,.025,.013,1);r.color_ramp.elements[1].position=.8;r.color_ramp.elements[1].color=(.38,.29,.18,1);l.new(tex.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Base Color']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.42;bump.inputs['Distance'].default_value=.065;l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
ridge=material('Bark | raised grey ridges',(.27,.205,.135),.92);dark=material('Bark | crevice shadow',(.065,.042,.021),.94)
leaves=[]
for name,c in [('forest',(.055,.095,.012)),('olive',(.16,.22,.029)),('young',(.27,.34,.065)),('sage',(.105,.19,.042))]:
 m=material('Leaf | '+name,c,.43);p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Subsurface Weight'].default_value=.07;p.inputs['Subsurface Radius'].default_value=(.3,.7,.15);leaves.append(m)
petals=[material('Petal | ivory',(.84,.80,.66),.5),material('Petal | blush',(.77,.41,.42),.51)];pollen=material('Blossom | golden stamens',(.53,.28,.025),.65)
fruitm=[material('Apple | russet red',(.36,.055,.02),.28),material('Apple | soft gold',(.46,.31,.056),.33),material('Apple | rose blush',(.47,.135,.065),.3)]
for m in fruitm:
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Coat Weight'].default_value=.18
soil=material('Soil | cultivated earth',(.032,.023,.013),1);stone=material('Planter | warm limestone',(.35,.31,.235),.74);green=material('Planter | bottle green',(.027,.063,.047),.31,.52);brass=material('Planter | aged brass',(.43,.28,.09),.32,.78)
paths=[]
def catmull(points,steps=8):
 out=[]
 for i in range(len(points)-1):
  a=Vector(points[max(0,i-1)]);b=Vector(points[i]);c=Vector(points[i+1]);d=Vector(points[min(len(points)-1,i+2)])
  for j in range(steps):
   t=j/steps;out.append((2*b+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t)*.5)
 out.append(Vector(points[-1]));return out
def tube(name,points,r0,r1,col='01 Heartwood and limbs',segments=14,barkrelief=True):
 ps=catmull(points,7);vs=[];fs=[];frames=[]
 for i,c in enumerate(ps):
  t=i/(len(ps)-1);tangent=(ps[min(i+1,len(ps)-1)]-ps[max(i-1,0)]).normalized();u=tangent.cross(Vector((0,1,0)))
  if u.length<.05:u=tangent.cross(Vector((1,0,0)))
  u.normalize();v=tangent.cross(u).normalized();rr=r0*(1-t)**.85+r1*t;frames.append((c,u,v,rr))
  for j in range(segments):
   a=j*math.tau/segments;rad=rr*(1+.12*math.sin(5*a+t*9)+.045*math.sin(9*a-t*11));vs.append(c+(u*math.cos(a)+v*math.sin(a))*rad)
  if i:
   for j in range(segments):a=(i-1)*segments+j;b=(i-1)*segments+(j+1)%segments;fs.append((a,b,b+segments,a+segments))
 fs.append(tuple(reversed(range(segments))));fs.append(tuple((len(ps)-1)*segments+j for j in range(segments)))
 ob=mesh(name,vs,fs,bark,col)
 if barkrelief and r0>.18:paths.append(frames)
 return ps,frames
trunk=[(0,0,.40),(-.35,.12,1.6),(.15,.05,3.0),(.65,.1,4.2),(.3,.05,5.6),(-.15,.2,6.7)]
tube('Heartwood | sinuous central bole',trunk,1.28,.70,segments=44)
for k in range(3):
 pts=[]
 for j in range(12):
  t=j/11;a=k*math.tau/3+t*3.9;rad=.94-.29*t;pts.append((math.cos(a)*rad+.3*math.sin(t*4),math.sin(a)*rad, .44+6*t))
 tube('Trunk | interwoven buttress %02d'%k,pts,.57,.19,segments=24)
for k in range(11):
 a=k*math.tau/11+.11*random.random();reach=random.uniform(3.0,4.7);pts=[(math.cos(a)*.72,math.sin(a)*.72,2.3+random.random()),(math.cos(a+.15)*1.2,math.sin(a+.15)*1.2,1.35),(math.cos(a+.08)*2.0,math.sin(a+.08)*2,.68),(math.cos(a)*reach*.8,math.sin(a)*reach*.8,.49),(math.cos(a-.15)*reach,math.sin(a-.15)*reach,.43)]
 tube('Root | ancient buttress %02d'%k,pts,.48,.035,'02 Surface roots',20)
 for s in [-1,1]:
  p=Vector(pts[2]);end=Vector(pts[-1])+Vector((math.cos(a+s*.5),math.sin(a+s*.5),0))*.55;tube('Root | fine radial %02d %d'%(k,s),[p,(p+end)*.5+Vector((0,0,.08)),end],.13,.014,'02 Surface roots',9,False)
# Deliberately asymmetric leaders with low, sweeping arms and a broken crown.
arms=[([(0,0,3.6),(-1.3,0,5.1),(-3.0,.1,6.1),(-4.9,.1,7.1),(-6.3,.2,8.4)],.69), ([(.1,.2,4.5),(1.8,.3,5.7),(3.2,.4,7.1),(3.8,.7,9.6),(3.1,.9,11.3)],.72), ([(.3,0,5.2),(-.7,.1,7.1),(-1.8,.0,9.1),(-2.6,-.3,10.6),(-4.0,-.2,11.5)],.61), ([(0,.3,3.5),(.8,1.7,4.8),(2.7,3.0,6.3),(4.4,4.0,8.0)],.58), ([(0,0,5.1),(-.5,-1.6,6.6),(-1.6,-3.2,8.1),(-2.1,-4.9,9.2)],.52), ([(0,0,4.0),(1.6,-1.0,5.0),(3.3,-2.4,5.8),(5.4,-3.1,7.6)],.56), ([(0,.2,5.2),(-1.4,1.6,6.8),(-3.5,3.1,7.9),(-4.2,4.6,9.4)],.51), ([(.1,.1,5.7),(.8,1.8,7.8),(.4,2.9,10.0),(1.0,3.6,11.5)],.47)]
tips=[]
for ai,(points,rad) in enumerate(arms):
 ps,frames=tube('Limb | sculptural arm %02d'%ai,points,rad,.075,segments=24)
 for j in range(3,9):
  t=j/10;idx=int(t*(len(ps)-1));base=ps[idx];along=(ps[min(idx+2,len(ps)-1)]-ps[max(0,idx-2)]).normalized();az=math.atan2(base.y,base.x)+(1 if j%2 else -1)*random.uniform(.45,1.3);reach=random.uniform(1.1,2.0);end=base+Vector((math.cos(az)*reach,math.sin(az)*reach,random.uniform(.65,1.4)))
  mid=base+(end-base)*.50+Vector((0,0,-.1));tube('Branch | %02d.%02d'%(ai,j),[base,mid,end],rad*(1-t)*.45+.035,.018,segments=10,barkrelief=False)
  for q in range(4):
   az2=az+(q-1.5)*.75;leafend=end+Vector((math.cos(az2)*random.uniform(.55,1.05),math.sin(az2)*random.uniform(.55,1.05),random.uniform(-.1,.65)));st=end-(end-mid)*random.uniform(.0,.5);tube('Twig | %02d.%02d.%02d'%(ai,j,q),[st,(st+leafend)*.5+Vector((0,0,.12)),leafend],.025,.003,segments=6,barkrelief=False);tips.append((leafend,az2))
 tips.append((ps[-1],math.atan2(ps[-1].y,ps[-1].x)))
print('STRUCTURE',len(paths),len(tips),flush=True)
# Raised broken bark ribbons follow the trunk's actual local frames.
rv=[];rf=[]
for frames in paths:
 count=max(8,int(frames[0][3]*42))
 for k in range(count):
  a=k*math.tau/count+random.uniform(-.06,.06);start=random.randrange(0,3)
  for j in range(start,len(frames)-3,random.choice([3,4,5])):
   width=random.uniform(.018,.044);length=random.randint(2,4);base=len(rv)
   for jj in range(j,min(j+length,len(frames))):
    c,u,v,rad=frames[jj];t=jj/(len(frames)-1);aa=a+.16*math.sin(t*9+k);radius=rad*(1+.12*math.sin(5*aa+t*9)+.045*math.sin(9*aa-t*11))
    for offset,h in [(-width,0),(0,random.uniform(.018,.052)),(width,0)]:rv.append(c+(u*math.cos(aa+offset)+v*math.sin(aa+offset))*(radius+h))
    if jj>j:
     m=base+(jj-j)*3;rf.extend([(m-3,m-2,m+1,m),(m-2,m-1,m+2,m+1)])
mesh('Bark | layered longitudinal relief',rv,rf,ridge,'03 Bark relief')
# Leaves are folded, pointed geometry, distributed along fine sprays rather than opaque canopy spheres.
lv=[];lf=[];lm=[];fv=[];ff=[];fm=[];av=[];af=[];am=[]
def leaf(center,direction,length,width,verts,faces,indices,mi):
 d=Vector(direction).normalized();side=d.cross(Vector((0,0,1)))
 if side.length<.1:side=d.cross(Vector((0,1,0)))
 side.normalize();normal=side.cross(d).normalized();c=Vector(center);b=len(verts)
 for t,w,h in [(0,0,0),(.25,.72,.06),(.55,1,.09),(.82,.57,.04),(1,0,-.04)]:
  for s in [-1,0,1]:verts.append(c+d*(length*t)+side*(width*w*s)+normal*(length*(h-(.08 if s else 0)*w)))
 for row in range(4):
  for col in range(2):faces.append((b+row*3+col,b+row*3+col+1,b+(row+1)*3+col+1,b+(row+1)*3+col));indices.append(mi)
def flower(c,size=.12):
 c=Vector(c);angle=random.random()*math.tau;normal=Vector((random.uniform(-.5,.5),random.uniform(-.5,.5),1)).normalized();u=normal.cross(Vector((0,1,0))).normalized();v=normal.cross(u)
 for j in range(5):
  a=angle+j*math.tau/5;direction=u*math.cos(a)+v*math.sin(a);side=normal.cross(direction);b=len(fv)
  fv.extend([c,c+direction*size*.55+side*size*.37+normal*.015,c+direction*size+side*size*.20,c+direction*size*1.12,c+direction*size-side*size*.20,c+direction*size*.55-side*size*.37+normal*.015,c+direction*size*.57+normal*.026]);ff.extend([(b,b+1,b+6),(b+1,b+2,b+6),(b+2,b+3,b+6),(b+3,b+4,b+6),(b+4,b+5,b+6),(b+5,b,b+6)]);fm.extend([0 if random.random()<.84 else 1]*6)
 b=len(fv);fv.extend([c+normal*.025,c+u*.024+normal*.03,c+v*.024+normal*.03,c-u*.024+normal*.03,c-v*.024+normal*.03]);ff.extend([(b,b+1,b+2),(b,b+2,b+3),(b,b+3,b+4),(b,b+4,b+1)]);fm.extend([2]*4)
def apple(c,size,mi):
 c=Vector(c);b=len(av);rings=12;seg=16
 for i in range(rings+1):
  phi=math.pi*i/rings
  for j in range(seg):
   a=j*math.tau/seg;r=size*math.sin(phi)*(1+.045*math.cos(5*a));z=size*math.cos(phi)*.92
   if i<3:z-=size*.13*(1-i/3)
   av.append(c+Vector((r*math.cos(a),r*math.sin(a),z)))
 for i in range(rings):
  for j in range(seg):af.append((b+i*seg+j,b+i*seg+(j+1)%seg,b+(i+1)*seg+(j+1)%seg,b+(i+1)*seg+j));am.append(mi)
 tube('Fruit | hanging stem',[(c.x,c.y,c.z+size*.75),(c.x+.025,c.y,c.z+size*1.5)],.009,.006,'06 Orchard fruit',5,False)
for ti,(center,az) in enumerate(tips):
 for k in range(100):
  ang=random.random()*math.tau;r=math.sqrt(random.random())*random.uniform(.5,1.0);c=center+Vector((math.cos(ang)*r,math.sin(ang)*r,random.gauss(0,.27)));d=Vector((math.cos(ang),math.sin(ang),random.uniform(-.4,.65)));leaf(c,d,random.uniform(.19,.34),random.uniform(.055,.105),lv,lf,lm,random.choices(range(4),[4,4,1,2])[0])
 if ti%2==0:
  for j in range(random.randint(3,6)):flower(center+Vector((random.uniform(-.7,.7),random.uniform(-.7,.7),random.uniform(-.22,.35))),random.uniform(.065,.105))
 if ti%3==0:apple(center+Vector((random.uniform(-.3,.3),random.uniform(-.3,.3),-.43)),random.uniform(.12,.175),random.randrange(3))
ob=mesh('Canopy | individually folded leaves',lv,lf,leaves,'04 Canopy leaves')
for p,i in zip(ob.data.polygons,lm):p.material_index=i
ob=mesh('Blossoms | five petal orchard flowers',fv,ff,petals+[pollen],'05 Blossom')
for p,i in zip(ob.data.polygons,fm):p.material_index=i
ob=mesh('Fruit | hanging apples',av,af,fruitm,'06 Orchard fruit')
for p,i in zip(ob.data.polygons,am):p.material_index=i
print('CANOPY',len(lv),len(av),flush=True)
# Ivy follows selected trunk channels, with fine vines and alternating leaves.
iv=[];iff=[];imi=[]
for k in range(8):
 a=k*math.tau/8;pts=[]
 for j in range(48):
  t=j/47;aa=a+t*2.4;rad=1.10-.27*t;c=Vector((math.cos(aa)*rad+.3*math.sin(t*4),math.sin(aa)*rad, .55+5.8*t));pts.append(c)
  for s in [-1,1]:leaf(c,(math.cos(aa+s*.55),math.sin(aa+s*.55),random.uniform(-.4,.2)),random.uniform(.17,.25),.075,iv,iff,imi,k%4)
 tube('Ivy | climbing stem %02d'%k,pts,.014,.005,'07 Understory',5,False)
meshob=mesh('Ivy | climbing leaves',iv,iff,leaves,'07 Understory')
for p,i in zip(meshob.data.polygons,imi):p.material_index=i
uv=[];uf=[];um=[]
for k in range(135):
 a=random.random()*math.tau;r=random.uniform(1.5,4.9);c=Vector((r*math.cos(a),r*math.sin(a),.51))
 for j in range(random.randint(5,9)):
  angle=random.random()*math.tau;length=random.uniform(.3,.8);d=Vector((math.cos(angle),math.sin(angle),random.uniform(.3,.7)))
  if k%3:
   leaf(c,d,length,.08,uv,uf,um,random.randrange(4))
  else:
   for s in range(9):
    t=s/10;base=c+d*length*t+Vector((0,0,.18*math.sin(t*math.pi)))
    for lr in [-1,1]:leaf(base,(-math.sin(angle)*lr,math.cos(angle)*lr,.08),length*.26*(1-t)+.03,.025,uv,uf,um,1)
ob=mesh('Understory | fern fronds and broad leaves',uv,uf,leaves,'07 Understory')
for p,i in zip(ob.data.polygons,um):p.material_index=i
def ringmesh(name,ri,ro,z,h,mat,col='08 Planter',segments=96):
 vs=[];fs=[]
 for radius,zz in [(ri,z),(ro,z),(ro,z+h),(ri,z+h)]:
  vs.extend([(radius*math.cos(j*math.tau/segments),radius*math.sin(j*math.tau/segments),zz) for j in range(segments)])
 for i in range(4):
  for j in range(segments):fs.append((i*segments+j,i*segments+(j+1)%segments,((i+1)%4)*segments+(j+1)%segments,((i+1)%4)*segments+j))
 return mesh(name,vs,fs,mat,col)
ringmesh('Planter | limestone perimeter',4.96,5.28,0,.43,stone)
ringmesh('Planter | dark inset band',5.279,5.291,.12,.18,green)
for z in [.07,.115,.30,.39]:ringmesh('Planter | brass moulding',5.29,5.315,z,.022,brass)
ringmesh('Planter | dressed capstone',4.88,5.37,.43,.10,stone)
ringmesh('Soil | planted bed',0,4.97,.10,.31,soil)
for k in range(16):
 a=k*math.tau/16;rad=5.305;tube('Planter | brass pilaster %02d'%k,[(rad*math.cos(a),rad*math.sin(a),.1),(rad*math.cos(a),rad*math.sin(a),.41)],.022,.022,'08 Planter',6,False)
 # Assign brass to pilasters made with the organic tube helper.
 ob=cols['08 Planter'].objects[-1];ob.data.materials.clear();ob.data.materials.append(brass)
stage=material('Studio | warm neutral',(.16,.18,.16),.8)
mesh('Studio | ground',[(-200,-200,-.04),(200,-200,-.04),(200,200,-.04),(-200,200,-.04)],[(0,1,2,3)],stage,'90 Studio')
world=bpy.data.worlds.new('Studio daylight');world.use_nodes=True;world.node_tree.nodes.get('Background').inputs[0].default_value=(.62,.73,.85,1);world.node_tree.nodes.get('Background').inputs[1].default_value=.35;sc.world=world
def area(name,pos,power,size,color,target):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(name,d);cols['90 Studio'].objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Studio | golden canopy light',(-8,3,18),5200,8,(1,.79,.49),(0,0,5));area('Studio | soft front light',(1,-12,9),3300,10,(.83,.90,1),(0,0,5));area('Studio | rim',(8,7,11),4500,7,(1,.86,.61),(0,0,5))
d=bpy.data.lights.new('Studio | sunlight','SUN');d.energy=2.2;d.angle=.12;o=bpy.data.objects.new(d.name,d);cols['90 Studio'].objects.link(o);o.rotation_euler=(.4,-.55,-.6)
def camera(name,pos,target,lens):
 d=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,d);cols['90 Studio'].objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_end=500;return ob
sc.camera=camera('CAM | Hero',(18,-27,12),(0,0,6),47);camera('CAM | Root detail',(7,-10,5.0),(0,0,2.6),53);camera('CAM | Rear',(-21,25,13),(0,0,6),48)
ref=bpy.data.images.load('C:/Users/ASUS TUF/Downloads/tree.png');ref.pack();ob=bpy.data.objects.new('REFERENCE | John supplied tree',None);cols['99 Reference'].objects.link(ob);ob.empty_display_type='IMAGE';ob.data=ref;ob.empty_display_size=12;ob.location=(-16,3,6);ob.rotation_euler=(math.pi/2,0,0);ob.hide_render=True
sc.render.engine='CYCLES';sc.cycles.samples=48;sc.cycles.use_denoising=True;sc.cycles.use_adaptive_sampling=True;sc.render.resolution_x=1400;sc.render.resolution_y=1400;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.view_settings.view_transform='AgX'
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type!='CPU'
 sc.cycles.device='GPU'
except:sc.cycles.device='CPU'
bpy.ops.object.select_all(action='DESELECT');root.select_set(True);bpy.context.view_layer.objects.active=root
for screen in bpy.data.screens:
 for ar in screen.areas:
  if ar.type=='VIEW_3D':ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.shading.type='MATERIAL';ar.spaces.active.overlay.show_overlays=False
text=bpy.data.texts.new('START HERE | TREE-MASTER');text.write('TREE-MASTER — large dome centrepiece study\nMetres. Ground origin (0,0,0). Separate trunk, roots, bark, leaves, blossom, fruit, understorey and planter collections. Studio and packed user reference are authoring only.\nThis is an editable first sculptural interpretation for refinement in Blender. No Unreal import, gameplay, LOD, wind or collision implementation. No claim that the reference design is perfectly matched.\n')
sc.render.filepath='//TREE-MASTER-Hero.png';bpy.ops.wm.save_as_mainfile(filepath=str(O/'TREE-MASTER.blend'))
for name,cam in [('Hero','CAM | Hero'),('Roots','CAM | Root detail'),('Rear','CAM | Rear')]:
 sc.camera=bpy.data.objects[cam];sc.render.filepath=str(O/('TREE-MASTER-'+name+'.png'));bpy.ops.render.render(write_still=True);print('RENDERED',name,flush=True)
asset=[o for o in sc.objects if o.type=='MESH' and any(c.name[:2] in ['01','02','03','04','05','06','07','08'] for c in o.users_collection)];tri=0
for ob in asset:ob.data.calc_loop_triangles();tri+=len(ob.data.loop_triangles)
(O/'MasterReport.json').write_text(json.dumps({'version':'0.1 Blender review','blender':bpy.app.version_string,'model_objects':len(asset),'triangles':tri,'canopy_sprays':len(tips),'leaf_count':len(lv)//15,'unreal_imported':False},indent=2));print('TREE_MASTER_COMPLETE',tri,flush=True)
