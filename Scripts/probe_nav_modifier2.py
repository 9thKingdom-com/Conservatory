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
    b=v.get_component_by_class(u.BrushComponent); report['brush_found']=bool(b)
    if b:
        report['props']=[p for p in dir(b) if 'brush' in p.lower() or 'builder' in p.lower() or 'shape' in p.lower() or 'extent' in p.lower() or 'box' in p.lower()]
        report['class_props']=[]
        cls=b.get_class()
        try:
            report['class_name']=cls.get_name()
            report['properties']=[p for p in dir(cls) if 'brush' in p.lower() or 'builder' in p.lower() or 'shape' in p.lower() or 'extent' in p.lower()]
        except Exception as e: report['class_error']=str(e)
        for method in ['set_box_extent','set_collision_profile_name','set_static_mesh','set_editor_property']:
            report['has_'+method]=hasattr(b,method)
    for cname in ['CubeBuilder','CylinderBuilder']:
        try:
            c=u.find_class(cname)
            report['found_'+cname]=str(c)
            if c:
                obj=u.new_object(c)
                report[cname+'_props']=[p for p in dir(obj) if p.lower() in ['x','y','z','sides','radius','height','name']]
        except Exception as e: report['error_'+cname]=str(e)
    v.destroy_actor(); finish()
except Exception: finish(traceback.format_exc())