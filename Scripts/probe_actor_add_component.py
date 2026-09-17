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
    report["actor_methods_with_add"] = [str(x) for x in dir(lift) if "add" in str(x).lower() and "component" in str(x).lower()]
    report["actor_methods_with_component"] = [str(x) for x in dir(lift) if "component" in str(x).lower()]
    out = R / "Documentation" / "ActorAddComponentProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("ACTOR_ADD_COMPONENT_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "ActorAddComponentProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("ACTOR_ADD_COMPONENT_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass