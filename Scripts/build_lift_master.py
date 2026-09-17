"""Reference-led, editable lift master. Run in an isolated Blender process only."""
import bpy, math, json
from mathutils import Vector
from pathlib import Path
ROOT=Path('C:/Users/ASUS TUF/Documents/1 conservatory');OUT=ROOT/'SourceAssets/LiftMaster';OUT.mkdir(exist_ok=True)
assert not bpy.data.filepath, 'Use a new isolated Blender process'
scene=bpy.context.scene;scene.name='MASTER | Conservatory service lift'
for ob in list(scene.objects):bpy.data.objects.remove(ob,do_unlink=True)
scene.unit_settings.system='METRIC';scene.unit_settings.length_unit='METERS'
cols={}
for name in ['01 Structure','02 Columns and capitals','03 Cast ornament','04 Glazing','05 Cabin interior','06 Controls and signage','07 Crown','08 Game anchors','90 Studio','99 Reference']:
 c=bpy.data.collections.new(name);scene.collection.children.link(c);cols[name]=c
root=bpy.data.objects.new('LIFT_MASTER | floor origin | front -Y',None);cols['08 Game anchors'].objects.link(root)
root['asset']='9th Kingdom | Conservatory Service Lift';root['source_reference']='lift1-reference.png';root['status']='Editable high detail authoring master; Unreal integration pending'
root['opening_width_m']=1.58;root['opening_height_m']=2.70;root['units']='meters';root['front']='-Y';root['floor_datum_m']=0.08
def put(o,group,mat=None):
 for c in list(o.users_collection):c.objects.unlink(o)
 cols[group].objects.link(o)
 if group not in ['90 Studio','99 Reference']:o.parent=root
 if mat:o.data.materials.append(mat)
 return o
def material(name,color,metal=0,rough=.35,noise=False):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
 if noise:
  tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=90;tex.inputs['Detail'].default_value=3
  ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.18;ramp.color_ramp.elements[0].color=(*(v*.72 for v in color),1);ramp.color_ramp.elements[1].position=.82;ramp.color_ramp.elements[1].color=(*color,1);l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
  rem=n.new('ShaderNodeMapRange');rem.inputs['From Min'].default_value=0;rem.inputs['From Max'].default_value=1;rem.inputs['To Min'].default_value=rough*.8;rem.inputs['To Max'].default_value=rough*1.25;l.new(tex.outputs['Fac'],rem.inputs[0]);l.new(rem.outputs[0],p.inputs['Roughness'])
 return m
green=material('01 | Deep bottle-green enamel',(.035,.074,.060),.68,.30,True)
brass=material('02 | Aged warm brass',(.46,.30,.105),.83,.28,True)
edge=material('03 | Polished brass beads',(.64,.44,.19),.86,.23)
patina=material('04 | Dark bronze recesses',(.075,.063,.033),.78,.39)
ivory=material('05 | Warm ivory enamel',(.67,.63,.49),.17,.32,True)
rubber=material('06 | Glazing gaskets',(.017,.022,.019),0,.68)
glass=material('07 | Clear architectural glass',(.89,.96,.94),0,.07);gp=glass.node_tree.nodes.get('Principled BSDF');gp.inputs['Transmission Weight'].default_value=1;gp.inputs['IOR'].default_value=1.46
stone=material('08 | Honed limestone cabin floor',(.59,.55,.43),0,.3)
n=stone.node_tree.nodes;l=stone.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=4;tex.inputs['Detail'].default_value=5;tex.inputs['Roughness'].default_value=.72
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.29,.28,.23,1);ramp.color_ramp.elements[0].position=.16;ramp.color_ramp.elements[1].color=(.77,.73,.60,1);ramp.color_ramp.elements[1].position=.78;l.new(tex.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.007;l.new(tex.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
lamp=material('09 | Opal luminaire',(.92,.81,.55),0,.22);lp=lamp.node_tree.nodes.get('Principled BSDF');lp.inputs['Emission Color'].default_value=(1,.76,.37,1);lp.inputs['Emission Strength'].default_value=2.7
def mesh(name,verts,faces,mat,group):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);cols[group].objects.link(o);o.parent=root
 if mat:me.materials.append(mat)
 return o
def bevel(o,w=.005,seg=3):
 mod=o.modifiers.new('Machined edge radius','BEVEL');mod.width=w;mod.segments=seg
 mod=o.modifiers.new('Weighted corner normals','WEIGHTED_NORMAL');mod.keep_sharp=True
 return o
def box(name,p,s,mat=green,group='01 Structure',b=.006):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=bpy.context.object;o.name=name;o.dimensions=s;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);put(o,group,mat)
 if b:bevel(o,b)
 return o
