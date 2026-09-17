# Verification — 7 September 2026

- Installed engine verified from Engine/Build/Build.version: UE 5.8.2.
- ConservatoryEditor Win64 Development: built successfully with Visual Studio 2022 / MSVC 14.44.
- Conservatory Win64 Development: built successfully.
- Final map generation completed with no logged errors; the saved .umap contains the landscape and environment.
- Standalone editor game-mode smoke test: passed. The character travelled approximately 15 m using the movement function bound to W and remained grounded at the overlook.
- Village: vertical trace located the terrain; the character settled on it and remained grounded at (12000, -10500, 954.999) cm.
- Final run logged no failed material compilation or missing instanced-mesh material usage.
- Hilltop and village screenshots were rendered in the running game and visually inspected. Roof visibility, ground textures, foliage, distant terrain and the village view were checked.
- The three-module conservatory was added following the user's design reference. Exterior and interior game screenshots were inspected after correcting the Python rotation convention to named axes.
- Conservatory traversal: passed. The character walked 1118.1 cm from the corridor into the dome and remained on the raised floor at capsule-centre elevation 6318.6 cm. The test explicitly rejects walking on the underlying terrain.
- Lumen mesh distance fields are enabled. The valley has a stronger low-lying volumetric fog layer.

The copied JSON reports and PNG screenshots in this directory document that final run. Full transient logs remain in Saved/BuildExterior.log and Saved/SmokeTest.log.

This is a playable procedural environment and basic architectural shell. The conservatory has a walkable interior; village cottages remain exterior set pieces. It has no survival mechanics, player construction or trapping/sealing behaviour, or finished photoreal art pass. It has not been cooked into a redistributable package, and no exhaustive whole-map traversal or performance benchmark was performed.

## Library, hill-edge terrace and bunker - 8 September 2026

The current map is L_Exterior_Library; the older results above apply to the original map. The owned-library foliage upgrade brought in 50 assets and dependencies with no unresolved package references. The enlarged 66 x 21.6 m conservatory sits on a supported hill-edge terrace; the runtime exterior walking test passed with 18.75 m travel and the player on the architectural floor. See HillEdgeWalkTest.json and HillEdgePlacement.json.

The Habitat runtime module and both Win64 Development targets compiled successfully. The bunker generator completed with zero logged errors or warnings. Runtime checks passed for travel down and up using the same service-lift Travel function called by E, an 11.15 m corridor walk, all twelve doorways, and physical descent and ascent of the full spiral without jumping. See BunkerWalkTest.json. Keyboard E/Home input itself was not simulated by the automated check.

The final art cleanup added chair legs, monitor supports and corrected dial orientation after those traversal tests. These changes do not alter the tested hall, doors, stairs or lift. The final map was regenerated successfully and rendered for visual review. Source/Habitat implements the lift; Content/Python startup code runs verification only with explicit test flags.

Limits: early primitive-based bunker props; equipment gauges are not simulated. The lift uses a fade transfer and has no excavated shaft. Village buildings remain exteriors. There is no cooked distributable or exhaustive performance benchmark.

Final rerun after moving the conservatory lift inward and raising its floor: passed, including both lift transfers, all twelve doorways, stair descent/ascent and an 11.13 m corridor walk. BunkerWalkTest.json now records this final map. The final lift preview confirms the conservatory column no longer intersects the cabin.

Room-gap fix: saved and visually verified in L_Exterior_Sealed. All twelve generated structural joins were counted before saving; the runtime preview shows the former opening closed. The lower corridor also has a continuous ceiling. The previous map remains untouched because Unreal held it locked. New launches default to L_Exterior_Sealed.

Master-based revision: L_Exterior_Modular is now the active map. Both lower-wall connections were walked through in one continuous 18.74 m traversal; the capsule remained on the architectural floor at Z=6332.88 cm. Lift travel down to the bunker and back to its new north-dome cabin passed. The full 16-sector frame, shorter connector and interiors were visually reviewed in runtime screenshots. See ModularWalkTest.json and ModularExterior/Connection/Interior.png. Import completed successfully; tangent-basis notices remain on portions of the detailed source mesh, which currently uses materials without normal maps. Dedicated LOD/collision optimisation remains future work before extensive player building.

Ornate lift revision: the crowned brass/glass upper enclosure was placed against the north dome's inland facade, with a low-roof matching lower cabin. Runtime tests passed walking into the upper enclosure, transfer down, walking out of the lower enclosure, returning inside and transfer upstairs. See OrnateLiftTest.json. The final plaque alignment was adjusted afterwards without changing collision or travel behavior. An in-game preview checks facade clearance and appearance. The Blender/FBX source is retained in SourceAssets/OrnateLift. Import completed successfully with smoothing-group notices on these prototype meshes.
