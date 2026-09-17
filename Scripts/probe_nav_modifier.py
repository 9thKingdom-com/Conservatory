import unreal as u, json, datetime, traceback
from pathlib import Path
R=Path(u.Paths.project_dir()); MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
report={}
def xyz(v): return [v.x,v.y,v.z]
def finish(error=None):
    if error: report['error']=error
    (R/'Documentation'/'NavModifierProbe.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('NAV_MODIFIER_PROBE_DONE',json.dumps({'passed':not error}))
    try: u.SystemLibrary.quit_editor()
    except Exception: pass
try:
    w=u.EditorLoadingAndSavingUtils.load_map(MAP)
    cls=u.load_class(None,'/Script/NavigationSystem.NavModifierVolume')
    v=u.get_editor_subsystem(u.EditorActorSubsystem).spawn_actor_from_class(cls,u.Vector(-14000,-1000,6600))
    if not v: raise RuntimeError('spawn failed')
    report['components_by_class']={name:[c.get_path_name() for c in v.get_components_by_class(cls2)] for name,cls2 in [('Brush',u.BrushComponent),('Primitive',u.PrimitiveComponent),('Shape',u.ShapeComponent)]}
    b=v.get_component_by_class(u.BrushComponent)
    report['brush_found']=bool(b)
    if b:
        report['brush_properties']=[p for p in dir(b) if 'brush' in p.lower() or 'shape' in p.lower() or 'extent' in p.lower() or 'box' in p.lower()][:200]
        for prop in ['brush_builder','brush','area_class']:
            try: report[prop]=str(b.get_editor_property(prop))
            except Exception as e: report[prop+'_error']=str(e)
        report['bounds_default']={'min':xyz(v.get_actor_bounds(False)[0]-v.get_actor_bounds(False)[1]),'max':xyz(v.get_actor_bounds(False)[0]+v.get_actor_bounds(False)[1]),'extent':[abs(x) for x in xyz(v.get_actor_bounds(False)[0]-v.get_actor_bounds(False)[1])]}
        for scale in [1,10,50]:
            v.set_actor_scale3d(u.Vector(scale,scale,scale))
            o,e=v.get_actor_bounds(False)
            report['bounds_scale_'+str(scale)]={'min':xyz(o-e),'max':xyz(o+e),'extent':[abs(x) for x in xyz(o-e)]}
        for builder_name in ['CubeBuilder','CylinderBuilder']:
            try:
                bcls=u.load_class(None,'/Script/Engine.'+builder_name)
                report[builder_name+'_class']=str(bcls)
                builder=u.new_object(builder_name)
                report[builder_name+'_props']=[p for p in dir(builder) if p.lower() in ['x','y','z','sides','radius','height','name']]
            except Exception as e: report[builder_name+'_error']=str(e)
    v.destroy_actor(); report['probe_actor_destroyed']=True; report['map_dirty']=u.EditorLoadingAndSavingUtils.get_dirty_package_names()
    finish()
except Exception: finish(traceback.format_exc())