def curve(name,points,r=.012,mat=brass,group='03 Cast ornament',cyclic=False,radii=None):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=16;cu.bevel_depth=r;cu.bevel_resolution=3;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for i,(p,v) in enumerate(zip(sp.points,points)):p.co=(*v,1);p.radius=radii[i] if radii else 1
 sp.use_cyclic_u=cyclic;o=bpy.data.objects.new(name,cu);cols[group].objects.link(o);o.parent=root;cu.materials.append(mat);return o
def rod(name,a,b,r=.015,mat=brass,group='03 Cast ornament'):return curve(name,[a,b],r,mat,group)
def ring(name,c,r,tube=.01,plane='XZ',mat=brass,group='03 Cast ornament',n=64):
 pts=[]
 for i in range(n):
  a=i*math.tau/n
  pts.append((c[0]+r*math.cos(a),c[1],c[2]+r*math.sin(a)) if plane=='XZ' else ((c[0],c[1]+r*math.cos(a),c[2]+r*math.sin(a)) if plane=='YZ' else (c[0]+r*math.cos(a),c[1]+r*math.sin(a),c[2])))
 return curve(name,pts,tube,mat,group,True)
def lathe(name,xy,profile,mat=brass,group='02 Columns and capitals',n=64,flutes=0):
 vs=[]
 for z,r in profile:
  for i in range(n):
   a=i*math.tau/n;rr=r*(1+.045*math.cos(a*flutes)) if flutes else r;vs.append((xy[0]+rr*math.cos(a),xy[1]+rr*math.sin(a),z))
 fs=[]
 for j in range(len(profile)-1):
  for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i))
 fs.extend([tuple(reversed(range(n))),tuple((len(profile)-1)*n+i for i in range(n))]);o=mesh(name,vs,fs,mat,group)
 for f in o.data.polygons:f.use_smooth=True
 return o
def sphere(name,p,r,mat,group='03 Cast ornament',scale=None):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=r,location=p);o=bpy.context.object;o.name=name
 if scale:o.scale=scale
 put(o,group,mat)
 for f in o.data.polygons:f.use_smooth=True
 return o
def frame(name,x0,x1,y,z0,z1,mat=brass,r=.008,group='05 Cabin interior'):
 return curve(name,[(x0,y,z0),(x1,y,z0),(x1,y,z1),(x0,y,z1)],r,mat,group,True)

# Cabin footing and flush threshold. Top floor datum is +0.08m.
box('Foundation | bevelled bronze shoe',(0,0,-.018),(2.68,2.44,.115),patina,b=.015)
box('Foundation | perimeter brass nosing',(0,0,.034),(2.62,2.39,.045),brass,b=.01)
box('Cabin | limestone floor',(0,0,.062),(2.50,2.27,.036),stone,b=.008)
for inset,width in [(.08,.018),(.13,.007)]:
 x=1.25-inset;y=1.135-inset;curve('Floor | double border',[(x,y,.082),(-x,y,.082),(-x,-y,.082),(x,-y,.082)],width,brass,'05 Cabin interior',True)
