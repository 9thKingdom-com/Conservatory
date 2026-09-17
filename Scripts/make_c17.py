"""C-17: original mechanical character modelled against robot-1.png.
Blender 5.1. Metre modelling space; use the verified Unreal import preset for centimetres. No external asset dependencies.
"""
import bpy, math, random, json
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'SourceAssets/C17';OUT.mkdir(parents=True,exist_ok=True)
random.seed(17);bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.fps=30
# Tileable paint wear. These textures, rather than Blender-only shaders, also ship to Unreal.
import numpy as np
rng=np.random.default_rng(17);N=512
colors={'Ochre':(.60,.34,.035),'Graphite':(.075,.09,.095),'Steel':(.30,.33,.32),'Rubber':(.015,.02,.021),'Sensor':(.012,.035,.045),'Ivory':(.78,.76,.61),'Amber':(1,.49,.06)}
mats={}
for name,col in colors.items():
 m=bpy.data.materials.new('C17_'+name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Metallic'].default_value=.65 if name in ['Ochre','Graphite','Steel'] else .05;p.inputs['Roughness'].default_value=.32 if name=='Sensor' else .58
 m.diffuse_color=(*col,1)
 if name in ['Ochre','Graphite','Steel']:
  noise=rng.random((N,N));a=np.ones((N,N,4),dtype=np.float32);base=np.array(col);a[:,:,:3]=base*(.80+.3*noise[:,:,None])
  # Small paint losses, oxide flecks and hairline service scratches.
  for k in range(700):
   x,y=rng.integers(0,N,2);length=int(rng.integers(1,14));v=(.11,.115,.105) if name=='Ochre' else (.18,.17,.13)
   a[y,min(x,N-1):min(x+length,N),:3]=v
  img=bpy.data.images.new('T_C17_'+name,N,N);img.pixels.foreach_set(a.ravel());img.filepath_raw=str(OUT/('T_C17_'+name+'.png'));img.file_format='PNG';img.save();img.pack()
  tex=m.node_tree.nodes.new('ShaderNodeTexImage');tex.image=img;m.node_tree.links.new(tex.outputs['Color'],p.inputs['Base Color'])
 if name=='Amber':p.inputs['Emission Color'].default_value=(*col,1);p.inputs['Emission Strength'].default_value=3
 mats[name]=m
parts=[]
def finish(o,name,bone,mat,bevel=0):
 o.name=name;o.data.materials.append(mats[mat]);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Machined edge','BEVEL');mod.width=bevel;mod.segments=2
  bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
 for poly in o.data.polygons:poly.use_smooth=len(poly.vertices)==4 and name.startswith('Joint')
 g=o.vertex_groups.new(name=bone);g.add(list(range(len(o.data.vertices))),1,'REPLACE');parts.append(o);return o

def box(name,pos,size,bone,mat='Graphite',bevel=.006):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.scale=size;return finish(o,name,bone,mat,bevel)
def cyl(name,pos,r,depth,bone,mat='Steel',axis=(1,0,0),verts=20):
 bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=pos);o=bpy.context.object;o.rotation_mode='QUATERNION';o.rotation_quaternion=Vector((0,0,1)).rotation_difference(Vector(axis));return finish(o,name,bone,mat,.002)
def tube(name,a,b,r,bone,mat='Steel',verts=12):
 a,b=Vector(a),Vector(b);return cyl(name,(a+b)*.5,r,(b-a).length,bone,mat,b-a,verts)
def plate(name,a,b,width,depth,bone,mat='Ochre'):
 a,b=Vector(a),Vector(b);o=box(name,(a+b)/2,(width,depth,(b-a).length),bone,mat);o.rotation_mode='QUATERNION';o.rotation_quaternion=Vector((0,0,1)).rotation_difference(b-a);return o
def text(name,body,pos,size,bone,mat='Ivory'):
 bpy.ops.object.text_add(location=pos,rotation=(math.pi/2,0,0));o=bpy.context.object;o.data.body=body;o.data.size=size;o.data.align_x='CENTER';o.data.extrude=.00025;o.data.space_line=1.15;bpy.ops.object.convert(target='MESH');return finish(bpy.context.object,name,bone,mat)
