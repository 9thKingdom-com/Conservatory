"""Reload and validate the saved detailed robot; pose test is not saved."""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];arm=bpy.data.objects['C17_Detailed_Rig'];parts=[o for o in bpy.data.objects if o.type=='MESH' and o.get('joint')]
bad=[]
for o in parts:
 joint=o['joint'];groups={g.index:g.name for g in o.vertex_groups}
 for v in o.data.vertices:
  if len(v.groups)!=1 or abs(v.groups[0].weight-1)>1e-6 or groups.get(v.groups[0].group)!=joint:bad.append(o.name);break
 assert joint in arm.data.bones
assert not bad,bad
manifest=json.loads((ROOT/'SourceAssets/C17Detailed/Manifest.json').read_text());assert len(parts)==manifest['editable_mesh_parts']
assert not [o.name for o in parts if any(k in o.name.lower() for k in ['hydraulic','piston','actuator','flex hose','flex cable','sensor loom','protected pack cable','protected harness'])]
references=[im for im in bpy.data.images if im.name.startswith('robot-1')];assert len(references)==3 and all(im.packed_file for im in references)
hand=next(o for o in parts if o['joint']=='hand_L');head=next(o for o in parts if o['joint']=='head')
def sample(o):
 dep=bpy.context.evaluated_depsgraph_get();e=o.evaluated_get(dep);me=e.to_mesh();vs=[e.matrix_world@v.co for v in list(me.vertices)[:32]];e.to_mesh_clear();return vs
before=sample(hand);head_before=sample(head)
pb=arm.pose.bones['forearm_L'];pb.rotation_mode='XYZ';pb.rotation_euler.x=.45;bpy.context.view_layer.update();after=sample(hand);head_after=sample(head)
motion=max((a-b).length for a,b in zip(after,before));rigidity=abs((after[1]-after[0]).length-(before[1]-before[0]).length)
assert motion>.02 and rigidity<1e-5
assert max((a-b).length for a,b in zip(head_after,head_before))<1e-6
pb.matrix_basis=Matrix.Identity(4)
report={'reloaded_blend':bpy.data.filepath,'mesh_parts':len(parts),'bones':len(arm.data.bones),'packed_reference_images':len(references),'bad_rigid_weights':bad,'forearm_pose_moves_hand_m':motion,'rigid_sample_distance_error_m':rigidity,'unrelated_head_preserved':True,'passed':True}
(ROOT/'Documentation/C17Detailed/Validation.json').write_text(json.dumps(report,indent=2));print('C17D_VALIDATED '+json.dumps(report),flush=True)

