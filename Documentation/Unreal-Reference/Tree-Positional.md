# Olive tree positional assembly

13 September 2026; Blender 5.1.1, Unreal 5.8.2.

John explicitly requests the current olive tree with a circular reference-style limestone base in the large dome for positioning. This supersedes the earlier instruction to wait for a perfected source. Later refinement and reimport are intended; this is not finished art or a Fab-ready tree.

Source: `Asset Chest/01 John Originals/TREE-MASTER/TREE-MASTER.blend`. The wood remains one sculptable mesh. The new `08 Circular limestone planter` collection contains separate editable stone courses, panels, pilasters and compass cartouches. `98 Archived original planter` preserves the old assembly, hidden from viewport and render. The timestamped pre-circular-base Blender backup preserves the entire starting file. Packed reference: John's `tree2-base.png`.

The planter is 12.78 m across, 0.80 m high, with four 1.01 m cartouches. These dimensions are adjustable implementation choices. Reference inscriptions, seating and surrounding architecture were not added. The existing tree geometry and foliage were retained.

Export uses `Scripts/export_tree_positional.py` on a separate background Blender process. It evaluates the current source, exports Structure and Foliage FBXs, and reduces only the derivative wood mesh to 40 percent. It does not save changes to the master. Export report records 634,862 structure and 1,096,032 foliage triangles. This is a detailed positional asset, without production LODs or wind. Blender procedural shaders are approximated with source colours, stone/bark noise and two-sided silver-backed leaves in Unreal.

Before import, Unreal was closed and the saved map timestamp matched the prior session (07:31:18). `TreePositionBaseline.json` records all current actors. The centre is taken from the live saved Centre Floor actor, not the old habitat origin. The two existing placeholders, Dome planter and Young white oak under dome, are the scoped replacements; their original state remains in the map backup. No whole-map generator is used.

Scripts: `audit_tree_position.py`, `add_tree_circular_base.py`, `export_tree_positional.py`, `import_tree_positional.py`, `view_tree_positional.py`. The authoring/import scripts are initial revisions, not safe blind rerun commands. Inspect the current master and map before future work. For a future update, re-export the latest Blender master and reimport the two mesh assets at their existing actor transforms.

Use forward slashes in Unreal's `-script=` argument on Windows: backslash followed by the project folder's `1` was interpreted as an escape in an initial read-only commandlet attempt. No mutation occurred in that failed attempt.

Verification evidence is recorded separately in TreePositionalImport.json, TreePositionalRuntime.json and TreePositionalUnreal.png after the relevant runs finish.

## Verified result — 14:12, 13 September 2026
Saved L_Exterior_RobotVR with the two existing placeholder actors reassigned to the new structure/foliage meshes, at (-14308.320922, -1378.138839, 6242.750000) cm, unit scale. All 2186 actors retained; the other 2184 actor transforms matched the immediate baseline exactly. Map checkpoint: Saved/Backups/TreePositional/20260913-141017/L_Exterior_RobotVR.umap. No landscape, architecture or lighting changes.

Reopened the saved map in a bounded windowed runtime. Walking toward the planter stopped at radius 672.07 cm; standing height matched the floor. Player capsule sweeps around a 900 cm radius circle passed all 72 segments. This checks local circulation and planter collision, not a complete navigation rebuild or lift regression suite. TreePositionalUnreal.png was visually inspected: tree and base sit inside the large dome, foliage and stone are visible, and the surrounding lift/architecture remain intact. Review exited normally. Blender remains open with the current tree and circular planter visible.

Limitations: source tree is still a sculpting work in progress. The FBX importer reported some near-zero normals/tangents on Structure; the inspected positional render has no obvious missing faces, but production topology and tangent cleanup remain appropriate when the source is refined. Foliage has no collision; Structure uses triangle collision. Navigation was not rebuilt. No final-art approval is claimed.
