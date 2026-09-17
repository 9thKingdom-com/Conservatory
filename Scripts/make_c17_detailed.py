"""C-17 detailed reference model, based on supplied front/side/back views.
Run with Blender 5.1 --background --python. Does not replace the game robot.
"""
import bpy, math, json, random, time
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'SourceAssets/C17Detailed';DOC=ROOT/'Documentation/C17Detailed'
OUT.mkdir(parents=True,exist_ok=True);DOC.mkdir(parents=True,exist_ok=True)
random.seed(1717);bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
collections={}
for n in ['01 Sensor head','02 Torso and power pack','03 Left arm','04 Right arm','05 Pelvis','06 Left leg','07 Right leg','08 Rig','09 Reference orthographics','10 Studio']:
 c=bpy.data.collections.new(n);scene.collection.children.link(c);collections[n]=c
group='02 Torso and power pack';parts=[];bind={};bones={}
colors={'Safety yellow':(.52,.335,.025),'Chassis graphite':(.035,.043,.046),'Machined steel':(.18,.205,.215),'Dark titanium':(.095,.113,.120),'Rubber':(.009,.012,.014),'Recess black':(.003,.005,.006),'Optical glass':(.008,.035,.043),'Stencil ivory':(.72,.70,.59),'Amber indicator':(1,.42,.025),'Copper':(.23,.12,.048)}
mats={}
for name,col in colors.items():
 m=bpy.data.materials.new('C17D / '+name);m.diffuse_color=(*col,1);m.use_nodes=True;nt=m.node_tree;p=nt.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1)
 p.inputs['Metallic'].default_value=.78 if name in ['Machined steel','Dark titanium','Copper'] else .35 if name in ['Safety yellow','Chassis graphite'] else 0
 p.inputs['Roughness'].default_value=.38 if name=='Safety yellow' else .43 if name in ['Machined steel','Dark titanium'] else .54
 if name in ['Safety yellow','Chassis graphite','Machined steel','Dark titanium']:
  tc=nt.nodes.new('ShaderNodeTexCoord');n=nt.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=65;n.inputs['Detail'].default_value=3;nt.links.new(tc.outputs['Generated'],n.inputs['Vector'])
  ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*[x*.70 for x in col],1);ramp.color_ramp.elements[1].color=(*[min(1,x*1.15) for x in col],1);nt.links.new(n.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],p.inputs['Base Color'])
  bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.16;bump.inputs['Distance'].default_value=.00045;nt.links.new(n.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],p.inputs['Normal'])
  rough=nt.nodes.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.32;rough.inputs['To Max'].default_value=.53;nt.links.new(n.outputs['Fac'],rough.inputs['Value']);nt.links.new(rough.outputs[0],p.inputs['Roughness'])
  if name=='Safety yellow':
   geom=nt.nodes.new('ShaderNodeNewGeometry');edge=nt.nodes.new('ShaderNodeValToRGB');edge.color_ramp.elements[0].position=.49;edge.color_ramp.elements[1].position=.57
   nt.links.new(geom.outputs['Pointiness'],edge.inputs[0]);mul=nt.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';nt.links.new(edge.outputs[0],mul.inputs[0]);nt.links.new(n.outputs['Fac'],mul.inputs[1])
   mix=nt.nodes.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.13,.15,.15,1);nt.links.new(mul.outputs[0],mix.inputs[0]);nt.links.new(ramp.outputs[0],mix.inputs[1]);nt.links.new(mix.outputs[0],p.inputs['Base Color'])
 if name=='Optical glass':
  p.inputs['Metallic'].default_value=.32;p.inputs['Roughness'].default_value=.075;p.inputs['Coat Weight'].default_value=.8;p.inputs['Coat Roughness'].default_value=.035
 if name=='Amber indicator':
  p.inputs['Emission Color'].default_value=(*col,1);p.inputs['Emission Strength'].default_value=2.4
 mats[name]=m
def link(o,coll=None):
 for c in list(o.users_collection):c.objects.unlink(o)
 collections[coll or group].objects.link(o)
def finish(o,name,bone,mat='Dark titanium',bevel=0):
 o.name=name;link(o);o.data.materials.append(mats[mat]);bpy.context.view_layer.objects.active=o
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Machined edge radius','BEVEL');mod.width=bevel;mod.segments=3;mod.affect='EDGES';bpy.ops.object.modifier_apply(modifier=mod.name)
 # Flat armour faces with smooth curved bevels; normals remain editable.
 for p in o.data.polygons:p.use_smooth=True
 mod=o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL');mod.keep_sharp=True;mod.weight=40
 o['assembly']=group;o['joint']=bone;parts.append(o);bind[o.name]=bone;return o
def box(name,pos,size,bone,mat='Dark titanium',bevel=.003):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.scale=size;return finish(o,name,bone,mat,bevel)
def cyl(name,pos,r,depth,bone,mat='Machined steel',axis=(1,0,0),verts=32,bevel=.001):
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=pos);o=bpy.context.object;o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();return finish(o,name,bone,mat,bevel)
def tube(name,a,b,r,bone,mat='Machined steel',verts=16):
 a,b=Vector(a),Vector(b);return cyl(name,(a+b)/2,r,(b-a).length,bone,mat,b-a,verts,min(.001,r*.12))
def ring(name,pos,major,minor,bone,mat='Machined steel',axis=(1,0,0)):
 bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=40,minor_segments=10,location=pos);o=bpy.context.object;o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();return finish(o,name,bone,mat)
def panel(name,outline,y,depth,bone,mat='Dark titanium',bevel=.003):
 # Shaped armour silhouette in XZ, extruded through Y.
 n=len(outline);v=[(x,y+d,z) for d in [-depth/2,depth/2] for x,z in outline];f=[tuple(reversed(range(n))),tuple(range(n,2*n))]
 f += [(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);return finish(o,name,bone,mat,bevel)
def hose(name,pts,r,bone,mat='Rubber'):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=10;cu.bevel_depth=r;cu.bevel_resolution=3;s=cu.splines.new('BEZIER');s.bezier_points.add(len(pts)-1)
 for p,co in zip(s.bezier_points,pts):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,cu);scene.collection.objects.link(o);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');return finish(o,name,bone,mat)
def bolt(pos,bone,r=.004,axis=(0,-1,0),name='Captive hex fastener'):
 cyl(name,pos,r,.003,bone,'Machined steel',axis,6,.0004)
 q=Vector(pos)+Vector(axis)*.002;cyl('Hex socket recess',q,r*.43,.0006,bone,'Recess black',axis,6,0)
def stencil(body,pos,size,bone,back=False):
 bpy.ops.object.text_add(location=pos,rotation=(math.pi/2,0,math.pi if back else 0));o=bpy.context.object;o.data.body=body;o.data.align_x='CENTER';o.data.size=size;o.data.extrude=.00012;o.data.resolution_u=6;bpy.ops.object.convert(target='MESH');return finish(o,'Stencil / '+body,bone,'Stencil ivory')
def leafbadge(x,y,z,bone,scale=1):
 for dx,dz,angle in [(-.014,.012,-.6),(.014,.012,.6),(0,.030,0)]:
  pts=[(-.007,0),(0,.034),(.007,0),(0,-.006)]
  outline=[(x+(dx+a*math.cos(angle)+b*math.sin(angle))*scale,z+(dz-a*math.sin(angle)+b*math.cos(angle))*scale) for a,b in pts]
  panel('Botanical enamel badge',outline,y,.0008,bone,'Stencil ivory',0)
 tube('Botanical badge stem',(x,y,z-.015*scale),(x,y,z+.025*scale),.0012*scale,bone,'Stencil ivory',8)
def bone(n,h,t,parent=None):bones[n]=(Vector(h),Vector(t),parent)
bone('root',(0,0,0),(0,0,.12));bone('pelvis',(0,0,.98),(0,0,1.08),'root');bone('waist',(0,0,1.08),(0,0,1.17),'pelvis');bone('chest',(0,0,1.17),(0,0,1.49),'waist');bone('neck',(0,0,1.49),(0,-.02,1.61),'chest');bone('head',(0,-.02,1.61),(0,-.02,1.77),'neck')
for side,s in [('L',1),('R',-1)]:
 bone('shoulder_'+side,(s*.22,0,1.45),(s*.265,.005,1.22),'chest');bone('forearm_'+side,(s*.265,.005,1.22),(s*.32,-.015,1.01),'shoulder_'+side);bone('hand_'+side,(s*.32,-.015,1.01),(s*.327,-.018,.925),'forearm_'+side)
 for f,dx,dy in [('index',-.025,-.025),('middle',.025,-.025),('thumb',0,.025)]:
  x=s*(.327+dx);bone(f+'1_'+side,(x,dy,.934),(x+s*.007,dy-.006,.878),'hand_'+side);bone(f+'2_'+side,(x+s*.007,dy-.006,.878),(x+s*.003,dy-.028,.849),f+'1_'+side)
 bone('thigh_'+side,(s*.135,0,1.015),(s*.148,-.008,.590),'pelvis');bone('shin_'+side,(s*.148,-.008,.590),(s*.15,.022,.178),'thigh_'+side);bone('foot_'+side,(s*.15,.022,.178),(s*.15,-.115,.078),'shin_'+side);bone('toe_'+side,(s*.15,-.115,.078),(s*.15,-.235,.055),'foot_'+side)
bone('camera_mount',(0,-.16,1.704),(0,-.22,1.704),'head');bone('cargo_mount',(0,.19,1.31),(0,.28,1.31),'chest')

# Torso: tapered shell, multilayer bolted service hatch, removable side guards.
outline=[(-.145,1.115),(-.195,1.23),(-.192,1.425),(-.145,1.50),(.145,1.50),(.192,1.425),(.195,1.23),(.145,1.115)]
panel('Tapered torso inner casting',outline,.01,.25,'chest','Chassis graphite',.012)
panel('Chest armour backing',[(-.143,1.17),(-.16,1.43),(-.124,1.465),(.124,1.465),(.16,1.43),(.143,1.17)],-.136,.018,'chest','Machined steel',.004)
panel('Removable chest access panel',[(-.112,1.185),(-.132,1.217),(-.132,1.414),(.132,1.414),(.132,1.217),(.112,1.185)],-.151,.019,'chest','Dark titanium',.004)
for s in [-1,1]:
 panel('Shaped yellow side guard',[(s*.145,1.15),(s*.195,1.205),(s*.202,1.418),(s*.168,1.505),(s*.142,1.493),(s*.158,1.41),(s*.156,1.24),(s*.130,1.185)],-.124,.044,'chest','Safety yellow',.004)
 for z in [1.198,1.28,1.39,1.476]:bolt((s*(.165 if z<1.43 else .158),-.151,z),'chest',.005)
 for z in [1.24,1.36]:
  box('Chest service latch',(s*.112,-.170,z),(.019,.012,.041),'chest','Chassis graphite',.003)
  tube('Latch pivot pin',(s*.112-.009,-.180,z+.008),(s*.112+.009,-.180,z+.008),.003,'chest')
 for z in [1.211,1.392]:bolt((s*.099,-.166,z),'chest',.0035)
 # Side gills, frame struts, power bus and ports.
 for z in [1.24,1.27,1.30,1.33,1.36]:box('Lateral heat exchanger fin',(s*.192,.025,z),(.018,.135,.009),'chest','Machined steel',.001)
 tube('Chest structural side rail',(s*.174,.11,1.16),(s*.178,.11,1.47),.014,'chest','Chassis graphite')
 for z in [1.20,1.41]:cyl('Recessed service port',(s*.204,.06,z),.012,.009,'chest','Recess black',(s,0,0),20)
box('Yellow header band',(0,-.157,1.435),(.25,.017,.030),'chest','Safety yellow',.003)
for x in [-.10,-.06,-.02,.02,.06,.10]:
 o=box('Header caution separator',(x,-.168,1.436),(.009,.002,.022),'chest','Chassis graphite',.0005);o.rotation_euler.y=-.4
stencil('C-17',(0,-.162,1.367),.033,'chest');leafbadge(0,-.164,1.272,'chest',1.0)
stencil('FIELD SERVICE',(0,-.162,1.224),.0085,'chest')
box('Lower chest control recess',(0,-.131,1.139),(.145,.04,.045),'chest','Recess black',.006)
for x in [-.05,-.025,0,.025,.05]:box('Lower chest grille',(x,-.153,1.14),(.011,.008,.028),'chest','Machined steel',.001)

# Back view: deep rectangular removable power pack with independent protective rails.
box('Backpack energy core',(0,.145,1.315),(.29,.16,.335),'chest','Chassis graphite',.018)
panel('Power pack rear armour',[(-.14,1.16),(-.152,1.195),(-.152,1.466),(-.125,1.49),(.125,1.49),(.152,1.466),(.152,1.195),(.14,1.16)],.232,.026,'chest','Dark titanium',.005)
box('Backpack gasket',(0,.249,1.325),(.246,.006,.243),'chest','Rubber',.008)
box('Rear removable service lid',(0,.255,1.325),(.232,.012,.231),'chest','Dark titanium',.007)
leafbadge(0,.263,1.32,'chest',1.35)
for s in [-1,1]:
 box('Yellow rear impact rail',(s*.16,.175,1.329),(.025,.15,.346),'chest','Safety yellow',.007)
 for z in [1.185,1.26,1.43,1.484]:bolt((s*.155,.26,z),'chest',.0045,(0,1,0))
 for z in [1.237,1.425]:bolt((s*.092,.265,z),'chest',.004,(0,1,0))
 for z in [1.20,1.22,1.24]:box('Rear lower heat sink',(s*.085,.27,z),(.076,.018,.007),'chest','Chassis graphite',.001)
 tube('Backpack lift lug',(s*.09,.17,1.49),(s*.09,.20,1.522),.009,'chest')
tube('Backpack lift handle',(-.09,.20,1.522),(.09,.20,1.522),.009,'chest')
box('Rear yellow top cap',(0,.18,1.50),(.24,.11,.022),'chest','Safety yellow',.005)
for x in [-.08,.08]:bolt((x,.18,1.516),'chest',.004,(0,0,1))

# Neck and compact sensor head. Head-to-body ratio follows the new three-view reference.
group='01 Sensor head'
cyl('Neck base yaw bearing',(0,0,1.527),.065,.034,'neck','Chassis graphite',(0,0,1),40)
cyl('Neck polished shaft',(0,0,1.566),.036,.060,'neck','Machined steel',(0,0,1),32)
for z in [1.546,1.557,1.568,1.579]:ring('Neck bellows rib',(0,0,z),.038,.006,'neck','Rubber',(0,0,1))
for s in [-1,1]:
 panel('Neck side yoke',[(s*.042,1.54),(s*.063,1.61),(s*.044,1.646),(s*.025,1.60)],.0,.085,'neck','Dark titanium',.004)
panel('Sensor head faceted casting',[(-.123,1.622),(-.139,1.65),(-.139,1.756),(-.10,1.798),(.10,1.798),(.139,1.756),(.139,1.65),(.123,1.622)],-.012,.193,'head','Chassis graphite',.006)
panel('Yellow sensor head shell',[(-.127,1.635),(-.147,1.668),(-.144,1.75),(-.109,1.790),(.109,1.790),(.144,1.75),(.147,1.668),(.127,1.635)],-.013,.181,'head','Safety yellow',.006)
box('Recessed optical face gasket',(0,-.110,1.702),(.255,.016,.132),'head','Rubber',.015)
box('Optical face plate',(0,-.121,1.700),(.242,.012,.122),'head','Dark titanium',.013)
box('Face dark field',(0,-.129,1.698),(.220,.006,.099),'head','Recess black',.011)
box('Head top service lid',(0,-.002,1.795),(.196,.151,.014),'head','Dark titanium',.004)
for s in [-1,1]:
 cyl('Head pitch trunnion',(s*.151,.001,1.699),.047,.028,'head','Chassis graphite',(1,0,0),36)
 ring('Head bearing retaining ring',(s*.168,.001,1.699),.033,.003,'head','Machined steel',(1,0,0))
 cyl('Head lateral black end cap',(s*.168,.001,1.699),.029,.012,'head','Dark titanium',(1,0,0),32)
 for z in [1.658,1.745]:bolt((s*.105,-.138,z),'head',.003)
 for y in [-.05,.052]:bolt((s*.172,y,1.70),'head',.003,(s,0,0))
for x,z,r in [(.064,1.708,.036),(-.064,1.695,.024),(-.004,1.662,.011)]:
 cyl('Optics machined recess',(x,-.142,z),r+.007,.018,'head','Chassis graphite',(0,-1,0),48)
 ring('Camera bezel',(x,-.155,z),r,.0025,'head','Machined steel',(0,-1,0))
 cyl('Recessed coated lens',(x,-.155,z),r*.83,.004,'head','Optical glass',(0,-1,0),48,0)
 ring('Optical inner ring',(x,-.158,z),r*.56,.0012,'head','Recess black',(0,-1,0))
 cyl('Optical iris',(x,-.158,z),r*.37,.002,'head','Recess black',(0,-1,0),32,0)
box('Amber status bar housing',(-.046,-.14,1.747),(.087,.010,.013),'head','Chassis graphite',.002)
for x in [-.072,-.047,-.022]:box('Amber status segment',(x,-.147,1.747),(.020,.004,.005),'head','Amber indicator',.001)
for z in [1.657,1.672,1.687,1.702]:box('Rear sensor cooling slot',(0,.091,z),(.095,.005,.004),'head','Recess black',.001)
stencil('C17 / OPTICS',(0,-.127,1.777),.0065,'head')
cyl('Radio antenna foot',(-.118,.159,1.519),.014,.030,'chest','Safety yellow',(0,0,1),24)
for z in [1.54,1.55,1.56,1.57]:ring('Antenna spring rib',(-.118,.159,z),.008,.002,'chest','Rubber',(0,0,1))
tube('Radio whip',(-.118,.159,1.58),(-.118,.159,1.90),.0026,'chest','Chassis graphite',12)
cyl('Antenna protective tip',(-.118,.159,1.902),.004,.016,'chest','Rubber',(0,0,1),16)

# Pelvis: exposed narrow waist and shaped central gear housing.
group='05 Pelvis'
cyl('Waist rotary bearing',(0,0,1.105),.085,.05,'waist','Chassis graphite',(0,0,1),48)
for z in [1.084,1.096,1.115]:ring('Waist steel retaining ring',(0,0,z),.078,.003,'waist','Machined steel',(0,0,1))
panel('Pelvis chassis',[(-.116,.943),(-.135,1.04),(-.09,1.088),(.09,1.088),(.135,1.04),(.116,.943)],.0,.185,'pelvis','Chassis graphite',.008)
panel('Pelvis shaped front plate',[(-.082,.947),(-.098,1.032),(-.08,1.065),(.08,1.065),(.098,1.032),(.082,.947)],-.108,.022,'pelvis','Dark titanium',.006)
box('Pelvis lower skid',(0,-.03,.949),(.153,.14,.02),'pelvis','Machined steel',.004)
for s in [-1,1]:
 for z in [.973,1.04]:bolt((s*.065,-.124,z),'pelvis',.0045)
 tube('Pelvis harness strut',(s*.09,.06,.966),(s*.11,.07,1.067),.012,'pelvis','Machined steel')

# Concentric mechanical bearings with bolt circles and yellow protective sector plates.
def bearing(label,p,r,width,bone,outer_sign,accent=True):
 p=Vector(p);cyl(label+' central drive',p,r,width,bone,'Recess black',(1,0,0),48)
 for sign in [-1,1]:
  q=p+Vector((sign*(width/2+.004),0,0));cyl(label+' bearing rim',q,r*.92,.014,bone,'Machined steel',(1,0,0),48)
  q+=Vector((sign*.009,0,0));cyl(label+' end cover',q,r*.75,.013,bone,'Dark titanium',(1,0,0),40)
  ring(label+' labyrinth seal',q+Vector((sign*.008,0,0)),r*.60,r*.035,bone,'Recess black')
  cyl(label+' axle boss',q+Vector((sign*.010,0,0)),r*.24,.012,bone,'Machined steel',(1,0,0),24)
  for k in range(6):
   a=k*math.tau/6;bolt(q+Vector((sign*.01,math.cos(a)*r*.78,math.sin(a)*r*.78)),bone,.0035,(sign,0,0))
 if accent:
  q=p+Vector((outer_sign*(width/2+.014),0,0));ring(label+' yellow outer bumper',q,r*.91,r*.075,bone,'Safety yellow')
for side,s in [('L',1),('R',-1)]:
 group='03 Left arm' if s==1 else '04 Right arm';upper='shoulder_'+side;lower='forearm_'+side;hand='hand_'+side
 bearing('Shoulder gearbox',(s*.22,0,1.45),.086,.090,upper,s)
 panel('Shoulder scalloped guard',[(s*.235,1.524),(s*.284,1.505),(s*.322,1.434),(s*.315,1.355),(s*.287,1.35),(s*.274,1.43),(s*.222,1.493)],-.007,.13,upper,'Safety yellow',.005)
 for x,z in [(s*.264,1.495),(s*.303,1.432),(s*.30,1.377)]:bolt((x,-.079,z),upper,.0045)
 tube('Upper arm internal spar',(s*.239,0,1.40),(s*.261,.005,1.25),.025,upper,'Chassis graphite',20)
 panel('Upper arm shaped titanium casing',[(s*.22,1.395),(s*.261,1.415),(s*.295,1.275),(s*.28,1.251),(s*.243,1.268)],-.023,.065,upper,'Dark titanium',.004)
 bearing('Elbow',(s*.265,.005,1.22),.053,.083,lower,s,False)
 panel('Forearm structural casing',[(s*.236,1.185),(s*.28,1.199),(s*.349,1.057),(s*.346,1.029),(s*.287,1.026)],-.007,.093,lower,'Dark titanium',.004)
 panel('Forearm yellow outer shield',[(s*.269,1.195),(s*.297,1.177),(s*.341,1.064),(s*.333,1.041),(s*.309,1.050),(s*.276,1.16)],-.066,.021,lower,'Safety yellow',.003)
 panel('Forearm central access cover',[(s*.245,1.166),(s*.263,1.178),(s*.309,1.061),(s*.299,1.039),(s*.280,1.045)],-.063,.016,lower,'Machined steel',.003)
 for z in [1.075,1.11,1.153]:bolt((s*(.30-(z-1.075)*.35),-.081,z),lower,.0035)
 for z in [1.10,1.123,1.146]:box('Forearm ventilation slot',(s*(.315-(z-1.10)*.32),-.080,z),(.012,.005,.006),lower,'Recess black',.001)
 bearing('Wrist coupling',(s*.32,-.015,1.01),.031,.060,hand,s,False)
 panel('Gripper palm casting',[(s*.294,.979),(s*.293,.941),(s*.315,.914),(s*.357,.933),(s*.36,.97),(s*.344,.987)],-.018,.063,hand,'Dark titanium',.003)
 box('Palm tactile pad',(s*.327,-.054,.954),(.045,.012,.037),hand,'Rubber',.004)
 for finger in ['index','middle','thumb']:
  for seg in [1,2]:
   bn=finger+str(seg)+'_'+side;a,b,_=bones[bn];tube('Finger articulated link',a,b,.009,bn,'Machined steel',12)
   cyl('Finger hinge axle',a,.011,.028,bn,'Chassis graphite',(1,0,0),20)
   for sign in [-1,1]:bolt(a+Vector((sign*.016,0,0)),bn,.003,(sign,0,0))
   if seg==2:box('Finger replaceable gripping pad',(b.x,b.y-.006,b.z+.008),(.017,.015,.026),bn,'Rubber',.003)
 # Legs have tapered long plates, open backs and structural spars.
 group='06 Left leg' if s==1 else '07 Right leg';thigh='thigh_'+side;shin='shin_'+side;foot='foot_'+side;toe='toe_'+side
 bearing('Hip reduction drive',(s*.135,0,1.015),.094,.104,thigh,s)
 tube('Thigh core spar',(s*.14,0,.946),(s*.148,-.008,.668),.032,thigh,'Chassis graphite',24)
 panel('Thigh tapered front armour',[(s*.09,.949),(s*.158,.949),(s*.209,.888),(s*.205,.679),(s*.174,.652),(s*.10,.691)],-.081,.039,thigh,'Dark titanium',.005)
 panel('Thigh side yellow guard',[(s*.181,.976),(s*.213,.953),(s*.236,.91),(s*.229,.751),(s*.21,.721),(s*.195,.763),(s*.20,.901),(s*.176,.946)],-.012,.133,thigh,'Safety yellow',.004)
 panel('Thigh inset steel plate',[(s*.109,.894),(s*.179,.872),(s*.184,.716),(s*.157,.686),(s*.112,.711)],-.106,.008,thigh,'Machined steel',.003)
 for x,z in [(s*.114,.867),(s*.177,.842),(s*.119,.729),(s*.176,.715)]:bolt((x,-.112,z),thigh,.004)
 for z in [.78,.813,.846]:box('Thigh cooling slot',(s*.144,-.112,z),(.025,.004,.006),thigh,'Recess black',.001)
 bearing('Knee',(s*.148,-.008,.590),.066,.091,shin,s)
 panel('Knee frontal impact shield',[(s*.103,.64),(s*.18,.64),(s*.193,.603),(s*.178,.554),(s*.112,.554),(s*.097,.598)],-.076,.026,shin,'Chassis graphite',.005)
 box('Knee yellow forehead',(s*.147,-.094,.631),(.055,.018,.021),shin,'Safety yellow',.004)
 box('Knee service indicator',(s*.147,-.105,.621),(.023,.003,.004),shin,'Amber indicator',.001)
 tube('Shin rear tension strut',(s*.15,.045,.527),(s*.15,.066,.221),.019,shin,'Chassis graphite')
 panel('Shin taper casting',[(s*.09,.539),(s*.191,.529),(s*.193,.484),(s*.177,.215),(s*.130,.209),(s*.106,.314)],-.021,.080,shin,'Dark titanium',.005)
 panel('Shin front service plate',[(s*.113,.505),(s*.171,.498),(s*.165,.269),(s*.145,.241),(s*.122,.284)],-.067,.013,shin,'Machined steel',.003)
 panel('Shin yellow side strip',[(s*.183,.50),(s*.205,.478),(s*.181,.259),(s*.163,.245),(s*.172,.324)],-.030,.060,shin,'Safety yellow',.003)
 for z in [.299,.456]:bolt((s*.144,-.078,z),shin,.004)
 bearing('Ankle',(s*.15,.022,.178),.043,.078,foot,s)
 # Low foot with angular toe segments, heel and traction blocks.
 panel('Ankle yellow armour',[(s*.103,.181),(s*.111,.228),(s*.17,.229),(s*.19,.189),(s*.19,.151),(s*.12,.144)],-.035,.10,foot,'Safety yellow',.004)
 box('Heel traction sole',(s*.15,.043,.039),(.142,.128,.052),foot,'Rubber',.008)
 panel('Foot arch frame',[(s*.077,.063),(s*.09,.134),(s*.127,.162),(s*.187,.136),(s*.222,.066)],-.059,.17,foot,'Dark titanium',.005)
 box('Toe undercarriage',(s*.15,-.171,.042),(.168,.179,.052),toe,'Rubber',.007)
 for dx in [-.055,0,.055]:
  o=box('Independent toe armour',(s*.15+dx,-.179,.084),(.047,.152,.051),toe,'Dark titanium',.005);o.rotation_euler.x=-.13
  box('Toe yellow strike strip',(s*.15+dx,-.228,.081),(.038,.033,.022),toe,'Safety yellow',.003)
  bolt((s*.15+dx,-.178,.114),toe,.003,(0,0,1))
 for y in [-.242,-.210,-.175,-.140,.077]:box('Foot traction lug',(s*.15,y,.022),(.172,.020,.028),toe if y<0 else foot,'Rubber',.003)
 for sign in [-1,1]:cyl('Toe pivot pin',(s*.15+sign*.092,-.114,.07),.014,.009,toe,'Machined steel',(1,0,0),20)

print('C17D_GEOMETRY',len(parts),'parts',flush=True)
# Poseable rigid mechanical rig. Every part has a single named bone influence.
armdata=bpy.data.armatures.new('C17 Detailed mechanical skeleton');arm=bpy.data.objects.new('C17_Detailed_Rig',armdata);collections['08 Rig'].objects.link(arm)
bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm;bpy.ops.object.mode_set(mode='EDIT')
for n,(h,t,parent) in bones.items():
 b=armdata.edit_bones.new(n);b.head=h;b.tail=t
 if parent:b.parent=armdata.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT');arm.show_in_front=True;arm.data.display_type='STICK'
for o in parts:
 bn=bind[o.name];vg=o.vertex_groups.new(name=bn);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');o.parent=arm;mod=o.modifiers.new('Rigid joint / '+bn,'ARMATURE');mod.object=arm
arm['Reference model']='Front / side / back supplied 9 September 2026';arm['Body height metres']=1.805;arm['Rig notes']='FK rigid mechanical articulation. New proportions and bone names; no automatic compatibility with existing C17 clips.'

# Keep all three packed image references in an optional orthographic collection.
refcoll=collections['09 Reference orthographics']
for fn,name,pos,rot in [('robot-1a.png','FRONT reference',(0,.5,.94),(math.pi/2,0,0)),('robot-1b.png','SIDE reference',(.55,0,.94),(math.pi/2,0,math.pi/2)),('robot-1c.png','BACK reference',(0,-.5,.94),(math.pi/2,0,math.pi))]:
 img=bpy.data.images.load(str(OUT/'References'/fn));img.pack();o=bpy.data.objects.new(name,None);refcoll.objects.link(o);o.empty_display_type='IMAGE';o.data=img;o.empty_display_size=1.95;o.color[3]=.35;o.location=pos;o.rotation_euler=rot;o.hide_render=True
refcoll.hide_viewport=True;refcoll.hide_render=True

# Studio views, aligned to the supplied orthographics.
group='10 Studio'
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.0005));floor=bpy.context.object;floor.name='Studio floor';link(floor)
fm=bpy.data.materials.new('Neutral charcoal studio');fm.use_nodes=True;fm.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.085,.10,.11,1);fm.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.78;floor.data.materials.append(fm)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,power,size,color in [('Key',(-3,-4,4.5),650,3.5,(1,.91,.79)),('Fill',(3,-2,2.8),420,3,(.79,.88,1)),('Rim',(1,3,3.8),850,2.5,(1,.95,.83))]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='Studio / '+name;link(o);o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color;aim(o,(0,0,1))
cameras={}
for name,pos,scale in [('Hero',(2.6,-4.5,2.25),2.23),('Front',(0,-5,.95),2.13),('Side',(5,0,.95),2.13),('Back',(0,5,.95),2.13),('HeadDetail',(.6,-1.4,1.92),.54)]:
 bpy.ops.object.camera_add(location=pos);o=bpy.context.object;o.name='Camera / '+name;link(o);aim(o,(0,0,1.70) if name=='HeadDetail' else (0,0,.94));o.data.type='ORTHO';o.data.ortho_scale=scale;cameras[name]=o
scene.camera=cameras['Hero'];scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=1600;scene.render.resolution_percentage=100;scene.world.color=(.18,.18,.18);scene.view_settings.view_transform='AgX'
scene.render.image_settings.file_format='PNG'
# Choose a useful opening viewport and keep studio helpers out of the modeling viewport.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_distance=2.6;area.spaces.active.region_3d.view_location=Vector((0,0,.94));area.spaces.active.clip_end=500;area.spaces.active.shading.type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);bpy.context.view_layer.objects.active=arm
tri=sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in parts)
manifest={'source_references':['References/robot-1a.png','References/robot-1b.png','References/robot-1c.png'],'body_height_m':1.805,'antenna_height_m':1.91,'scale_note':'Assumed human-scale 1.8 m body; reference drawings have no measured dimension.','editable_mesh_parts':len(parts),'base_mesh_triangles':tri,'bones':len(bones),'materials':list(colors),'rig':'Rigid single-bone weights; FK poseable joints, not animation-retargeted.','game_robot_replaced':False,'master_file':'C17-Detailed-Reference.blend'}
(OUT/'Manifest.json').write_text(json.dumps(manifest,indent=2))
readme=bpy.data.texts.new('READ ME — C17 detailed reference');readme.write('C-17 detailed reference model\nFront is -Y, up is +Z; metres.\nOriginal front/side/back images are packed in collection 09.\nSeparate named mechanical parts are rigidly bound to the FK skeleton in collection 08.\nUse Pose Mode for joints. Studio and reference collections can be hidden while editing.\nThis model is a separate derivative: the currently deployed Unreal C17 remains unchanged.\nProcedural Cycles materials need baking before an Unreal material import.\nSource dimensions are assumed, not measured. See Manifest.json.\n')
scene.render.filepath=str(DOC/'C17Detailed-Hero.png');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'C17-Detailed-Reference.blend'))
for name in ['Hero','Front','Side','Back','HeadDetail']:
 scene.camera=cameras[name];scene.render.filepath=str(DOC/('C17Detailed-'+name+'.png'))
 scene.render.resolution_x=1200 if name in ['Hero','HeadDetail'] else 900;scene.render.resolution_y=1200 if name=='HeadDetail' else 1600
 bpy.ops.render.render(write_still=True);print('C17D_RENDERED '+name,flush=True)
scene.camera=cameras['Hero'];scene.render.resolution_x=1200;scene.render.resolution_y=1600;scene.render.filepath=str(DOC/'C17Detailed-Hero.png');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'C17-Detailed-Reference.blend'))
print('C17_DETAILED_COMPLETE '+json.dumps(manifest),flush=True)
