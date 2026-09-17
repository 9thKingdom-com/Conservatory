import bpy,bmesh,json,math
from pathlib import Path
from mathutils import Matrix,Vector
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory');OUT=R/'Asset Chest/01 John Originals/LIFT-MASTER/UnrealExport';OUT.mkdir(parents=True,exist_ok=True)
sc=bpy.context.scene;source=[o for o in sc.objects if o.type in {'MESH','CURVE','FONT'} and any(c.name[:2] in ['01','02','03','04','05','06','07'] for c in o.users_collection) and not o.hide_render]
materials={}
for o in source:
 for m in o.data.materials:
  if m and m.name not in materials:
   p=m.node_tree.nodes.get('Principled BSDF');r=next((n for n in m.node_tree.nodes if n.type=='VALTORGB'),None);nr=next((n for n in m.node_tree.nodes if n.type=='MAP_RANGE'),None)
   materials[m.name]={'slot':'Lift'+m.name[:2],'color':list(p.inputs['Base Color'].default_value)[:3],'metal':p.inputs['Metallic'].default_value,'rough':p.inputs['Roughness'].default_value,'emission':list(p.inputs['Emission Color'].default_value)[:3],'emission_strength':p.inputs['Emission Strength'].default_value,'glass':p.inputs['Transmission Weight'].default_value>.5,'ramp':[list(e.color)[:3] for e in r.color_ramp.elements] if r else None,'rough_range':[nr.inputs['To Min'].default_value,nr.inputs['To Max'].default_value] if nr else None}
dg=bpy.context.evaluated_depsgraph_get();buckets={'Solid':[],'Glass':[]};corrected=[]
exportscene=bpy.data.scenes.new('DERIVED EXPORT');bpy.context.window.scene=exportscene
rot=Matrix.Rotation(math.pi/2,4,'Z');offset=Matrix.Translation((0,0,-.06));xf=offset@rot
for o in source:
 ev=o.evaluated_get(dg);me=bpy.data.meshes.new_from_object(ev,depsgraph=dg);me.transform(xf@o.matrix_world)
 bm=bmesh.new();bm.from_mesh(me)
 invalid=[v for v in bm.verts if not all(math.isfinite(x) for x in v.co)]
 if invalid:
  print('INVALID_EVALUATED_VERTICES',o.name,len(invalid),len(bm.verts),flush=True);bmesh.ops.delete(bm,geom=invalid,context='VERTS')
 if bm.edges and all(e.is_manifold for e in bm.edges) and bm.calc_volume(signed=True)<0:bmesh.ops.reverse_faces(bm,faces=list(bm.faces));corrected.append(o.name)
 bm.to_mesh(me);bm.free();me.update()
 for uv in me.uv_layers:
  for poly in me.polygons:
   axis=max(range(3),key=lambda i:abs(poly.normal[i]));axes=[i for i in range(3) if i!=axis]
   for li in poly.loop_indices:
    if not all(math.isfinite(v) for v in uv.data[li].uv):
     co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
 ob=bpy.data.objects.new(o.name,me);exportscene.collection.objects.link(ob)
 # Dedicated safe export slots keep Blender material names and nodes unmodified.
 for i,m in enumerate(me.materials):
  if m:
   slot=materials[m.name]['slot'];new=bpy.data.materials.get(slot) or bpy.data.materials.new(slot);new.diffuse_color=m.diffuse_color;me.materials[i]=new
 # Classify actual polygon assignments, including John's mixed-material edits.
 glass_indices={i for i,m in enumerate(me.materials) if m and m.name=='Lift07'}
 used={p.material_index for p in me.polygons}
 if used & glass_indices and used-glass_indices:
  glassme=me.copy();glassob=bpy.data.objects.new(o.name+' glass faces',glassme);exportscene.collection.objects.link(glassob)
  for target,keepglass in [(me,False),(glassme,True)]:
   bm=bmesh.new();bm.from_mesh(target);remove=[f for f in bm.faces if (f.material_index in glass_indices)!=keepglass];bmesh.ops.delete(bm,geom=remove,context='FACES');bm.to_mesh(target);bm.free();target.update()
  buckets['Solid'].append(ob);buckets['Glass'].append(glassob)
 else:buckets['Glass' if used & glass_indices else 'Solid'].append(ob)
counts={}
for kind,objects in buckets.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();ob=bpy.context.object;ob.name='SM_LiftMaster_'+kind;ob.data.calc_loop_triangles();counts[kind]=len(ob.data.loop_triangles)
 # Replace incompatible generated layers on this derivative only; source uses
 # procedural materials, with no image textures dependent on these UVs.
 for uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(uv)
 uv=ob.data.uv_layers.new(name='UV0')
 for poly in ob.data.polygons:
  axes=sorted(range(3),key=lambda i:abs(poly.normal[i]))[:2]
  for li in poly.loop_indices:
   co=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
 ob.data.update();bpy.context.view_layer.update()
 # Purge unused material slots so a spare glass slot cannot disable Nanite.
 used=sorted({p.material_index for p in ob.data.polygons});newmats=[ob.data.materials[i] for i in used];remap={old:new for new,old in enumerate(used)};indices=[remap[p.material_index] for p in ob.data.polygons]
 ob.data.materials.clear()
 for m in newmats:ob.data.materials.append(m)
 for p,idx in zip(ob.data.polygons,indices):p.material_index=idx
 bpy.ops.export_scene.fbx(filepath=str(OUT/(ob.name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,bake_space_transform=False,add_leaf_bones=False,mesh_smooth_type='FACE',use_mesh_modifiers=True)
report={'source_snapshot':bpy.data.filepath,'source_objects':len(source),'triangles':counts,'corrected_inward_solids':corrected,'geometry_transform':'Rotate +90deg Z (-Y front to +X), lower source floor datum by 0.06m; no scale change','materials':materials}
(OUT/'ExportReport.json').write_text(json.dumps(report,indent=2))
bpy.context.window.scene=sc;sc.camera=bpy.data.objects.get('CAM | Hero three-quarter') or sc.camera;sc.render.resolution_x=800;sc.render.resolution_y=1000;sc.render.resolution_percentage=100;sc.cycles.samples=32;sc.render.filepath=str(OUT/'FinishedSource.png')
prefs=bpy.context.preferences.addons['cycles'].preferences
try:
 prefs.compute_device_type='OPTIX';prefs.get_devices()
 for d in prefs.devices:d.use=d.type!='CPU'
 sc.cycles.device='GPU'
except:sc.cycles.device='CPU'
bpy.ops.render.render(write_still=True)
print('FINISHED_LIFT_EXPORTED',counts)
