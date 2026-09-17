import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    for name in ["NavCollisionBase", "NavCollision", "NavigationSystem"]:
        if hasattr(u, name):
            cls = getattr(u, name)
            report[name] = {"dir": [str(x) for x in dir(cls) if not x.startswith("_")]}
            try:
                report[name]["static_class"] = str(cls.static_class().get_path_name())
            except Exception as e:
                report[name]["static_class_error"] = str(e)
            try:
                report[name]["editor_property_names"] = [str(x) for x in cls.get_editor_property_names()]
            except Exception as e:
                report[name]["editor_property_names_error"] = str(e)
    out = R / "Documentation" / "NavCollisionApiProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_COLLISION_API_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavCollisionApiProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_COLLISION_API_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass