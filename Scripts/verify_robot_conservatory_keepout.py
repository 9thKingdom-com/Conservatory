import unreal as u,time,json,math,traceback,datetime
from pathlib import Path
R=Path(u.Paths.project_dir());start=time.monotonic();started_game=None;rows={};r11=None;report={'timestamp':datetime.datetime.now().isoformat(),'engine':u.SystemLibrary.get_engine_version()}
def xyz(v): return [v.x,v.y,v.z]
def finish(error=None):
    outdoor=[r for k,r in rows.items() if int(k)<=10]
    if r11 is not None:
        report['robot_11']=r11
    else: report['robot_11']={'error':'missing'}
    report['robots']=rows
    report['passed']=bool(outdoor and len(outdoor)==10 and all(r['inside_failures']==0 and r['destination_failures']==0 and r['distance_cm']>1000 and r['grounded']/max(1,r['samples'])>.95 for r in outdoor) and r11 is not None and r11['distance_cm']<10 and r11['samples']>10)
    if error:
        report['error']=error;report['passed']=False
    (R/'Documentation'/'RobotConservatoryKeepOut-Runtime.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('ROBOT_CONSERVATORY_KEEPOUT_RUNTIME_DONE',json.dumps({'passed':report['passed'],'outdoor_count':len(outdoor),'error':str(error)[:300]}))
    try: u.unregister_slate_post_tick_callback(handle)
    except Exception: pass
    try: u.SystemLibrary.quit_game(w,u.GameplayStatics.get_player_controller(w,0),u.QuitPreference.QUIT,False)
    except Exception: pass
def tick(dt):
    global w,started_game,rows,r11
    try:
        w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
        if not w:return
        pc=u.GameplayStatics.get_player_controller(w,0)
        if not pc:return
        t=u.GameplayStatics.get_time_seconds(w)
        if started_game is None:started_game=t;return
        if t<5:return
        bots=sorted(u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot')),key=lambda b:b.robot_id)
        if len(bots)!=11:
            if time.monotonic()-start>30:finish('expected 11 robots, found '+str(len(bots)))
            return
        if not rows:
            for b in bots:
                rows[str(b.robot_id)]={'start':xyz(b.get_actor_location()),'last':xyz(b.get_actor_location()),'distance_cm':0,'grounded':0,'samples':0,'inside_failures':0,'destination_failures':0,'destinations':[]}
            report['robot_flags']={str(b.robot_id):{'keep_out':b.keep_out_of_conservatory,'clearance':b.conservatory_keep_out_clearance,'mins':len(b.conservatory_keep_out_mins),'maxs':len(b.conservatory_keep_out_maxs),'terrain_wander':b.terrain_wander,'wander_enabled':b.wander_enabled,'patrol_enabled':b.patrol_enabled} for b in bots}
            return
        for b in bots:
            p=xyz(b.get_actor_location());key=str(b.robot_id);r=rows[key]
            r['distance_cm']+=math.dist(p[:2],r['last'][:2]);r['last']=p;r['samples']+=1
            r['grounded']+=b.character_movement.is_moving_on_ground()
            if b.robot_id==11:
                r11=r
            else:
                inside=b.is_inside_conservatory_keep_out(b.get_actor_location())
                r['inside_failures']+=inside
                dest=b.get_wander_destination();d=xyz(dest)
                if any(v!=0 for v in d):
                    r['destination_failures']+=b.is_inside_conservatory_keep_out(dest)
                    if d not in r['destinations']:r['destinations'].append(d)
        if time.monotonic()-start>75:finish()
    except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick)