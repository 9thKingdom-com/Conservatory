import unreal as u, json, datetime, traceback
from pathlib import Path
R=Path(u.Paths.project_dir()); MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
report={'engine':u.SystemLibrary.get_engine_version(),'timestamp':datetime.datetime.now().isoformat(),'map':MAP}
def finish(error=None):
    if error: report['error']=error
    out=R/'Documentation'/'RobotZoneAudit.json'; out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('ROBOT_ZONE_AUDIT_DONE',json.dumps({'passed':not error,'error':str(error)[:250]}))
    try: u.SystemLibrary.quit_editor()
    except Exception: pass
try:
    w=u.EditorLoadingAndSavingUtils.load_map(MAP)
    sub=u.get_editor_subsystem(u.EditorActorSubsystem); actors=list(sub.get_all_level_actors())
    report['actor_count']=len(actors)
    robots=sorted([a for a in actors if a.get_class().get_name()=='C17Robot'],key=lambda a:a.get_editor_property('robot_id'))
    habitat=[a for a in actors if 'CoreHabitat' in [str(t) for t in a.tags]]
    navs=[a for a in actors if a.get_class().get_name() in ['NavMeshBoundsVolume','NavModifierVolume','RecastNavMesh']]
    def vec(v): return [v.x,v.y,v.z]
    def box(a):
        o,e=a.get_actor_bounds(False); return {'min':vec(o-e),'max':vec(o+e)}
    report['robots']=[]
    for b in robots:
        row={'id':b.get_editor_property('robot_id'),'name':b.get_name(),'label':b.get_actor_label(),'location':vec(b.get_actor_location()),'folder':str(b.get_folder_path()),'is_spatially_loaded':b.get_editor_property('is_spatially_loaded')}
        for p in ['terrain_wander','wander_enabled','patrol_enabled','limit_terrain_wander']:
            try: row[p]=b.get_editor_property(p)
            except Exception: row[p]='ERR'
        try:
            row['wander_bounds_min']=vec(b.get_editor_property('wander_bounds_min')); row['wander_bounds_max']=vec(b.get_editor_property('wander_bounds_max'))
        except Exception: pass
        report['robots'].append(row)
    boxes=[box(a) for a in habitat]
    mins=[min(b['min'][i] for b in boxes) for i in range(3)] if boxes else None
    maxs=[max(b['max'][i] for b in boxes) for i in range(3)] if boxes else None
    report['habitat_union_bounds']={'min':mins,'max':maxs,'actor_count':len(habitat)}
    report['habitat_actors_sample']=[{'name':a.get_name(),'label':a.get_actor_label(),'box':box(a)} for a in habitat[:24]]
    report['nav_actors']=[{'name':a.get_name(),'class':a.get_class().get_name(),'label':a.get_actor_label(),'folder':str(a.get_folder_path()),'bounds':box(a)} for a in navs]
    finish()
except Exception: finish(traceback.format_exc())