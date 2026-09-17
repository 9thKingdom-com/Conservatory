import bpy,math,random,json
from pathlib import Path
from mathutils import Vector,noise
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory');O=R/'Asset Chest/01 John Originals/TREE-MASTER';random.seed(13926)
bpy.ops.wm.open_mainfile(filepath=str(O/'TREE-MASTER.blend'));sc=bpy.context.scene
# Replace the coarse applied bark-strip study with continuous sculptural surface relief.
ob=bpy.data.objects.get('Bark | layered longitudinal relief')
if ob:bpy.data.objects.remove(ob,do_unlink=True)
tex=bpy.data.textures.new('Bark | sculpted fissures',type='CLOUDS');tex.noise_scale=.14;tex.noise_depth=2
for ob in list(bpy.data.objects):
 if ob.type!='MESH' or not any(c.name in ['01 Heartwood and limbs','02 Surface roots'] for c in ob.users_collection):continue
 if not any(key in ob.name for key in ['Heartwood','Trunk |','Limb |','Root | ancient']):continue
 # Subdivision provides actual relief geometry while keeping the master stack editable.
 sub=ob.modifiers.new('Organic surface subdivision','SUBSURF');sub.levels=2;sub.render_levels=2
 dis=ob.modifiers.new('Fine broken bark relief','DISPLACE');dis.texture=tex;dis.strength=.12 if 'Heartwood' in ob.name or 'Trunk' in ob.name else .065;dis.mid_level=.45;dis.texture_coords='GLOBAL'
 # Add slow growth irregularity without moving attachment endpoints.
 zs=[v.co.z for v in ob.data.vertices];lo=min(zs);hi=max(zs)
 for v in ob.data.vertices:
  t=(v.co.z-lo)/max(.1,hi-lo);fade=math.sin(math.pi*t)**2
  warp=noise.noise_vector(v.co*.64);v.co+=warp*fade*(.12 if 'Limb' in ob.name else .065)
 ob.data.update()
bark=bpy.data.materials['Bark | weathered warm grey'];nodes=bark.node_tree.nodes;links=bark.node_tree.links;p=nodes.get('Principled BSDF');r=next(n for n in nodes if n.type=='VALTORGB');r.color_ramp.elements[0].color=(.021,.013,.008,1);r.color_ramp.elements[1].color=(.19,.135,.08,1)
mapping=next(n for n in nodes if n.type=='VECT_MATH');mapping.inputs[1].default_value=(2.3,2.3,.52)
for m in bpy.data.materials:
 if m.name.startswith('Leaf |'):
  p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.62;p.inputs['Specular IOR Level'].default_value=.24
  c=p.inputs['Base Color'].default_value;p.inputs['Base Color'].default_value=(c[0]*.72,c[1]*.85,c[2]*.72,1)
# Ivy leaf clusters widen into natural patches rather than a single regular ladder.
ivy=bpy.data.objects['Ivy | climbing leaves'];original=ivy.data.copy();verts=[];faces=[];indices=[]
for v in original.vertices:verts.append(v.co.copy())
for p in original.polygons:faces.append(tuple(p.vertices));indices.append(p.material_index)
for k in range(3):
 angle=(k-1)*.09+.03;offset=len(verts)
 for v in original.vertices:
  c=v.co.copy();a=angle+.045*math.sin(c.z*2.3+k);c.x,c.y=c.x*math.cos(a)-c.y*math.sin(a),c.x*math.sin(a)+c.y*math.cos(a);c.z+=.055*(k+1);verts.append(c)
 for p in original.polygons:faces.append(tuple(offset+i for i in p.vertices));indices.append(p.material_index)
me=bpy.data.meshes.new('Ivy | clustered foliage');me.from_pydata(verts,[],faces);me.update()
for m in original.materials:me.materials.append(m)
for p,i in zip(me.polygons,indices):p.material_index=i;p.use_smooth=True
ivy.data=me
# A low camera gives the intended monumental trunk-led reading.
cam=bpy.data.objects['CAM | Hero'];cam.location=(12,-26,8.2);cam.rotation_euler=(Vector((0,0,6.4))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=44;sc.camera=cam
sc.world.node_tree.nodes.get('Background').inputs[0].default_value=(.45,.51,.55,1);sc.world.node_tree.nodes.get('Background').inputs[1].default_value=.35
bpy.data.lights['Studio | sunlight'].energy=1.4
sc.cycles.samples=64;sc.render.filepath='//TREE-MASTER-Hero.png'
bpy.ops.wm.save_as_mainfile(filepath=str(O/'TREE-MASTER.blend'))
for name,camname in [('Hero','CAM | Hero'),('Roots','CAM | Root detail'),('Rear','CAM | Rear')]:
 sc.camera=bpy.data.objects[camname];sc.render.filepath=str(O/('TREE-MASTER-'+name+'.png'));bpy.ops.render.render(write_still=True);print('REFINED_RENDER',name,flush=True)
dg=bpy.context.evaluated_depsgraph_get();tri=0;bounds=[];count=0
for ob in sc.objects:
 if ob.type!='MESH' or not any(c.name[:2] in ['01','02','03','04','05','06','07','08'] for c in ob.users_collection):continue
 me=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg);me.calc_loop_triangles();tri+=len(me.loop_triangles);count+=1
 assert all(math.isfinite(x) for v in me.vertices for x in v.co),ob.name
 bounds.extend([ob.matrix_world@Vector(c) for c in ob.evaluated_get(dg).bound_box]);bpy.data.meshes.remove(me)
mi=[min(v[i] for v in bounds) for i in range(3)];ma=[max(v[i] for v in bounds) for i in range(3)]
(O/'MasterReport.json').write_text(json.dumps({'version':'0.2 Blender review','blender':bpy.app.version_string,'model_objects':count,'evaluated_triangles':tri,'dimensions_m':[ma[i]-mi[i] for i in range(3)],'canopy_leaves':20000,'nonfinite_vertices':0,'unreal_imported':False},indent=2));print('TREE_REFINEMENT_COMPLETE',tri,flush=True)
