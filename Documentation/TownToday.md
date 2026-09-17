# Town — sudden interruption pass

User direction, 9 September 2026: make the village read as a real small town, with a road, gas station, a few older cars and localized crash damage, without overgrowth.

The active `L_Exterior_C17_Ready` map now includes a terrain-following two-lane main road, cross street, residential lanes, pavements and markings; a Valley Fuel station with canopy, two pump islands, hoses, service shop and roadside sign; a Valley Stores shop with an open damaged display frontage; and six cars. One car has a compressed front end inside the shop opening, with local debris and short braking marks. Other cars are left at the station and in the roads. Street lamps, benches and bins establish ordinary town infrastructure.

Eighteen original cottages use new derivative meshes with baked facade vines removed. The replaced cottage remains hidden with collision disabled, rather than deleted. The first application removed 2,531 vegetation instances from the town footprint and main-road corridor. Surrounding woodland remains. Valley fog density was reduced from 0.12 to 0.018 to make the town readable; this is a shared atmosphere adjustment, visible from the conservatory as well.

This is a first environment pass with original modeled assets, not an approved final realism benchmark. The station and store are exterior set pieces; cars and pumps are static dressing, not interactive salvage or driving systems.

## Sources and regeneration

- Editable Blender scene: `SourceAssets/TownToday/Town-Today.blend`.
- Unreal assets: `/Game/Conservatory/Environment/TownToday`.
- Actor folder: `03 Village/Town today`; generated actors use tag `TownToday`.
- Source generation: run `Scripts/make_town_today.py` in Blender background mode.
- Apply: run `Scripts/apply_town_today.py` through Unreal's Python commandlet. It reads the default map, makes a dated backup, imports the kit, and replaces its tagged layer.
- The pre-town map backup is `Saved/Backups/TownToday/20260909-092219/L_Exterior_C17_Ready.umap`. Later backups contain subsequent iterations. Original cottage FBX and Unreal assets remain available.

The apply script verifies protected habitat transforms and retention of the 46 rockface actors before saving. `TownToday.json` records the latest application. Normal launches do not run inspection scripts. Use `-game -TownTodayInspection -RenderOffscreen` for the opt-in runtime photographs and road-walking check; the latter writes `TownTodayWalkTest.json`.

## Runtime views

![Town overview](TownTodayOverview.png)

![Gas station](TownTodayFuel.png)

![Shopfront incident](TownTodayCrash.png)

![Street view](TownTodayStreet.png)
