import unreal as u,json
from pathlib import Path
r={'classes':[x for x in dir(u) if 'Landscape' in x and any(k in x for k in ['Layer','Factory','Editor'])]}
w=u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
l=next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a,u.Landscape))
r['methods']=[x for x in dir(l) if 'layer' in x or 'landscape' in x]
for key in ['target_layers','landscape_material','landscape_components']:
 try:r[key]=str(l.get_editor_property(key))
 except Exception as e:r[key]=str(e)
try:
 l.set_editor_property('target_layers',l.get_editor_property('target_layers'));r['target_layers_write']='OK'
except Exception as e:r['target_layers_write']=str(e)
for name in ['LandscapeTargetLayerSettings','LandscapeLayerInfoObject','LandscapeLayerInfoObjectFactory']:
 cls=getattr(u,name,None)
 if cls:r[name]=str(cls.__doc__)
(Path(u.Paths.project_dir())/'Documentation/LandscapePaintAPI.json').write_text(json.dumps(r,indent=2))
