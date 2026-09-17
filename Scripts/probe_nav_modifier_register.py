import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    ok = u.EditorLoadingAndSavingUtils.load_map("/Game/Conservatory/Maps/L_Exterior_RobotVR")
    report["map_loaded"] = bool(ok)
    sub = u.get_editor_subsystem(u.EditorActorSubsystem)
    actors = list(sub.get_all_level_actors())
    lift = next((a for a in actors if a.get_name() == "StaticMeshActor_1858"), None)
    if lift is None:
        raise RuntimeError("lift actor not found")
    comp = u.NavModifierComponent(lift)
    report["comp_methods_register"] = [str(x) for x in dir(comp) if "register" in str(x).lower() or "owner" in str(x).lower() or "attach" in str(x).lower()]
    report["comp_methods_add"] = [str(x) for x in dir(comp) if "add" in str(x).lower()]
    report["comp_methods"] = [str(x) for x in dir(comp) if not x.startswith("_")]
    out = R / "Documentation" / "NavModifierComponentRegisterProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_REGISTER_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavModifierRegisterProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_REGISTER_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass