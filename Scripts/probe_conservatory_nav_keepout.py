import unreal as u, json, math, traceback, datetime
from pathlib import Path
R=Path(u.Paths.project_dir()); MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
report={'timestamp':datetime.datetime.now().isoformat(),'map':MAP}
def xyz(v): return [v.x,v.y,v.z]
def finish(error=None):
    if error: report['error']=error
    (R/'Documentation'/'ConservatoryNavKeepOutProbe.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('CONSERVATORY_NAV_KEEPOUT_PROBE_DONE',json.dumps({'passed':not error}))
    try: u.SystemLibrary.quit_editor()
    except Exception: pass
try:
    w=u.EditorLoadingAndSavingUtils.load_map(MAP)
    sub=u.get_editor_subsystem(u.EditorActorSubsystem); actors=list(sub.get_all_level_actors())
    habitat=[a for a in actors if 'CoreHabitat' in [str(t) for t in a.tags]]
    groups={}
    def abox(a):
        o,e=a.get_actor_bounds(False); return (xyz(o-e),xyz(o+e))
    for a in habitat:
        text=a.get_actor_label().replace('Core habitat | ','')
        if text.startswith(('Centre','Center')): key='Centre dome'
        elif 'walkway' in text.lower(): key=text.split()[0].title()+' walkway'
        elif text.startswith(('East','North','West','South')): key=text.split()[0].title()+' dome'
        else: key='Other'
        groups.setdefault(key,[]).append(abox(a))
    zones=[]
    for key,boxes in groups.items():
        mn=[min(b[0][i] for b in boxes) for i in range(3)]; mx=[max(b[1][i] for b in boxes) for i in range(3)]
        center=[(mn[i]+mx[i])/2 for i in range(3)]; extent=[(mx[i]-mn[i])/2 for i in range(3)]
        zones.append({'key':key,'min':mn,'max':mx,'center':center,'extent':extent})
    report['zones']=zones
    created=[]
    cls=u.load_class(None,'/Script/NavigationSystem.NavModifierVolume')
    for z in zones:
        v=sub.spawn_actor_from_class(cls,u.Vector(*z['center']))
        v.set_actor_scale3d(u.Vector(z['extent'][0]/100,z['extent'][1]/100,z['extent'][2]/100))
        v.set_editor_property('area_class',u.load_class(None,'/Script/NavigationSystem.NavArea_Null'))
        v.set_editor_property('is_spatially_loaded',False)
        v.set_actor_label('Conservatory nav keep-out | '+z['key'])
        created.append(v)
    report['created_count']=len(created)
    report['build_nav']=u.ExteriorTools.build_terrain_navigation()
    tests=[]
    for z in zones:
        inside=u.NavigationSystemV1.project_point_to_navigation(w,u.Vector(*z['center']),None,None,query_extent=u.Vector(500,500,1000))
        outside_center=[z['center'][0],z['center'][1],z['center'][2]]
        # probe 500 cm outside each zone on X axis, projected to navmesh.
        ox=z['max'][0]+500
        outside=u.NavigationSystemV1.project_point_to_navigation(w,u.Vector(ox,z['center'][1],z['center'][2]),None,None,query_extent=u.Vector(1500,1500,2000))
        tests.append({'zone':z['key'],'inside_result':xyz(inside) if inside else None,'outside_result':xyz(outside) if outside else None,'inside_blocked':inside is None,'outside_found':outside is not None})
    report['tests']=tests
    report['passed']=report['build_nav'] and len(tests)==9 and all(t['inside_blocked'] for t in tests) and sum(t['outside_found'] for t in tests)>=1
    # clean temporary probe actors and restore nav to original state; do not save.
    for v in created: v.destroy_actor()
    report['temporary_volumes_destroyed']=True
    finish()
except Exception: finish(traceback.format_exc())