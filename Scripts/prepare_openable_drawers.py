import bpy, bmesh, json, math, os, sys
from pathlib import Path
from mathutils import Vector

SOURCE = Path(r"C:\Users\ASUS TUF\Documents\1 conservatory\Asset-resources\Control-Room-Assets\Johns-Drawers\Control-room-5x3.blend")
OUT = SOURCE.parent / "GameReady" / "Openable"
OUT.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
sc = bpy.context.scene

coll = bpy.data.collections.new("OPENABLE_EXPORT")
sc.collection.children.link(coll)

source_objs = [o for o in bpy.data.objects if o.type == 'MESH' and not o.name.startswith(('SM_ControlRoom_Drawers_5x3','UCX_SM_ControlRoom_Drawers_5x3'))]
drawer_src = bpy.data.objects.get('Cube.003')
if not drawer_src:
    raise RuntimeError('Cube.003 is missing')
cabinet_srcs = [o for o in source_objs if o != drawer_src]

def duplicate_and_apply(obj):
    dup = obj.copy()
    dup.data = obj.data.copy()
    for coll2 in list(dup.users_collection):
        coll2.objects.unlink(dup)
    coll.objects.link(dup)
    bpy.ops.object.select_all(action='DESELECT')
    dup.select_set(True)
    bpy.context.view_layer.objects.active = dup
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return dup

cabinet_parts = [duplicate_and_apply(o) for o in cabinet_srcs]
bpy.ops.object.select_all(action='DESELECT')
for o in cabinet_srcs:
    o.select_set(True)
bpy.context.view_layer.objects.active = cabinet_srcs[0]
bpy.ops.object.join()
cabinet = bpy.context.view_layer.objects.active
cabinet.name = "SM_CR_Drawers_5x3_Cabinet"

drawer_dup = duplicate_and_apply(drawer_src)
me = drawer_dup.data
bm = bmesh.new(); bm.from_mesh(me)
bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
parent = list(range(len(bm.verts)))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a,b):
    ra,rb = find(a),find(b)
    if ra != rb: parent[rb] = ra
for e in bm.edges:
    union(e.verts[0].index, e.verts[1].index)
groups = {}
for v in bm.verts:
    groups.setdefault(find(v.index), []).append(v.index)

verts = me.vertices
comps = []
for ids in groups.values():
    pts = [verts[i].co for i in ids]
    cx = sum(p.x for p in pts) / len(pts)
    cz = sum(p.z for p in pts) / len(pts)
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    comps.append((lo, hi, ids, Vector((cx, 0, cz))))
if len(comps) != 60:
    raise RuntimeError(f"Expected 60 ornate-front components, got {len(comps)}")
lo_all = Vector((min(c[0].x for c in comps), min(c[0].y for c in comps), min(c[0].z for c in comps)))
hi_all = Vector((max(c[1].x for c in comps), max(c[1].y for c in comps), max(c[1].z for c in comps)))
col_w = (hi_all.x - lo_all.x) / 4.0
row_h = (hi_all.z - lo_all.z) / 5.0
grouped = {}
for idx, (lo, hi, ids, center) in enumerate(comps):
    col = min(3, max(0, int((center.x - lo_all.x) / col_w)))
    row = min(4, max(0, int((center.z - lo_all.z) / row_h)))
    grouped.setdefault((row, col), []).append(idx)
if len(grouped) != 20:
    raise RuntimeError(f"Expected 20 drawer groups, got {len(grouped)}")

for row in range(5):
    for col in range(4):
        ids = grouped[(row, col)]
        allowed = set()
        for i in ids:
            allowed.update(groups[find(i)])
        selected_faces = []
        for f_idx, f in enumerate(bm.faces):
            vs = set(v.index for v in f.verts)
            if vs and all(v in allowed for v in vs):
                selected_faces.append(f_idx)
        if not selected_faces:
            raise RuntimeError(f"No faces for drawer {row}-{col}")
        new_bm = bmesh.new()
        vert_map = {}
        for v in bm.verts:
            if v.index in allowed:
                vert_map[v.index] = new_bm.verts.new(v.co)
        new_bm.verts.ensure_lookup_table()
        for f_idx in selected_faces:
            f = bm.faces[f_idx]
            new_verts = [vert_map[v.index] for v in f.verts]
            nf = new_bm.faces.new(new_verts)
            nf.material_index = f.material_index
            nf.smooth = f.smooth
        new_bm.normal_update()
        new_mesh = bpy.data.meshes.new(f"SM_CR_Drawers_5x3_Drawer_{row:02d}{col:02d}")
        new_bm.to_mesh(new_mesh)
        new_bm.free()
        new_obj = bpy.data.objects.new(new_mesh.name, new_mesh)
        coll.objects.link(new_obj)
        for slot in me.materials:
            new_mesh.materials.append(slot)

bpy.ops.object.select_all(action='DESELECT')
cabinet.select_set(True)
bpy.context.view_layer.objects.active = cabinet
bb = [cabinet.matrix_world @ Vector(c) for c in cabinet.bound_box]
lo = Vector((min(p.x for p in bb), min(p.y for p in bb), min(p.z for p in bb)))
hi = Vector((max(p.x for p in bb), max(p.y for p in bb), max(p.z for p in bb)))
center = (lo + hi) * 0.5
size = hi - lo
bpy.ops.mesh.primitive_cube_add(location=center)
ucx = bpy.context.object
ucx.name = "UCX_SM_CR_Drawers_5x3_Cabinet_00"
ucx.dimensions = size
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

bpy.ops.object.select_all(action='DESELECT')
cabinet.select_set(True)
ucx.select_set(True)
bpy.context.view_layer.objects.active = cabinet
bpy.ops.export_scene.fbx(
    filepath=str(OUT / "SM_CR_Drawers_5x3_Cabinet.fbx"),
    use_selection=True,
    object_types={'MESH'},
    use_mesh_modifiers=True,
    apply_unit_scale=True,
    apply_scale_options='FBX_SCALE_ALL',
    axis_forward='-Y',
    axis_up='Z',
    mesh_smooth_type='FACE',
    add_leaf_bones=False,
    bake_anim=False,
    path_mode='AUTO',
)

drawer_objs = sorted([o for o in coll.objects if o.name.startswith("SM_CR_Drawers_5x3_Drawer_")])
for o in drawer_objs:
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.export_scene.fbx(
        filepath=str(OUT / f"{o.name}.fbx"),
        use_selection=True,
        object_types={'MESH'},
        use_mesh_modifiers=True,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Y',
        axis_up='Z',
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        bake_anim=False,
        path_mode='AUTO',
    )

manifest = {
    "source": str(SOURCE),
    "output": str(OUT),
    "drawer_count": len(drawer_objs),
    "drawer_objects": [o.name for o in drawer_objs],
    "cabinet": cabinet.name,
    "collision": ucx.name,
    "open_direction_local": [0.0, -1.0, 0.0],
    "open_distance_cm": 45.0,
    "origin": "bottom-center of cabinet geometry; drawer meshes are in the same local space",
}
(OUT / "Control-room-5x3_Openable.json").write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print("CONTROL_ROOM_DRAWERS_OPENABLE_READY", json.dumps(manifest))
