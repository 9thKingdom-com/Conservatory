"""Derive a detailed repeatable passage kit from the unmodified Blender master."""
import bpy,math,json,hashlib,bmesh
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'SourceAssets/PassageDetail';OUT.mkdir(parents=True,exist_ok=True)
L=16*math.sin(math.pi/16);W=L/2;R=W-.13;F=.61
master=ROOT/'Reference images/Conservatory-MASTER.blend';digest=hashlib.sha256(master.read_bytes()).hexdigest()
source=bpy.context.evaluated_depsgraph_get();out=bpy.data.scenes.new('Detailed passage kit');groups={'Body':[],'JoinFrame':[]};mats={}
for n,c in {'IvoryFrame':(.58,.55,.46,1),'Brass':(.43,.27,.095,1),'FloorLight':(.4,.38,.31,1),'FloorDark':(.16,.20,.19,1),'ConservatoryGlass':(.4,.6,.65,.12),'Gasket':(.018,.024,.022,1)}.items():m=bpy.data.materials.new(n);m.diffuse_color=c;mats[n]=m
seen=set();restored=[]
body_terms=['barrel longitudinal','side plinth','side dentil','longitudinal entablature','intermediate barrel hoop','walking surface paving','foundation slab','decorative side scroll']
for inst in source.object_instances:
 o=inst.object;parent=inst.parent.name if inst.parent else ''
 if not inst.is_instance or not o.name.startswith('Corridor |') or 'LINEAR PROCEDURAL REPEAT' not in parent or o.type not in ['MESH','CURVE']:continue
 key=(o.name,tuple(round(v,5) for row in inst.matrix_world for v in row))
 if key in seen:continue
 seen.add(key);group='Body' if any(k in o.name for k in body_terms) else 'JoinFrame'
 transform=Matrix.Translation((-11.2-(W if group=='Body' else 0),0,0))@inst.matrix_world
 me=bpy.data.meshes.new_from_object(o,depsgraph=source)
 mat='FloorLight' if any(k in o.name for k in ['Base |','foundation','paving','plinth']) else 'Brass' if any(k in o.name for k in ['bead','keystone','scroll']) else 'IvoryFrame'
 me.materials.clear();me.materials.append(mats[mat]);ob=bpy.data.objects.new(o.name,me);out.collection.objects.link(ob);ob.matrix_world=transform;groups[group].append(ob)
 if group=='Body':restored.append(o.name)
bpy.context.window.scene=out
def finish(o,name,mat,bevel=0):
 o.name=name;o.data.materials.append(mats[mat]);bpy.context.view_layer.objects.active=o
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:
  mod=o.modifiers.new('Small machined edge','BEVEL');mod.width=bevel;mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 groups['Body'].append(o);return o
def box(name,c,s,mat,bevel=.002):
 bpy.ops.mesh.primitive_cube_add(size=1,location=c);o=bpy.context.object;o.scale=s;return finish(o,name,mat,bevel)
def tube(name,a,b,r,mat):
 a,b=Vector(a),Vector(b);d=b-a;bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=r,depth=d.length,location=(a+b)/2);o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return finish(o,name,mat)
def curve(name,pts,r,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=r;cu.bevel_resolution=2;s=cu.splines.new('POLY');s.points.add(len(pts)-1)
 for p,co in zip(s.points,pts):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cu);out.collection.objects.link(ob);bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;bpy.ops.object.convert(target='MESH');return finish(ob,name,mat)
def face(name,v,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],[tuple(range(len(v)))]);me.update();ob=bpy.data.objects.new(name,me);out.collection.objects.link(ob);return finish(ob,name,mat)
def bolt(c,axis=(0,1,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=6,radius=.009,depth=.008,location=c);o=bpy.context.object;o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler();finish(o,'Glazing clip screw','Brass')
# Side glazing divided into serviceable panes, using the established full side width.
for side in [-1,1]:
 y=side*W
 for a,b in [(-W,-W/3),(-W/3,W/3),(W/3,W)]:
  for lo,hi in [(F,1.22),(1.22,2.50),(2.50,4.35)]:face('Glazed side pane',[(a,y,lo),(b,y,lo),(b,y,hi),(a,y,hi)],'ConservatoryGlass')
 for x in [-W/3,W/3]:
  box('Slender side mullion',(x,y,2.48),(.030,.050,3.74),'IvoryFrame')
  box('Side mullion glazing seal',(x,y-side*.027,2.48),(.036,.006,3.73),'Gasket',0)
 for z in [1.22,2.50]:
  box('Side transom',(0,y,z),(L,.045,.032),'IvoryFrame')
  box('Transom bead',(0,y-side*.028,z),(L,.008,.012),'Brass',.001)
 # A subtle roundel repeats the dome language in each side bay.
 for radius in [.225,.195]:curve('Dome-derived side roundel',[(radius*math.cos(t),y-side*.035,3.81+radius*math.sin(t)) for t in [j*math.tau/64 for j in range(65)]],.009,'Brass')
 tube('Roundel suspension',(0,y-side*.035,4.31),(0,y-side*.035,4.035),.010,'IvoryFrame')
 # Low sealed service trim and restrained fasteners.
 box('Lower service sill',(0,y,.76),(L,.10,.11),'IvoryFrame')
 box('Sill gasket',(0,y-side*.055,.76),(L,.006,.084),'Gasket',.001)
 for x in [-1.30,-.77,0,.77,1.30]:
  box('Service sill cover',(x,y-side*.062,.76),(.32,.016,.066),'IvoryFrame',.003)
  for dx in [-.13,.13]:bolt((x+dx,y-side*.073,.76),(0,-side,0))
 for x in [-1.15,0,1.15]:
  for z in [1.22,2.50,4.30]:
   box('Glazing retention tab',(x,y-side*.032,z),(.062,.013,.043),'IvoryFrame',.003);bolt((x,y-side*.043,z),(0,-side,0))
 # Collecting gutter profile stays outside the glazed envelope.
 box('Eaves condensate channel',(0,y+side*.11,4.38),(L,.075,.055),'IvoryFrame')
 box('Eaves channel shadow',(0,y+side*.11,4.411),(L,.05,.012),'Gasket',0)
 for x in [-W/3,W/3]:tube('Drain return',(x,y+side*.12,.64),(x,y+side*.12,4.36),.014,'IvoryFrame')
# Roof matches the original hoops centrally and the dome portal at either end.
def rr(x):return R+.13*(abs(x)/W)**6
for k in range(12):
 a=-W+k*L/12;b=a+L/12
 for j in range(48):
  t=j*math.pi/48;v=t+math.pi/48
  face('Barrel glazing',[(x,rr(x)*math.cos(q),4.35+rr(x)*math.sin(q)) for x,q in [(a,t),(b,t),(b,v),(a,v)]],'ConservatoryGlass')
 for side in [-1,1]:face('Roof shoulder seal',[(a,side*rr(a),4.35),(b,side*rr(b),4.35),(b,side*W,4.35),(a,side*W,4.35)],'ConservatoryGlass')
for x in [-W+.018,W-.018]:
 curve('End barrel sealing collar',[(x,rr(x)*math.cos(t),4.35+rr(x)*math.sin(t)) for t in [j*math.pi/64 for j in range(65)]],.014,'IvoryFrame')
for y in [-W+.18,W-.18]:box('Floor perimeter inlay',(0,y,F-.001),(L,.014,.002),'Brass',0)
for x in [-W+.055,W-.055]:box('Flush connection threshold',(x,0,F-.002),(.07,2*W-.36,.004),'FloorDark',.001)
# Keep source pieces editable; export combined static meshes separately.
# Bake evaluated mirrored transforms and restore outward solid normals.
# The source paving had downward top normals, which made UE reject step-up.
for objs in groups.values():
 for o in objs:
  o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
stats={}
for group,objs in groups.items():
 copies=[]
 for o in objs:
  dup=o.copy();dup.data=o.data.copy();out.collection.objects.link(dup);copies.append(dup)
 bpy.ops.object.select_all(action='DESELECT')
 for o in copies:o.select_set(True)
 bpy.context.view_layer.objects.active=copies[0];bpy.ops.object.join();ob=bpy.context.object;ob.name='SM_Passage_'+('Detailed' if group=='Body' else 'JoinFrame');bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
 uv=ob.data.uv_layers.new(name='SurfaceUV')
 for p in ob.data.polygons:
  axes=sorted(range(3),key=lambda k:abs(p.normal[k]))[:2]
  for li in p.loop_indices:
   co=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
 bpy.ops.export_scene.fbx(filepath=str(OUT/(ob.name+'.fbx')),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},add_leaf_bones=False,mesh_smooth_type='FACE')
 stats[group]={'editable_parts':len(objs),'triangles':sum(len(p.vertices)-2 for p in ob.data.polygons)}
 bpy.data.objects.remove(ob,do_unlink=True)
for o in groups['JoinFrame']:o.location.x+=6
for name,x,yaw in [('Attach_PositiveX',W,0),('Attach_NegativeX',-W,180)]:
 o=bpy.data.objects.new(name,None);out.collection.objects.link(o);o.location=(x,0,F);o.rotation_euler.z=math.radians(yaw);o.empty_display_type='ARROWS';o.empty_display_size=.25
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Passage-Detailed-Workbench.blend'))
report={'source_sha256':digest,'native_length_m':L,'floor_datum_m':F,'clear_width_m':L-.4,'game_scale':1.5,'sockets':[{'name':'Attach_PositiveX','position_m':[W,0,F],'yaw':0},{'name':'Attach_NegativeX','position_m':[-W,0,F],'yaw':180}],'meshes':stats,'restored_master_details':sorted(set(n.split('.')[0] for n in restored)),'assembly_rule':'Dome portal owns end frame. At a passage-to-passage seam place exactly one JoinFrame at the shared socket, offset down by floor datum. No duplicate end columns.'}
(OUT/'PassageKit.json').write_text(json.dumps(report,indent=2));assert hashlib.sha256(master.read_bytes()).hexdigest()==digest
print('PASSAGE_DETAIL_COMPLETE '+json.dumps(report),flush=True)

