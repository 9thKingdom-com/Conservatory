import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["collision_related_names"] = [str(x) for x in dir(u) if "Collision" in x or "collision" in x]
    out = R / "Documentation" / "CollisionApiProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("COLLISION_API_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "CollisionApiProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("COLLISION_API_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass