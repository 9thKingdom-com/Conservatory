import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    ok = u.EditorLoadingAndSavingUtils.load_map("/Game/Conservatory/Maps/L_Exterior_RobotVR")
    sub = u.get_editor_subsystem(u.EditorActorSubsystem)
    actors = list(sub.get_all_level_actors())
    lift = next((a for a in actors if a.get_name() == "StaticMeshActor_1858"), None)
    if lift is None:
        raise RuntimeError("lift actor not found")
    comp = u.NavModifierComponent(lift)
    report["component_created"] = bool(comp)
    if comp:
        report["component_class"] = str(comp.get_class().get_name())
        report["component_owner"] = str(comp.get_owner())
        comp.set_area_class(u.NavArea_Obstacle.static_class())
        comp.set_navigation_relevancy(True)
        report["area_class"] = str(comp.get_editor_property("area_class"))
        report["navigation_relevancy"] = str(comp.get_editor_property("navigation_relevancy"))
        lift.add_instance_component(comp)
        report["component_added"] = True
    out = R / "Documentation" / "NavModifierComponentAttachProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_COMPONENT_ATTACH_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavModifierComponentAttachProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_COMPONENT_ATTACH_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass