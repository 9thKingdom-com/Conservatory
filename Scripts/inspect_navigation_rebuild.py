import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["NavigationSystemV1_dir"] = [str(x) for x in dir(u.NavigationSystemV1) if not x.startswith("_")]
    report["RecastNavMesh_dir"] = [str(x) for x in dir(u.RecastNavMesh) if not x.startswith("_")]
    out = R / "Documentation" / "NavigationRebuildProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAVIGATION_REBUILD_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavigationRebuildProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAVIGATION_REBUILD_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass