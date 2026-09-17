"""Bake every source scene to editable meshes, retaining a procedural backup."""
import bpy,json,shutil,datetime,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'Reference images/Conservatory-MASTER.blend'
sourcefile=Path(bpy.data.filepath).resolve()
if sourcefile==target.resolve():
 backup=ROOT/'Saved/Backups/MasterMeshConversion'/datetime.datetime.now().strftime('%Y%m%d-%H%M%S')/target.name
 backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,backup)
else:
 assert (ROOT/'Saved/Backups/MasterMeshConversion').resolve() in sourcefile.parents
 backup=sourcefile
digest=hashlib.sha256(backup.read_bytes()).hexdigest()
source_scenes=list(bpy.data.scenes);active=bpy.context.scene;report=[];created=[]
for source in source_scenes:
 bpy.context.window.scene=source;dep=bpy.context.evaluated_depsgraph_get()
 name=source.name;source.name='PROCEDURAL SOURCE / '+name
 dst=bpy.data.scenes.new(name);created.append((source,dst));dst.unit_settings.system=source.unit_settings.system;dst.unit_settings.scale_length=source.unit_settings.scale_length
 dst.world=source.world;cache={};collections={};ninst=0;nv=0;nf=0;coords=[];seen=set()
 for item in dep.object_instances:
  ev=item.object
  if ev.type not in {'MESH','CURVE','SURFACE','FONT','META'}:continue
  if not item.show_self:continue
  key=ev.original.name
  placement=(key,tuple(round(v,7) for row in item.matrix_world for v in row))
  if placement in seen:continue
  seen.add(placement)
  if key not in cache:cache[key]=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=dep)
  mesh=cache[key]
  if not len(mesh.vertices):continue
  # Individual datablocks allow each repeated piece to be refined independently.
  copy=mesh.copy();ob=bpy.data.objects.new(key,copy);ob.matrix_world=item.matrix_world.copy()
  group=item.parent.name if item.is_instance and item.parent else (ev.original.users_collection[0].name if ev.original.users_collection else 'Parts')
  if group not in collections:
   coll=bpy.data.collections.new(group+' / meshes');dst.collection.children.link(coll);collections[group]=coll
  collections[group].objects.link(ob)
  ob['source_object']=key;ob['source_scene']=name;ob['baked_instance']=bool(item.is_instance)
  nv+=len(copy.vertices);nf+=len(copy.polygons);ninst+=int(item.is_instance)
  # Bounds from the actual evaluated geometry, without changing local origins.
  vs=[v.co for v in mesh.vertices]
  lo=Vector([min(v[k] for v in vs) for k in range(3)]);hi=Vector([max(v[k] for v in vs) for k in range(3)])
  coords.extend(ob.matrix_world@Vector((x,y,z)) for x in [lo.x,hi.x] for y in [lo.y,hi.y] for z in [lo.z,hi.z])
 for mesh in cache.values():
  if mesh.users==0:bpy.data.meshes.remove(mesh)
 bounds=[[min(p[k] for p in coords) for k in range(3)],[max(p[k] for p in coords) for k in range(3)]]
 report.append({'scene':name,'mesh_objects':len(dst.objects),'realized_instances':ninst,'vertices':nv,'polygons':nf,'bounds':bounds})
 print('BAKED_SCENE '+json.dumps(report[-1]),flush=True)
# Remove source scene objects only after every scene has been evaluated.
newobjects={o for _,s in created for o in s.objects}
for o in list(bpy.data.objects):
 if o not in newobjects:bpy.data.objects.remove(o,do_unlink=True)
for old,new in created:
 if old==active:bpy.context.window.scene=new
for old,new in created:bpy.data.scenes.remove(old)
bpy.data.orphans_purge(do_recursive=True)
assert all(o.type=='MESH' and not o.modifiers and o.instance_type=='NONE' for o in bpy.data.objects)
assert len(bpy.data.objects)==sum(r['mesh_objects'] for r in report)
assert len(bpy.data.curves)==0
current=next(r for r in report if r['scene']==bpy.context.scene.name);lo,hi=map(Vector,current['bounds']);centre=(lo+hi)/2
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   sp=area.spaces.active;sp.region_3d.view_location=centre;sp.region_3d.view_distance=max(hi-lo)*1.7
   sp.region_3d.view_rotation=Vector((1,-1,.7)).to_track_quat('Z','Y');sp.region_3d.view_perspective='PERSP';sp.clip_end=1000
   sp.shading.type='SOLID';sp.shading.color_type='MATERIAL';sp.shading.show_cavity=True
for o in bpy.context.scene.objects:o.select_set(False)
note=bpy.data.texts.new('READ ME - Mesh master conversion')
note.write('All design objects in both scenes are editable meshes. Curves, evaluated modifiers and collection/Geometry Nodes instances are baked. Each piece has its own mesh datablock.\nThe original procedural file is backed up at:\n'+str(backup)+'\nOlder generators that inspect procedural instances must use that backup as their input.\n')
bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
out={'file':str(target),'procedural_backup':str(backup),'procedural_sha256':digest,'scenes':report,'all_objects_are_meshes':True,'remaining_modifiers':0,'remaining_curve_datablocks':len(bpy.data.curves),'remaining_instances':0}
(ROOT/'Documentation/MasterMeshConversion.json').write_text(json.dumps(out,indent=2))
print('MASTER_MESH_CONVERSION_COMPLETE '+json.dumps(out),flush=True)
