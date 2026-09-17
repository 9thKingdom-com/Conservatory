import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    paths = ["/Game/Conservatory/Botanical/TreeMaster/SM_TreeMaster_Structure", "/Game/Conservatory/Architecture/LiftMaster/SM_LiftMaster_Solid"]
    report["meshes"] = {}
    for path in paths:
        sm = u.EditorAssetLibrary.load_asset(path)
        nav = sm.get_editor_property("nav_collision")
        md = {}
        for prop in ["bUseSimpleCollisionAsComplex", "bUseComplexCollisionAsSimple", "bUseSimpleCollision", "bUseComplexCollision", "bUseSimpleCollisionAsComplexCollision", "bUseComplexCollisionAsSimpleCollision", "bIsDynamicObstacle", "bObstacle", "bNavModifier", "bUseGeometry"]:
            try:
                md[prop] = str(nav.get_editor_property(prop))
            except Exception as e:
                md[prop] = "ERROR: " + str(e)
        report["meshes"][str(path)] = md
    out = R / "Documentation" / "NavCollisionPropertyProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_COLLISION_PROPERTY_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavCollisionPropertyProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_COLLISION_PROPERTY_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass