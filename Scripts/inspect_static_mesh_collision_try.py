import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    sm = u.EditorAssetLibrary.load_asset("/Game/Conservatory/Botanical/TreeMaster/SM_TreeMaster_Structure")
    report["try_props"] = {}
    for prop in ["collision_complexity", "collision_trace_flag", "collision_settings", "body_setup", "body_instance", "nav_collision", "collision_complexity_enum", "collision_trace_enum", "collision_complexity_value"]:
        try:
            report["try_props"][prop] = str(sm.get_editor_property(prop))
        except Exception as e:
            report["try_props"][prop] = "ERROR: " + str(e)
    out = R / "Documentation" / "StaticMeshCollisionTryProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_COLLISION_TRY_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "StaticMeshCollisionTryProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_COLLISION_TRY_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass