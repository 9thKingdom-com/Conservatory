import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat(), "meshes": {}}
try:
    sub = u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
    for path in ["/Game/Conservatory/Botanical/TreeMaster/SM_TreeMaster_Structure", "/Game/Conservatory/Architecture/LiftMaster/SM_LiftMaster_Solid"]:
        sm = u.EditorAssetLibrary.load_asset(path)
        md = {"path": str(sm.get_path_name()), "name": str(sm.get_name())}
        try:
            md["collision_complexity"] = str(sub.get_collision_complexity(sm))
        except Exception as e:
            md["collision_complexity_error"] = str(e)
        try:
            md["simple_collision_count"] = str(sub.get_simple_collision_count(sm))
        except Exception as e:
            md["simple_collision_count_error"] = str(e)
        try:
            md["convex_collision_count"] = str(sub.get_convex_collision_count(sm))
        except Exception as e:
            md["convex_collision_count_error"] = str(e)
        try:
            md["num_triangles"] = str(sm.get_num_triangles(0))
        except Exception as e:
            md["num_triangles_error"] = str(e)
        try:
            md["num_vertices"] = str(sm.get_num_vertices(0))
        except Exception as e:
            md["num_vertices_error"] = str(e)
        try:
            md["num_lods"] = str(sm.get_num_lods())
        except Exception as e:
            md["num_lods_error"] = str(e)
        try:
            md["lod_for_collision"] = str(sm.lod_for_collision)
        except Exception as e:
            md["lod_for_collision_error"] = str(e)
        report["meshes"][str(path)] = md
    out = R / "Documentation" / "HeavyNavMeshInspect.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("HEAVY_NAV_MESH_INSPECT_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "HeavyNavMeshInspect.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("HEAVY_NAV_MESH_INSPECT_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass