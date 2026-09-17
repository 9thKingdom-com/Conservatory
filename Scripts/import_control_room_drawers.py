import datetime
import json
from pathlib import Path
import unreal as u

ROOT = Path(u.Paths.project_dir())
SRC = ROOT / "Asset-resources" / "Control-Room-Assets" / "Johns-Drawers" / "GameReady"
FBX = SRC / "SM_ControlRoom_Drawers_5x3.fbx"
MANIFEST = SRC / "Control-room-5x3_GameReady.json"
BASE = "/Game/Conservatory/Interiors/ControlRoom/Drawers5x3"
MAP = "/Game/Conservatory/Maps/L_Exterior_RobotVR"
MESH_PATH = BASE + "/SM_ControlRoom_Drawers_5x3"
ACTOR_LABEL = "CONTROL ROOM | Walnut drawers 5x3"

assert FBX.exists() and MANIFEST.exists(), "Prepared Blender export is missing"
spec = json.loads(MANIFEST.read_text(encoding="utf-8"))
assert spec["export_status"] == "exported"

lib = u.EditorAssetLibrary
assets = u.AssetToolsHelpers.get_asset_tools()
mel = u.MaterialEditingLibrary
actor_sub = u.get_editor_subsystem(u.EditorActorSubsystem)
level_sub = u.get_editor_subsystem(u.LevelEditorSubsystem)
world = u.EditorLevelLibrary.get_editor_world()
assert world.get_path_name().startswith(MAP + "."), world.get_path_name()

try:
    assert not u.EditorLoadingAndSavingUtils.get_dirty_content_packages(), "Content became dirty before import"
    assert not u.EditorLoadingAndSavingUtils.get_dirty_map_packages(), "Map became dirty before import"
except AttributeError:
    pass

actors_before = actor_sub.get_all_level_actors()
assert len([a for a in actors_before if a.get_class().get_name() == "VRSuitStation"]) == 11
assert not any(a.get_actor_label() == ACTOR_LABEL or "FIRST_BASEMENT_REAL_ASSET" in [str(t) for t in a.tags] for a in actors_before)

target_assets = [
    MESH_PATH,
    BASE + "/M_CR_Walnut_Dark",
    BASE + "/M_CR_Walnut_Trim",
    BASE + "/M_CR_Aged_Brass",
]
assert not any(lib.does_asset_exist(path) for path in target_assets), "Control Room drawer assets already exist; inspect instead of overwriting"

def transform(actor):
    p = actor.get_actor_location()
    r = actor.get_actor_rotation()
    s = actor.get_actor_scale3d()
    return [p.x, p.y, p.z, r.pitch, r.yaw, r.roll, s.x, s.y, s.z]

before_transforms = {a.get_name(): transform(a) for a in actors_before}
lib.make_directory(BASE)

def scalar(material, value, x, y):
    node = mel.create_material_expression(material, u.MaterialExpressionConstant, x, y)
    node.set_editor_property("r", value)
    return node

def color(material, values, x, y):
    node = mel.create_material_expression(material, u.MaterialExpressionConstant3Vector, x, y)
    node.set_editor_property("constant", u.LinearColor(*values, 1.0))
    return node

def lerp(material, a, b, alpha, x, y):
    node = mel.create_material_expression(material, u.MaterialExpressionLinearInterpolate, x, y)
    mel.connect_material_expressions(a, "", node, "A")
    mel.connect_material_expressions(b, "", node, "B")
    mel.connect_material_expressions(alpha, "", node, "Alpha")
    return node

def make_wood(name, dark, light, rough_low, rough_high, noise_scale):
    material = assets.create_asset(name, BASE, u.Material, u.MaterialFactoryNew())
    noise = mel.create_material_expression(material, u.MaterialExpressionNoise, -560, 100)
    noise.set_editor_property("scale", noise_scale)
    noise.set_editor_property("levels", 3)
    noise.set_editor_property("quality", 1)
    noise.set_editor_property("output_min", 0.0)
    noise.set_editor_property("output_max", 1.0)
    base = lerp(material, color(material, dark, -560, -120), color(material, light, -560, -20), noise, -230, -70)
    roughness = lerp(material, scalar(material, rough_low, -560, 240), scalar(material, rough_high, -560, 330), noise, -230, 285)
    mel.connect_material_property(base, "", u.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(roughness, "", u.MaterialProperty.MP_ROUGHNESS)
    mel.connect_material_property(scalar(material, 0.0, -230, 380), "", u.MaterialProperty.MP_METALLIC)
    mel.set_material_usage(material, u.MaterialUsage.MATUSAGE_NANITE)
    mel.recompile_material(material)
    assert lib.save_loaded_asset(material)
    return material

walnut = make_wood("M_CR_Walnut_Dark", (0.012, 0.003, 0.001), (0.065, 0.016, 0.005), 0.32, 0.46, 0.028)
trim = make_wood("M_CR_Walnut_Trim", (0.006, 0.0015, 0.0005), (0.026, 0.005, 0.0015), 0.38, 0.50, 0.035)

brass = assets.create_asset("M_CR_Aged_Brass", BASE, u.Material, u.MaterialFactoryNew())
mel.connect_material_property(color(brass, (0.23, 0.105, 0.021), -220, -80), "", u.MaterialProperty.MP_BASE_COLOR)
mel.connect_material_property(scalar(brass, 0.92, -220, 20), "", u.MaterialProperty.MP_METALLIC)
mel.connect_material_property(scalar(brass, 0.34, -220, 120), "", u.MaterialProperty.MP_ROUGHNESS)
mel.set_material_usage(brass, u.MaterialUsage.MATUSAGE_NANITE)
mel.recompile_material(brass)
assert lib.save_loaded_asset(brass)

u.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
task = u.AssetImportTask()
task.filename = str(FBX)
task.destination_path = BASE
task.destination_name = "SM_ControlRoom_Drawers_5x3"
task.automated = True
task.save = True
task.replace_existing = False
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
data.normal_import_method = u.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
task.options = options
assets.import_asset_tasks([task])

mesh = lib.load_asset(MESH_PATH)
assert mesh, "FBX import did not create the expected static mesh"
materials = {
    "CR_Walnut_Dark": walnut,
    "CR_Walnut_Trim": trim,
    "CR_Aged_Brass": brass,
}
assigned = []
for index, slot in enumerate(mesh.get_editor_property("static_materials")):
    slot_name = str(slot.material_slot_name)
    key = next((name for name in materials if name in slot_name), "CR_Walnut_Dark")
    mesh.set_material(index, materials[key])
    assigned.append([index, slot_name, materials[key].get_path_name()])

nanite = mesh.get_editor_property("nanite_settings")
nanite.enabled = True
nanite.fallback_relative_error = 0.05
mesh.set_editor_property("nanite_settings", nanite)
body = mesh.get_editor_property("body_setup")
body.set_editor_property("collision_trace_flag", u.CollisionTraceFlag.CTF_USE_DEFAULT)
assert lib.save_loaded_asset(mesh, only_if_is_dirty=False)

# North wall of the former Library & Study. Front faces south into the Control Room.
location = u.Vector(-13600.0, -828.0, 4000.0)
rotation = u.Rotator(pitch=0.0, yaw=-90.0, roll=0.0)
cabinet = actor_sub.spawn_actor_from_object(mesh, location, rotation)
assert cabinet
cabinet.set_actor_label(ACTOR_LABEL)
cabinet.set_folder_path("08 Bunker/01 Habitat/Control Room/Real assets")
cabinet.tags = ["CONTROL_ROOM_REAL_ASSET", "FIRST_BASEMENT_REAL_ASSET", "JOHN_ORIGINAL"]
cabinet.static_mesh_component.set_editor_property("mobility", u.ComponentMobility.STATIC)
cabinet.static_mesh_component.set_collision_enabled(u.CollisionEnabled.QUERY_AND_PHYSICS)

center, extent = cabinet.get_actor_bounds(False)
bounds_min = [center.x - extent.x, center.y - extent.y, center.z - extent.z]
bounds_max = [center.x + extent.x, center.y + extent.y, center.z + extent.z]
assert bounds_min[0] >= -14200.5 and bounds_max[0] <= -12999.5, [bounds_min, bounds_max]
assert bounds_min[1] >= -2200.5 and bounds_max[1] <= -799.0, [bounds_min, bounds_max]
assert bounds_min[2] >= 3999.0 and bounds_max[2] <= 4352.5, [bounds_min, bounds_max]

unchanged = {
    a.get_name(): transform(a)
    for a in actor_sub.get_all_level_actors()
    if a.get_name() in before_transforms
}
unexpected = [name for name, value in unchanged.items() if value != before_transforms[name]]
assert not unexpected, unexpected

assert u.EditorLoadingAndSavingUtils.save_map(world, MAP)
u.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

level_sub.set_level_viewport_camera_info(
    u.Vector(-13600.0, -1775.0, 4135.0),
    u.Rotator(pitch=-4.0, yaw=90.0, roll=0.0),
    "",
)

report = {
    "engine": u.SystemLibrary.get_engine_version(),
    "timestamp": datetime.datetime.now().isoformat(),
    "map": MAP,
    "asset": mesh.get_path_name(),
    "actor": cabinet.get_name(),
    "label": cabinet.get_actor_label(),
    "folder": str(cabinet.get_folder_path()),
    "location": [location.x, location.y, location.z],
    "rotation": [rotation.pitch, rotation.yaw, rotation.roll],
    "bounds_min": bounds_min,
    "bounds_max": bounds_max,
    "materials": assigned,
    "nanite": True,
    "collision": "Imported UCX simple cabinet volume; Query and Physics enabled",
    "actor_count_before": len(actors_before),
    "actor_count_after": len(actor_sub.get_all_level_actors()),
    "unrelated_transform_changes": unexpected,
    "backup": str(ROOT / "Saved" / "Backups" / "ControlRoomDrawersUnreal" / "20260915-143359"),
    "placement_reason": "Centred on open north wall; south suit line, east monitor and west doorway remain clear",
}
(ROOT / "Documentation" / "ControlRoomDrawersUnreal.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("CONTROL_ROOM_DRAWERS_IMPORT_COMPLETE", json.dumps(report))
