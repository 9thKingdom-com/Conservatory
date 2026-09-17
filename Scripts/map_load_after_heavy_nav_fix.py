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
    targets = [a for a in actors if a.get_name() in ("StaticMeshActor_5", "StaticMeshActor_1858")]
    report["found_targets"] = [a.get_name() for a in targets]
    out = R / "Documentation" / "HeavyNavMeshMapLoadAfterFix.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("HEAVY_NAV_MESH_MAP_LOAD_AFTER_FIX_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "HeavyNavMeshMapLoadAfterFix.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("HEAVY_NAV_MESH_MAP_LOAD_AFTER_FIX_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass