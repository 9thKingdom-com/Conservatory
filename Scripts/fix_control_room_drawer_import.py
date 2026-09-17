import json
from pathlib import Path
import unreal as u

ROOT = Path(u.Paths.project_dir())
FBX = ROOT / "Asset-resources" / "Control-Room-Assets" / "Johns-Drawers" / "GameReady" / "SM_ControlRoom_Drawers_5x3.fbx"
BASE = "/Game/Conservatory/Interiors/ControlRoom/Drawers5x3"
MESH_PATH = BASE + "/SM_ControlRoom_Drawers_5x3"
LABEL = "CONTROL ROOM | Walnut drawers 5x3"

lib = u.EditorAssetLibrary
assets = u.AssetToolsHelpers.get_asset_tools()
actor_sub = u.get_editor_subsystem(u.EditorActorSubsystem)
level_sub = u.get_editor_subsystem(u.LevelEditorSubsystem)
mesh = lib.load_asset(MESH_PATH)
assert mesh and FBX.exists()
cabinet = next(a for a in actor_sub.get_all_level_actors() if a.get_actor_label() == LABEL)

u.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
task = u.AssetImportTask()
task.filename = str(FBX)
task.destination_path = BASE
task.destination_name = "SM_ControlRoom_Drawers_5x3"
task.automated = True
task.save = True
task.replace_existing = True
options = u.FbxImportUI()
options.import_mesh = True
options.import_materials = False
options.import_textures = False
options.import_as_skeletal = False
options.mesh_type_to_import = u.FBXImportType.FBXIT_STATIC_MESH
data = options.static_mesh_import_data
data.combine_meshes = True
data.auto_generate_collision = False
data.generate_lightmap_u_vs = True
data.normal_import_method = u.FBXNormalImportMethod.FBXNIM_COMPUTE_NORMALS
data.import_uniform_scale = 100.0
task.options = options
assets.import_asset_tasks([task])

mesh = lib.load_asset(MESH_PATH)
assert mesh
walnut = lib.load_asset(BASE + "/M_CR_Walnut_Dark")
trim = lib.load_asset(BASE + "/M_CR_Walnut_Trim")
brass = lib.load_asset(BASE + "/M_CR_Aged_Brass")
assert walnut and trim and brass

slots = list(mesh.get_editor_property("static_materials"))
slot_names = [str(slot.material_slot_name) for slot in slots]
if not any("CR_Aged_Brass" in name for name in slot_names):
    new_slot = u.StaticMaterial()
    new_slot.set_editor_property("material_interface", brass)
    new_slot.set_editor_property("material_slot_name", "CR_Aged_Brass")
    new_slot.set_editor_property("imported_material_slot_name", "CR_Aged_Brass")
    slots.append(new_slot)
    mesh.set_editor_property("static_materials", slots)

material_map = {
    "CR_Walnut_Dark": walnut,
    "CR_Walnut_Trim": trim,
    "CR_Aged_Brass": brass,
}
assigned = []
for index, slot in enumerate(mesh.get_editor_property("static_materials")):
    name = str(slot.material_slot_name)
    key = next((key for key in material_map if key in name), "CR_Walnut_Dark")
    mesh.set_material(index, material_map[key])
    assigned.append([index, name, material_map[key].get_path_name()])

nanite = mesh.get_editor_property("nanite_settings")
nanite.enabled = True
nanite.fallback_relative_error = 0.05
mesh.set_editor_property("nanite_settings", nanite)
body = mesh.get_editor_property("body_setup")
body.set_editor_property("collision_trace_flag", u.CollisionTraceFlag.CTF_USE_DEFAULT)
assert lib.save_loaded_asset(mesh, only_if_is_dirty=False)

cabinet.static_mesh_component.set_static_mesh(mesh)
cabinet.set_actor_location(u.Vector(-13600.0, -828.0, 4000.0), False, False)
cabinet.set_actor_rotation(u.Rotator(pitch=0.0, yaw=0.0, roll=0.0), False)
cabinet.set_actor_scale3d(u.Vector(1.0, 1.0, 1.0))
cabinet.static_mesh_component.set_editor_property("override_materials", [])
cabinet.static_mesh_component.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS)

center, extent = cabinet.get_actor_bounds(False)
bounds_min = [center.x - extent.x, center.y - extent.y, center.z - extent.z]
bounds_max = [center.x + extent.x, center.y + extent.y, center.z + extent.z]
dimensions = [extent.x * 2.0, extent.y * 2.0, extent.z * 2.0]
assert 225.0 < dimensions[0] < 240.0, dimensions
assert 50.0 < dimensions[1] < 60.0, dimensions
assert 120.0 < dimensions[2] < 132.0, dimensions
assert bounds_min[0] >= -14200.5 and bounds_max[0] <= -12999.5, [bounds_min, bounds_max]
assert bounds_min[1] >= -2200.5 and bounds_max[1] <= -799.0, [bounds_min, bounds_max]
assert bounds_min[2] >= 3999.0 and bounds_max[2] <= 4352.5, [bounds_min, bounds_max]

world = u.EditorLevelLibrary.get_editor_world()
assert u.EditorLoadingAndSavingUtils.save_map(world, "/Game/Conservatory/Maps/L_Exterior_RobotVR")
u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

level_sub.set_level_viewport_camera_info(
    u.Vector(-13600.0, -1830.0, 4140.0),
    u.Rotator(pitch=-4.0, yaw=90.0, roll=0.0),
    "",
)

report_path = ROOT / "Documentation" / "ControlRoomDrawersUnreal.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
report.update({
    "location": [-13600.0, -828.0, 4000.0],
    "rotation": [0.0, 0.0, 0.0],
    "scale": [1.0, 1.0, 1.0],
    "dimensions_cm": dimensions,
    "bounds_min": bounds_min,
    "bounds_max": bounds_max,
    "materials": assigned,
    "normal_import": "Computed normals and tangents in Unreal; zero-tangent FBX warnings resolved by reimport",
    "scale_fix": "FBX reimported at 100 uniform import scale so the static mesh is true centimetre size at actor scale 1",
})
report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
print("CONTROL_ROOM_DRAWERS_IMPORT_FIXED", json.dumps(report))
