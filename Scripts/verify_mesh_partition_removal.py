import unreal as u, json, datetime
from pathlib import Path

R = Path(u.Paths.project_dir())
MAP = "/Game/Conservatory/Maps/L_Exterior_RobotVR"

w = u.EditorLoadingAndSavingUtils.load_map(MAP)
sub = u.get_editor_subsystem(u.EditorActorSubsystem)
actors = list(sub.get_all_level_actors())
classes = {}
leftovers = []
for x in actors:
    cn = x.get_class().get_name()
    classes[cn] = classes.get(cn, 0) + 1
    if "meshpartition" in cn.lower() or "megamesh" in cn.lower():
        leftovers.append(x.get_name())

report = {
    "engine": u.SystemLibrary.get_engine_version(),
    "timestamp": datetime.datetime.now().isoformat(),
    "map": MAP,
    "actor_count": len(actors),
    "actor_classes": classes,
    "meshpartition_megamesh_remaining": leftovers,
}
assert len(actors) == 1846, f"expected 1846 actors, found {len(actors)}"
assert not leftovers, f"unexpected MeshPartition/MegaMesh actors: {leftovers}"

out = R / "Documentation" / "MeshPartitionRemoval-Verification.json"
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
print("MESHPARTITION_VERIFICATION_DONE", json.dumps({"actors": len(actors), "leftovers": len(leftovers)}))

try:
    u.SystemLibrary.quit_editor()
except Exception:
    pass