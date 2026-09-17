import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["NavModifierComponent_dir"] = [str(x) for x in dir(u.NavModifierComponent) if not x.startswith("_")]
    report["NavArea_Obstacle_dir"] = [str(x) for x in dir(u.NavArea_Obstacle) if not x.startswith("_")]
    out = R / "Documentation" / "NavModifierComponentProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_COMPONENT_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavModifierComponentProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_COMPONENT_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass