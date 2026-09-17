import unreal as u, json, datetime, traceback
from pathlib import Path
R=Path(u.Paths.project_dir()); MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
report={'timestamp':datetime.datetime.now().isoformat(),'map':MAP,'engine':u.SystemLibrary.get_engine_version()}
def xyz(v): return [v.x,v.y,v.z]
def tr(a):
    p=a.get_actor_location(); r=a.get_actor_rotation(); s=a.get_actor_scale3d()
    return [p.x,p.y,p.z,r.pitch,r.yaw,r.roll,s.x,s.y,s.z]
def finish(error=None):
    if error: report['error']=error
    (R/'Documentation'/'RobotConservatoryKeepOut.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('ROBOT_CONSERVATORY_KEEPOUT_DONE',json.dumps({'passed':not error,'error':str(error)[:300]}))
    try: u.SystemLibrary.quit_editor()
    except Exception: pass
try:
    w=u.EditorLoadingAndSavingUtils.load_map(MAP); sub=u.get_editor_subsystem(u.EditorActorSubsystem); actors=list(sub.get_all_level_actors())
    report['actor_count_before']=len(actors)
    before={a.get_name():tr(a) for a in actors}
    robots=sorted([a for a in actors if a.get_class().get_name()=='C17Robot'],key=lambda a:a.get_editor_property('robot_id'))
    assert len(robots)==11, f'expected 11 robots, found {len(robots)}'
    habitat=[a for a in actors if 'CoreHabitat' in [str(t) for t in a.tags]]
    assert habitat, 'no CoreHabitat actors found'
    groups={}
    for a in habitat:
        text=a.get_actor_label().replace('Core habitat | ','')
        if text.startswith(('Centre','Center')): key='Centre dome'
        elif 'walkway' in text.lower(): key=text.split()[0].title()+' walkway'
        elif text.startswith(('East','North','West','South')): key=text.split()[0].title()+' dome'
        else: key='Other'
        groups.setdefault(key,[]).append(a)
    zones=[]
    for key,items in groups.items():
        boxes=[]
        for a in items:
            o,e=a.get_actor_bounds(False); boxes.append((xyz(o-e),xyz(o+e)))
        mn=[min(b[0][i] for b in boxes) for i in range(3)]
        mx=[max(b[1][i] for b in boxes) for i in range(3)]
        zones.append({'key':key,'min':mn,'max':mx,'actor_count':len(items),'center':[(mn[i]+mx[i])/2 for i in range(3)],'extent':[(mx[i]-mn[i])/2 for i in range(3)]})
    report['zones']=zones
    mins=[]; maxs=[]
    for z in zones:
        mins.append(u.Vector(*z['min'])); maxs.append(u.Vector(*z['max']))
    rows=[]
    for b in robots:
        rid=b.get_editor_property('robot_id')
        if 1<=rid<=10:
            b.set_editor_property('keep_out_of_conservatory',True)
            b.set_editor_property('conservatory_keep_out_clearance',200.0)
            b.set_editor_property('conservatory_keep_out_mins',mins)
            b.set_editor_property('conservatory_keep_out_maxs',maxs)
        else:
            b.set_editor_property('keep_out_of_conservatory',False)
            b.set_editor_property('conservatory_keep_out_clearance',0.0)
            b.set_editor_property('conservatory_keep_out_mins',[])
            b.set_editor_property('conservatory_keep_out_maxs',[])
            b.set_editor_property('terrain_wander',False)
            b.set_editor_property('wander_enabled',False)
            b.set_editor_property('patrol_enabled',False)
        row={'id':rid,'keep_out':b.get_editor_property('keep_out_of_conservatory'),'clearance':b.get_editor_property('conservatory_keep_out_clearance'),'mins':len(b.get_editor_property('conservatory_keep_out_mins')),'maxs':len(b.get_editor_property('conservatory_keep_out_maxs')),'terrain_wander':b.get_editor_property('terrain_wander'),'wander_enabled':b.get_editor_property('wander_enabled'),'patrol_enabled':b.get_editor_property('patrol_enabled'),'location':xyz(b.get_actor_location())}
        if rid==11:
            row['position_preserved']=xyz(b.get_actor_location())
        rows.append(row)
    report['robots']=rows
    assert len(rows)==11
    assert all(r['keep_out'] is True and r['mins']==9 and r['maxs']==9 for r in rows if r['id']<=10)
    assert rows[10]['keep_out'] is False and rows[10]['terrain_wander'] is False and rows[10]['wander_enabled'] is False and rows[10]['patrol_enabled'] is False
    assert all(before[a.get_name()]==tr(a) for a in actors), 'transforms changed'
    report['transforms_preserved']=True
    assert u.EditorLoadingAndSavingUtils.save_map(w,MAP)
    assert u.EditorLoadingAndSavingUtils.save_dirty_packages(True,True)
    # reload and verify persistence
    w=u.EditorLoadingAndSavingUtils.load_map(MAP); actors=list(sub.get_all_level_actors()); robots=sorted([a for a in actors if a.get_class().get_name()=='C17Robot'],key=lambda a:a.get_editor_property('robot_id'))
    report['actor_count_after_reload']=len(actors)
    assert len(robots)==11
    after=[]
    for b in robots:
        rid=b.get_editor_property('robot_id')
        after.append({'id':rid,'keep_out':b.get_editor_property('keep_out_of_conservatory'),'clearance':b.get_editor_property('conservatory_keep_out_clearance'),'mins':len(b.get_editor_property('conservatory_keep_out_mins')),'maxs':len(b.get_editor_property('conservatory_keep_out_maxs')),'terrain_wander':b.get_editor_property('terrain_wander'),'wander_enabled':b.get_editor_property('wander_enabled'),'patrol_enabled':b.get_editor_property('patrol_enabled'),'inside_keep_out':b.is_inside_conservatory_keep_out(b.get_actor_location())})
    report['after_reload']=after
    assert all(r['keep_out'] is True and r['mins']==9 and r['maxs']==9 for r in after if r['id']<=10)
    assert after[10]['keep_out'] is False and after[10]['terrain_wander'] is False and after[10]['wander_enabled'] is False and after[10]['patrol_enabled'] is False
    assert not after[10]['inside_keep_out']
    report['saved_and_reloaded']=True
    finish()
except Exception: finish(traceback.format_exc())