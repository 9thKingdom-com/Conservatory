import unreal as u,json
from pathlib import Path
out={}
for name in ['MM_Idle','MM_Walk_InPlace','MM_Walk_Fwd']:
 a=u.load_asset('/Game/Characters/Mannequins/Animations/Manny/'+name)
 poses=[]
 for t in [0,.15,.3,.45,.6]:
  p=u.AnimationLibrary.get_bone_pose_for_time(a,'foot_l',t,False)
  poses.append(str(p))
 out[name]={'length':a.get_play_length(),'additive':str(a.get_editor_property('additive_anim_type')),'root_motion':a.get_editor_property('enable_root_motion'),'poses':poses}
Path(u.Paths.project_dir()+'Documentation/RobotLocomotionAudit.json').write_text(json.dumps(out,indent=2))
