import unreal as u, json, datetime, traceback
from pathlib import Path
R=Path(u.Paths.project_dir()); MAP='/Game/Conservatory/Maps/L_Exterior_RobotVR'
report={'engine':u.SystemLibrary.get_engine_version(),'timestamp':datetime.datetime.now().isoformat(),'map':MAP}
def finish(error=None):
    if error: report['error']=error
    (R/'Documentation'/'HabitatZoneFootprintAudit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('HABITAT_ZONE_AUDIT_DONE',json.dumps({'passed':not error}))
    try: u.SystemLibrary.quit_editor()
    except Exception: pass
try:
    w=u.EditorLoadingAndSavingUtils.load_map(MAP); actors=list(u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors())
    habitat=[a for a in actors if 'CoreHabitat' in [str(t) for t in a.tags]]
    groups={}
    def vec(v): return [v.x,v.y,v.z]
    def abox(a):
        o,e=a.get_actor_bounds(False); return (vec(o-e),vec(o+e))
    for a in habitat:
        label=a.get_actor_label(); text=label.replace('Core habitat | ','')
        if text.startswith(('Centre','Center')): key='Centre dome'
        elif text.startswith('East walkway'): key='East walkway'
        elif text.startswith('North walkway'): key='North walkway'
        elif text.startswith('West walkway'): key='West walkway'
        elif text.startswith('South walkway'): key='South walkway'
        elif text.startswith('East '): key='East dome'
        elif text.startswith('North '): key='North dome'
        elif text.startswith('West '): key='West dome'
        elif text.startswith('South '): key='South dome'
        else: key='Other'
        groups.setdefault(key,[]).append(abox(a))
    report['groups']={}
    for key,boxes in groups.items():
        mn=[min(b[0][i] for b in boxes) for i in range(3)]; mx=[max(b[1][i] for b in boxes) for i in range(3)]
        report['groups'][key]={'min':mn,'max':mx,'actor_count':len(boxes),'center':[(mn[i]+mx[i])/2 for i in range(3)],'extent':[(mx[i]-mn[i])/2 for i in range(3)]}
    finish()
except Exception: finish(traceback.format_exc())