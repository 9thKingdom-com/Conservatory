import bpy
import json

if not bpy.data.filepath:
    bpy.ops.import_scene.fbx(filepath=r"C:\Users\ASUS TUF\Documents\1 conservatory\Asset-resources\Control-Room-Assets\Johns-Drawers\GameReady\SM_ControlRoom_Drawers_5x3.fbx")

rows = []
for obj in bpy.data.objects:
    if obj.type != "MESH" or (bpy.data.filepath and obj.name not in {"Cube.012", "SM_ControlRoom_Drawers_5x3"}):
        continue
    counts = {}
    for poly in obj.data.polygons:
        counts[poly.material_index] = counts.get(poly.material_index, 0) + 1
    rows.append({
        "object": obj.name,
        "dimensions": list(obj.dimensions),
        "scale": list(obj.scale),
        "materials": [slot.material.name if slot.material else None for slot in obj.material_slots],
        "polygon_material_counts": counts,
    })
print("DRAWER_BLEND_EXPORT_AUDIT", json.dumps(rows))
