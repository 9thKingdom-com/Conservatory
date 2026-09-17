import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    sub = u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
    path = "/Game/Conservatory/Architecture/LiftMaster/SM_LiftMaster_Solid"
    sm = u.EditorAssetLibrary.load_asset(path)
    md = {"path": str(sm.get_path_name()), "name": str(sm.get_name())}
    try:
        md["before_collision_complexity"] = str(sub.get_collision_complexity(sm))
    except Exception as e:
        md["before_collision_complexity_error"] = str(e)
    try:
        md["before_simple_collision_count"] = str(sub.get_simple_collision_count(sm))
    except Exception as e:
        md["before_simple_collision_count_error"] = str(e)
    try:
        md["before_convex_collision_count"] = str(sub.get_convex_collision_count(sm))
    except Exception as e:
        md["before_convex_collision_count_error"] = str(e)
    try:
        md["before_num_triangles"] = str(sm.get_num_triangles(0))
    except Exception as e:
        md["before_num_triangles_error"] = str(e)
    try:
        added = int(sub.add_simple_collisions(sm, u.ScriptCollisionShapeType.NDOP26))
        md["added_simple_collision_count"] = str(added)
    except Exception as e:
        md["add_simple_collision_error"] = str(e)
    try:
        body = sm.get_editor_property("body_setup")
        body.set_editor_property("collision_trace_flag", u.CollisionTraceFlag.CTF_USE_SIMPLE_AS_COMPLEX)
        md["collision_trace_flag_after_set"] = str(body.get_editor_property("collision_trace_flag"))
        sm.set_editor_property("body_setup", body)
    except Exception as e:
        md["set_collision_trace_flag_error"] = str(e)
    try:
        saved = u.EditorAssetLibrary.save_asset(path)
        md["saved"] = bool(saved)
    except Exception as e:
        md["save_error"] = str(e)
    try:
        md["after_collision_complexity"] = str(sub.get_collision_complexity(sm))
    except Exception as e:
        md["after_collision_complexity_error"] = str(e)
    try:
        md["after_simple_collision_count"] = str(sub.get_simple_collision_count(sm))
    except Exception as e:
        md["after_simple_collision_count_error"] = str(e)
    try:
        md["after_convex_collision_count"] = str(sub.get_convex_collision_count(sm))
    except Exception as e:
        md["after_convex_collision_count_error"] = str(e)
    report["mesh"] = md
    out = R / "Documentation" / "HeavyNavMeshLiftSimpleCollision.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("LIFT_SIMPLE_COLLISION_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "HeavyNavMeshLiftSimpleCollision.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("LIFT_SIMPLE_COLLISION_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass