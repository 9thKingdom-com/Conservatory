import bpy,json,math
from pathlib import Path
O=Path('C:/Users/ASUS TUF/Documents/1 conservatory/Asset Chest/01 John Originals/TREE-MASTER');sc=bpy.context.scene
for name,cam in [('Hero','CAM | Hero'),('Trunk','CAM | Root detail')]:
 sc.camera=bpy.data.objects[cam];sc.render.filepath=str(O/('OLIVE-TREE-'+name+'.png'));bpy.ops.render.render(write_still=True)
tri=0;dg=bpy.context.evaluated_depsgraph_get()
for ob in sc.objects:
 if ob.type!='MESH' or not any(c.name[:2] in ['01','02','04','06','07','08'] for c in ob.users_collection):continue
 me=bpy.data.meshes.new_from_object(ob.evaluated_get(dg),depsgraph=dg);assert all(math.isfinite(x) for v in me.vertices for x in v.co);me.calc_loop_triangles();tri+=len(me.loop_triangles);bpy.data.meshes.remove(me)
(O/'OliveReport.json').write_text(json.dumps({'species_direction':'ancient olive','version':'0.3 review','evaluated_triangles':tri,'canopy_leaves':60000,'fruit':240,'nonfinite_vertices':0,'unreal_imported':False},indent=2));print('OLIVE_REVIEW_READY',tri)
