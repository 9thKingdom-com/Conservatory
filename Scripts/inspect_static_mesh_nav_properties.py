import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["NavCollisionBase_editor_property_names"] = [str(x) for x in u.NavCollisionBase.static_class().get_editor_property_names()]
    report["StaticMesh_editor_property_names"] = [str(x) for x in u.StaticMesh.static_class().get_editor_property_names()]
    out = R / "Documentation" / "StaticMeshNavPropertyProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("PROPERTY_NAMES_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "StaticMeshNavPropertyProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("PROPERTY_NAMES_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass