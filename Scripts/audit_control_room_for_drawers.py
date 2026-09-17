import json
from pathlib import Path
import unreal as u

root = Path(u.Paths.project_dir())
actor_sub = u.get_editor_subsystem(u.EditorActorSubsystem)
level_sub = u.get_editor_subsystem(u.LevelEditorSubsystem)
actors = actor_sub.get_all_level_actors()

suits = [a for a in actors if a.get_class().get_name() == "VRSuitStation"]
assert len(suits) == 11, f"Expected 11 Control Room suits, found {len(suits)}"
cx = sum(a.get_actor_location().x for a in suits) / len(suits)
cy = sum(a.get_actor_location().y for a in suits) / len(suits)
cz = sum(a.get_actor_location().z for a in suits) / len(suits)

rows = []
for actor in actors:
    p = actor.get_actor_location()
    if abs(p.x - cx) > 2300 or abs(p.y - cy) > 2300 or abs(p.z - cz) > 1800:
        continue
    c, e = actor.get_actor_bounds(False)
    row = {
        "name": actor.get_name(),
        "label": actor.get_actor_label(),
        "class": actor.get_class().get_name(),
        "folder": str(actor.get_folder_path()),
        "location": [round(p.x, 2), round(p.y, 2), round(p.z, 2)],
        "rotation": [round(actor.get_actor_rotation().pitch, 2), round(actor.get_actor_rotation().yaw, 2), round(actor.get_actor_rotation().roll, 2)],
        "bounds_center": [round(c.x, 2), round(c.y, 2), round(c.z, 2)],
        "bounds_extent": [round(e.x, 2), round(e.y, 2), round(e.z, 2)],
    }
    if isinstance(actor, u.StaticMeshActor):
        mesh = actor.static_mesh_component.static_mesh
        row["mesh"] = mesh.get_path_name() if mesh else None
    rows.append(row)

try:
    dirty_content = [str(x) for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
    dirty_maps = [str(x) for x in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()]
except Exception:
    dirty_content = []
    dirty_maps = []

report = {
    "engine": u.SystemLibrary.get_engine_version(),
    "world": u.EditorLevelLibrary.get_editor_world().get_path_name(),
    "actor_count": len(actors),
    "control_room_center": [cx, cy, cz],
    "dirty_content": dirty_content,
    "dirty_maps": dirty_maps,
    "nearby_actors": sorted(rows, key=lambda r: (r["class"], r["label"])),
}
(root / "Documentation" / "ControlRoomDrawersPlacementAudit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

# View from the room's entry side toward the suit wall; viewport-only, not a map mutation.
level_sub.set_level_viewport_camera_info(
    u.Vector(cx, cy - 1450.0, cz + 235.0),
    u.Rotator(pitch=-4.0, yaw=90.0, roll=0.0),
    "",
)
print("CONTROL_ROOM_DRAWERS_AUDIT_COMPLETE", len(rows), report["world"], dirty_maps, dirty_content)
