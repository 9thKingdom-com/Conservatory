import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["NavigationSystemV1_dir_rebuild"] = [str(x) for x in dir(u.NavigationSystemV1) if "rebuild" in str(x).lower() or "build" in str(x).lower()]
    report["RecastNavMesh_dir_rebuild"] = [str(x) for x in dir(u.RecastNavMesh) if "rebuild" in str(x).lower() or "build" in str(x).lower()]
    report["EditorLevelUtils_dir_rebuild"] = [str(x) for x in dir(u.EditorLevelUtils) if "rebuild" in str(x).lower() or "build" in str(x).lower()]
    out = R / "Documentation" / "RebuildProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("REBUILD_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "RebuildProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("REBUILD_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass