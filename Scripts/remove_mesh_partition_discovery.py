import unreal as u, json, datetime, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
report = {"engine": u.SystemLibrary.get_engine_version(), "timestamp": datetime.datetime.now().isoformat()}

# ---- 1. Enumerate every asset via the Asset Registry ----
ar = u.AssetRegistryHelpers.get_asset_registry()
assets = None
for candidate in ("get_all_assets",):
    if hasattr(ar, candidate):
        assets = getattr(ar, candidate)()
        report["registry_api"] = candidate
        break
if assets is None and hasattr(ar, "get_assets_by_path"):
    assets = ar.get_assets_by_path("/Game", True)
    report["registry_api"] = "get_assets_by_path"
if assets is None:
    raise RuntimeError("No asset registry enumeration API found")

def class_name(a):
    for attr in ("asset_class", "asset_class_path"):
        try:
            v = getattr(a, attr)
            if v is not None:
                return str(v)
        except Exception:
            pass
    return "UNKNOWN"

report["total_assets"] = len(assets)
sample = None
external_classes = {}
flagged = []
for a in assets:
    try:
        pkg = str(a.package_name)
        name = str(a.asset_name)
    except Exception:
        pkg = str(a.get_editor_property("package_name"))
        name = str(a.get_editor_property("asset_name"))
    if pkg.startswith("/Game/__ExternalActors__") and sample is None:
        sample = {"dir": [m for m in dir(a) if not m.startswith("_")],
                  "package_name": pkg, "asset_name": name, "class": class_name(a)}
    cn = class_name(a)
    if pkg.startswith("/Game/__ExternalActors__") or pkg.startswith("/Game/__ExternalObjects__"):
        external_classes[cn] = external_classes.get(cn, 0) + 1
    hay = (pkg + " " + name + " " + cn).lower()
    if "meshpartition" in hay or "megamesh" in hay:
        flagged.append({"package": pkg, "object": name, "class": cn})

report["external_actor_classes"] = external_classes
report["registry_meshpartition_megamesh_assets"] = flagged
report["asset_data_dir_sample"] = sample

# ---- 2. Load each flagged external package and read the actor directly ----
details = []
for f in flagged:
    d = dict(f)
    try:
        obj = u.EditorAssetLibrary.load_asset(f["package"])
        d["loaded_class"] = obj.get_class().get_name()
        d["loaded_path"] = obj.get_path_name()
        try:
            d["label"] = obj.get_actor_label()
        except Exception:
            d["label"] = None
        try:
            loc = obj.get_actor_location()
            d["location"] = [loc.x, loc.y, loc.z]
        except Exception:
            d["location"] = None
        try:
            d["components"] = sorted({c.get_class().get_name() for c in obj.get_components_by_class(u.ActorComponent)})
        except Exception:
            d["components"] = None
    except Exception as e:
        d["error"] = repr(e)
    details.append(d)
report["flagged_details"] = details

# ---- 3. What is loaded in the editor world right now? ----
try:
    actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
    report["loaded_actor_count"] = len(actors)
    loaded_classes = {}
    loaded_flags = []
    for x in actors:
        cn = x.get_class().get_name()
        loaded_classes[cn] = loaded_classes.get(cn, 0) + 1
        if "meshpartition" in cn.lower() or "megamesh" in cn.lower():
            p = x.get_actor_location()
            loaded_flags.append({"name": x.get_name(), "label": x.get_actor_label(), "class": cn,
                                 "location": [p.x, p.y, p.z], "path": x.get_path_name()})
    report["loaded_actor_classes"] = loaded_classes
    report["loaded_meshpartition_megamesh"] = loaded_flags
except Exception as e:
    report["loaded_actor_error"] = traceback.format_exc()

out = R / "Documentation" / "MeshPartitionRemoval-Discovery.json"
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
print("MESHPARTITION_DISCOVERY_DONE", json.dumps({"total": report["total_assets"], "flagged": len(flagged), "loaded": report.get("loaded_actor_count")}))

try:
    u.SystemLibrary.quit_editor()
except Exception:
    pass
