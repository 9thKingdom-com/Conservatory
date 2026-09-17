import unreal as u
import time
import json
import math
import datetime
import traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
start = time.monotonic()
rows = {}
last_sample = 0.0
photo = False

def xyz(p):
    return [p.x, p.y, p.z]

def tick(dt):
    global last_sample, photo
    try:
        w = u.find_object(None, "/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR")
        if not w:
            return
        pc = u.GameplayStatics.get_player_controller(w, 0)
        if not pc:
            return
        t = u.GameplayStatics.get_time_seconds(w)

        def finish(error=None):
            grounded = sum(r["grounded"] for r in rows.values())
            samples = sum(r["samples"] for r in rows.values())
            moved = [k for k, r in rows.items() if r["distance_cm"] > 1000 and k != "11"]
            stationary_11 = rows.get("11", {}).get("distance_cm", 999999) < 10
            result = {
                "engine": u.SystemLibrary.get_engine_version(),
                "timestamp": datetime.datetime.now().isoformat(),
                "seconds_from_script_start_to_world": round(start - start, 3),
                "game_time_seconds": round(t, 1),
                "robots_seen": len(rows),
                "grounded_samples": grounded,
                "total_samples": samples,
                "grounded_fraction": round(grounded / max(1, samples), 4),
                "outdoor_moved_count": len(moved),
                "robot11_stationary": stationary_11,
                "error": error,
                "robots": rows,
            }
            (R / "Documentation" / "HeavyNavMeshRuntime.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            print("HEAVY_NAV_MESH_RUNTIME_DONE", json.dumps({"robots": len(rows), "game_time": round(t, 1), "error": error}))
            u.unregister_slate_post_tick_callback(handle)
            u.SystemLibrary.quit_game(w, pc, u.QuitPreference.QUIT, False)

        if time.monotonic() - start > 150:
            finish("timeout")
            return
        if t < 5 or t - last_sample < 0.2:
            return
        last_sample = t
        bots = u.GameplayStatics.get_all_actors_of_class(w, u.load_class(None, "/Script/Conservatory.C17Robot"))
        for b in bots:
            p = xyz(b.get_actor_location())
            key = str(b.robot_id)
            if key not in rows:
                rows[key] = {"start": p, "last": p, "distance_cm": 0, "grounded": 0, "samples": 0}
            r = rows[key]
            r["distance_cm"] += math.dist(p[:2], r["last"][:2])
            r["last"] = p
            r["samples"] += 1
            r["grounded"] += 1 if b.character_movement.is_moving_on_ground() else 0

        if not photo and t > 15:
            p = u.GameplayStatics.get_player_pawn(w, 0)
            b = next(b for b in bots if b.robot_id == 3)
            p.set_actor_enable_collision(False)
            p.character_movement.set_movement_mode(u.MovementMode.MOVE_FLYING)
            p.set_actor_location(b.get_actor_location() + u.Vector(-700, -700, 400), False, True)
            pc.set_control_rotation(u.Rotator(pitch=-18, yaw=45, roll=0))
            photo = True
        if photo and t > 17 and photo is True:
            u.SystemLibrary.execute_console_command(
                w,
                "HighResShot 1280x720 filename=\"" + (R / "Documentation" / "HeavyNavMeshRuntime.png").as_posix() + "\"",
            )
            photo = "done"
        if t > 40:
            finish(None)
    except Exception:
        try:
            finish(traceback.format_exc())
        except Exception:
            pass

handle = u.register_slate_post_tick_callback(tick)