import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    sm = u.EditorAssetLibrary.load_asset("/Game/Conservatory/Botanical/TreeMaster/SM_TreeMaster_Structure")
    body = sm.get_editor_property("body_setup")
    report["body_setup_dir"] = [str(x) for x in dir(body) if not x.startswith("_")]
    for prop in ["collision_trace_flag", "collision_reponse", "collision_profile_name", "collision_enabled", "collision_object_type", "simple_collision", "complex_collision", "use_simple_as_complex", "use_complex_as_simple", "use_simple_and_complex", "use_default"]:
        try:
            report["body_setup_" + prop] = str(body.get_editor_property(prop))
        except Exception as e:
            report["body_setup_" + prop] = "ERROR: " + str(e)
    out = R / "Documentation" / "StaticMeshBodySetupProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_BODY_SETUP_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "StaticMeshBodySetupProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("STATIC_MESH_BODY_SETUP_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass