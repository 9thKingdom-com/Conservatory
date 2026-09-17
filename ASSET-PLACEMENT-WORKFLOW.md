# Asset placement workflow

**Purpose:** Capture the repeatable path for bringing a bespoke Blender asset into the Conservatory project and making it playable where interaction is needed. Use this before the next Control Room furniture piece.

## Core principle
- Treat the Blender source as the authority for geometry and materials.
- Never regenerate or overwrite John's work; make a derivative package and place that in Unreal.
- Separate visual geometry from interaction geometry. A drawer, lid, door or similar part should be its own mesh object when it must move.
- Keep the source Blender file untouched. Work from a duplicate or a separate export collection.

## 1. Blender source audit
- Confirm the file path and that the source is the intended version.
- Identify the authored object names and which parts are structural vs interactive.
- If an interactive part is currently a single mesh, split it into separate objects for export without changing the original.
- Keep the cabinet/prop body and interactive parts in one local coordinate system so Unreal can place them consistently.
- Record source mesh count, triangle counts, dimensions and the local origin.

## 2. Derivative game-ready export
- Export a separate FBX for the prop body and each interactive part.
- Use names that make the relationship obvious, e.g. `SM_<Asset>_<Part>` and `SM_<Asset>_<Part>_Drawer_00`.
- For a cabinet, use a simple box collision (`UCX_...`) for the body. If an interactive part needs collision, use its own collision mesh or a component-level box.
- Keep a JSON manifest next to the FBX files describing the source, outputs, drawer/part count, open direction and open distance.

## 3. Unreal asset import
- Import into a scoped content folder under `/Game/Conservatory/Interiors/...`.
- Use legacy FBX import for this project's current workflow; set `import_materials=false` so Unreal materials can be reused or created deliberately.
- Rebuild or assign the Unreal materials from the source palette. Do not rely on FBX materials.
- Use Nanite only when the asset is static or extremely high detail and performance is acceptable. For interactive parts, test movement and collision first.
- If the imported scale is wrong, fix the FBX import scale rather than scaling the actor. Verify real dimensions in centimetres after import.

## 4. Interactive placement pattern
- Create a dedicated C++ actor for the interactive pattern, not a one-off static mesh.
- Give it editable properties for the body mesh, array of interactive meshes, open distance and interaction range.
- On construction or BeginPlay, create one component per interactive mesh.
- Keep the interactive part's closed transform as `FVector::ZeroVector` (or its authored transform) and move it along a local open direction.
- Use a line trace from the player camera to identify the aimed interactive part, and toggle that part on the interaction key.
- Do not hard-code one prop's geometry into a generic actor. Keep the actor reusable for future chests, cabinets and drawers.

## 5. Placement discipline
- Back up the saved map before modifying it.
- Place the prop against an available wall, with the front facing the walkable side.
- Verify the actor bounds against the room and leave circulation clear.
- Record the actor label, folder, transform and placement reason.

## 6. Verification checklist
- Map saved.
- Asset appears in the intended room and at real-world scale.
- Materials respond correctly to room lighting.
- Collision blocks the body but does not obstruct circulation.
- Each interactive part opens and closes without clipping.
- The player can reach and use it.
- Runtime screenshot inspected.

## 7. Documentation
- Update the relevant Unreal-Reference recipe with tested evidence, not assumptions.
- Record limitations (e.g., procedural Blender materials not translating exactly, no LODs yet, no full navigation rebuild).
- Keep `ASSET-PLACEMENT-WORKFLOW.md` as the shared pattern for future assets.
