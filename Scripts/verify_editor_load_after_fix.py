import unreal as u, json, datetime, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
MAP = "/Game/Conservatory/Maps/L_Exterior_RobotVR"
report = {"engine": u.SystemLibrary.get_engine_version(), "timestamp": datetime.datetime.now().isoformat()}

def finish_and_quit(result=None, error=None):
    if error is not None:
        report["error"] = error
    out = R / "Documentation" / "RobotStreamingFix-EditorLoad.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("EDITOR_LOAD_" + ("DONE" if error is None else "FAILED"), json.dumps(result or {"error": str(error)[:200]}))
    try:
        u.SystemLibrary.quit_editor()
    except Exception:
        pass

try:
    w = u.EditorLoadingAndSavingUtils.load_map(MAP)
    sub = u.get_editor_subsystem(u.EditorActorSubsystem)
    actors = list(sub.get_all_level_actors())
    report["actor_count"] = len(actors)
    assert len(actors) == 1867, f"expected 1867 actors, found {len(actors)}"

    def has_range(x):
        try:
            return any(c.get_class().get_name() == "SphereComponent" and "InteractionRange" in c.get_name() for c in x.get_components_by_class(u.PrimitiveComponent))
        except Exception:
            return False

    stations = [x for x in actors if x.get_class().get_name() == "VRSuitStation"]
    hubs = [x for x in actors if x.get_class().get_name() == "RobotVRHub"]
    cabinets = [x for x in actors if x.get_class().get_name() == "ControlRoomDrawerCabinet"]
    report["stations_with_range"] = sum(1 for x in stations if has_range(x))
    report["hubs_with_range"] = sum(1 for x in hubs if has_range(x))
    report["cabinets_with_range"] = sum(1 for x in cabinets if has_range(x))
    report["station_count"] = len(stations)
    report["hub_count"] = len(hubs)
    report["cabinet_count"] = len(cabinets)
    assert report["stations_with_range"] == 11, f"stations with range: {report['stations_with_range']}"
    assert report["hubs_with_range"] == 1, f"hubs with range: {report['hubs_with_range']}"
    assert report["cabinets_with_range"] == len(cabinets), "cabinet range missing"
    finish_and_quit({"actors": len(actors), "stations_with_range": report["stations_with_range"], "hubs": report["hubs_with_range"], "cabinets": report["cabinets_with_range"]})
except Exception:
    finish_and_quit(error=traceback.format_exc())