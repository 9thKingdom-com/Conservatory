import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["create_method_probe"] = {
        "NavModifierComponent.new_object": str(getattr(u.NavModifierComponent, "new_object", None)),
        "NavModifierComponent_call": str(getattr(u.NavModifierComponent, "__call__", None)),
        "NavModifierComponent_cast": str(getattr(u.NavModifierComponent, "cast", None)),
        "NavModifierComponent_static_class": str(getattr(u.NavModifierComponent, "static_class", None)),
        "NavModifierVolume_new_object": str(getattr(u.NavModifierVolume, "new_object", None)),
        "NavModifierVolume_static_class": str(getattr(u.NavModifierVolume, "static_class", None)),
    }
    out = R / "Documentation" / "NavModifierCreationProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_CREATION_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavModifierCreationProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_CREATION_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass