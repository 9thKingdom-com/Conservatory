# Mesh Partition removal and safe plugin disabling

**Status:** Tested in UE 5.8.2 on 16 September 2026. John decided he does not use Mesh Terrain/Mesh Partition, so all of its content was removed from the production map and the plugin suite was disabled.

## Critical pitfall discovered (binding for future plugin changes)

Disabling a plugin whose classes appear in **saved map actors** makes UE 5.8 fatal-error at startup, before the editor opens:

`WorldPartitionActorDesc.cpp [Line: 334] Missing custom version for actor descriptor '<external actor package>'`

World Partition reads each external actor's descriptor (embedded in its package) at startup; if the descriptor was serialized with a custom version owned by a plugin that is no longer loaded, the check is fatal - not a warning. On 16 September John disabled `MeshPartition` from the Plugins browser while four orphaned partition section actors were still in `L_Exterior_RobotVR`, and the next project start crashed exactly this way. **Rule: remove or re-save all actors that depend on a plugin before disabling it, then verify a plugin-off start.**

## Tested workflow

1. **Back up first**: map, both HLOD layer assets, all `__ExternalActors__`/`__ExternalObjects__` packages, `.uproject` and config (see `Saved/Backups/MeshPartitionRemoval/20260916-110827`).
2. **Discover** (read-only): `Scripts/remove_mesh_partition_discovery.py` scans the Asset Registry plus all loaded actors for MeshPartition/MegaMesh classes. The flat test partition was `MeshPartition_UAID_..._1522962665` at the origin with four ~500k-triangle sections; its PIE cost was ~43-45 s every Play.
3. **Remove the partition actor** with the plugin still enabled: `Scripts/remove_mesh_partition.py` (keep-transform snapshot, destroy, save, reload, re-verify). It also deletes the orphaned external package and re-saves.
4. **Remove the orphaned section/provider actors** while the plugin is still enabled: `Scripts/remove_mesh_partition_providers.py`. They were generic `Actor`s named `Section_X0-Y0_0/X1-Y0_0/X0-Y1_0/X1-Y1_0` sharing the partition's UAID prefix, stored in `2/GB/RAF50C2...`, `3/YZ/OG8YS4...`, `4/ZZ/N2EQUKJ...`, `C/4J/12AWEI...` (the 3.7 MB package carried the baked section data). Cross-check deletion against these known package paths.
5. **Only then disable the plugins** in `Conservatory.uproject`: MeshPartition, MeshTerrainMode, PCGMeshPartitionInterop, PCGPrimitives_MeshPartitionInterop, FastGeoStreaming (all Epic experimental; MegaMesh is internal to MeshPartition, not a separate plugin).
6. **Verify a plugin-off start**: `Scripts/verify_mesh_partition_removal.py` loads the map headlessly with everything disabled - actor count matches, zero plugin-class actors, and the log must contain no `Missing custom version`, `uses an unknown` or `Fatal` lines.
7. **Play test**: `Scripts/run_mesh_partition_runtime.ps1` launches a bounded windowed game, samples the wandering robots, captures a screenshot and self-quits.

## Evidence (16 September 2026)

- Map actors: 1845 -> 1844 after partition removal -> 1846 after John's own six new actors (kept, transforms verified) -> 1846 final; external actor packages 1850 -> 1846.
- Plugin-off start: 1,846 actors, zero MeshPartition/MegaMesh, clean log, plugin not mounted.
- Windowed play test: 40 s clean run, exit 0, robots 1/2 wandered 75-78 m, docked robot 11 unmoved, screenshot `Documentation/MeshPartitionFix-Runtime.png`.
- Startup crash before the fix: `Conservatory.log` 12:06 PM fatal on `2/GB/RAF50C2...`; after the fix the same launch path is clean.

## Limitations

- PIE still duplicates the editor's fully loaded region; use a smaller loaded region or the standalone launcher when measuring.
- The 2 navmesh over-triangle warnings, robot always-tick pose and synchronous wander path-finds from the performance diagnosis remain content/code candidates needing John's approval.
