import unreal as u, json, datetime, traceback, inspect
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    s = u.get_editor_subsystem(u.StaticMeshEditorSubsystem)
    for name in ["get_collision_complexity", "add_simple_collisions", "bulk_set_convex_decomposition_collisions", "set_convex_decomposition_collisions", "remove_collisions", "get_simple_collision_count", "get_convex_collision_count"]:
        try:
            fn = getattr(s, name)
            report[name] = {
                "doc": str(fn.__doc__),
                "signature": str(inspect.signature(fn))
            }
        except Exception as e:
            report[name] = {"error": str(e)}
    out = R / "Documentation" / "StaticMeshEditorSubsystemSignatureProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("SIGNATURE_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "StaticMeshEditorSubsystemSignatureProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_EDITOR_SUBSYSTEM_SIGNATURE_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass