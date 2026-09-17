"""Import independent native Landscape weightmaps into the isolated study only."""
import unreal as u, time, json, traceback
from pathlib import Path
root=Path(u.Paths.project_dir())
world=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
assert world.get_name()=='L_LandscapePaintStudy'
results={}
for name in ['Gravel','Asphalt','Soil']:
 results[name]=u.ExteriorTools.paint_study_layer(str(root/'SourceAssets/LandscapePaintStudy'/f'{name}.raw'),name)
 assert results[name],name
start=time.monotonic()
def finish(dt):
 if time.monotonic()-start<20:return
 u.unregister_slate_post_tick_callback(handle)
 try:
  land=next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a,u.Landscape))
  for name in results:u.EditorAssetLibrary.save_asset('/Game/Conservatory/Environment/LandscapePaintStudy/LI_'+name,False)
  assert u.EditorLoadingAndSavingUtils.save_map(world,'/Game/Conservatory/Maps/L_LandscapePaintStudy')
  results['target_layers']=[str(n) for n in land.get_target_layer_names()]
  results['saved']=True
  u.get_editor_subsystem(u.UnrealEditorSubsystem).set_level_viewport_camera_info(u.Vector(16000,-6500,5000),u.Rotator(pitch=-32,yaw=35,roll=0))
 except:results['error']=traceback.format_exc()
 (root/'Documentation/LandscapePaintResult.json').write_text(json.dumps(results,indent=2))
handle=u.register_slate_post_tick_callback(finish)