def bolt(pos,bone,r=.005,axis=(0,-1,0)):return cyl('Captive bolt',pos,r,.005,bone,'Steel',axis,6)
# Humanoid deform skeleton, plus explicit functional attachments.
bones={}
def bone(n,h,t,parent=None):bones[n]=(Vector(h),Vector(t),parent)
bone('root',(0,0,0),(0,0,.12));bone('pelvis',(0,0,.76),(0,0,.87),'root');bone('spine_01',(0,0,.87),(0,0,1.01),'pelvis');bone('spine_02',(0,0,1.01),(0,0,1.22),'spine_01');bone('neck_01',(0,0,1.22),(0,0,1.32),'spine_02');bone('head',(0,0,1.32),(0,0,1.48),'neck_01')
for side,s in [('l',1),('r',-1)]:
 bone('clavicle_'+side,(0,0,1.19),(s*.245,0,1.19),'spine_02');bone('upperarm_'+side,(s*.245,0,1.19),(s*.335,0,.96),'clavicle_'+side);bone('lowerarm_'+side,(s*.335,0,.96),(s*.375,-.005,.745),'upperarm_'+side);bone('hand_'+side,(s*.375,-.005,.745),(s*.38,-.005,.665),'lowerarm_'+side)
 for finger,dx,dy in [('index',-.033,-.027),('middle',.033,-.027),('thumb',0,.04)]:
  x=s*(.38+dx);y=dy
  bone(finger+'_01_'+side,(x,y,.674),(x,y,.625),'hand_'+side);bone(finger+'_02_'+side,(x,y,.625),(x,y-(.027 if finger=='thumb' else -.012),.592),finger+'_01_'+side)
 bone('thigh_'+side,(s*.135,0,.78),(s*.145,-.005,.455),'pelvis');bone('calf_'+side,(s*.145,-.005,.455),(s*.145,0,.145),'thigh_'+side);bone('foot_'+side,(s*.145,0,.145),(s*.145,-.13,.068),'calf_'+side);bone('ball_'+side,(s*.145,-.13,.068),(s*.145,-.21,.068),'foot_'+side)
 bone('tool_'+side,(s*.38,-.005,.63),(s*.38,-.10,.63),'hand_'+side)
bone('camera_mount',(0,-.18,1.395),(0,-.24,1.395),'head');bone('cargo_mount',(0,.205,1.03),(0,.26,1.03),'spine_02')
# Torso: protective yoke, replaceable central service panel and compact power pack.
box('Pelvis gearbox',(0,0,.79),(.245,.205,.18),'pelvis',bevel=.025)
box('Hip yellow armour',(0,-.115,.79),(.19,.025,.12),'pelvis','Ochre',.015)
for x in [-.087,.087]:bolt((x,-.132,.835),'pelvis')
cyl('Waist bearing',(0,0,.88),.09,.065,'spine_01','Rubber',(0,0,1));cyl('Waist rotation collar',(0,0,.913),.077,.025,'spine_01','Steel',(0,0,1))
box('Torso inner chassis',(0,.015,1.07),(.325,.22,.30),'spine_02','Graphite',.035)
box('Front titanium service hatch',(0,-.112,1.07),(.252,.037,.24),'spine_02','Steel',.018)
for s in [-1,1]:
 o=box('Yellow torso rail',(s*.153,-.10,1.075),(.047,.08,.30),'spine_02','Ochre',.012);o.rotation_euler[1]=s*-.10
 for z in [.966,1.065,1.176]:bolt((s*.151,-.145,z),'spine_02',.006)
 box('Service hatch latch',(s*.098,-.141,1.03),(.018,.015,.045),'spine_02','Graphite',.004)
box('Upper hazard stripe',(0,-.135,1.173),(.20,.007,.015),'spine_02','Ochre',.001)
for x in [-.09,-.045,0,.045,.09]:
 o=box('Stripe divider',(x,-.140,1.173),(.012,.004,.016),'spine_02','Graphite',.0005);o.rotation_euler[1]=-.4
text('Unit number','C-17',(0,-.139,1.105),.043,'spine_02')
text('Chest designation','CONSERVATORY',(0,-.139,.977),.012,'spine_02')
# Botanical badge: three tapered leaves and stem.
for x,z,rot in [(-.022,1.048,-.55),(.022,1.048,.55),(0,1.063,0)]:
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1,location=(x,-.14,z));o=bpy.context.object;o.scale=(.010,.002,.023);o.rotation_euler[1]=rot;finish(o,'Leaf emblem','spine_02','Ivory')
tube('Leaf stem',(0,-.142,1.013),(0,-.142,1.055),.002,'spine_02','Ivory')
box('Backpack power module',(0,.155,1.07),(.27,.13,.28),'spine_02','Graphite',.022)
box('Backpack removable cover',(0,.229,1.075),(.23,.021,.215),'spine_02','Steel',.012)
for s in [-1,1]:
 box('Power pack guard',(s*.14,.19,1.085),(.022,.10,.25),'spine_02','Ochre',.007)
 for z in [1.005,1.025,1.045,1.065,1.085]:box('Cooling fin',(s*.068,.244,z),(.08,.015,.007),'spine_02','Rubber',.001)
 tube('Pack lifting handle',(s*.08,.17,1.23),(s*.08,.21,1.26),.010,'spine_02','Steel')
tube('Pack handle bridge',(-.08,.21,1.26),(.08,.21,1.26),.010,'spine_02')
# Neck cable race and sensor head.
cyl('Neck servo',(0,0,1.27),.048,.085,'neck_01','Steel',(0,0,1));cyl('Neck gaiter',(0,0,1.28),.061,.036,'neck_01','Rubber',(0,0,1))
box('Sensor head housing',(0,-.015,1.397),(.365,.255,.215),'head','Ochre',.030)
box('Sensor face bezel',(0,-.15,1.389),(.325,.038,.165),'head','Steel',.018)
box('Sensor dark inset',(0,-.174,1.389),(.296,.015,.138),'head','Rubber',.013)
box('Head top armour',(0,-.003,1.510),(.27,.205,.018),'head','Graphite',.007)
for s in [-1,1]:
 cyl('Head swivel', (s*.188,.012,1.40),.057,.025,'head','Graphite',(1,0,0));cyl('Head bearing cap',(s*.204,.012,1.40),.035,.008,'head','Steel',(1,0,0))
 for z in [1.337,1.461]:bolt((s*.143,-.176,z),'head')
# Asymmetrical stereo and spectral cameras, all opaque coated optics for game rendering.
for x,z,r in [(.086,1.398,.054),(-.085,1.39,.033),(-.018,1.351,.016)]:
 cyl('Camera outer shroud',(x,-.188,z),r+.012,.031,'head','Graphite',(0,-1,0),32)
 cyl('Camera silver ring',(x,-.207,z),r+.004,.007,'head','Steel',(0,-1,0),32)
 cyl('Camera black rim',(x,-.214,z),r,.008,'head','Rubber',(0,-1,0),32)
 cyl('Coated optical glass',(x,-.219,z),r*.77,.005,'head','Sensor',(0,-1,0),32)
 cyl('Lens inner iris',(x,-.223,z),r*.40,.002,'head','Graphite',(0,-1,0),24)
