import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    ok = u.EditorLoadingAndSavingUtils.load_map("/Game/Conservatory/Maps/L_Exterior_RobotVR")
    report["map_loaded"] = bool(ok)
    sub = u.get_editor_subsystem(u.EditorActorSubsystem)
    actors = list(sub.get_all_level_actors())
    report["loaded_actor_count"] = len(actors)
    lift = next((a for a in actors if a.get_name() == "StaticMeshActor_1858"), None)
    if lift is None:
        raise RuntimeError("lift actor not found")
    report["lift_label"] = str(lift.get_actor_label())
    comps = lift.get_components_by_class(u.StaticMeshComponent)
    report["before_components"] = []
    for c in comps:
        entry = {"name": str(c.get_name()), "can_ever_affect_navigation": str(c.get_editor_property("can_ever_affect_navigation"))}
        c.set_editor_property("can_ever_affect_navigation", False)
        entry["after_can_ever_affect_navigation"] = str(c.get_editor_property("can_ever_affect_navigation"))
        report["before_components"].append(entry)
    comp = u.NavModifierComponent(lift)
    report["component_created"] = bool(comp)
    if comp:
        comp.set_area_class(u.NavArea_Obstacle.static_class())
        comp.set_navigation_relevancy(True)
        lift.add_instance_component(comp)
        report["area_class"] = str(comp.get_editor_property("area_class"))
        report["navigation_relevancy"] = str(comp.get_editor_property("navigation_relevancy"))
        report["component_owner"] = str(comp.get_owner())
        report["component_class"] = str(comp.get_class().get_name())
        report["component_path"] = str(comp.get_path_name())
    out = R / "Documentation" / "HeavyNavMeshLiftNavModifier.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("LIFT_NAV_MODIFIER_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "HeavyNavMeshLiftNavModifier.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("LIFT_NAV_MODIFIER_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass