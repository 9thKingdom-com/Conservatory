# Master-derived modular conservatory

Update, 9 September 2026: the active `L_Exterior_C17_Ready` level uses the detailed connector described in `PassageDetail.md`, with unchanged socket datums. The older generator below still produces the earlier passage, so run `apply_passage_detail.py` afterwards when rebuilding.

The current architecture is derived from the user's Reference images/Conservatory-MASTER.blend. That reference is unchanged. The editable derivative is SourceAssets/ModularMaster/Conservatory-GameModules.blend; FBX exports sit beside it.

The starter remains two large domes joined by one short passage. It now uses the master's 16-sector radius-8 m dome, detailed columns, arches, ribs and seated cupola. The passage meets an open lower wall bay, beneath the eaves, instead of intersecting the curved roof.

## Connection standard

| Dimension | Native metres | At game scale 1.5 |
| --- | --- | --- |
| Passage length | 3.121445 | 4.682168 |
| Column-centre width | 3.121445 | 4.682168 |
| Clear arch width | 2.721445 | 4.082168 |
| Floor datum | 0.61 | World Z 62.4275 |
| Dome radius | 8 | 12 |
| Arch spring above origin | 4.35 | 6.525 |

Both meshes have Attach_PositiveX and Attach_NegativeX sockets. Snap opposing socket positions together and rotate their forward axes to face one another. MasterSockets.json records the native datums. The two dome centres are at Y +/-1411.0507 cm, with X=-10600 cm. This reduces the complete starter footprint to approximately 53 x 25 m, leaving more terrace for later additions.

The current dome preset opens the two opposite axial bays. The decorative window infill is omitted there and glass fills the space above the passage arch. Other bays remain glazed. Side branching will need an additional open-bay preset; socket snapping alone does not remove closed wall geometry. Player construction, resource costs and sealing behaviour remain future mechanics.

## Files and regeneration

- derive_master_modules.py: run Blender in background with the reference blend loaded; explicitly bakes all 16 sectors, adds glazing/floors and exports the game meshes. It saves a separate editable derivative.
- apply_master_modules.py: imports the derived meshes, assigns materials, adds sockets and places the two domes and short connector. Preserves landscape, terrace and bunker. Moves the upper service-lift cabin into the north dome.
- Run this pass after the original environment, terrace and bunker generators when rebuilding the complete site.
- Current map: L_Exterior_Modular. Earlier Sealed and Library levels remain as snapshots.

The master retains its procedural source scenes. The game exports are baked meshes for this planning pass. Detailed frame geometry is relatively heavy and should receive a dedicated collision/LOD optimisation pass before a player can build many copies.