for rr in [.285,.312,.336]:ring('Floor | compass medallion',(0,-.35,.084),rr,.0045,'XY',brass,'05 Cabin interior')
for i in range(8):
 a=i*math.tau/8;c=Vector((0,-.35,.085));rad=Vector((math.cos(a),math.sin(a),0));tan=Vector((-math.sin(a),math.cos(a),0));v=[c+rad*.275,c+rad*.33+tan*.017,c+rad*.38,c+rad*.33-tan*.017];mesh('Floor | compass petal',v,[(0,1,2,3)],brass,'05 Cabin interior')
box('Threshold | solid brass sill',(0,-1.15,.087),(1.63,.11,.045),edge,b=.005)
for x in [-.81,.81]:box('Door jamb | substantial cast upright',(x,-1.085,1.435),(.105,.16,2.70),green,b=.01)
for x in [-.873,-.762,.762,.873]:box('Door jamb | brass reveal',(x,-1.175,1.435),(.014,.017,2.69),edge,b=.002)
box('Door opening | lintel',(0,-1.09,2.805),(1.82,.17,.13),green)
for z in [2.742,2.86]:box('Lintel | brass bead',(0,-1.185,z),(1.83,.017,.018),edge,b=.004)

# Four articulated fluted columns with stepped plinths and turned capitals.
for x in [-1.18,1.18]:
 for y in [-1.04,1.04]:
  tag=('L' if x<0 else 'R')+(' front' if y<0 else ' rear')
  for z,s,h,m in [(.13,.30,.17,green),(.055,.33,.026,brass),(.23,.31,.035,brass),(.27,.255,.04,patina)]:box(tag+' | octagonal base block',(x,y,z),(s,s,h),m,'02 Columns and capitals',.018)
  lathe(tag+' | moulded foot',(x,y),[(.285,.13),(.30,.14),(.32,.14),(.335,.117),(.36,.106),(.375,.111),(.39,.111),(.405,.087),(.46,.081)],brass)
  lathe(tag+' | fluted enamel shaft',(x,y),[(.405,.083),(.46,.079),(2.97,.076),(3.02,.085)],green,n=96,flutes=16)
  for i in range(16):
   a=math.tau*i/16;rr=.081;rod(tag+' | fine flute arris',(x+rr*math.cos(a),y+rr*math.sin(a),.465),(x+.078*math.cos(a),y+.078*math.sin(a),2.96),.0028,brass,'02 Columns and capitals')
  for z in [.42,.47,2.94,2.985]:lathe(tag+' | shaft collar',(x,y),[(z,.086),(z+.008,.091),(z+.018,.091),(z+.025,.082)],brass)
  lathe(tag+' | leaf capital bell',(x,y),[(3.01,.079),(3.035,.095),(3.08,.101),(3.16,.117),(3.185,.135),(3.215,.135),(3.228,.111),(3.25,.13),(3.28,.13)],green)
  for z,r in [(3.045,.099),(3.19,.137),(3.225,.128),(3.28,.135)]:ring(tag+' | capital bead',(x,y,z),r,.01,'XY',edge,'02 Columns and capitals')
  lathe(tag+' | finial pedestal',(x,y),[(3.28,.12),(3.37,.11),(3.395,.145),(3.42,.145),(3.435,.112),(3.46,.08),(3.49,.06)],brass)
  lathe(tag+' | acorn finial',(x,y),[(3.47,.042),(3.5,.034),(3.54,.056),(3.58,.071),(3.63,.058),(3.68,.031),(3.735,.001)],brass,n=48)
  for i in range(8):
   a=i*math.tau/8;curve(tag+' | capital leaf vein',[(x+r*math.cos(a),y+r*math.sin(a),z) for z,r in [(3.045,.099),(3.08,.116),(3.13,.137),(3.18,.139)]],.005,edge)

# Perimeter entablature, individually layered rails rather than a solid roof box.
for z,h,span,m in [(3.16,.035,2.38,brass),(3.23,.105,2.36,green),(3.29,.022,2.43,edge),(3.325,.044,2.48,green),(3.35,.015,2.5,brass)]:
 for y in [-1.045,1.045]:box('Cornice | front/rear moulding',(0,y,z),(span,.125,h),m,b=.004)
 for x in [-1.18,1.18]:box('Cornice | side moulding',(x,0,z),(.125,2.09,h),m,b=.004)
for x in [-1.015,1.015]:
 box('Entrance | enamel ornament stile',(x,-1.08,1.56),(.235,.09,2.57),green)
 for xx in [x-.112,x+.112]:rod('Stile | outer brass bead',(xx,-1.132,.29),(xx,-1.132,2.96),.008,edge)
box('Rear | enclosure panel',(0,1.057,1.64),(2.18,.085,3.12),green)
box('Rear interior | ivory upper panel',(0,1.004,2.01),(2.03,.025,2.13),ivory,'05 Cabin interior')
box('Rear interior | green dado panel',(0,.993,.515),(2.03,.042,.85),green,'05 Cabin interior')
for y in [.970,1.109]:
 for bounds in [(-.95,.95,.16,.89),(-.95,.95,1.03,3.025)]:
  frame('Rear | inset panel moulding',bounds[0],bounds[1],y,bounds[2],bounds[3],brass,.012)
  frame('Rear | inner fine panel bead',bounds[0]+.036,bounds[1]-.036,y-.007,bounds[2]+.036,bounds[3]-.036,edge,.004)
for x in [-1.105,1.105]:
 for z in [.15,.49,.97,3.09]:box('Side | framed horizontal rail',(x,0,z),(.075,2.08,.055),green)
 for y in [-.95,0,.95]:box('Side | glazing mullion',(x,y,1.82),(.066,.045,2.60),green)
 for yy in [-.95,.95]:rod('Interior | handrail standoff',(x,yy,.96),(x-math.copysign(.08,x),yy,.96),.025,brass,'05 Cabin interior')
 rod('Interior | polished side handrail',(x-math.copysign(.08,x),-.95,.96),(x-math.copysign(.08,x),.95,.96),.022,edge,'05 Cabin interior')
 for ya,yb in [(-.927,-.027),(.027,.927)]:
  box('Side | individual laminated glass pane',(x,(ya+yb)/2,1.81),(.008,yb-ya,2.53),glass,'04 Glazing',.001)
  for side in [-1,1]:
   xx=x+side*.035;curve('Glazing | brass glazing bead',[(xx,ya,.55),(xx,yb,.55),(xx,yb,3.07),(xx,ya,3.07)],.007,brass,'04 Glazing',True)
 for ya in [-.53,.53]:
  box('Side | lower enamel panel',(x,ya,.31),(.075,.91,.31),green)

# Flush control fascia with separate rings, buttons and fasteners.
box('Controls | brass backplate',(0,.953,1.64),(.205,.032,.49),brass,'06 Controls and signage',.018)
box('Controls | dark inset',(0,.929,1.64),(.164,.017,.447),patina,'06 Controls and signage',.012)
for z in [1.54,1.77]:
 ring('Controls | button bezel',(0,.914,z),.031,.006,'XZ',edge,'06 Controls and signage')
 sphere('Controls | separate pushbutton',(0,.912,z),.023,lamp if z>1.7 else green,'06 Controls and signage',(1,.25,1))
for x in [-.072,.072]:
 for z in [1.44,1.84]:
  sphere('Controls | countersunk screw',(x,.916,z),.006,edge,'06 Controls and signage',(1,.3,1));rod('Controls | screw slot',(x-.003,.913,z),(x+.003,.913,z),.0009,patina,'06 Controls and signage')
