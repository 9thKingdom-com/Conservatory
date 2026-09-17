import unreal as u, time, json, math, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
started = time.monotonic()
stage = 0
idx = 0
mark = 0.0
rows = []
report = {}

def tick(dt):
    global stage, idx, mark
    w = u.find_object(None, "/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR")
    if not w:
        return
    pc = u.GameplayStatics.get_player_controller(w, 0)
    if not pc:
        return
    now = u.GameplayStatics.get_time_seconds(w)
    t = now - mark

    def finish(error=None):
        report.update(error=error, suits=rows)
        (R / "Documentation" / "SuitInteractionDiagnostic.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print("SUIT_DIAGNOSTIC_DONE", json.dumps({"suits": len(rows), "error": error}))
        u.unregister_slate_post_tick_callback(handle)
        u.SystemLibrary.quit_game(w, pc, u.QuitPreference.QUIT, False)

    try:
        if time.monotonic() - started > 150:
            finish("timeout")
            return
        human = u.GameplayStatics.get_player_pawn(w, 0)
        suits = sorted(u.GameplayStatics.get_all_actors_of_class(w, u.load_class(None, "/Script/Conservatory.VRSuitStation")), key=lambda s: s.robot_id)
        hub = u.GameplayStatics.get_actor_of_class(w, u.load_class(None, "/Script/Conservatory.RobotVRHub"))
        if stage == 0:
            if now > 5:
                report["hub_is_remote_at_start"] = hub.is_remote()
                stage = 1
                mark = now
            return
        if stage == 1:
            if idx == len(suits):
                finish(None)
                return
            s = suits[idx]
            p = s.get_actor_location() + s.get_actor_forward_vector() * 60 + u.Vector(0, 0, 87)
            human.set_actor_location(p, False, True)
            human.character_movement.stop_movement_immediately()
            pc.set_control_rotation(u.Rotator(pitch=0, yaw=s.get_actor_rotation().yaw + 180, roll=0))
            stage = 2
            mark = now
            return
        if stage == 2 and t > 1.2:
            s = suits[idx]
            eye = pc.player_camera_manager.get_camera_location()
            view = pc.get_control_rotation()
            row = {"id": s.robot_id, "can_use": s.can_use(), "hub_is_remote": hub.is_remote()}
            p = human.get_actor_location()
            row["pawn_pos"] = [p.x, p.y, p.z]
            row["camera_eye"] = [eye.x, eye.y, eye.z]
            row["view_rot"] = [view.pitch, view.yaw, view.roll]
            row["targets"] = []
            vr = u.MathLibrary.get_forward_vector(view)
            for height in (80.0, 120.0, 170.0):
                target = s.get_actor_location() + u.Vector(0, 0, height)
                delta = u.Vector(target.x - eye.x, target.y - eye.y, target.z - eye.z)
                nlen = math.sqrt(delta.x * delta.x + delta.y * delta.y + delta.z * delta.z)
                dot = (vr.x * delta.x + vr.y * delta.y + vr.z * delta.z) / max(nlen, 0.001)
                hit = u.SystemLibrary.line_trace_single(w, eye, target, u.TraceTypeQuery.ECC_VISIBILITY, False, [human], u.DrawDebugTrace.NONE)
                tup = hit.to_tuple() if hit else None
                row["targets"].append({
                    "height": height,
                    "target": [target.x, target.y, target.z],
                    "distance_cm": nlen,
                    "dot": round(dot, 4),
                    "blocked": bool(tup and tup[0]),
                    "blocking": str(tup[9]) if tup and tup[0] else None,
                })
            nearby = []
            for a in u.GameplayStatics.get_all_actors_of_class(w, u.Actor):
                d = u.Vector(a.get_actor_location().x - s.get_actor_location().x, a.get_actor_location().y - s.get_actor_location().y, a.get_actor_location().z - s.get_actor_location().z)
                dist = math.sqrt(d.x * d.x + d.y * d.y + d.z * d.z)
                if 0 < dist < 350:
                    nearby.append({"name": a.get_name(), "class": a.get_class().get_name(), "label": a.get_actor_label(), "dist_cm": round(dist)})
            row["nearby_actors"] = sorted(nearby, key=lambda n: n["dist_cm"])[:12]
            rows.append(row)
            idx += 1
            stage = 1
            return
    except Exception:
        finish(traceback.format_exc())

handle = u.register_slate_post_tick_callback(tick)