box('Status bar bezel',(-.052,-.19,1.448),(.132,.017,.024),'head','Graphite',.004)
for i in range(5):box('Status LED',(-.101+i*.023,-.201,1.448),(.017,.007,.011),'head','Amber',.002)
tube('Antenna base',(-.13,.185,1.19),(-.13,.185,1.26),.020,'spine_02','Ochre')
tube('Antenna mast',(-.13,.185,1.26),(-.13,.185,1.67),.004,'spine_02','Steel');cyl('Antenna tip',(-.13,.185,1.67),.007,.022,'spine_02','Rubber',(0,0,1))
# Limbs. Bearings are explicit; armour is rigidly bound to one bone.
for side,s in [('l',1),('r',-1)]:
 upper='upperarm_'+side;lower='lowerarm_'+side;hand='hand_'+side;thigh='thigh_'+side;calf='calf_'+side;foot='foot_'+side
 for label,p,r,b in [('shoulder',(s*.25,0,1.19),.083,upper),('elbow',(s*.335,0,.96),.054,lower),('hip',(s*.137,0,.78),.077,thigh),('knee',(s*.145,-.005,.455),.065,calf),('ankle',(s*.145,0,.145),.044,foot)]:
  cyl('Joint '+label,p,r,.085,b,'Rubber')
  for dd in [-1,1]:
   q=Vector(p)+Vector((dd*.047,0,0));cyl('Bearing machined rim',q,r*.89,.012,b,'Steel');cyl('Bearing central cap',q+Vector((dd*.008,0,0)),r*.62,.013,b,'Graphite');cyl('Bearing spindle',q+Vector((dd*.015,0,0)),r*.25,.009,b,'Steel')
 box('Shoulder cap',(s*.264,0,1.245),(.126,.17,.058),'clavicle_'+side,'Ochre',.018)
 plate('Upper arm actuator',(s*.274,0,1.15),(s*.323,0,1.003),.064,.076,upper,'Steel')
 plate('Upper arm guard',(s*.29,-.054,1.16),(s*.329,-.054,1.03),.085,.031,upper)
 plate('Forearm core',(s*.341,0,.922),(s*.373,0,.777),.092,.093,lower,'Steel')
 plate('Forearm armour',(s*.344,-.060,.922),(s*.374,-.060,.79),.105,.033,lower)
 for z in [.812,.887]:bolt((s*.355,-.081,z),lower)
 text('Forearm stencil','TEND',(s*.355,-.081,.843),.014,lower)
 tube('Arm hydraulic barrel',(s*.40,.016,.906),(s*.411,.016,.82),.011,lower,'Graphite');tube('Arm hydraulic rod',(s*.411,.016,.82),(s*.407,.016,.757),.006,lower)
 cyl('Wrist collar',(s*.375,-.005,.749),.043,.032,hand,'Graphite',(0,0,1))
 box('Gripper palm',(s*.38,-.005,.692),(.092,.082,.075),hand,'Steel',.010)
 box('Palm tool coupling',(s*.38,-.052,.693),(.057,.020,.049),hand,'Graphite',.006)
 for finger in ['index','middle','thumb']:
  for seg in ['01','02']:
   b=finger+'_'+seg+'_'+side;h,t,_=bones[b];tube('Finger hinge',h-Vector((.012,0,0)),h+Vector((.012,0,0)),.009,b,'Graphite');plate('Articulated finger',h,t,.019,.023,b,'Steel');
   if seg=='02':box('Gripper traction pad',(t.x,t.y-.008,t.z+.010),(.022,.015,.025),b,'Rubber',.003)
 plate('Thigh chassis',(s*.139,0,.715),(s*.145,0,.515),.12,.135,thigh,'Graphite')
 plate('Thigh front plate',(s*.14,-.081,.70),(s*.145,-.081,.528),.105,.026,thigh,'Steel')
 plate('Thigh side yellow rail',(s*.205,-.015,.716),(s*.210,-.015,.528),.032,.126,thigh)
 for z in [.55,.676]:bolt((s*.145,-.10,z),thigh)
 box('Knee front bumper',(s*.145,-.074,.455),(.097,.039,.065),calf,'Ochre',.012)
 plate('Shin main beam',(s*.145,0,.407),(s*.145,0,.194),.085,.086,calf,'Graphite')
 plate('Shin titanium plate',(s*.145,-.058,.393),(s*.145,-.058,.22),.103,.026,calf,'Steel')
 plate('Shin ochre rail',(s*.199,-.035,.402),(s*.182,-.035,.213),.025,.052,calf)
 tube('Shin cylinder',(s*.098,.053,.399),(s*.098,.053,.275),.018,calf,'Graphite');tube('Shin piston',(s*.098,.053,.275),(s*.098,.053,.182),.009,calf)
 for z in [.236,.375]:bolt((s*.145,-.077,z),calf)
 box('Heel sole',(s*.145,.014,.042),(.158,.16,.068),foot,'Rubber',.012)
 box('Heel shell',(s*.145,.009,.085),(.133,.145,.055),foot,'Ochre',.014)
 box('Toe traction sole',(s*.145,-.132,.037),(.17,.16,.058),'ball_'+side,'Rubber',.013)
 box('Toe armour',(s*.145,-.124,.079),(.16,.151,.034),'ball_'+side,'Steel',.009)
 for dx in [-.053,0,.053]:box('Toe yellow rib',(s*.145+dx,-.125,.099),(.019,.12,.014),'ball_'+side,'Ochre',.003)
 for yy in [-.192,-.16,-.126]:box('Toe tread',(s*.145,yy,.024),(.176,.013,.028),'ball_'+side,'Rubber',.002)
