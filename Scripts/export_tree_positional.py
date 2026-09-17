import bpy,bmesh,json,math
from pathlib import Path
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory');O=R/'Asset Chest/01 John Originals/TREE-MASTER/UnrealExport';O.mkdir(exist_ok=True)
source_scene=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get()
src=[o for o in source_scene.objects if o.type=='MESH' and any(c.name[:2] in ['01','04','06','07','08'] for c in o.users_collection)]
materials={};buckets={'Structure':[],'Foliage':[]}
export=bpy.data.scenes.new('DERIVED TREE POSITIONAL EXPORT');bpy.context.window.scene=export
for ob in src:
 me=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg);me.transform(ob.matrix_world);copy=bpy.data.objects.new(ob.name,me);export.collection.objects.link(copy)
 foliage=any(c.name[:2] in ['04','06','07'] for c in ob.users_collection)
 for i,m in enumerate(me.materials):
  if not m:continue
  if m.name not in materials:
   p=m.node_tree.nodes.get('Principled BSDF');ram=next((n for n in m.node_tree.nodes if n.type=='VALTORGB'),None);mix=next((n for n in m.node_tree.nodes if n.type=='MIX_RGB'),None)
   c=list(p.inputs['Base Color'].default_value)[:3]
   if ram:c=list(ram.color_ramp.elements[len(ram.color_ramp.elements)//2].color)[:3]
   if mix:c=list(mix.inputs[1].default_value)[:3]
   slot='Tree%02d'%len(materials);materials[m.name]=dict(slot=slot,color=c,rough=p.inputs['Roughness'].default_value,metal=p.inputs['Metallic'].default_value,foliage=foliage,back_color=list(mix.inputs[2].default_value)[:3] if mix else None)
  desc=materials[m.name];new=bpy.data.materials.get(desc['slot']) or bpy.data.materials.new(desc['slot']);new.diffuse_color=(*desc['color'],1);me.materials[i]=new
 if 'SCULPT' in ob.name:
  bpy.ops.object.select_all(action='DESELECT');copy.select_set(True);bpy.context.view_layer.objects.active=copy
  mod=copy.modifiers.new('Positional export reduction only','DECIMATE');mod.ratio=.4;bpy.ops.object.modifier_apply(modifier=mod.name)
 buckets['Foliage' if foliage else 'Structure'].append(copy)
counts={}
for kind,obs in buckets.items():
 bpy.ops.object.select_all(action='DESELECT')
 for o in obs:o.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();ob=bpy.context.object;ob.name='SM_TreeMaster_'+kind
 for uv in list(ob.data.uv_layers):ob.data.uv_layers.remove(uv)
 uv=ob.data.uv_layers.new(name='UV0')
 for poly in ob.data.polygons:
  axes=sorted(range(3),key=lambda i:abs(poly.normal[i]))[:2]
  for li in poly.loop_indices:
   co=ob.data.vertices[ob.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
 ob.data.calc_loop_triangles();counts[kind]=len(ob.data.loop_triangles)
 assert all(math.isfinite(x) for v in ob.data.vertices for x in v.co)
 bpy.ops.export_scene.fbx(filepath=str(O/(ob.name+'.fbx')),use_selection=True,object_types={'MESH'},axis_forward='-Y',axis_up='Z',apply_unit_scale=True,bake_space_transform=False,add_leaf_bones=False,mesh_smooth_type='FACE')
(O/'ExportReport.json').write_text(json.dumps(dict(source=bpy.data.filepath,materials=materials,triangles=counts,source_geometry_unchanged=True,units='metres exported to Unreal centimetres',purpose='Positional; re-export after John refines the master'),indent=2));print('TREE_EXPORTED',counts)
