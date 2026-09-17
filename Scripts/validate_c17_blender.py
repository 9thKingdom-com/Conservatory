import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];arm=bpy.data.objects['C17_Rig'];scene=bpy.context.scene;scene.cycles.samples=12;scene.render.resolution_x=600;scene.render.resolution_y=700
for clip,frame in [('Walk',9),('Lift',46),('ShelfPick',46),('Chop',28),('BreakStone',28),('CarryWalk',11)]:
 arm.animation_data.action=bpy.data.actions['C17_'+clip];scene.frame_set(frame);scene.render.filepath=str(ROOT/('Documentation/C17/Pose_'+clip+'.png'));bpy.ops.render.render(write_still=True)
mesh=bpy.data.objects['SK_C17'];bad=[v.index for v in mesh.data.vertices if len(v.groups)!=1 or abs(sum(g.weight for g in v.groups)-1)>.0001]
contact={}
for clip,frames in [('Idle',90),('Walk',32),('CarryWalk',40),('Lift',90),('ShelfPick',90),('Chop',60),('BreakStone',60)]:
 arm.animation_data.action=bpy.data.actions['C17_'+clip];samples=[]
 for f in [1,1+frames//4,1+frames//2,1+frames*3//4,1+frames]:
  scene.frame_set(f);deps=bpy.context.evaluated_depsgraph_get();obj=mesh.evaluated_get(deps);m=obj.to_mesh();samples.append(min((obj.matrix_world@v.co).z for v in m.vertices));obj.to_mesh_clear()
 contact[clip]={'lowest_vertex_z_m':samples,'feet_contact_passed':all(-.015<z<.04 for z in samples)}
(ROOT/'Documentation/C17/FootContact.json').write_text(json.dumps(contact,indent=2))
(ROOT/'Documentation/C17/RigValidation.json').write_text(json.dumps({'vertices':len(mesh.data.vertices),'bones':len(arm.data.bones),'unweighted_or_nonrigid_vertices':len(bad),'actions':[a.name for a in bpy.data.actions],'rigid_skin_passed':not bad},indent=2))