# Join into one skinned mesh; every vertex retains exactly one rigid bone weight.
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();mesh=bpy.context.object;mesh.name='SK_C17';bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
# Fix imported normals and supply non-overlapping UV islands for future unique texture painting.
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False) if hasattr(bpy.ops.mesh,'normals_make_consistent') else None
bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.015);bpy.ops.object.mode_set(mode='OBJECT')
armdata=bpy.data.armatures.new('C17_Skeleton');arm=bpy.data.objects.new('C17_Rig',armdata);scene.collection.objects.link(arm);bpy.context.view_layer.objects.active=arm;mesh.select_set(False);arm.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
for n,(h,t,parent) in bones.items():
 b=armdata.edit_bones.new(n);b.head=h;b.tail=t
 if parent:b.parent=armdata.edit_bones[parent]
bpy.ops.object.mode_set(mode='OBJECT');arm.show_in_front=True
mesh.parent=arm;mod=mesh.modifiers.new('Rigid mechanical skin','ARMATURE');mod.object=arm
# Analytic 2-bone IK used to author actions, then baked to ordinary bone transforms.
def pose_bone(n,h,t):
 b=arm.pose.bones[n];rest=arm.data.bones[n];q=(rest.tail_local-rest.head_local).rotation_difference(Vector(t)-Vector(h)) @ rest.matrix_local.to_quaternion();b.matrix=Matrix.LocRotScale(Vector(h),q,Vector((1,1,1)));bpy.context.view_layer.update()
def ik(a,b,end,bend):
 h=arm.pose.bones[a].head.copy();target=Vector(end);L1=(bones[a][1]-bones[a][0]).length;L2=(bones[b][1]-bones[b][0]).length;v=target-h;dist=min(v.length,L1+L2-.0001);dist=max(dist,abs(L1-L2)+.0001);d=v.normalized();along=(L1*L1-L2*L2+dist*dist)/(2*dist);p=Vector(bend);p=(p-d*p.dot(d)).normalized();mid=h+d*along+p*math.sqrt(max(0,L1*L1-along*along));target=h+d*dist;pose_bone(a,h,mid);pose_bone(b,mid,target);return target
clips={'Idle':90,'Walk':32,'CarryWalk':40,'Lift':90,'ShelfPick':90,'Chop':60,'BreakStone':60}
for clip,endframe in clips.items():
 arm.animation_data_clear();action=bpy.data.actions.new('C17_'+clip);arm.animation_data_create();arm.animation_data.action=action
 for f in range(1,endframe+2):
  scene.frame_set(f);t=(f-1)/endframe;phase=t*math.tau
  for p in arm.pose.bones:p.matrix_basis=Matrix.Identity(4);p.rotation_mode='QUATERNION'
  bob=.008*(1-math.cos(phase*2)) if clip in ['Walk','CarryWalk'] else .002*math.sin(phase)
  arm.pose.bones['pelvis'].location.y=bob-(.25*math.sin(math.pi*t)**2 if clip=='Lift' else 0)
  bpy.context.view_layer.update()
  for side,s in [('l',1),('r',-1)]:
   cycle=phase+(0 if s==1 else math.pi);stride=.105 if clip=='Walk' else .075
   y=stride*math.cos(cycle) if clip in ['Walk','CarryWalk'] else 0
   lift=.045*max(0,math.sin(cycle)) if clip in ['Walk','CarryWalk'] else 0
   ankle=ik('thigh_'+side,'calf_'+side,(s*.145,y,.145+lift),(0,-1,0))
   pose_bone('foot_'+side,ankle,ankle+Vector((0,-.13,-.077)))
   # Targets define complete work arcs, with hands close together for two-handed tools.
   target=Vector((s*.375,-.005,.745))
   if clip=='Idle':target.y+=.008*math.sin(phase)
   elif clip=='Walk':target.y=-.10*math.cos(cycle);target.z+=.02
   elif clip=='CarryWalk':target=Vector((s*.20,-.30,.96+bob))
   elif clip=='Lift':
    a=(1-math.cos(phase))*.5;target=Vector((s*.19,-.29,.93-.45*math.sin(math.pi*t)**2));
   elif clip=='ShelfPick':
    a=math.sin(math.pi*t)**2;target=Vector((s*(.375-.18*a),-.005-.38*a,.745+.44*a))
   elif clip in ['Chop','BreakStone']:
    # Wind up slowly, strike quickly, recover. In-place; tool/contact supplied by gameplay.
    keys=[(0,0),(.45,1),(.60,.08),(1,0)];a=0
    for (t0,v0),(t1,v1) in zip(keys,keys[1:]):
     if t0<=t<=t1:
      u=(t-t0)/(t1-t0);u=u*u*(3-2*u);a=v0+(v1-v0)*u;break
    target=Vector((s*.12,-.38+.04*a,(.95 if clip=='Chop' else .82)+.49*a))
   wrist=ik('upperarm_'+side,'lowerarm_'+side,target,(s*.7,.3,-.2))
   direction=Vector((0,-.055,-.058)) if clip not in ['Idle','Walk'] else Vector((s*.005,0,-.08));pose_bone('hand_'+side,wrist,wrist+direction)
   if clip not in ['Idle','Walk']:
    for finger in ['index','middle','thumb']:
     p=arm.pose.bones[finger+'_02_'+side];p.rotation_mode='XYZ';p.rotation_euler.x=(.48 if finger!='thumb' else -.48)*math.sin(math.pi*t)**2 if clip not in ['CarryWalk','Chop','BreakStone'] else (.48 if finger!='thumb' else -.48)
  # Quiet sensor scan while idle; keep the work view steady during manipulation.
  p=arm.pose.bones['head'];p.rotation_mode='XYZ';p.rotation_euler.y=.10*math.sin(phase) if clip=='Idle' else .02*math.sin(phase)
  for p in arm.pose.bones:
   p.keyframe_insert('location',frame=f);p.keyframe_insert('rotation_euler' if p.rotation_mode=='XYZ' else 'rotation_quaternion',frame=f);p.keyframe_insert('scale',frame=f)
 action.use_fake_user=True
# Export rig and clips. Unreal legacy import preset uses import_uniform_scale=100.
arm.animation_data_clear()
for p in arm.pose.bones:p.matrix_basis=Matrix.Identity(4)
scene.frame_set(1);bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT');arm.select_set(True);mesh.select_set(True);bpy.context.view_layer.objects.active=arm
# FBX global_scale scales geometry and translation keys consistently.
settings=dict(use_selection=True,object_types={'ARMATURE','MESH'},add_leaf_bones=False,primary_bone_axis='Y',secondary_bone_axis='X',axis_forward='-Y',axis_up='Z',global_scale=100,apply_unit_scale=True,apply_scale_options='FBX_SCALE_ALL',use_armature_deform_only=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,path_mode='STRIP',mesh_smooth_type='FACE')
bpy.ops.export_scene.fbx(filepath=str(OUT/'SK_C17.fbx'),bake_anim=False,**settings)
for clip,frames in clips.items():
 arm.animation_data_create();arm.animation_data.action=bpy.data.actions['C17_'+clip];scene.frame_start=1;scene.frame_end=frames+1
 bpy.ops.export_scene.fbx(filepath=str(OUT/('A_C17_'+clip+'.fbx')),bake_anim=True,bake_anim_simplify_factor=0,**settings)
arm.animation_data.action=bpy.data.actions['C17_Idle'];scene.frame_start=1;scene.frame_end=91;scene.frame_set(1)
# Studio preview with neutral floor, broad lights and a front three-quarter camera.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.005));floor=bpy.context.object;floor.name='PREVIEW_Ground';fm=bpy.data.materials.new('Studio');fm.diffuse_color=(.12,.15,.15,1);floor.data.materials.append(fm)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
for name,pos,energy,size in [('Key',(-3,-4,5),650,4),('Fill',(4,-1,3),400,3),('Rim',(1,3,4),850,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.name='PREVIEW_'+name;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,.8))
bpy.ops.object.camera_add(location=(2.3,-3.8,2));cam=bpy.context.object;cam.name='PREVIEW_Camera';aim(cam,(0,0,.85));cam.data.type='ORTHO';cam.data.ortho_scale=2.1;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1200;scene.render.resolution_y=1400;scene.render.resolution_percentage=100;scene.world.color=(.25,.25,.25)
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(ROOT/'Documentation/C17/C17_Studio.png')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'C17-Workbench.blend'));bpy.ops.render.render(write_still=True)
triangles=sum(len(p.vertices)-2 for p in mesh.data.polygons)
(OUT/'C17_Manifest.json').write_text(json.dumps({'body_height_m':1.519,'antenna_height_m':1.681,'triangles':triangles,'vertices':len(mesh.data.vertices),'bones':list(bones),'animations':clips,'fps':30,'rig':'Rigid vertex weights; analytic IK baked into deform bone transforms; no external rig plugin required','source_reference':'Reference images/robot-1.png'},indent=2))
print('C17_COMPLETE',triangles,'triangles',len(bones),'bones',flush=True)




