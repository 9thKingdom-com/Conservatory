import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat(), "methods": {}}
try:
    ns = u.NavigationSystemV1.get_navigation_system(u.get_editor_world()) if hasattr(u.NavigationSystemV1, "get_navigation_system") else None
    if ns:
        report["methods"]["rebuild_all"] = str(getattr(ns, "rebuild_all", None))
        report["methods"]["rebuild"] = str(getattr(ns, "rebuild", None))
        report["methods"]["build"] = str(getattr(ns, "build", None))
        report["methods"]["rebuild_navmesh"] = str(getattr(ns, "rebuild_navmesh", None))
    else:
        report["error"] = "navigation system not found"
    out = R / "Documentation" / "NavigationSystemMethodProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_SYSTEM_METHOD_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavigationSystemMethodProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_SYSTEM_METHOD_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass