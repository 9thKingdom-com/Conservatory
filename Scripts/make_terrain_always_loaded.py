import unreal as u, json, datetime, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
MAP = "/Game/Conservatory/Maps/L_Exterior_RobotVR"

report = {"engine": u.SystemLibrary.get_engine_version(), "timestamp": datetime.datetime.now().isoformat(),
          "map": MAP, "purpose": "Make the terrain always loaded so always-loaded wandering robots always have ground under them"}

def finish_and_quit(result=None, error=None):
    if error is not None:
        report["error"] = error
    out = R / "Documentation" / "TerrainAlwaysLoadedFix.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("TERRAIN_ALWAYS_LOADED_" + ("DONE" if error is None else "FAILED"), json.dumps(result or {"error": str(error)[:200]}))
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
    report["actor_count"] = len(actors)

    targets = [x for x in actors if x.get_class().get_name() in ("Landscape", "LandscapeStreamingProxy")]
    assert 4 <= len(targets) <= 6, f"unexpected terrain actor count {len(targets)}"
    report["terrain_actors"] = [{"name": x.get_name(), "class": x.get_class().get_name()} for x in targets]

    prop_name = "is_spatially_loaded"
    report["spatial_before"] = {x.get_name(): x.get_editor_property(prop_name) for x in targets}

    keep = {x.get_name(): tr(x) for x in actors}
    target_names = {x.get_name() for x in targets}

    for x in targets:
        x.set_editor_property(prop_name, False)
    for x in targets:
        assert x.get_editor_property(prop_name) is False, f"flag did not take on {x.get_name()}"
    assert keep == {x.get_name(): tr(x) for x in sub.get_all_level_actors()}, "actor transforms changed while setting terrain flags"

    assert u.EditorLoadingAndSavingUtils.save_map(w, MAP)
    u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

    w = u.EditorLoadingAndSavingUtils.load_map(MAP)
    alive = list(sub.get_all_level_actors())
    report["actor_count_after_reload"] = len(alive)
    assert keep == {x.get_name(): tr(x) for x in alive}, "actor transforms changed after reload"
    flags_after = {x.get_name(): x.get_editor_property(prop_name) for x in alive if x.get_name() in target_names}
    report["spatial_after_reload"] = flags_after
    assert all(v is False for v in flags_after.values()), "terrain actors still spatially loaded after reload"
    report["transforms_preserved"] = True
    report["reload_verified"] = True
    finish_and_quit({"terrain_actors_non_spatial": len(flags_after), "actors": len(alive)})
except Exception:
    finish_and_quit(error=traceback.format_exc())