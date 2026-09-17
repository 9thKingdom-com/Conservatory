import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["CollisionTraceFlag"] = [str(x) for x in dir(u.CollisionTraceFlag) if not x.startswith("_")]
    report["CollisionTypeEnum"] = [str(x) for x in dir(u.CollisionTypeEnum) if not x.startswith("_")]
    out = R / "Documentation" / "CollisionEnumsProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("COLLISION_ENUMS_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "CollisionEnumsProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("COLLISION_ENUMS_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass