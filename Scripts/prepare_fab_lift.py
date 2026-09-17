import bpy,bmesh,math,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory')
OUT=R/'Asset Chest/01 John Originals/LIFT-MASTER/FabRelease/v1.0'
for name in ['Product/Blender','Product/FBX','Media','Seller']:(OUT/name).mkdir(parents=True,exist_ok=True)
source_path=bpy.data.filepath
sc=bpy.context.scene
asset=[o for o in sc.objects if o.type in {'MESH','CURVE','FONT'} and any(c.name[:2] in ['01','02','03','04','05','06','07'] for c in o.users_collection) and not o.hide_render]
audit={'blender':bpy.app.version_string,'source_sha256':hashlib.sha256(Path(source_path).read_bytes()).hexdigest(),'source_objects':len(asset),'repairs':[]}
# Weld collapsed decorative leaf tips before evaluating their bevels. Source on disk is untouched.
for o in asset:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 damaged=[v for v in bm.verts if not all(math.isfinite(x) for x in v.co)]
 if damaged:
  count=len(damaged)
  while damaged:
   updates=[]
   for v in damaged:
    neighbors=[e.other_vert(v) for e in v.link_edges if all(math.isfinite(x) for x in e.other_vert(v).co)]
    if neighbors:updates.append((v,sum((n.co for n in neighbors),Vector())/len(neighbors)))
   assert updates,'Disconnected invalid geometry in '+o.name
   for v,co in updates:v.co=co
   damaged=[v for v in damaged if not all(math.isfinite(x) for x in v.co)]
  audit['repairs'].append({'object':o.name,'nonfinite_source_vertices_reconstructed_from_neighbors':count})
 before=len(bm.verts)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000001)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=0.0000001)
 bm.to_mesh(o.data);bm.free();o.data.update()
 if len(o.data.vertices)!=before:audit['repairs'].append({'object':o.name,'welded_vertices':before-len(o.data.vertices)})
# Font outlines are converted, so no proprietary font file is redistributed.
for o in asset:
 if o.type=='FONT':
  bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
for o in list(bpy.data.objects):
 if any(c.name.startswith('99') for c in o.users_collection):bpy.data.objects.remove(o,do_unlink=True)
for im in list(bpy.data.images):
 if im.type!='RENDER_RESULT':bpy.data.images.remove(im,do_unlink=True)
for t in list(bpy.data.texts):bpy.data.texts.remove(t)
for f in list(bpy.data.fonts):
 if f.name!='Bfont' and f.users==0:bpy.data.fonts.remove(f)
for o in bpy.data.objects:
 for key in list(o.keys()):del o[key]
for key in list(sc.keys()):del sc[key]
readme=bpy.data.texts.new('START HERE')
readme.write('LIFT-MASTER | Ornate Glass Service Lift | 1.0\nStatic high-detail architectural prop. Blender 5.1.1.\nMetres, Z up, entrance faces -Y. Collections 01-07 are the model; 08 contains optional placement anchors; 90 Studio contains preview lights, cameras and floor.\nProcedural materials: no baked image textures. Lettering is geometry; no external fonts or reference images are included.\nNo animations, moving doors, shaft, scripts or functional elevator system. See included documentation.\n')
sc.unit_settings.system='METRIC';sc.unit_settings.scale_length=1.0
sc.render.engine='CYCLES';sc.cycles.samples=64;sc.cycles.use_denoising=True
sc.render.resolution_x=1920;sc.render.resolution_y=1080;sc.render.resolution_percentage=100
sc.render.image_settings.file_format='JPEG';sc.render.image_settings.quality=92
try:
 prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type!='CPU'
 sc.cycles.device='GPU'
except:sc.cycles.device='CPU'
shots=[('01_Hero',(7,-12,6.6),(0,0,2.38),46),('02_Front',(0,-14,3.0),(0,0,2.38),46),('03_Cabin',(1.0,-5.0,2.7),(0,.40,1.65),43),('04_Crown',(3.0,-5.0,5.25),(0,0,3.97),53),('05_Rear',(-8,11,6.0),(0,0,2.38),44)]
cam=sc.camera
for name,pos,target,lens in []:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
 sc.render.filepath=str(OUT/'Media'/(name+'.jpg'));bpy.ops.render.render(write_still=True)
 print('RENDERED',name,flush=True)
cam.location=shots[0][1];cam.rotation_euler=(Vector(shots[0][2])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=shots[0][3]
sc.render.filepath='//Preview.jpg'
bpy.ops.object.select_all(action='DESELECT')
bpy.context.view_layer.update()
# Confirm evaluated source is finite; convert only any remaining problematic object.
dg=bpy.context.evaluated_depsgraph_get();derived=[];invalid_total=0
for o in asset:
 me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg);me.transform(o.matrix_world)
 bm=bmesh.new();bm.from_mesh(me);bad=[v for v in bm.verts if not all(math.isfinite(x) for x in v.co)]
 if bad:
  invalid_total+=len(bad);bm.free();bpy.data.meshes.remove(me)
  disabled=[]
  for modifier in o.modifiers:
   if modifier.type=='BEVEL':modifier.show_viewport=False;modifier.show_render=False;disabled.append(modifier.name)
  bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
  me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg);me.transform(o.matrix_world)
  assert all(math.isfinite(x) for v in me.vertices for x in v.co),'Needs manual topology repair: '+o.name
  bm=bmesh.new();bm.from_mesh(me);audit['repairs'].append({'object':o.name,'disabled_invalid_bevels':disabled,'preserved_complete_base_surface':True})
 bm.to_mesh(me);bm.free();me.update()
 if bad:
  replacement=me.copy();replacement.transform(o.matrix_world.inverted());o.data=replacement;o.modifiers.clear()
  audit['repairs'][-1]['release_object_modifiers_baked']=True
 ob=bpy.data.objects.new(o.name,me);derived.append(ob)
audit['invalid_after_tip_weld']=invalid_total
for o in asset:
 if o.type=='MESH':
  for uv in o.data.uv_layers:
   for p in o.data.polygons:
    axes=sorted(range(3),key=lambda i:abs(p.normal[i]))[:2]
    for li in p.loop_indices:
     if not all(math.isfinite(x) for x in uv.data[li].uv):
      co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
for o in asset:
 check=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg)
 assert all(math.isfinite(x) for v in check.vertices for x in v.co),o.name
 bpy.data.meshes.remove(check)
audit['remaining_nonfinite_vertices']=0
for name,pos,target,lens in shots:
 cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
 sc.render.filepath=str(OUT/'Media'/(name+'.jpg'));bpy.ops.render.render(write_still=True)
 print('RENDERED_RELEASE',name,flush=True)
cam.location=shots[0][1];cam.rotation_euler=(Vector(shots[0][2])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=shots[0][3];sc.render.filepath='//Preview.jpg'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Product/Blender/LIFT-MASTER.blend'))
ex=bpy.data.scenes.new('Export');bpy.context.window.scene=ex;ex.unit_settings.system='METRIC';ex.unit_settings.scale_length=1
for o in derived:ex.collection.objects.link(o);o.select_set(True)
bpy.context.view_layer.objects.active=derived[0];bpy.ops.object.join();ob=bpy.context.object;ob.name='SM_LiftMaster';me=ob.data
# Metric projection is deliberately documented as overlapping, for procedural/triplanar materials.
for uv in list(me.uv_layers):me.uv_layers.remove(uv)
uv=me.uv_layers.new(name='UV0_MetricProjection')
for p in me.polygons:
 axes=sorted(range(3),key=lambda i:abs(p.normal[i]))[:2]
 for li in p.loop_indices:
  co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
used=sorted({p.material_index for p in me.polygons});mats=[me.materials[i] for i in used];remap={old:new for new,old in enumerate(used)};indices=[remap[p.material_index] for p in me.polygons]
me.materials.clear()
for m in mats:me.materials.append(m)
for p,idx in zip(me.polygons,indices):p.material_index=idx
spec={}
for m in mats:
 p=m.node_tree.nodes.get('Principled BSDF');r=next((n for n in m.node_tree.nodes if n.type=='VALTORGB'),None);nr=next((n for n in m.node_tree.nodes if n.type=='MAP_RANGE'),None)
 spec[m.name]={'slot':'Lift'+m.name[:2],'color':list(p.inputs['Base Color'].default_value)[:3],'metal':p.inputs['Metallic'].default_value,'rough':p.inputs['Roughness'].default_value,'emission':list(p.inputs['Emission Color'].default_value)[:3],'emission_strength':p.inputs['Emission Strength'].default_value,'glass':p.inputs['Transmission Weight'].default_value>.5,'ramp':[list(e.color)[:3] for e in r.color_ramp.elements] if r else None,'rough_range':[nr.inputs['To Min'].default_value,nr.inputs['To Max'].default_value] if nr else None}
 # FBX standard palette with no unsupported procedural links. Native copy retains the full shaders.
 new=bpy.data.materials.new('Lift'+m.name[:2]);new.use_nodes=True;np=new.node_tree.nodes.get('Principled BSDF')
 for key in ['Base Color','Metallic','Roughness','Transmission Weight','IOR','Emission Color','Emission Strength']:np.inputs[key].default_value=p.inputs[key].default_value
 me.materials[list(me.materials).index(m)]=new
me.calc_loop_triangles();audit['triangles']=len(me.loop_triangles);audit['vertices']=len(me.vertices);audit['materials']=len(me.materials)
audit['bounds_m']={'min':[min(v.co[i] for v in me.vertices) for i in range(3)],'max':[max(v.co[i] for v in me.vertices) for i in range(3)]}
bpy.ops.export_scene.fbx(filepath=str(OUT/'Product/FBX/SM_LiftMaster.fbx'),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,mesh_smooth_type='FACE',add_leaf_bones=False,bake_anim=False)
(OUT/'Seller/GeometryAudit.json').write_text(json.dumps(audit,indent=2))
(OUT/'Seller/MaterialSpec.json').write_text(json.dumps(spec,indent=2))
print('FAB_MODEL_READY',audit['triangles'],audit['vertices'],flush=True)
