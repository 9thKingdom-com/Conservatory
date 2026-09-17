import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["NavCollisionBase_dir"] = [str(x) for x in dir(u.NavCollisionBase) if not x.startswith("_")]
    report["NavCollisionBase_class_dir"] = [str(x) for x in dir(u.NavCollisionBase.static_class()) if not x.startswith("_")]
    out = R / "Documentation" / "NavCollisionBaseProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_COLLISION_BASE_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavCollisionBaseProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_COLLISION_BASE_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass