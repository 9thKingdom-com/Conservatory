import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat(), "meshes": {}}
try:
    sub = u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
    targets = ["/Game/Conservatory/Botanical/TreeMaster/SM_TreeMaster_Structure", "/Game/Conservatory/Architecture/LiftMaster/SM_LiftMaster_Solid"]
    for path in targets:
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
            md["before_num_vertices"] = str(sm.get_num_vertices(0))
        except Exception as e:
            md["before_num_vertices_error"] = str(e)
        try:
            md["before_nav_collision"] = str(sm.get_editor_property("nav_collision"))
        except Exception as e:
            md["before_nav_collision_error"] = str(e)
        if str(path).endswith("SM_TreeMaster_Structure"):
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
        try:
            md["after_nav_collision"] = str(sm.get_editor_property("nav_collision"))
        except Exception as e:
            md["after_nav_collision_error"] = str(e)
        report["meshes"][str(path)] = md
    out = R / "Documentation" / "HeavyNavMeshFixResult.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("HEAVY_NAV_MESH_FIX_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "HeavyNavMeshFixResult.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("HEAVY_NAV_MESH_FIX_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass