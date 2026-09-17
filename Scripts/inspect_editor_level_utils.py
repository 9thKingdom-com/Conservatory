import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["EditorLevelUtils_dir"] = [str(x) for x in dir(u.EditorLevelUtils) if not x.startswith("_")]
    report["EditorLevelLibrary_dir"] = [str(x) for x in dir(u.EditorLevelLibrary) if not x.startswith("_")]
    report["EditorActorSubsystem_dir"] = [str(x) for x in dir(u.EditorActorSubsystem) if not x.startswith("_")]
    out = R / "Documentation" / "EditorLevelUtilsProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("EDITOR_LEVEL_UTILS_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "EditorLevelUtilsProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("EDITOR_LEVEL_UTILS_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass