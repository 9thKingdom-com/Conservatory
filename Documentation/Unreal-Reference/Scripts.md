# Reusable script shelf

Paths below are relative to the project root. Read the script before execution: this is an index, not an instruction to run every step.

| Script | Purpose | Mutation scope |
|---|---|---|
| Scripts/make_landscape_paint_masks.py | Generate road/field masks from settlement layout | SourceAssets/LandscapePaintStudy outputs |
| Scripts/prepare_landscape_study.py | Build native-layer material and prepare study | Study map and material |
| Scripts/paint_landscape_study.py | Import native weightmaps and save | Study map and Layer Info assets; C++ helper rejects other maps |
| Scripts/run_landscape_review.ps1 | Reopen saved study, capture town/farm, exit | Review images/logs; launches a windowed game |
| Scripts/make_study_foundations.py | Export infrastructure without main road/soil sheets | Derivative FBX; preserves original Blender source |
| Scripts/inspect_valley_settlements.py | Traverse each interior and capture review views | Runtime inspection and reports |
| Scripts/run_valley_test.ps1 | Launch bounded windowed settlement test | Runtime inspection and reports |
| Scripts/rebuild_valley_infrastructure.py | Rebuild settlement infrastructure | Inspect current implementation and import sequence before reuse |
| Scripts/make_gameplay_actors_always_loaded.py, Scripts/make_terrain_always_loaded.py | Set Is Spatially Loaded=false on gameplay/terrain actors | Production map actor packages; back up first |
| Scripts/verify_robot_streaming_fix.py, Scripts/run_diagnose_suit_interactions.ps1 | Full 11-suit wear/return plus far-robot long-hold runtime test, or suit sightline diagnostics | Runtime reports; no map writes |
| Scripts/remove_mesh_partition.py, Scripts/remove_mesh_partition_providers.py | Remove Mesh Partition content from the production map | Production map external actor packages; back up first |
| Scripts/verify_mesh_partition_removal.py, Scripts/run_mesh_partition_runtime.ps1 | Verify plugin-off map load and bounded windowed play | Read-only reports and screenshot |
| Scripts/finish_control_room_drawers.py | Apply the walnut/brass review finish and regenerate the cabinet FBX/UCX package | Validates the exact drawer source file; changes that Blender file and replaces its GameReady outputs |

Editor helper: Source/ConservatoryEditor/ExteriorTools.cpp. Its navigation build, terrain creation, instance creation and study paint operations have different side effects; call only the function needed for the current task.
| `Scripts/verify_heavy_nav_mesh_runtime.py`, `Scripts/run_heavy_nav_mesh_runtime.ps1` | Bounded standalone robot runtime test after heavy nav mesh collision changes | Runtime reports and screenshot; no map writes |
