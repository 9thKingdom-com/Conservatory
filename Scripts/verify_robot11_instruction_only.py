import unreal as u,time,json,math,traceback,datetime
from pathlib import Path
R=Path(u.Paths.project_dir());start=time.monotonic();stage=0;mark=0;robot=None;hub=None;human=None;start_pos=None;before_pos=None;report={'timestamp':datetime.datetime.now().isoformat(),'engine':u.SystemLibrary.get_engine_version()}
def xyz(v): return [v.x,v.y,v.z]
def finish(error=None):
    if error: report['error']=error
    report['passed']=not error
    (R/'Documentation'/'Robot11InstructionOnly.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('ROBOT11_INSTRUCTION_ONLY_DONE',json.dumps({'passed':not error,'error':str(error)[:300]}))
    try: u.unregister_slate_post_tick_callback(handle)
    except Exception: pass
    try: u.SystemLibrary.quit_game(w,u.GameplayStatics.get_player_controller(w,0),u.QuitPreference.QUIT,False)
    except Exception: pass
def tick(dt):
    global stage,mark,robot,hub,human,start_pos,before_pos
    try:
        w=u.find_object(None,'/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR')
        if not w:return
        pc=u.GameplayStatics.get_player_controller(w,0)
        if not pc:return
        now=u.GameplayStatics.get_time_seconds(w);t=now-mark
        if stage==0:
            if now<5:return
            hub=u.GameplayStatics.get_actor_of_class(w,u.load_class(None,'/Script/Conservatory.RobotVRHub'))
            robots=u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot'))
            robot=next((b for b in robots if b.robot_id==11),None);human=u.GameplayStatics.get_player_pawn(w,0)
            if not robot or not hub:finish('missing robot 11 or hub');return
            report['autonomous_position']=xyz(robot.get_actor_location());start_pos=xyz(robot.get_actor_location())
            # Put the human at the wall monitor so EnterRobot can authorize instruction control directly.
            human.set_actor_location(hub.get_actor_location()+u.Vector(0,0,87),False,True);human.character_movement.stop_movement_immediately();pc.set_control_rotation(u.Rotator(pitch=0,yaw=180,roll=0))
            stage=1;mark=now;return
        if stage==1 and t>0.5:
            report['can_enter']=hub.enter_robot(11);report['entered']=u.GameplayStatics.get_player_pawn(w,0)==robot
            if not report['entered']:finish('robot 11 could not be possessed');return
            stage=2;mark=now;return
        elif stage==2:
            if t<1.5:
                robot.add_movement_input(robot.get_actor_forward_vector(),1,False)
            else:
                before_pos=xyz(robot.get_actor_location());report['instructed_position']=before_pos;report['instruction_move_cm']=math.dist(start_pos,before_pos);stage=3;mark=now
            return
        elif stage==3 and t>0.5:
            report['returned']=hub.return_to_human();report['human_after']=u.GameplayStatics.get_player_pawn(w,0)==human
            stage=4;mark=now;return
        elif stage==4 and t>5:
            robot=next((b for b in u.GameplayStatics.get_all_actors_of_class(w,u.load_class(None,'/Script/Conservatory.C17Robot')) if b.robot_id==11),None)
            report['returned_position']=xyz(robot.get_actor_location()) if robot else None
            report['passed']=report.get('entered') is True and report.get('instruction_move_cm',0)>20 and report.get('returned') is True and math.dist(report['returned_position'] or [0,0,0],before_pos or [999999]*3)<50
            finish()
    except Exception:finish(traceback.format_exc())
handle=u.register_slate_post_tick_callback(tick)