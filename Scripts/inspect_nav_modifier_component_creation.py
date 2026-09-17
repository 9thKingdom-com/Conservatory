import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["NavModifierComponent_creation_methods"] = {
        "new_object": str(getattr(u.NavModifierComponent, "new_object", None)),
        "call": str(getattr(u.NavModifierComponent, "__call__", None)),
        "static_class": str(getattr(u.NavModifierComponent, "static_class", None)),
        "spawn_actor_from_class": str(getattr(u.EditorActorSubsystem, "spawn_actor_from_class", None)),
    }
    out = R / "Documentation" / "NavModifierComponentCreationProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_COMPONENT_CREATION_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavModifierComponentCreationProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_COMPONENT_CREATION_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass