# Valley settlements — 11 September 2026

John authorised replacing the old town with a rustic modern settlement, outer villages and farms, with every building interior explorable for future treasure hunts and mysteries.

## Authored layout

| Area | Buildings | Character |
| --- | ---: | --- |
| Main town | 16 | Cottages, provisions shop, repair workshops and ordinary rural roads |
| North hamlet | 4 | Three cottages and a workshop on a connecting country lane |
| South hamlet | 4 | Three cottages and a workshop on a connecting country lane |
| West farm | 2 | Farmhouse, accessible storage barn, field strips and fencing |
| East farm | 2 | Farmhouse, accessible storage barn, field strips and fencing |

Working names and placements are editable implementation choices. They do not establish a real geographic location or new story canon.

The seven original building variants use stone, timber, pale render, sage paint and dark metal roofs. Cottages have a living/kitchen area and a connected rear bedroom/study. Shops, workshops and barns have furnished open work/storage space. Roof space is part of the room, with no inaccessible upper storey. Door leaves are fixed open; interactive door mechanics are not implemented. Entrances are 1.8m clear, or 2.8m for barns. Broad approaches connect the porch floors to the terrain.

Each building has an ID, V01–V28. Two `FutureClueAnchor` target points per building identify potential discovery positions. They are editor metadata, not visible treasure, implemented puzzles, rewards, saved progress or unlock mechanics.

## Editable sources

- `SourceAssets/ValleySettlements/Valley-Settlements.blend`: separate KIT and LAYOUT scenes, linked mesh instances and building IDs.
- `SourceAssets/ValleySettlements/layout.json`: metre-based positions, entrances, rear-room test destinations and clue anchors. JSON coordinates use Unreal's world orientation; Blender placement negates Y.
- `Scripts/make_valley_settlements.py`: complete original geometry generator.
- `Scripts/organize_valley_blend.py`: organises the completed source into editable scenes.
- `Scripts/apply_valley_settlements.py`: scoped Unreal import/replacement with map backup, foliage clearance and navigation rebuilding. Run only in the active RobotVR map.
- `Scripts/inspect_valley_settlements.py`: standalone runtime entrance-to-rear-room collision traversal and review screenshots.
- `Scripts/check_valley_approaches.py`: full navigation paths from outside the ramps into every rear room.

Unreal content lives in `/Game/Conservatory/Environment/ValleySettlements`; level actors are under `03 Village/Valley settlements` and tagged `ValleySettlements`.

This is a playable environment foundation with original working assets. Photoreal material refinement, additional interior storytelling props and the mystery systems remain future work. Check the separate import/runtime evidence for verified results; generation alone is not proof of successful integration.

## Integration and approach correction

Imported and saved in `L_Exterior_RobotVR`. Replaced the old cottage actors, bell tower and previous town pass; retained a pair of abandoned vehicles and placed street furnishings. Cleared 360 foliage instances from building sites, roads and fields. The 129 protected habitat/lift/robot actors kept their transforms, including all 11 robots. The map backup is recorded in `ValleySettlementsImport.json`.

Initial door-to-rear-room collision tests passed for all 28 buildings. A broader navigation check found five disconnected approaches: some ramp polygons faced downward. Corrected their orientation, kept ramps above the terrain, added sloped gravel shoulders and solid porch foundations, then rebuilt navigation. All 28 exterior-to-interior navigation paths pass in `ValleyApproachNavigation.json`. Interior fill lights now use 80 lumens with shadows, replacing the overly bright initial values.

Final verification: all 28 full terrain-to-rear-room walks passed with collision enabled, including the approaches and internal doorways; all 28 runtime navigation queries passed. See `ValleySettlementsRuntime.json`. Inspected final town overview, street, cottage interior, north hamlet and west farm screenshots. The windowed test exited automatically with code 0. These checks validate access, not a completed treasure-hunt system or final art approval.
