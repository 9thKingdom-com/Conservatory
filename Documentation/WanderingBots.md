# Wandering mannequin bots â€” 10 September 2026

User direction: replace the custom robot presentation with Unreal's standard character, with ten wandering bots outdoors and one indoors. They remain robots in the setting.

Map: `/Game/Conservatory/Maps/L_Exterior_WanderingBots`. The previous `L_Exterior_C17_Ready` scene and custom robot source assets are preserved. Existing robot actors are reused where possible to preserve workstation references.

Manny Simple, MM_Idle and MM_Walk_InPlace were copied with their mannequin content dependencies from the user's existing `Documents/Unreal Projects/DomeMaster/Content/Characters/Mannequins` assets. These are Epic Unreal mannequin assets. AnimGen Example is installed in UE 5.8, but its civilian walk references SK_UEFN_Mannequin; Manny's matching walk is used without mixing skeletons.

Ten units wander along the east and west exterior terrace strips; one wanders inside the central connecting passage. Movement uses CharacterMovement collision, capsule clearance sweeps, floor probes, individual pauses and random heading choices within local bounds. This is local wandering, not a navigation-mesh route planner. It will turn away from barriers rather than solve long routes around buildings. Bots remain separated from stairs and the sealed entrances.

The existing C17 class retains workstation feeds and collection task interfaces. C17-specific work poses cannot run on Manny; work tasks use a timed idle placeholder until matching work animations are authored. Collection gameplay was not part of this validation.

Placement: `WanderingBots.json`. Runtime results: `WanderingBotsRuntime.json`. Screenshots: `WanderingBotsOutside.png` and `WanderingBotInside.png`. Re-run the inspection with the new map and `-game -WanderingBotsInspection`. This is an implemented gameplay pass, not an approved finished visual benchmark.

Validation completed: UE 5.8 Development Editor build succeeded. Saved-map gameplay contained exactly 11 Manny units. All moved 152–533 cm from their first sampled position over the inspection, stayed within configured bounds, and were grounded in all 2,454 samples per bot. One outdoor bot stepped over a 12.8 cm surface variation (below the 25 cm step limit). Runtime screenshots were inspected. Editor and Walk Around now load this map.
