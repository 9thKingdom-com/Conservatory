import unreal as u, json, datetime
from pathlib import Path

R = Path(u.Paths.project_dir())
MAP = "/Game/Conservatory/Maps/L_Exterior_RobotVR"
EXT = R / "Content" / "__ExternalActors__"

report = {"engine": u.SystemLibrary.get_engine_version(), "timestamp": datetime.datetime.now().isoformat(),
          "map": MAP, "backup": "Saved/Backups/MeshPartitionRemoval/20260916-110827"}

w = u.EditorLoadingAndSavingUtils.load_map(MAP)
sub = u.get_editor_subsystem(u.EditorActorSubsystem)
actors = list(sub.get_all_level_actors())
report["actor_count_before"] = len(actors)
assert len(actors) == 1845, f"expected 1845 actors, found {len(actors)}"

def tr(x):
    p = x.get_actor_location(); r = x.get_actor_rotation(); s = x.get_actor_scale3d()
    return [p.x, p.y, p.z, r.pitch, r.yaw, r.roll, s.x, s.y, s.z]

def comps(x):
    try:
        return [c.get_class().get_name() for c in x.get_components_by_class(u.ActorComponent)]
    except Exception:
        return []

def info(x, component_list=None):
    p = x.get_actor_location()
    return {"name": x.get_name(), "label": x.get_actor_label(), "class": x.get_class().get_name(),
            "location": [p.x, p.y, p.z], "folder": str(x.get_folder_path()),
            "components": component_list if component_list is not None else comps(x),
            "path": x.get_path_name()}

# --- identify targets ---
partition_actors = [x for x in actors if x.get_class().get_name() == "MeshPartition"]
report["mesh_partition_actors"] = [info(x) for x in partition_actors]

provider_actors = []
for x in actors:
    cl = comps(x)
    if any("MegaMesh" in c for c in cl):
        provider_actors.append((x, cl))
report["megamesh_component_actors"] = [info(x, cl) for x, cl in provider_actors]

# Safety: only generic empty 'Actor' holders may be removed for MegaMesh components.
protected = [x for x, cl in provider_actors if x.get_class().get_name() != "Actor"]
assert not protected, "MegaMesh components found on non-generic actors; refusing to change: " + json.dumps([info(x) for x in protected])

delete_targets = list(partition_actors) + [x for x, cl in provider_actors]
keep = {x.get_name(): tr(x) for x in actors if x not in delete_targets}
report["delete_targets"] = [info(x) for x in delete_targets]
assert 1 <= len(delete_targets) <= 8, f"unexpected delete target count {len(delete_targets)}"

ext_before = len(list(EXT.rglob("*.uasset")) + list(EXT.rglob("*.umap")))
report["external_files_before"] = ext_before

# --- destroy ---
for x in reversed(delete_targets):
    assert sub.destroy_actor(x)

alive = sub.get_all_level_actors()
assert keep == {x.get_name(): tr(x) for x in alive}, "retained actor transforms changed during deletion"
report["actor_count_after_destroy"] = len(alive)

# --- save ---
assert u.EditorLoadingAndSavingUtils.save_map(w, MAP)
u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
report["saved"] = True

# External actor packages should be gone from disk after save; clean any orphan explicitly.
removed_paths = []
for t in report["delete_targets"]:
    pkg_path = t["path"]
    actor_pkg = pkg_path[: pkg_path.find(".")] if False else None
# external package path comes from the world path; derive from get_path_name is unreliable, use registry instead
reg = u.AssetRegistryHelpers.get_asset_registry()
leftovers = []
for a in reg.get_all_assets():
    try:
        pkg = str(a.package_name); obj = str(a.asset_name)
    except Exception:
        continue
    if pkg.startswith("/Game/__ExternalActors__") and ("MeshPartition" in obj or "MegaMesh" in obj):
        leftovers.append(pkg)
report["registry_leftover_packages"] = leftovers
for pkg in leftovers:
    try:
        u.EditorAssetLibrary.delete_asset(pkg)
        removed_paths.append(pkg)
    except Exception as e:
        report.setdefault("delete_asset_errors", []).append({"package": pkg, "error": repr(e)})
if removed_paths:
    assert u.EditorLoadingAndSavingUtils.save_map(w, MAP)
    u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
report["explicitly_deleted_packages"] = removed_paths

# --- reload and re-verify ---
w = u.EditorLoadingAndSavingUtils.load_map(MAP)
alive = sub.get_all_level_actors()
report["actor_count_after_reload"] = len(alive)
assert keep == {x.get_name(): tr(x) for x in alive}, "retained actor transforms changed after reload"
assert not [x for x in alive if x.get_class().get_name() == "MeshPartition"], "MeshPartition actor still present"
assert not [x for x in alive if any("MegaMesh" in c for c in comps(x))], "MegaMesh component actor still present"

ext_after = len(list(EXT.rglob("*.uasset")) + list(EXT.rglob("*.umap")))
report["external_files_after"] = ext_after
report["external_files_removed"] = ext_before - ext_after
report["transforms_preserved"] = True
report["reload_verified"] = True

out = R / "Documentation" / "MeshPartitionRemoval.json"
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
print("MESHPARTITION_REMOVAL_DONE", json.dumps({"before": report["actor_count_before"],
      "after": report["actor_count_after_reload"], "deleted": len(delete_targets),
      "external_removed": report["external_files_removed"]}))

try:
    u.SystemLibrary.quit_editor()
except Exception:
    pass