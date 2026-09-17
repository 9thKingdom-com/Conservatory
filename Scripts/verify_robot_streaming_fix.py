import unreal as u, time, json, math, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
started = time.monotonic()
stage = 0
idx = 0
mark = 0.0
rows = []
report = {}
human = None
robot_start = None
before = None

def xyz(v):
    return [v.x, v.y, v.z]

def tick(dt):
    global stage, idx, mark, human, robot_start, before
    w = u.find_object(None, "/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR")
    if not w:
        return
    pc = u.GameplayStatics.get_player_controller(w, 0)
    if not pc:
        return
    now = u.GameplayStatics.get_time_seconds(w)
    t = now - mark

    def finish(error=None):
        longhold = report.get("long_hold", {})
        suit_pass = len(rows) == 11 and all(r.get("wear") and r.get("correct") and r.get("returned") and r.get("return_error", 999) < 1 for r in rows)
        hold_pass = longhold.get("held_ok") and longhold.get("returned") and longhold.get("pawn_is_human_after") and longhold.get("return_pos_error", 999) < 1
        report.update(error=error, suits=rows, long_hold=longhold, passed=bool(suit_pass and hold_pass))
        (R / "Documentation" / "RobotStreamingFix-Runtime.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print("ROBOT_STREAMING_RUNTIME_DONE", json.dumps({"passed": report["passed"], "suits": len(rows), "error": error}))
        u.unregister_slate_post_tick_callback(handle)
        u.SystemLibrary.quit_game(w, pc, u.QuitPreference.QUIT, False)

    try:
        if time.monotonic() - started > 180:
            finish("timeout")
            return
        suits = sorted(u.GameplayStatics.get_all_actors_of_class(w, u.load_class(None, "/Script/Conservatory.VRSuitStation")), key=lambda s: s.robot_id)
        hub = u.GameplayStatics.get_actor_of_class(w, u.load_class(None, "/Script/Conservatory.RobotVRHub"))
        robots = u.GameplayStatics.get_all_actors_of_class(w, u.load_class(None, "/Script/Conservatory.C17Robot"))
        if stage == 0:
            if now > 5:
                human = u.GameplayStatics.get_player_pawn(w, 0)
                report["robots_found_at_start"] = len(robots)
                report["robot_positions_at_start"] = {str(b.robot_id): xyz(b.get_actor_location()) for b in robots}
                report["suits_found"] = len(suits)
                report["hub_found"] = hub is not None
                report["select_robot_results"] = {}
                for rid in range(1, 12):
                    report["select_robot_results"][str(rid)] = hub.select_robot(rid)
                report["all_selects_ok"] = all(report["select_robot_results"].values())
                if len(robots) != 11 or len(suits) != 11 or hub is None or not report["all_selects_ok"]:
                    finish("startup check failed: robots=%d suits=%d hub=%s selects_ok=%s" % (len(robots), len(suits), hub is not None, report["all_selects_ok"]))
                    return
                stage = 1
                mark = now
            return
        if stage == 1:
            if idx == len(suits):
                stage = 4
                return
            s = suits[idx]
            p = s.get_actor_location() + s.get_actor_forward_vector() * 60 + u.Vector(0, 0, 87)
            human.set_actor_location(p, False, True)
            human.character_movement.stop_movement_immediately()
            pc.set_control_rotation(u.Rotator(pitch=0, yaw=s.get_actor_rotation().yaw + 180, roll=0))
            stage = 2
            mark = now
            return
        if stage == 2 and t > 1:
            s = suits[idx]
            before = xyz(human.get_actor_location())
            row = dict(id=s.robot_id, can_use=s.can_use())
            rows.append(row)
            eye = pc.player_camera_manager.get_camera_location()
            target = s.get_actor_location() + u.Vector(0, 0, 120)
            hit = u.SystemLibrary.line_trace_single(w, eye, target, u.TraceTypeQuery.ECC_VISIBILITY, False, [human], u.DrawDebugTrace.NONE)
            tup = hit.to_tuple() if hit else None
            row["camera_eye"] = [eye.x, eye.y, eye.z]
            row["blocked_by"] = str(tup[9]) if tup and tup[0] else None
            near = []
            for b in robots:
                d = u.Vector(b.get_actor_location().x - s.get_actor_location().x, b.get_actor_location().y - s.get_actor_location().y, b.get_actor_location().z - s.get_actor_location().z)
                dist = (d.x*d.x + d.y*d.y + d.z*d.z) ** 0.5
                if dist < 600:
                    near.append({"robot_id": str(b.robot_id), "dist_cm": round(dist)})
            row["robots_within_600cm"] = near
            row["wear"] = s.wear_suit()
            if row["wear"]:
                pawn = u.GameplayStatics.get_player_pawn(w, 0)
                row["correct"] = pawn.robot_id == s.robot_id
                robot_start = xyz(pawn.get_actor_location())
                stage = 3
                mark = now
            else:
                idx += 1
                stage = 1
            return
        if stage == 3:
            pawn = u.GameplayStatics.get_player_pawn(w, 0)
            if t < 1:
                pawn.add_movement_input(pawn.get_actor_forward_vector(), 1, False)
            else:
                rows[-1]["robot_moved_cm"] = math.dist(robot_start, xyz(pawn.get_actor_location()))
                rows[-1]["returned"] = hub.return_to_human()
                rows[-1]["return_error"] = math.dist(before, xyz(u.GameplayStatics.get_player_pawn(w, 0).get_actor_location()))
                idx += 1
                stage = 1
            return
        if stage == 4:
            s = suits[7]
            p = s.get_actor_location() + s.get_actor_forward_vector() * 60 + u.Vector(0, 0, 87)
            human.set_actor_location(p, False, True)
            human.character_movement.stop_movement_immediately()
            pc.set_control_rotation(u.Rotator(pitch=0, yaw=s.get_actor_rotation().yaw + 180, roll=0))
            report["suit_before_long_hold"] = xyz(human.get_actor_location())
            stage = 5
            mark = now
            return
        if stage == 5 and t > 1:
            s = suits[7]
            longhold = dict(id=8, can_use=s.can_use(), wear=s.wear_suit())
            report["long_hold"] = longhold
            if longhold["wear"]:
                pawn = u.GameplayStatics.get_player_pawn(w, 0)
                longhold["correct"] = pawn.robot_id == 8
                longhold["start_z"] = pawn.get_actor_location().z
                longhold["min_z"] = longhold["start_z"]
                stage = 6
                mark = now
            else:
                finish("long hold wear failed: can_use=%s" % longhold["can_use"])
                return
            return
        if stage == 6:
            pawn = u.GameplayStatics.get_player_pawn(w, 0)
            is_robot = False
            try:
                is_robot = pawn.robot_id == 8
            except Exception:
                is_robot = False
            if not is_robot:
                report["long_hold"]["auto_returned_early"] = True
                report["long_hold"]["held_seconds"] = round(t, 2)
                finish("long hold: pawn left robot early at %.2fs" % t)
                return
            report["long_hold"]["min_z"] = min(report["long_hold"]["min_z"], pawn.get_actor_location().z)
            if t > 6:
                report["long_hold"]["held_ok"] = True
                report["long_hold"]["end_z"] = pawn.get_actor_location().z
                report["long_hold"]["returned"] = hub.return_to_human()
                report["long_hold"]["pawn_is_human_after"] = u.GameplayStatics.get_player_pawn(w, 0) == human
                report["long_hold"]["return_pos_error"] = math.dist(report["suit_before_long_hold"], xyz(u.GameplayStatics.get_player_pawn(w, 0).get_actor_location()))
                u.SystemLibrary.execute_console_command(w, "HighResShot 1280x720 filename=" + chr(34) + (R / "Documentation" / "RobotStreamingFix-Runtime.png").as_posix() + chr(34))
                finish(None)
            return
    except Exception:
        finish(traceback.format_exc())

handle = u.register_slate_post_tick_callback(tick)