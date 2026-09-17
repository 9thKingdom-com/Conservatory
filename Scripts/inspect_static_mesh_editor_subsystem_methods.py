import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    s = u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
    report["dir"] = [str(x) for x in dir(s) if not x.startswith("_")]
    report["methods"] = {}
    for name in ["get_collision_complexity", "get_simple_collision_count", "get_convex_collision_count", "add_simple_collisions", "bulk_set_convex_decomposition_collisions", "set_convex_decomposition_collisions", "remove_collisions"]:
        try:
            fn = getattr(s, name)
            report["methods"][name] = str(fn.__doc__)
        except Exception as e:
            report["methods"][name] = "ERROR: " + str(e)
    out = R / "Documentation" / "StaticMeshEditorSubsystemMethodProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_EDITOR_SUBSYSTEM_METHOD_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "StaticMeshEditorSubsystemMethodProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_EDITOR_SUBSYSTEM_METHOD_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass