import unreal as u,json,statistics
from pathlib import Path
out={}
for name in ['MM_Walk_InPlace','MM_Walk_Fwd']:
 a=u.load_asset('/Game/Characters/Mannequins/Animations/Manny/'+name)
 samples=[]
 for i in range(82):
  pose=u.AnimPoseExtensions.get_anim_pose_at_time(a,i/30,u.AnimPoseEvaluationOptions())
  row={}
  for bone in ['root','foot_l','foot_r']:
   v=u.AnimPoseExtensions.get_bone_pose(pose,bone,u.AnimPoseSpaces.WORLD).translation
   row[bone]=[v.x,v.y,v.z]
  samples.append(row)
 out[name]=samples
Path(u.Paths.project_dir()+'Documentation/RobotStrideSamples.json').write_text(json.dumps(out))
