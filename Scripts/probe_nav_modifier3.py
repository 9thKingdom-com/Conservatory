import unreal as u, json, traceback
from pathlib import Path
R=Path(u.Paths.project_dir()); report={}
def finish(error=None):
    if error: report['error']=error
    (R/'Documentation'/'NavModifierProbe.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('NAV_MODIFIER_PROBE_DONE',json.dumps({'passed':not error}))
    try: u.SystemLibrary.quit_editor()
    except Exception: pass
try:
    u.EditorLoadingAndSavingUtils.load_map('/Game/Conservatory/Maps/L_Exterior_RobotVR')
    v=u.get_editor_subsystem(u.EditorActorSubsystem).spawn_actor_from_class(u.load_class(None,'/Script/NavigationSystem.NavModifierVolume'),u.Vector(-14000,-1000,6600))
    report['actor']=str(v)
    for prop in ['area_class','area_class_to_replace']:
        try: report[prop]=str(v.get_editor_property(prop))
        except Exception as e: report[prop+'_error']=str(e)
    try:
        v.set_editor_property('area_class',u.load_class(None,'/Script/NavigationSystem.NavArea_Null'))
        report['area_after']=str(v.get_editor_property('area_class'))
    except Exception as e: report['set_area_error']=str(e)
    try: report['spatial_before']=v.get_editor_property('is_spatially_loaded')
    except Exception as e: report['spatial_error']=str(e)
    v.destroy_actor(); finish()
except Exception: finish(traceback.format_exc())