import unreal as u, time, json, datetime, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
start = time.monotonic()
rows = {}
last = 0.0
photo = False
world_seen_at = None
result = {}

def tick(dt):
    global last, photo, world_seen_at
    try:
        w = u.find_object(None, "/Game/Conservatory/Maps/L_Exterior_RobotVR.L_Exterior_RobotVR")
        if not w:
            return
        if world_seen_at is None:
            world_seen_at = round(time.monotonic() - start, 2)
        pc = u.GameplayStatics.get_player_controller(w, 0)
        if not pc:
            return
        t = u.GameplayStatics.get_time_seconds(w)

        def finish(error=None):
            result.update({
                "engine": u.SystemLibrary.get_engine_version(),
                "timestamp": datetime.datetime.now().isoformat(),
                "seconds_from_script_start_to_world": world_seen_at,
                "game_time_seconds": round(t, 1),
                "robots_seen": len(rows),
                "robots": rows,
                "screenshot": str(R / "Documentation" / "MeshPartitionFix-Runtime.png"),
                "error": error,
            })
            (R / "Documentation" / "MeshPartitionFix-Runtime.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            print("MESHPARTITION_RUNTIME_DONE", json.dumps({"robots": len(rows), "game_time": result["game_time_seconds"], "error": error}))
            u.unregister_slate_post_tick_callback(handle)
            u.SystemLibrary.quit_game(w, pc, u.QuitPreference.QUIT, False)

        if time.monotonic() - start > 150:
            finish("timeout")
            return
        bots = u.GameplayStatics.get_all_actors_of_class(w, u.load_class(None, "/Script/Conservatory.C17Robot"))
        for b in bots:
            key = str(b.robot_id)
            p = b.get_actor_location()
            if key not in rows:
                rows[key] = {"start": [p.x, p.y, p.z], "last": [p.x, p.y, p.z], "distance_cm": 0.0, "samples": 0}
            r = rows[key]
            r["distance_cm"] += abs(p.x - r["last"][0]) + abs(p.y - r["last"][1])
            r["last"] = [p.x, p.y, p.z]
            r["samples"] += 1
        if not photo and t > 15:
            u.SystemLibrary.execute_console_command(w, 'HighResShot 1280x720 filename="' + (R / "Documentation" / "MeshPartitionFix-Runtime.png").as_posix() + '"')
            photo = True
        if t > 40:
            finish(None)
    except Exception:
        try:
            finish(traceback.format_exc())
        except Exception:
            pass

handle = u.register_slate_post_tick_callback(tick)