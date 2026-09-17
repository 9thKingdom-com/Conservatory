import unreal as u, json, datetime, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
MAP = "/Game/Conservatory/Maps/L_Exterior_RobotVR"

report = {"engine": u.SystemLibrary.get_engine_version(), "timestamp": datetime.datetime.now().isoformat(),
          "map": MAP, "purpose": "Make gameplay-critical actors always loaded (Is Spatially Loaded = false) so World Partition streaming can never remove them"}

def finish_and_quit(result=None, error=None):
    if error is not None:
        report["error"] = error
    out = R / "Documentation" / "RobotAlwaysLoadedFix.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("ROBOT_ALWAYS_LOADED_" + ("DONE" if error is None else "FAILED"), json.dumps(result or {"error": str(error)[:200]}))
    try:
        u.SystemLibrary.quit_editor()
    except Exception:
        pass

def tr(x):
    p = x.get_actor_location(); r = x.get_actor_rotation(); s = x.get_actor_scale3d()
    return [p.x, p.y, p.z, r.pitch, r.yaw, r.roll, s.x, s.y, s.z]

try:
    w = u.EditorLoadingAndSavingUtils.load_map(MAP)
    sub = u.get_editor_subsystem(u.EditorActorSubsystem)
    actors = list(sub.get_all_level_actors())
    report["actor_count_before"] = len(actors)

    def class_of(x):
        return x.get_class().get_name()

    robots = [x for x in actors if class_of(x) == "C17Robot"]
    stations = [x for x in actors if class_of(x) == "VRSuitStation"]
    hubs = [x for x in actors if class_of(x) == "RobotVRHub"]
    navs = [x for x in actors if class_of(x) in ("RecastNavMesh", "NavMeshBoundsVolume")]
    assert len(robots) == 11, f"expected 11 robots, found {len(robots)}"
    assert len(stations) == 11, f"expected 11 stations, found {len(stations)}"
    assert len(hubs) == 1, f"expected 1 hub, found {len(hubs)}"

    report["robots"] = [{"name": x.get_name(), "robot_id": x.get_editor_property("robot_id")} for x in sorted(robots, key=lambda r: r.get_editor_property("robot_id"))]
    report["station_hub_refs"] = [{"name": x.get_name(), "robot_id": x.get_editor_property("robot_id"),
                                   "hub": str(x.get_editor_property("hub")) if x.get_editor_property("hub") else None}
                                  for x in sorted(stations, key=lambda s: s.get_editor_property("robot_id"))]

    targets = robots + stations + hubs + navs
    target_names = {x.get_name() for x in targets}
    report["targets"] = [{"name": x.get_name(), "class": class_of(x)} for x in targets]
    report["nav_actors"] = [{"name": x.get_name(), "class": class_of(x)} for x in navs]

    # discover the spatial-loading property name once
    prop_name = None
    for candidate in ("is_spatially_loaded", "bIsSpatiallyLoaded", "spatially_loaded"):
        try:
            actors[0].get_editor_property(candidate)
            prop_name = candidate
            break
        except Exception:
            continue
    assert prop_name, "no spatial loading property found on Actor"
    report["property_name"] = prop_name

    flags_before = {x.get_name(): x.get_editor_property(prop_name) for x in targets}
    report["spatial_before"] = flags_before

    keep = {x.get_name(): tr(x) for x in actors}

    for x in targets:
        x.set_editor_property(prop_name, False)

    for x in targets:
        assert x.get_editor_property(prop_name) is False, f"flag did not take on {x.get_name()}"
    assert keep == {x.get_name(): tr(x) for x in sub.get_all_level_actors()}, "actor transforms changed while setting flags"

    assert u.EditorLoadingAndSavingUtils.save_map(w, MAP)
    u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

    w = u.EditorLoadingAndSavingUtils.load_map(MAP)
    alive = list(sub.get_all_level_actors())
    report["actor_count_after_reload"] = len(alive)
    assert keep == {x.get_name(): tr(x) for x in alive}, "actor transforms changed after reload"
    flags_after = {}
    for x in alive:
        if x.get_name() in target_names:
            flags_after[x.get_name()] = x.get_editor_property(prop_name)
    report["spatial_after_reload"] = flags_after
    assert all(v is False for v in flags_after.values()), "some targets are still spatially loaded after reload"
    # sanity: ordinary prop actors stay spatially loaded
    sample = [x for x in alive if class_of(x) == "StaticMeshActor"][:5]
    report["static_sample_still_spatial"] = {x.get_name(): x.get_editor_property(prop_name) for x in sample}
    assert all(v is True for v in report["static_sample_still_spatial"].values()), "static mesh actors unexpectedly non-spatial"

    report["transforms_preserved"] = True
    report["reload_verified"] = True
    finish_and_quit({"actors": len(alive), "targets_non_spatial": len(flags_after)})
except Exception:
    finish_and_quit(error=traceback.format_exc())