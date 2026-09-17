"""Executed inside the C17 generator before binding: revised reference-led geometry."""
import bmesh

def discard(prefixes):
 for o in list(parts):
  if any(o.name.startswith(p) for p in prefixes):
   parts.remove(o);bind.pop(o.name,None);bpy.data.objects.remove(o,do_unlink=True)

def meshpart(name,verts,faces,joint,mat,bevel=.001):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 ob=bpy.data.objects.new(name,me);scene.collection.objects.link(ob)
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True)
 return finish(ob,name,joint,mat,bevel)

def formed(name,outline,y,depth,joint,mat='Dark titanium',crown=.012,inset=.86):
 # Four contour rings produce real folded shoulders and a raised central face.
 cx=sum(p[0] for p in outline)/len(outline);cz=sum(p[1] for p in outline)/len(outline);n=len(outline)
 verts=[]
 for scale,dy in [(1,depth/2),(1,-depth/2),(.97,-depth/2-crown*.38),(inset,-depth/2-crown)]:
  verts.extend((cx+(x-cx)*scale,y+dy,cz+(z-cz)*scale) for x,z in outline)
 faces=[tuple(reversed(range(n))),tuple(range(3*n,4*n))]
 for k in range(3):
  for i in range(n):j=(i+1)%n;faces.append((k*n+i,k*n+j,(k+1)*n+j,(k+1)*n+i))
 return meshpart(name,verts,faces,joint,mat,.0015)

def aperture(name,outer,inner,y,depth,joint,mat='Dark titanium'):
 # A genuinely open frame, not a dark rectangle pasted on a solid slab.
 n=len(outer);assert n==len(inner);verts=[(x,y+d,z) for d in [-depth/2,depth/2] for loop in [outer,inner] for x,z in loop];faces=[]
 for i in range(n):
  j=(i+1)%n
  faces.extend([(i,j,n+j,n+i),(2*n+i,3*n+i,3*n+j,2*n+j),(i,2*n+i,2*n+j,j),(n+i,n+j,3*n+j,3*n+i)])
 return meshpart(name,verts,faces,joint,mat,.001)

def sector(name,centre,inner,outer,width,a0,a1,joint,mat='Safety yellow'):
 # Annular side guard with exposed open ends around the working joint.
 x,y,z=centre;N=36;v=[]
 for dx in [-width/2,width/2]:
  for r in [inner,outer]:
   for i in range(N+1):a=math.radians(a0+(a1-a0)*i/N);v.append((x+dx,y+r*math.cos(a),z+r*math.sin(a)))
 k=N+1;f=[]
 for i in range(N):
  f.extend([(i,i+1,k+i+1,k+i),(2*k+i,3*k+i,3*k+i+1,2*k+i+1),(i,2*k+i,2*k+i+1,i+1),(k+i,k+i+1,3*k+i+1,3*k+i)])
 f.extend([(0,k,3*k,2*k),(N,2*k+N,3*k+N,k+N)])
 return meshpart(name,v,f,joint,mat,.0012)

def sideformed(name,outline,x,depth,joint,mat='Dark titanium',crown=.006):
 o=formed(name,outline,0,depth,joint,mat,crown)
 for v in o.data.vertices:xx,yy,zz=v.co;v.co=(x-yy,xx,zz)
 return o

def relief_slots(x,y,z,joint,count=4,span=.04):
 for i in range(count):
  zz=z+i*.012;box('Recessed cooling channel',(x,y,zz),(span,.004,.006),joint,'Recess black',.001)
  box('Channel lower lip',(x,y-.002,zz-.0035),(span,.003,.0015),joint,'Machined steel',.0004)

# Replace the slab-like central castings and large guards with shaped layered shells.
discard(['Tapered torso inner casting','Chest armour backing','Removable chest access panel','Shaped yellow side guard','Yellow header band','Header caution separator','Shoulder scalloped guard','Upper arm shaped titanium casing','Forearm structural casing','Forearm yellow outer shield','Forearm central access cover','Thigh tapered front armour','Thigh side yellow guard','Thigh inset steel plate','Shin taper casting','Shin front service plate','Shin yellow side strip','Knee frontal impact shield','Independent toe armour','Toe yellow strike strip','Foot arch frame','Ankle yellow armour'])
group='02 Torso and power pack'
formed('Faceted main thorax casting',[(-.123,1.13),(-.183,1.205),(-.190,1.405),(-.148,1.493),(.148,1.493),(.190,1.405),(.183,1.205),(.123,1.13)],.026,.205,'chest','Chassis graphite',.033,.83)
formed('Chest perimeter pressed surround',[(-.124,1.165),(-.150,1.21),(-.150,1.425),(-.115,1.463),(.115,1.463),(.150,1.425),(.150,1.21),(.124,1.165)],-.124,.018,'chest','Machined steel',.012,.88)
formed('Recessed chest hatch gasket',[(-.105,1.18),(-.133,1.215),(-.133,1.415),(-.11,1.429),(.11,1.429),(.133,1.415),(.133,1.215),(.105,1.18)],-.145,.010,'chest','Rubber',.006,.94)
formed('Chamfered removable chest hatch',[(-.104,1.186),(-.126,1.218),(-.126,1.408),(-.108,1.423),(.108,1.423),(.126,1.408),(.126,1.218),(.104,1.186)],-.146,.009,'chest','Dark titanium',.009,.91)
for s in [-1,1]:
 formed('Narrow stepped thorax guard',[(s*.139,1.175),(s*.177,1.216),(s*.184,1.403),(s*.157,1.502),(s*.125,1.51),(s*.134,1.449),(s*.153,1.399),(s*.153,1.242),(s*.124,1.191)],-.122,.043,'chest','Safety yellow',.010,.76)
 for z in [1.245,1.315,1.382]:
  cyl('Guard recessed mounting well',(s*.171,-.156,z),.008,.006,'chest','Recess black',(0,-1,0),24)
  bolt((s*.171,-.161,z),'chest',.003)
 formed('Clavicle socket bridge',[(s*.134,1.477),(s*.151,1.515),(s*.204,1.496),(s*.204,1.463),(s*.168,1.457)],-.03,.14,'chest','Dark titanium',.008)
 for z in [1.463,1.485]:bolt((s*.174,-.119,z),'chest',.004)
box('Chest identification strip',(0,-.162,1.439),(.226,.010,.022),'chest','Safety yellow',.002)
stencil('C-17  /  SERVICE UNIT',(0,-.168,1.434),.009,'chest')
for s in [-1,1]:
 aperture('Lower torso open attachment clevis',[(s*.08,1.137),(s*.122,1.137),(s*.122,1.183),(s*.08,1.183)],[(s*.09,1.148),(s*.111,1.148),(s*.111,1.172),(s*.09,1.172)],-.101,.040,'chest')
for x in [-.048,-.024,0,.024,.048]:box('Abdominal heat sink fin',(x,-.077,1.093),(.007,.109,.023),'waist','Machined steel',.001)

# Layered, split joint covers; exposed concentric bearings remain readable.
discard([n+' yellow outer bumper' for n in ['Shoulder gearbox','Hip reduction drive','Knee','Ankle']])
for side,s in [('L',1),('R',-1)]:
 upper='shoulder_'+side;lower='forearm_'+side;hand='hand_'+side;thigh='thigh_'+side;shin='shin_'+side;foot='foot_'+side;toe='toe_'+side
 group='03 Left arm' if s==1 else '04 Right arm'
 sector('Shoulder crescent impact casting',(s*.277,0,1.45),.080,.102,.023,12,170,upper)
 sideformed('Shoulder hanging scalloped wing',[(.065,1.496),(.104,1.459),(.09,1.382),(.055,1.355),(-.014,1.368),(-.035,1.42),(-.019,1.477)],s*.297,.025,upper,'Safety yellow',.007)
 for y,z in [(.062,1.473),(.072,1.408),(.015,1.387)]:cyl('Shoulder guard inset socket',(s*.316,y,z),.008,.005,upper,'Recess black',(s,0,0),20);bolt((s*.32,y,z),upper,.0035,(s,0,0))
 formed('Upper arm split cast housing',[(s*.218,1.402),(s*.256,1.42),(s*.295,1.286),(s*.281,1.249),(s*.242,1.264),(s*.225,1.338)],-.014,.080,upper,'Dark titanium',.013,.76)
 formed('Upper arm raised service spine',[(s*.236,1.389),(s*.25,1.394),(s*.28,1.285),(s*.265,1.274)],-.067,.007,upper,'Machined steel',.002)
 for z in [1.305,1.372]:bolt((s*(.271-(z-1.305)*.26),-.080,z),upper,.003)
 formed('Forearm faceted main casting',[(s*.233,1.185),(s*.271,1.202),(s*.301,1.172),(s*.350,1.075),(s*.350,1.036),(s*.326,1.024),(s*.284,1.036)],-.003,.091,lower,'Chassis graphite',.018,.73)
 formed('Forearm steel inspection hatch',[(s*.252,1.171),(s*.272,1.178),(s*.321,1.075),(s*.311,1.042),(s*.294,1.051)],-.058,.009,lower,'Dark titanium',.006,.82)
 formed('Forearm narrow yellow edge cover',[(s*.28,1.192),(s*.302,1.174),(s*.345,1.078),(s*.339,1.043),(s*.325,1.041),(s*.328,1.079),(s*.289,1.16)],-.045,.046,lower,'Safety yellow',.006,.76)
 for z in [1.074,1.123,1.165]:
  x=s*(.33-(z-1.074)*.40);cyl('Forearm recessed edge screw',(x,-.078,z),.006,.003,lower,'Recess black',(0,-1,0),20)
 sector('Elbow open rear bearing guard',(s*.313,.005,1.22),.049,.059,.012,205,345,lower,'Machined steel')
 # Gripper has clevis cheeks around each hinge and flat segmented phalanges.
 for finger in ['index','middle','thumb']:
  for seg in [1,2]:
   bn=finger+str(seg)+'_'+side;a,b,_=bones[bn]
   for ss in [-1,1]:
    o=box('Finger clevis cheek',tuple((a+b)/2+Vector((ss*.008,0,0))),(.003,.018,(b-a).length*.77),bn,'Dark titanium',.002)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
 group='06 Left leg' if s==1 else '07 Right leg'
 sector('Hip crown guard',(s*.198,0,1.015),.087,.108,.026,5,174,thigh)
 formed('Thigh sculpted split casting',[(s*.084,.945),(s*.122,.97),(s*.193,.918),(s*.204,.79),(s*.188,.690),(s*.160,.657),(s*.107,.679),(s*.09,.824)],-.035,.110,thigh,'Chassis graphite',.023,.72)
 formed('Thigh stepped face armour',[(s*.100,.902),(s*.134,.921),(s*.175,.877),(s*.180,.735),(s*.153,.681),(s*.119,.706),(s*.106,.81)],-.095,.010,thigh,'Dark titanium',.014,.80)
 sideformed('Thigh wrapping lateral shield',[(.071,.962),(.112,.923),(.106,.823),(.078,.731),(.035,.712),(-.014,.749),(-.055,.891),(-.035,.95)],s*.207,.027,thigh,'Safety yellow',.010)
 for y,z in [(.045,.924),(.066,.869),(.035,.771)]:
  cyl('Thigh shield counterbore',(s*.228,y,z),.009,.004,thigh,'Recess black',(s,0,0),24);bolt((s*.231,y,z),thigh,.004,(s,0,0))
 # Large side inspection plate is shaped independently of the forward thigh skin.
 sideformed('Thigh medial transmission plate',[(-.041,.865),(.032,.879),(.056,.847),(.04,.739),(-.022,.71),(-.043,.751)],s*.084,.012,thigh,'Dark titanium',.005)
 for z in [.741,.828,.857]:bolt((s*.071,0,z),thigh,.004,(-s,0,0))
 formed('Knee layered kneecap casting',[(s*.104,.642),(s*.181,.642),(s*.197,.610),(s*.181,.554),(s*.153,.537),(s*.108,.56),(s*.093,.602)],-.074,.030,shin,'Dark titanium',.020,.70)
 sector('Knee upper guard',(s*.205,-.008,.590),.063,.077,.018,24,154,shin)
 formed('Shin contoured load casting',[(s*.095,.535),(s*.165,.545),(s*.198,.509),(s*.184,.419),(s*.17,.260),(s*.143,.211),(s*.112,.248),(s*.099,.386)],-.008,.098,shin,'Chassis graphite',.022,.72)
 formed('Shin raised offset inspection hatch',[(s*.119,.504),(s*.167,.499),(s*.176,.467),(s*.157,.28),(s*.14,.252),(s*.12,.307),(s*.111,.434)],-.068,.012,shin,'Dark titanium',.010,.78)
 formed('Shin lower secondary armour',[(s*.108,.355),(s*.121,.362),(s*.141,.242),(s*.126,.224),(s*.109,.26)],-.053,.023,shin,'Machined steel',.007)
 sideformed('Shin wrapping yellow side splint',[(-.059,.483),(-.01,.492),(.038,.451),(.025,.349),(.012,.271),(-.018,.24),(-.042,.284)],s*.182,.020,shin,'Safety yellow',.007)
 relief_slots(s*.147,-.093,.429,shin,count=3,span=.022)
 for z in [.279,.483]:
  cyl('Shin round inspection recess',(s*.146,-.093,z),.012,.003,shin,'Recess black',(0,-1,0),24)
  ring('Inspection port retaining lip',(s*.146,-.096,z),.010,.0015,shin,'Machined steel',(0,-1,0))
 # Structural paired rear channels replace the former exposed hydraulic details.
 for dx in [-.025,.025]:
  aperture('Rear shin open structural channel',[(s*.15+dx-.008,.25),(s*.15+dx+.008,.25),(s*.15+dx+.008,.494),(s*.15+dx-.008,.494)],[(s*.15+dx-.004,.266),(s*.15+dx+.004,.266),(s*.15+dx+.004,.478),(s*.15+dx-.004,.478)],.054,.023,shin,'Dark titanium')
 # Low foot with sculpted instep, separate toe sectors and a projecting heel.
 formed('Foot instep faceted casting',[(s*.08,.061),(s*.082,.117),(s*.113,.173),(s*.17,.174),(s*.209,.122),(s*.22,.057)],-.052,.155,foot,'Dark titanium',.017,.65)
 formed('Ankle split yellow saddle',[(s*.103,.147),(s*.106,.214),(s*.133,.23),(s*.169,.215),(s*.19,.161),(s*.17,.144),(s*.157,.183),(s*.129,.188),(s*.126,.15)],-.06,.063,foot,'Safety yellow',.009,.90)
 for dx in [-.056,0,.056]:
  x=s*.15+dx
  formed('Toe sloped articulated cap',[(x-.023,.055),(x-.022,.099),(x-.010,.121),(x+.014,.112),(x+.024,.081),(x+.021,.05)],-.179,.143,toe,'Dark titanium',.010,.70)
  formed('Toe yellow impact edge',[(x-.019,.052),(x-.02,.079),(x-.012,.086),(x+.019,.071),(x+.018,.05)],-.255,.018,toe,'Safety yellow',.003)
  box('Toe longitudinal split',(x,-.184,.120),(.005,.090,.003),toe,'Recess black',.001)
  bolt((x,-.193,.123),toe,.003,(0,0,1))
 for ss in [-1,1]:
  cyl('Instep exposed pivot',(s*.15+ss*.068,-.069,.111),.021,.011,foot,'Chassis graphite',(1,0,0),32)
  ring('Instep pivot steel lip',(s*.15+ss*.075,-.069,.111),.017,.002,foot,'Machined steel')

print('C17_REFINED_PRIMARY_SHAPES',len(parts),flush=True)

group='01 Sensor head'
discard(['Sensor head faceted casting','Yellow sensor head shell','Head top service lid'])
formed('Compact optics cast housing',[(-.125,1.625),(-.145,1.66),(-.14,1.757),(-.104,1.799),(.104,1.799),(.14,1.757),(.145,1.66),(.125,1.625)],.001,.170,'head','Chassis graphite',.015,.87)
formed('Optics folded yellow brow',[(-.137,1.735),(-.134,1.772),(-.106,1.797),(.106,1.797),(.134,1.772),(.137,1.735),(.113,1.74),(.099,1.773),(-.099,1.773),(-.113,1.74)],-.020,.173,'head','Safety yellow',.006,.97)
formed('Optics crown inset lid',[(-.092,1.781),(-.078,1.815),(.079,1.815),(.093,1.781)],.012,.116,'head','Dark titanium',.006)
for s in [-1,1]:
 sideformed('Sensor cheek inset guard',[(-.05,1.649),(.035,1.647),(.06,1.67),(.06,1.727),(.029,1.751),(-.046,1.741)],s*.146,.010,'head','Safety yellow',.005)
 for z in [1.658,1.737]:bolt((s*.158,-.031,z),'head',.004,(s,0,0))
 for i in range(4):box('Optics crown vent',(s*.045,.012+i*.013,1.815),(.055,.005,.003),'head','Recess black',.0005)
box('Optics underface sensor bank',(0,-.098,1.633),(.142,.028,.021),'head','Chassis graphite',.004)
for x in [-.047,-.023,0,.023,.047]:cyl('Underface sensor aperture',(x,-.115,1.631),.0045,.003,'head','Recess black',(0,-1,0),20)
group='02 Torso and power pack'
discard(['Rear removable service lid','Yellow rear impact rail'])
formed('Rear field-service hatch',[(-.095,1.204),(-.116,1.225),(-.116,1.425),(-.098,1.445),(.098,1.445),(.116,1.425),(.116,1.225),(.095,1.204)],-.255,.012,'chest','Dark titanium',.009,.91)
# Rotate the rear hatch around Z: its formed face should point rearward.
o=parts[-1]
for v in o.data.vertices:v.co.y=-v.co.y
for s in [-1,1]:
 sideformed('Backpack folded impact spine',[(.125,1.174),(.212,1.183),(.246,1.209),(.246,1.455),(.214,1.492),(.143,1.506),(.132,1.473),(.202,1.455),(.211,1.218),(.125,1.209)],s*.151,.017,'chest','Safety yellow',.005)
 for z in [1.23,1.43]:
  box('Rear hatch captive latch',(s*.111,.271,z),(.019,.015,.034),'chest','Chassis graphite',.003)
  cyl('Rear latch cam',(s*.111,.282,z),.006,.004,'chest','Machined steel',(0,1,0),20)
 for z in [1.16,1.186]:box('Power pack underside fin',(s*.06,.173,z),(.085,.113,.007),'chest','Machined steel',.001)
stencil('POWER MODULE  /  17',(0,.265,1.406),.009,'chest',True)
stencil('ISOLATE BEFORE SERVICE',(0,.269,1.245),.006,'chest',True)

# Bake existing object transforms, then change the actual primary proportions.
for o in parts:
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
 joint=o['joint'];sign=1 if joint.endswith('_L') else -1
 if joint=='head':
  for v in o.data.vertices:
   v.co.x*=.78;v.co.y=-.012+(v.co.y+.012)*.82;v.co.z=1.699+(v.co.z-1.699)*.82
 elif joint.startswith('forearm_'):
  elbow=o.name.startswith('Elbow')
  for v in o.data.vertices:
   if elbow:v.co.z-=.03
   else:
    v.co.z=.84+(v.co.z-1.01)*(.35/.21)
    v.co.x=sign*(.265+(abs(v.co.x)-.265)*(.085/.055))
 elif joint.startswith(('hand_','index','middle','thumb')):
  for v in o.data.vertices:v.co.z-=.17;v.co.x+=sign*.03
 elif joint.startswith('shoulder_') and o.name.startswith('Upper arm'):
  for v in o.data.vertices:v.co.z=1.45+(v.co.z-1.45)*(.26/.23)
 elif joint.startswith('thigh_') and not o.name.startswith(('Hip ','Hip crown')):
  for v in o.data.vertices:v.co.z=1.015+(v.co.z-1.015)*(.465/.425)
 elif joint.startswith('shin_'):
  knee=o.name.startswith('Knee')
  for v in o.data.vertices:v.co.z=v.co.z-.04 if knee else .178+(v.co.z-.178)*(.372/.412)
 # Correct mirrored sculpted plates and keep actual planar armour faces planar.
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 for poly in o.data.polygons:
  if len(poly.vertices)>4:poly.use_smooth=False

for name,(h,t,parent) in list(bones.items()):
 h=h.copy();t=t.copy();sign=1 if name.endswith('_L') else -1
 if name.startswith('forearm_'):h.z-=.03;t.z-=.17;t.x+=sign*.03
 elif name.startswith(('hand_','index','middle','thumb')):h.z-=.17;t.z-=.17;h.x+=sign*.03;t.x+=sign*.03
 elif name.startswith('shoulder_'):t.z-=.03
 elif name.startswith('thigh_'):t.z-=.04
 elif name.startswith('shin_'):h.z-=.04
 elif name in ['head','camera_mount']:
  for p in [h,t]:p.x*=.78;p.y=-.012+(p.y+.012)*.82;p.z=1.699+(p.z-1.699)*.82
 bones[name]=(h,t,parent)

# Restrained coating wear and distinct material response, without a silver wash.
for name in ['Safety yellow','Chassis graphite','Dark titanium','Machined steel']:
 m=mats[name];nt=m.node_tree;nt.nodes.clear();p=nt.nodes.new('ShaderNodeBsdfPrincipled');out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(p.outputs[0],out.inputs[0])
 col={'Safety yellow':(.50,.285,.014),'Chassis graphite':(.024,.030,.032),'Dark titanium':(.085,.096,.098),'Machined steel':(.18,.195,.20)}[name]
 m.diffuse_color=(*col,1);p.inputs['Metallic'].default_value=.24 if name=='Safety yellow' else .63;p.inputs['Roughness'].default_value=.46
 tc=nt.nodes.new('ShaderNodeTexCoord');noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=145;noise.inputs['Detail'].default_value=2;nt.links.new(tc.outputs['Object'],noise.inputs['Vector'])
 cr=nt.nodes.new('ShaderNodeValToRGB');cr.color_ramp.elements[0].color=(*[v*.66 for v in col],1);cr.color_ramp.elements[1].color=(*[v*1.13 for v in col],1);nt.links.new(noise.outputs['Fac'],cr.inputs[0])
 geom=nt.nodes.new('ShaderNodeNewGeometry');edge=nt.nodes.new('ShaderNodeMapRange');edge.inputs['From Min'].default_value=.506;edge.inputs['From Max'].default_value=.535;nt.links.new(geom.outputs['Pointiness'],edge.inputs['Value'])
 chip=nt.nodes.new('ShaderNodeMath');chip.operation='GREATER_THAN';chip.inputs[1].default_value=.58;nt.links.new(noise.outputs['Fac'],chip.inputs[0])
 mult=nt.nodes.new('ShaderNodeMath');mult.operation='MULTIPLY';nt.links.new(edge.outputs[0],mult.inputs[0]);nt.links.new(chip.outputs[0],mult.inputs[1])
 mix=nt.nodes.new('ShaderNodeMixRGB');nt.links.new(mult.outputs[0],mix.inputs[0]);nt.links.new(cr.outputs[0],mix.inputs[1]);mix.inputs[2].default_value=(.17,.18,.175,1);nt.links.new(mix.outputs[0],p.inputs['Base Color'])
 rough=nt.nodes.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.34;rough.inputs['To Max'].default_value=.60;nt.links.new(noise.outputs['Fac'],rough.inputs[0]);nt.links.new(rough.outputs[0],p.inputs['Roughness'])
 bump=nt.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.10;bump.inputs['Distance'].default_value=.00008;nt.links.new(noise.outputs['Fac'],bump.inputs['Height']);nt.links.new(bump.outputs[0],p.inputs['Normal'])
print('C17_REFINED_PROPORTIONS_AND_MATERIALS',flush=True)
