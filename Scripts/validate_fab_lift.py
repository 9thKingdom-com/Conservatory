import bpy,json,math,hashlib,struct
from pathlib import Path
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory');OUT=R/'Asset Chest/01 John Originals/LIFT-MASTER/FabRelease/v1.0'
audit=json.loads((OUT/'Seller/GeometryAudit.json').read_text());spec=json.loads((OUT/'Seller/MaterialSpec.json').read_text())
native=OUT/'Product/Blender/LIFT-MASTER.blend'
bpy.ops.wm.open_mainfile(filepath=str(native),load_ui=False)
asset=[o for o in bpy.context.scene.objects if o.type in {'MESH','CURVE','FONT'} and any(c.name[:2] in ['01','02','03','04','05','06','07'] for c in o.users_collection) and not o.hide_render]
dg=bpy.context.evaluated_depsgraph_get();tri=0
for o in asset:
 me=bpy.data.meshes.new_from_object(o.evaluated_get(dg),depsgraph=dg);me.calc_loop_triangles();tri+=len(me.loop_triangles)
 assert all(math.isfinite(x) for v in me.vertices for x in v.co),o.name
 bpy.data.meshes.remove(me)
assert tri==audit['triangles'],(tri,audit['triangles'])
assert not [im for im in bpy.data.images if im.type!='RENDER_RESULT']
assert not [f for f in bpy.data.fonts if f.users and f.filepath and not f.filepath.startswith('<')]
assert not bpy.data.libraries
source=R/'Asset Chest/01 John Originals/LIFT-MASTER/LIFT-MASTER.blend'
assert hashlib.sha256(source.read_bytes()).hexdigest()==audit['source_sha256']
# Fresh-process native render also validates the release file, after all repairs.
bpy.context.scene.render.filepath=str(OUT/'Media/01_Hero.jpg');bpy.ops.render.render(write_still=True)
result={'native_reopened':True,'native_asset_objects':len(asset),'native_evaluated_triangles':tri,'external_images_fonts_libraries':0,'original_master_unchanged':True}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(OUT/'Product/FBX/SM_LiftMaster.fbx'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];assert len(meshes)==1
ob=meshes[0];me=ob.data;me.calc_loop_triangles();assert len(me.loop_triangles)==tri
assert all(math.isfinite(x) for v in me.vertices for x in v.co)
assert all(math.isfinite(x) for uv in me.uv_layers for v in uv.data for x in v.uv)
mins=[min((ob.matrix_world@v.co)[i] for v in me.vertices) for i in range(3)];maxs=[max((ob.matrix_world@v.co)[i] for v in me.vertices) for i in range(3)]
assert all(abs(mins[i]-audit['bounds_m']['min'][i])<.0001 and abs(maxs[i]-audit['bounds_m']['max'][i])<.0001 for i in range(3)),(mins,maxs)
result['fbx_reimported']=True;result['fbx_triangles']=len(me.loop_triangles);result['fbx_scale_and_bounds_match']=True;result['finite_uvs']=True
for m in me.materials:
 desc=next(d for d in spec.values() if d['slot']==m.name.split('.')[0]);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=(*desc['color'],1);p.inputs['Metallic'].default_value=desc['metal'];p.inputs['Roughness'].default_value=desc['rough']
 p.inputs['Transmission Weight'].default_value=1.0 if desc['glass'] else 0.0;p.inputs['IOR'].default_value=1.46
 p.inputs['Emission Color'].default_value=(*desc['emission'],1);p.inputs['Emission Strength'].default_value=desc['emission_strength']
(OUT/'Product/GLB').mkdir(exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(OUT/'Product/GLB/LIFT-MASTER.glb'),export_format='GLB',use_selection=True,export_animations=False,export_cameras=False,export_lights=False)
data=(OUT/'Product/GLB/LIFT-MASTER.glb').read_bytes();size,kind=struct.unpack_from('<II',data,12);gl=json.loads(data[20:20+size])
assert 'images' not in gl
result['glb_embedded_no_external_files']=True
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(OUT/'Product/GLB/LIFT-MASTER.glb'))
gtri=0
for o in bpy.context.scene.objects:
 if o.type=='MESH':o.data.calc_loop_triangles();gtri+=len(o.data.loop_triangles);assert all(math.isfinite(x) for v in o.data.vertices for x in v.co)
assert gtri==tri;result['glb_reimported']=True;result['glb_triangles']=gtri
result['gallery']=[]
for path in sorted((OUT/'Media').glob('*.jpg')):
 im=bpy.data.images.load(str(path));w,h=im.size;assert w>=1920 and h>=1080;assert path.stat().st_size<3000000
 result['gallery'].append({'file':path.name,'width':w,'height':h,'bytes':path.stat().st_size})
assert sum(i['bytes'] for i in result['gallery'])<25000000
(OUT/'Seller/Validation.json').write_text(json.dumps(result,indent=2));print('FAB_VALIDATION_PASSED',result,flush=True)
