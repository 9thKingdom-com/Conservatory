import unreal as u, json, datetime, os, shutil, traceback
from pathlib import Path

R = Path(u.Paths.project_dir())
MAP = "/Game/Conservatory/Maps/L_Exterior_RobotVR"
EXT = R / "Content" / "__ExternalActors__"
UMAP = R / "Content" / "Conservatory" / "Maps" / "L_Exterior_RobotVR.umap"
PREFIX = "UAID_60CF84A9A659E20103_"
KNOWN_PROVIDER_PACKAGES = [
    "3/YZ/OG8YS4ZLYM2PDKKWIXEVSF",
    "2/GB/RAF50C2EVFUVHDJ5CJY15B",
    "4/ZZ/N2EQUKJNXUTNSUC8JO5XIX",
    "C/4J/12AWEIT2V9TTY1A5P4807M",
]

report = {"engine": u.SystemLibrary.get_engine_version(), "timestamp": datetime.datetime.now().isoformat(),
          "map": MAP, "purpose": "Remove the four orphaned MeshPartition provider actors so the plugin can be disabled safely"}

def finish_and_quit(result=None, error=None):
    if error is not None:
        report["error"] = error
    out = R / "Documentation" / "MeshPartitionProviderRemoval.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("MESHPARTITION_PROVIDER_REMOVAL_" + ("DONE" if error is None else "FAILED"), json.dumps(result or {"error": str(error)[:200]}))
    try:
        u.SystemLibrary.quit_editor()
    except Exception:
        pass

try:
    # Lock safety: the launch wrapper verifies no other UnrealEditor instances before starting.
    w = u.EditorLoadingAndSavingUtils.load_map(MAP)
    sub = u.get_editor_subsystem(u.EditorActorSubsystem)
    actors = list(sub.get_all_level_actors())
    report["actor_count_before"] = len(actors)
    assert len(actors) >= 1840, f"actor count unexpectedly low: {len(actors)}"

    def tr(x):
        p = x.get_actor_location(); r = x.get_actor_rotation(); s = x.get_actor_scale3d()
        return [p.x, p.y, p.z, r.pitch, r.yaw, r.roll, s.x, s.y, s.z]

    def comps(x):
        try:
            return [c.get_class().get_name() for c in x.get_components_by_class(u.ActorComponent)]
        except Exception:
            return []

    def info(x):
        p = x.get_actor_location()
        return {"name": x.get_name(), "label": x.get_actor_label(), "class": x.get_class().get_name(),
                "location": [p.x, p.y, p.z], "folder": str(x.get_folder_path()),
                "components": comps(x), "path": x.get_path_name()}

    generic = [x for x in actors if x.get_class().get_name() == "Actor"]
    report["all_generic_actor_details"] = [info(x) for x in generic]
    targets = [x for x in generic if PREFIX in x.get_name()]
    report["delete_targets"] = [info(x) for x in targets]
    assert 1 <= len(targets) <= 8, f"unexpected provider target count {len(targets)}"
    for x in targets:
        assert x.get_class().get_name() == "Actor" and PREFIX in x.get_name()

    keep = {x.get_name(): tr(x) for x in actors if x not in targets}
    ext_before = len(list(EXT.rglob("*.uasset")) + list(EXT.rglob("*.umap")))
    report["external_files_before"] = ext_before

    for x in reversed(targets):
        assert sub.destroy_actor(x)
    alive = sub.get_all_level_actors()
    assert keep == {x.get_name(): tr(x) for x in alive}, "retained actor transforms changed during provider deletion"
    report["actor_count_after_destroy"] = len(alive)

    assert u.EditorLoadingAndSavingUtils.save_map(w, MAP)
    u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

    # Clean up external actor packages: by deleted actor names, plus the four known orphan paths.
    reg = u.AssetRegistryHelpers.get_asset_registry()
    deleted_names = {x["name"] for x in report["delete_targets"]}
    leftovers = set()
    for a in reg.get_all_assets():
        try:
            pkg = str(a.package_name); obj_name = str(a.asset_name)
        except Exception:
            continue
        if pkg.startswith("/Game/__ExternalActors__") and obj_name in deleted_names:
            leftovers.add(pkg)
    for rel in KNOWN_PROVIDER_PACKAGES:
        if (EXT / (rel + ".uasset")).exists():
            leftovers.add("/Game/__ExternalActors__/Conservatory/Maps/L_Exterior_RobotVR/" + rel)
    report["registry_leftover_packages"] = sorted(leftovers)
    removed = []
    for pkg in sorted(leftovers):
        try:
            u.EditorAssetLibrary.delete_asset(pkg)
            removed.append(pkg)
        except Exception as e:
            report.setdefault("delete_asset_errors", []).append({"package": pkg, "error": repr(e)})
    if removed:
        assert u.EditorLoadingAndSavingUtils.save_map(w, MAP)
        u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    report["explicitly_deleted_packages"] = removed
    report["known_provider_packages_remaining"] = [rel for rel in KNOWN_PROVIDER_PACKAGES if (EXT / (rel + ".uasset")).exists()]

    w = u.EditorLoadingAndSavingUtils.load_map(MAP)
    alive = sub.get_all_level_actors()
    report["actor_count_after_reload"] = len(alive)
    assert keep == {x.get_name(): tr(x) for x in alive}, "retained actor transforms changed after reload"
    assert not [x for x in alive if x.get_class().get_name() == "MeshPartition"], "MeshPartition actor still present"
    assert not [x for x in alive if x.get_class().get_name() == "Actor" and PREFIX in x.get_name()], "provider actor still present"

    ext_after = len(list(EXT.rglob("*.uasset")) + list(EXT.rglob("*.umap")))
    report["external_files_after"] = ext_after
    report["external_files_removed"] = ext_before - ext_after
    report["transforms_preserved"] = True
    report["reload_verified"] = True

    # Disable the MeshPartition plugin now that the map is clean.
    uproj = R / "Conservatory.uproject"
    text = uproj.read_text(encoding="utf-8")
    old = '"Name": "MeshPartition",' + chr(10) + chr(9) + chr(9) + chr(9) + '"Enabled": true'
    new = '"Name": "MeshPartition",' + chr(10) + chr(9) + chr(9) + chr(9) + '"Enabled": false'
    new_text = text.replace(old, new)
    assert new_text != text, "uproject MeshPartition entry not found"
    uproj.write_text(new_text, encoding="utf-8")
    report["meshpartition_plugin_disabled_in_uproject"] = True

    finish_and_quit({"before": report["actor_count_before"], "after": report["actor_count_after_reload"],
                     "deleted": len(targets), "external_removed": report["external_files_removed"],
                     "known_remaining": len(report["known_provider_packages_remaining"])})
except Exception:
    finish_and_quit(error=traceback.format_exc())