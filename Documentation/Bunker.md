# Underground habitat

The bunker lies beneath the hill, west of the conservatory. Twelve rooms flank a central corridor across two floors. A service-lift lobby occupies the south end and a spiral stair the north. Exact coordinates are in BunkerLayout.json.

The habitat floor is at Z=4000 cm and utilities at Z=3400 cm. Rooms are 12 x 14 m with approximately 3.5 m clear height and 2.6 m wide open doorways. The stair has 49 overlapping radial treads, 12.5 cm rise, a 540-degree turn, 4 m vertical separation per revolution, a central column, outer handrail and upper gallery.

## Habitat

Seed laboratory: seven drawer archives, workbenches, sample trays, vials and displays. Library: reference shelves, desks, chairs and journals. Sleeping room: four double bunks and lockers. Food reserve: sealed crates on shelving. Clinic: examination couches, monitors, storage and first-aid cabinet. Kitchen and washrooms: preparation counters, hobs, dining surface and screened sanitary fixtures.

## Utilities

Water room: three reservoirs, pumps, pipework and gauges. Air room: six oxygen cylinders and two filter cabinets. Power room: battery cabinets and inverters. Workshop: benches, tools and storage. Waste room: sealed treatment vessels, greywater return and segregated bins. Equipment store: additional shelf capacity.

## Implementation

Scripts/build_bunker.py creates editable actors under 08 Bunker. Props use engine primitives and shared materials. Teal marks habitat fittings; amber marks circulation and utilities. Lighting is dynamic. This is an initial architectural art pass.

Source/Habitat contains AServiceLift. Stations expose destination position, facing and label. E is accepted within 230 cm of the cabin station; travel fades out, transfers the player, clears velocity and fades in. A cooldown prevents repeat activation during transfer. The prototype has no moving lift car or excavated shaft through the Landscape. Home returns to the conservatory through the upper station's runtime handler.

Resource gauges and archive contents are representative scenery. Maintenance, seed inventory, oxygen consumption, water quality, waste processing and power simulation remain future work.

The upper stair now has a 2.66 m wide flush landing joining the first tread to the corridor gallery. The south railing opens onto this crossing; a side guard protects the remaining void. The previous floating guidance stripe has been replaced by one on the landing. Regeneration preserves this change in build_bunker.py.

The active map is now L_Exterior_Sealed. L_Exterior_Library was retained because the open editor held its file locked. Twelve full-depth structural joins seal the one-metre room-spacing gaps, including the lobby connections, on both decks. A lower-hall ceiling closes the overhead void. seal_bunker_joints.py applies this pass without replacing other actors; build_bunker.py also calls it during regeneration.
