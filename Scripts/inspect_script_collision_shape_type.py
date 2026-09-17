import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["ScriptCollisionShapeType"] = [str(x) for x in dir(u.ScriptCollisionShapeType) if not x.startswith("_")]
    report["ScriptingCollisionShapeType"] = [str(x) for x in dir(u.ScriptingCollisionShapeType) if not x.startswith("_")]
    report["ScriptingCollisionShapeType_Deprecated"] = [str(x) for x in dir(u.ScriptingCollisionShapeType_Deprecated) if not x.startswith("_")]
    out = R / "Documentation" / "ScriptCollisionShapeTypeProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("SHAPE_TYPE_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "ScriptCollisionShapeTypeProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("SHAPE_TYPE_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass