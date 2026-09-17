import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["static_mesh_component_dir"] = [str(x) for x in dir(u.StaticMeshComponent) if not x.startswith("_")]
    report["static_mesh_dir"] = [str(x) for x in dir(u.StaticMesh) if not x.startswith("_")]
    out = R / "Documentation" / "StaticMeshCollisionDirProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_DIR_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "StaticMeshCollisionDirProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_DIR_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass