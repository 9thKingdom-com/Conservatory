import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["static_mesh_collision_names"] = [str(x) for x in dir(u.StaticMesh) if "collision" in x.lower() or "nav" in x.lower() or "body" in x.lower()]
    report["static_mesh_component_collision_names"] = [str(x) for x in dir(u.StaticMeshComponent) if "collision" in x.lower() or "nav" in x.lower() or "body" in x.lower()]
    out = R / "Documentation" / "StaticMeshCollisionPropertyProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_COLLISION_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "StaticMeshCollisionPropertyProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_COLLISION_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass