# Core habitat conservatory — 10 September 2026

John approved the five-dome Blender assembly with midpoint walkway pillars as the core habitat in Chapter 1. It replaces the old two-dome conservatory in `/Game/Conservatory/Maps/L_Exterior_RobotVR`, the existing default editor/game map. `Walk Around.cmd` continues to launch this map.

The habitat contains a 24-bay central dome, four original-size 16-bay domes, and four two-section walkways with seven pillar positions per side. The centre is 1.5 times the original dome diameter. Repeating structural parts use Nanite static meshes; fitted glazing and floor meshes provide the playable shell. Materials follow the green frame, restrained brass, pale floor and transparent glass palette.

The final Unreal origin is **(-11000, 0, 6230.95) cm**. The floor remains **6242.75 cm**. The assembly sits four metres inland of the old centre so the retained lift enclosure fits inside the central dome. The lift, dock, bunker, room contents, intercoms, robots and town retain their saved actor placements.

John explicitly permitted terrain changes. Fitted ground supports the wider footprint and blends into the original landscape, replacing the obsolete narrow terrace and its rails/supports/rockface. Foliage instances intersecting the habitat were cleared. Navigation was rebuilt. See `CoreHabitatImport.json` for the affected actor list, foliage counts, backups, and unrelated-actor checks.

## Sources and regeneration

- Editable source: `Reference images/Conservatory-MAIN-PARTS1.blend`, scene `ASSEMBLY | Five domes - editable`.
- FBX parts and placement manifest: `SourceAssets/CoreHabitat/`.
- Unreal assets: `/Game/Conservatory/Architecture/CoreHabitat`.
- Run `Scripts/export_core_habitat.py` in Blender, then `Scripts/export_habitat_terrain.py`. Temporary export scenes preserve the editable source geometry.
- `Scripts/apply_core_habitat.py` imports the manifest into the default map, preserves unrelated actors, and rebuilds navigation. It backs up the map before editing it.
- `Scripts/fit_core_habitat_lift.py` records the placement refinement used during integration; a fresh full import already uses the final origin.

## Validation evidence

At the final origin, all four traversals covered approximately 37.7 metres with the player remaining on the floor. The lift successfully travelled to the bunker and back. All checks passed and the test process exited normally. Final rendered views were inspected, including clearance around the retained lift enclosure.

`CoreHabitatRuntime.json` records standalone walking/lift checks, tested origin and timestamp. The west route uses a one-metre lateral offset to pass an existing outdoor robot without moving it. `Scripts/run_core_habitat_test.ps1` runs the opt-in test with automatic exit and a process timeout.

Rendered views: `CoreHabitatOverview.png`, `CoreHabitatInterior.png`, `CoreHabitatWalkway.png`, and `CoreHabitatLift.png`.

This is the approved habitat layout integrated into Unreal, not a claim of final materials, Fab packaging or completed survival simulation. Existing placeholder content remains for continued development.

## White/brass and pillar-base repair — 10 September 2026
John restored ivory framing with brass trim. Inward-facing closed solids caused the apparently missing base panels; habitat_mesh_finish.py corrects their orientation during export and assigns restrained brass moulding bands. Seven frame/cap assets were reimported and visually checked in the live editor. Original Blender source remains preserved. Outdoor robot 01 was moved onto exterior navigation at (-14000, 5000, 6202.586) cm to clear the corridor; all eleven robots remain, including the lift-side indoor unit. Map and assets saved; see HabitatFinish.json and PillarNormalsCheck.json. The previous full traversal test predates this material/face-orientation repair and robot relocation.