fontpath=Path('C:/Windows/Fonts/times.ttf');font=bpy.data.fonts.load(str(fontpath)) if fontpath.exists() else None
def text(name,body,loc,size,mat=brass):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.align_x='CENTER';cu.align_y='CENTER';cu.size=size;cu.extrude=.00065;cu.bevel_depth=.0003
 if font:cu.font=font
 o=bpy.data.objects.new(name,cu);cols['06 Controls and signage'].objects.link(o);o.parent=root;o.location=loc;o.rotation_euler=(math.pi/2,0,0);cu.materials.append(mat);return o
text('Cabin | editable service inscription','SERVICE LIFT',(0,.970,2.46),.108)
text('Cabin | editable department inscription','HABITAT DEPT.',(0,.970,2.335),.064)
text('Control legend | upper','01',(0,.916,1.695),.025,ivory);text('Control legend | lower','00',(0,.916,1.468),.024,ivory)
rod('Cabin | inscription divider',(-.28,.964,2.23),(.28,.964,2.23),.002,brass,'06 Controls and signage')
for x in [-.10,0,.10]:ring('Cabin | small inscription flourish',(x,.96,2.21),.019,.003,'XZ',brass,'06 Controls and signage')
box('Cabin | ivory ceiling',(0,0,3.09),(2.14,2.01,.05),ivory,'05 Cabin interior')
lathe('Light | brass ceiling rose',(0,0),[(2.985,.21),(3.018,.24),(3.045,.24),(3.067,.19)],brass,'05 Cabin interior')
lathe('Light | opal shallow bowl',(0,0),[(2.905,.001),(2.911,.07),(2.925,.13),(2.947,.175),(2.98,.19),(2.99,.19)],lamp,'05 Cabin interior')
ring('Light | rim',(0,0,2.987),.19,.009,'XY',edge,'05 Cabin interior')

# Glazed low dome crown, continuous separate ribs with individual closed pane solids.
RX=1.19;RY=1.055;Z=3.365;H=.80
for k in range(16):
 a=math.tau*k/16
 curve('Crown | brass rib %02d'%k,[(RX*math.cos(t)*math.cos(a),RY*math.cos(t)*math.sin(a),Z+H*math.sin(t)) for t in [i*math.pi/2/36 for i in range(37)]],.015,brass,'07 Crown')
 aa=a+.014;bb=a+math.tau/16-.014;vs=[];fs=[]
 for j in range(17):
  t=.012+(math.pi/2-.10)*j/16
  for i in range(5):
   ang=aa+(bb-aa)*i/4;vs.append((RX*math.cos(t)*math.cos(ang),RY*math.cos(t)*math.sin(ang),Z+H*math.sin(t)))
 for j in range(16):
  for i in range(4):n=j*5+i;fs.append((n,n+1,n+6,n+5))
 ob=mesh('Crown | glass gore %02d'%k,vs,fs,glass,'04 Glazing');sol=ob.modifiers.new('4 mm crown glazing','SOLIDIFY');sol.thickness=.004
 for p in ob.data.polygons:p.use_smooth=True
curve('Crown | elliptical perimeter bead',[(RX*math.cos(a),RY*math.sin(a),Z) for a in [i*math.tau/128 for i in range(128)]],.021,edge,'07 Crown',True)
lathe('Crown | central turned spire',(0,0),[(4.10,.08),(4.14,.11),(4.17,.11),(4.19,.065),(4.23,.065),(4.25,.09),(4.28,.09),(4.30,.055),(4.34,.038),(4.39,.045),(4.43,.075),(4.48,.067),(4.53,.036),(4.59,.02),(4.70,.001)],brass,'07 Crown')
ring('Crown | front crest outer',(0,-.92,3.735),.24,.013,'XZ',brass,'07 Crown')
ring('Crown | front crest inner',(0,-.926,3.735),.214,.006,'XZ',edge,'07 Crown')
rod('Crown | crest stem',(0,-.92,3.37),(0,-.92,3.49),.013,brass,'07 Crown')
ring('Crown | crest foot',(0,-.93,3.405),.040,.009,'XZ',brass,'07 Crown')

# Scrolls are tapered cast ribbons, with rolled edges and separately modelled leaves.
def ribbon(name,pts,width=.026,depth=.009):
 vs=[];L=len(pts)
 for i,p in enumerate(pts):
  v=Vector(p);d=Vector(pts[min(i+1,L-1)])-Vector(pts[max(i-1,0)]);side=Vector((-d.z,0,d.x)).normalized();w=width*(.24+.76*(1-i/(L-1)))
  vs.extend([v+side*w/2+Vector((0,-depth/2,0)),v-side*w/2+Vector((0,-depth/2,0)),v+side*w/2+Vector((0,depth/2,0)),v-side*w/2+Vector((0,depth/2,0))])
 fs=[]
 for i in range(L-1):
  a=i*4;b=a+4;fs.extend([(a,b,b+1,a+1),(a+2,a+3,b+3,b+2),(a,a+2,b+2,b),(a+1,b+1,b+3,a+3)])
 fs.extend([(0,1,3,2),(4*(L-1),4*(L-1)+2,4*(L-1)+3,4*(L-1)+1)]);fs=[tuple(reversed(f)) for f in fs];o=mesh(name,vs,fs,brass,'03 Cast ornament');bevel(o,.002,2);return o
def scroll(name,cx,y,cz,r,turn=1.3,flip=1,angle=0):
 pts=[]
 for i in range(100):
  t=i/99;a=angle+turn*math.tau*t;rr=r*(1-.91*t);pts.append((cx+flip*rr*math.cos(a),y,cz+rr*math.sin(a)))
 return ribbon(name,pts,.032 if r>.15 else .021)
def leaf(name,base,tip,width=.07):
 a=Vector(base);b=Vector(tip);d=b-a;side=Vector((-d.z,0,d.x)).normalized();vs=[]
 for i in range(13):
  t=i/12;mid=a+d*t+Vector((0,-math.sin(math.pi*t)*.016,0));w=width*math.sin(math.pi*t)**.8*(1-.25*t)
  vs.extend([mid-side*w/2,mid+Vector((0,-.012*math.sin(math.pi*t),0)),mid+side*w/2])
 fs=[]
 for i in range(12):
  for j in range(2):n=i*3+j;fs.append((n,n+3,n+4,n+1))
 o=mesh(name,vs,fs,brass,'03 Cast ornament');m=o.modifiers.new('Cast leaf thickness','SOLIDIFY');m.thickness=.005;bevel(o,.002,2)
 curve(name+' | vein',[a+d*(i/20)+Vector((0,-.029*math.sin(math.pi*i/20),0)) for i in range(21)],.0025,edge)
# Arched tympanum in front of the lintel; open below, enamel behind spandrels.
for side in [-1,1]:
 # broad arched border and green decorative spandrel panels
 pts=[(side*(.79+.30*i/20),-1.09,2.89+.24*i/20) for i in range(21)]
 scroll('Front | large spandrel volute',side*.995,-1.157,3.015,.15,1.22,side,math.pi/2)
 scroll('Front | rising tendril',side*.80,-1.161,3.065,.11,1.15,-side,math.pi/2)
 leaf('Front | acanthus spandrel',(side*.76,-1.167,2.95),(side*.58,-1.167,3.18),.085)
 for cz,r in [(.41,.09),(.67,.085),(.92,.075),(2.56,.09),(2.81,.105)]:
  scroll('Entrance stile | scroll',side*1.015,-1.15,cz,r,1.2,side,math.pi/2)
 leaf('Entrance stile | terminal leaf',(side*1.015,-1.15,1.02),(side*.96,-1.15,1.22),.055)
 for z in [1.39,2.37]:
  ring('Stile | hanging ornament', (side*1.015,-1.153,z),.096,.009)
  ring('Stile | inner ornament', (side*1.015,-1.155,z),.077,.004,mat=edge)
  ring('Stile | suspension eye',(side*1.015,-1.153,z+.135),.024,.006)
 rod('Stile | slender stem',(side*1.015,-1.15,1.49),(side*1.015,-1.15,2.27),.008)
 scroll('Crown | lower corner curl',side*.93,-1.07,3.48,.14,1.18,side,math.pi)
 leaf('Crown | sweeping leaf',(side*.79,-1.07,3.36),(side*.58,-1.07,3.50),.066)
curve('Front | arch outer bead',[(.855*math.cos(a),-1.198,2.77+.405*math.sin(a)) for a in [i*math.pi/64 for i in range(65)]],.014,edge)
curve('Front | arch inner bead',[(.817*math.cos(a),-1.199,2.775+.367*math.sin(a)) for a in [i*math.pi/64 for i in range(65)]],.007,brass)
ring('Front | transom medallion',(0,-1.217,2.985),.157,.012)
ring('Front | transom inner medallion',(0,-1.222,2.985),.135,.004,mat=edge)
rod('Front | medallion pendant',(0,-1.213,3.14),(0,-1.213,3.28),.008)
for y in [-1.12,1.12]:
 sphere('Cornice | central cast rosette',(0,y,3.235),.040,brass,scale=(1,.25,1))
 for x in [-.072,.072]:leaf('Cornice | rosette wings',(0,y,3.235),(x,y,3.235),.026)
# Repeat side ornament in its own plane by rotating a copy of a front-plane design.
side_parts=[]
for yy in [-.53,.53]:
 for zz in [.32,2.83]:
  ob=scroll('Side | cast lower/upper scroll',yy,0,zz,.13,1.2,1,0);side_parts.append(ob)
 for zz in [1.05,2.44]:side_parts.append(ring('Side | suspended roundel',(yy,0,zz),.105,.009))
 side_parts.append(rod('Side | roundel stem',(yy,0,1.16),(yy,0,2.33),.007))
for side in [-1,1]:
 for src in side_parts:
  o=src.copy();o.data=src.data.copy();cols['03 Cast ornament'].objects.link(o);o.parent=root;o.name=src.name+(' | left' if side<0 else ' | right');o.rotation_euler.z=math.pi/2;o.location.x=side*1.154
for o in side_parts:bpy.data.objects.remove(o,do_unlink=True)
# Brass fixings placed at real rail joins.
for x in [-1.055,-.90,.90,1.055]:
 for z in [.30,1.0,2.69,3.23]:sphere('Front | domed brass fixing',(x,-1.158,z),.006,brass,scale=(1,.35,1))
for x in [-1.142,1.142]:
 for y in [-.97,0,.97]:
  for z in [.51,3.10]:sphere('Side | brass glazing fixing',(x,y,z),.0055,brass,scale=(.35,1,1))

# Mesh UVs: deterministic planar projection per face; curves remain editable masters.
for o in root.children:
 if o.type=='MESH' and not o.data.uv_layers:
  uv=o.data.uv_layers.new(name='UV0 | metric projection')
  for poly in o.data.polygons:
   normal=poly.normal;axis=max(range(3),key=lambda j:abs(normal[j]));axes=[j for j in range(3) if j!=axis]
   for li in poly.loop_indices:
    co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
for name,pos in [('SOCKET | Interaction',(0,-.1,1.1)),('SOCKET | Arrival',(0,-.45,1.04)),('SOCKET | Door_L',(-.79,-1.09,.08)),('SOCKET | Door_R',(.79,-1.09,.08))]:
 ob=bpy.data.objects.new(name,None);cols['08 Game anchors'].objects.link(ob);ob.parent=root;ob.location=pos;ob.empty_display_size=.12;ob.hide_render=True
ref=bpy.data.objects.new('REFERENCE | supplied lift1 image',None);cols['99 Reference'].objects.link(ref);ref.empty_display_type='IMAGE';ref.data=bpy.data.images.load(str(ROOT/'Reference images/lift1-reference.png'));ref.data.pack();ref.location=(-3,1,2.35);ref.rotation_euler=(math.pi/2,0,0);ref.empty_display_size=4.7;ref.hide_render=True

# Neutral daylight studio, with practical cabin light. Not part of exported game asset.
stage=material('Studio | soft mineral',(.19,.23,.22),0,.58)
box('Studio ground',(0,0,-.13),(200,200,.10),stage,'90 Studio',0)
world=bpy.data.worlds.new('Studio | cool daylight');world.use_nodes=True;world.node_tree.nodes.get('Background').inputs[0].default_value=(.40,.52,.60,1);world.node_tree.nodes.get('Background').inputs[1].default_value=.35;scene.world=world
def area(name,p,power,color,size,target):
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.color=color;data.shape='DISK';data.size=size;o=bpy.data.objects.new(name,data);cols['90 Studio'].objects.link(o);o.location=p;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
area('Daylight | large left softbox',(-3,-4,7),650,(.86,.93,1),5,(0,0,2))
area('Daylight | rear edge',(2.7,3.1,5.5),850,(1,.91,.73),3,(0,0,2.5))
area('Daylight | frontal reflection strip',(3,-4,3.5),340,(.94,.97,1),3,(0,0,1.7))
area('Cabin | warm practical',(0,0,2.97),38,(1,.78,.49),.32,(0,0,.2))
def camera(name,p,target,lens):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);cols['90 Studio'].objects.link(o);o.location=p;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_start=.05;return o
scene.camera=camera('CAM | Hero three-quarter', (6.1,-10.8,5.3),(0,0,2.28),64)
camera('CAM | Front elevation',(0,-11.8,3.0),(0,0,2.30),62)
camera('CAM | Cabin detail',(1.15,-4.6,2.55),(0,.5,1.7),48)
camera('CAM | Rear three-quarter',(-6.0,9.4,4.8),(0,0,2.24),58)
scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True;scene.cycles.max_bounces=10;scene.cycles.transmission_bounces=8
scene.render.resolution_x=1080;scene.render.resolution_y=1350;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.render.image_settings.file_format='PNG'
for screen in bpy.data.screens:
 for ar in screen.areas:
  if ar.type=='VIEW_3D':
   ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.shading.type='MATERIAL';ar.spaces.active.overlay.show_overlays=False
bpy.ops.object.select_all(action='DESELECT');root.select_set(True);bpy.context.view_layer.objects.active=root
scene['reference_interpretation']='Front-led reference; depth/rear and hidden joins designed to suit a functional game cabin. No shaft, moving doors or Unreal mechanics implied.'
readme=bpy.data.texts.new('READ ME | Lift master');readme.write('9th Kingdom — Service Lift master\nMetres; floor origin at (0,0,0); front is -Y.\nEditable meshes and curves, layered cast ornament, separate controls/glass.\n01–08 collections contain the asset; 90 Studio and 99 Reference are authoring only.\nSource reference is packed. Cameras show hero/front/interior/rear.\nThis is an authoring master: optimisation, texture baking, collision and moving-door/shaft integration remain separate production work.\nRear and hidden construction inferred from the single image.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Conservatory-Service-Lift-MASTER.blend'))
report={'blender':bpy.app.version_string,'objects':len(root.children),'mesh_objects':sum(o.type=='MESH' for o in root.children),'curves':sum(o.type=='CURVE' for o in root.children),'width_m':2.68,'depth_m':2.44,'height_m':4.70,'door_clear_width_m':1.515,'master_file':str(OUT/'Conservatory-Service-Lift-MASTER.blend'),'unreal_modified':False}
(OUT/'MasterReport.json').write_text(json.dumps(report,indent=2));print('LIFT_MASTER_SAVED',report)
