import unreal as u, json, datetime, traceback
from pathlib import Path
R = Path(u.Paths.project_dir())
report = {"timestamp": datetime.datetime.now().isoformat()}
try:
    report["NavModifierVolume_dir"] = [str(x) for x in dir(u.NavModifierVolume) if not x.startswith("_")]
    out = R / "Documentation" / "NavModifierVolumeProbe.json"
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_VOLUME_PROBE_DONE")
except Exception:
    report["error"] = traceback.format_exc()
    (R / "Documentation" / "NavModifierVolumeProbe.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("NAV_MODIFIER_VOLUME_PROBE_FAILED")
finally:
    try: u.SystemLibrary.quit_editor()
    except Exception: pass