import bpy
import json
import math
from pathlib import Path
from mathutils import Vector


EXPECTED = Path(r"C:\Users\ASUS TUF\Documents\1 conservatory\Asset-resources\Control-Room-Assets\Johns-Drawers\Control-room-5x3.blend")
ROOT = EXPECTED.parent
OUT = ROOT / "GameReady"
FBX_PATH = OUT / "SM_ControlRoom_Drawers_5x3.fbx"
PREVIEW_PATH = OUT / "Control-room-5x3_Walnut-Brass_Preview.png"
MANIFEST_PATH = OUT / "Control-room-5x3_GameReady.json"


def ensure_principled_material(name, color, metallic, roughness):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, 1.0)
    mat.metallic = metallic
    mat.roughness = roughness
    nodes = mat.node_tree.nodes
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.inputs["Base Color"].default_value = (*color, 1.0)
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    if "IOR" in shader.inputs:
        shader.inputs["IOR"].default_value = 1.48
    mat.node_tree.links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    return mat


def clear_collection(name):
    coll = bpy.data.collections.get(name)
    if coll:
        for obj in list(coll.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(coll)
    coll = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(coll)
    return coll


def world_bounds(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    return (
        Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points))),
        Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points))),
    )


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def link_only(obj, collection):
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection.objects.link(obj)


if Path(bpy.data.filepath).resolve() != EXPECTED.resolve():
    raise RuntimeError(f"Wrong Blender file is active: {bpy.data.filepath}")

authoring_collection = bpy.data.collections.get("Collection")
source = [obj for obj in authoring_collection.objects if obj.type == "MESH"] if authoring_collection else []
if len(source) != 13 or not bpy.data.objects.get("Cube.012"):
    raise RuntimeError(f"Unexpected authored mesh set: {len(source)} objects")

OUT.mkdir(parents=True, exist_ok=True)

# Import-safe PBR values: rich dark walnut and genuinely metallic aged brass.
walnut = ensure_principled_material("CR_Walnut_Dark", (0.031, 0.0085, 0.0032), 0.0, 0.36)
walnut_trim = ensure_principled_material("CR_Walnut_Trim", (0.014, 0.0032, 0.0012), 0.0, 0.43)
brass = ensure_principled_material("CR_Aged_Brass", (0.23, 0.105, 0.021), 0.92, 0.34)
stone = ensure_principled_material("CR_Preview_WarmStone", (0.075, 0.048, 0.030), 0.0, 0.72)
plaster = ensure_principled_material("CR_Preview_WarmPlaster", (0.082, 0.047, 0.024), 0.0, 0.82)

for obj in source:
    original_indices = [poly.material_index for poly in obj.data.polygons]
    obj.data.materials.clear()
    if obj.name == "Cube.012":
        obj.data.materials.append(walnut)
        obj.data.materials.append(brass)
        for poly, old_index in zip(obj.data.polygons, original_indices):
            poly.material_index = 1 if old_index == 1 else 0
    else:
        obj.data.materials.append(walnut_trim if len(obj.data.polygons) <= 6 else walnut)

    # Tiny bevels make the rectilinear cabinet catch warm light without altering its proportions.
    if obj.name != "Cube.012" and not obj.modifiers.get("GameReady_EdgeBevel"):
        bevel = obj.modifiers.new("GameReady_EdgeBevel", "BEVEL")
        bevel.width = 0.003
        bevel.segments = 2
        bevel.limit_method = "ANGLE"
        bevel.angle_limit = math.radians(35.0)

lo, hi = world_bounds(source)
center = (lo + hi) * 0.5
size = hi - lo

# A separate hidden collection contains the single-mesh Unreal export and simple UCX collision.
export_coll = clear_collection("GAME_EXPORT")
duplicates = []
for src in source:
    dup = src.copy()
    dup.data = src.data.copy()
    export_coll.objects.link(dup)
    duplicates.append(dup)

bpy.ops.object.select_all(action="DESELECT")
for dup in duplicates:
    dup.hide_set(False)
    dup.hide_viewport = False
    dup.select_set(True)
    bpy.context.view_layer.objects.active = dup
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for modifier in list(dup.modifiers):
        bpy.ops.object.modifier_apply(modifier=modifier.name)

bpy.context.view_layer.objects.active = duplicates[0]
bpy.ops.object.join()
game_obj = bpy.context.view_layer.objects.active
game_obj.name = "SM_ControlRoom_Drawers_5x3"

# Bottom-center pivot gives predictable floor placement in Unreal.
game_lo, game_hi = world_bounds([game_obj])
pivot = Vector(((game_lo.x + game_hi.x) * 0.5, (game_lo.y + game_hi.y) * 0.5, game_lo.z))
bpy.context.scene.cursor.location = pivot
bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="MEDIAN")
game_obj.location = (0.0, 0.0, 0.0)

local_points = [Vector(corner) for corner in game_obj.bound_box]
local_lo = Vector((min(p.x for p in local_points), min(p.y for p in local_points), min(p.z for p in local_points)))
local_hi = Vector((max(p.x for p in local_points), max(p.y for p in local_points), max(p.z for p in local_points)))
local_size = local_hi - local_lo
local_center = (local_lo + local_hi) * 0.5

bpy.ops.mesh.primitive_cube_add(location=local_center)
collision = bpy.context.object
collision.name = "UCX_SM_ControlRoom_Drawers_5x3_00"
collision.dimensions = local_size
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
collision.display_type = "WIRE"
collision.hide_render = True
link_only(collision, export_coll)

game_obj["asset_role"] = "Control-room storage cabinet"
game_obj["finish"] = "Dark walnut with aged brass drawer pulls"
game_obj["pivot"] = "Bottom center"
game_obj["collision"] = collision.name
game_obj["source_file"] = str(EXPECTED)

# Export only the game mesh and collision helper.
bpy.ops.object.select_all(action="DESELECT")
game_obj.hide_set(False)
collision.hide_set(False)
game_obj.select_set(True)
collision.select_set(True)
bpy.context.view_layer.objects.active = game_obj
export_status = "not attempted"
try:
    bpy.ops.export_scene.fbx(
        filepath=str(FBX_PATH),
        use_selection=True,
        object_types={"MESH"},
        use_mesh_modifiers=True,
        apply_unit_scale=True,
        apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Y",
        axis_up="Z",
        mesh_smooth_type="FACE",
        add_leaf_bones=False,
        bake_anim=False,
        path_mode="AUTO",
    )
    export_status = "exported"
except Exception as exc:
    export_status = f"failed: {exc}"

export_coll.hide_render = True
export_coll.hide_viewport = True

# Presentation-only environment: warm stone floor, plaster wall, and an amber practical-light setup.
presentation = clear_collection("PRESENTATION_ONLY")

bpy.ops.mesh.primitive_plane_add(size=max(size.x, size.y) * 3.2, location=(center.x, center.y, lo.z - 0.008))
ground = bpy.context.object
ground.name = "Preview_Ground"
ground.data.materials.append(stone)
link_only(ground, presentation)

bpy.ops.mesh.primitive_plane_add(size=max(size.x * 2.6, 5.0), location=(center.x, hi.y + 0.24, lo.z + max(size.z, 2.2) * 0.52), rotation=(math.radians(90), 0, 0))
backdrop = bpy.context.object
backdrop.name = "Preview_Backdrop"
backdrop.data.materials.append(plaster)
link_only(backdrop, presentation)

def add_area(name, location, target, energy, color, area_size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.color = color
    data.shape = "DISK"
    data.size = area_size
    obj = bpy.data.objects.new(name, data)
    presentation.objects.link(obj)
    obj.location = location
    look_at(obj, target)
    return obj

target = Vector((center.x, center.y, lo.z + size.z * 0.53))
add_area("Key_Warm_Right", (hi.x + size.x * 0.48, lo.y - size.x * 0.70, hi.z + size.z * 0.72), target, 520, (1.0, 0.53, 0.25), 1.15)
add_area("Fill_Soft_Left", (lo.x - size.x * 0.55, lo.y - size.x * 0.50, lo.z + size.z * 0.85), target, 210, (1.0, 0.72, 0.48), 1.7)
add_area("Rim_Warm", (center.x + size.x * 0.15, hi.y + size.y * 2.2, hi.z + size.z * 0.55), target, 300, (1.0, 0.58, 0.31), 1.0)

camera_data = bpy.data.cameras.new("Preview_Camera")
camera = bpy.data.objects.new("Preview_Camera", camera_data)
presentation.objects.link(camera)
camera_data.lens = 58
camera.location = (center.x + size.x * 0.08, lo.y - max(4.2, size.x * 1.92), lo.z + size.z * 0.62)
look_at(camera, target)
bpy.context.scene.camera = camera

world = bpy.context.scene.world or bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.012, 0.006, 0.003, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.11

scene = bpy.context.scene
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1100
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(PREVIEW_PATH)
scene.render.film_transparent = False
if hasattr(scene, "view_settings"):
    try:
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass

# Keep authored meshes visible and all helper geometry unselected.
bpy.ops.object.select_all(action="DESELECT")
for obj in source:
    obj.hide_render = False
    obj.hide_set(False)

bpy.ops.wm.save_as_mainfile(filepath=str(EXPECTED))
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(EXPECTED))

triangles = sum(len(poly.vertices) - 2 for poly in game_obj.data.polygons)
manifest = {
    "asset": game_obj.name,
    "source": str(EXPECTED),
    "fbx": str(FBX_PATH),
    "preview": str(PREVIEW_PATH),
    "export_status": export_status,
    "dimensions_m": [round(v, 4) for v in local_size],
    "source_mesh_objects": len(source),
    "export_triangles": triangles,
    "pivot": "bottom center",
    "collision": collision.name,
    "materials": {
        "CR_Walnut_Dark": {"base_color_linear": [0.031, 0.0085, 0.0032], "metallic": 0.0, "roughness": 0.36},
        "CR_Walnut_Trim": {"base_color_linear": [0.014, 0.0032, 0.0012], "metallic": 0.0, "roughness": 0.43},
        "CR_Aged_Brass": {"base_color_linear": [0.23, 0.105, 0.021], "metallic": 0.92, "roughness": 0.34},
    },
    "notes": [
        "Presentation lights, camera, ground, and backdrop are excluded from FBX export.",
        "Source geometry is preserved; GAME_EXPORT contains the joined export copy and UCX collision.",
        "Use Nanite for the ornate pull geometry or generate distance LODs after Unreal import.",
    ],
}
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("CONTROL_ROOM_DRAWERS_COMPLETE", json.dumps(manifest))
