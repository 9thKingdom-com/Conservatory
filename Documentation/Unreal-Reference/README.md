# Unreal Engine quick-reference library

John's 9th Kingdom project Ă‚Â· started 11 September 2026 Ă‚Â· current tested engine: UE 5.8

Use this index before repeating engine setup or troubleshooting. Read the relevant recipe, inspect its script's target map and side effects, then reuse the working approach. These are project-tested techniques, not a claim that every Unreal feature has been mastered.

## Find a technique

Start every Unreal session with the [manual-edit check](Session-Start.md) before modifying or reloading content.

| Task | Start here | Evidence / status |
|---|---|---|
| Import edited Blender lift master | [Finished lift import](Finished-Lift-Import.md) | Final detail view, walking access and round trip verified in UE 5.8.2 |
| Repair lift after moving its enclosure | [Lift relocation](Lift-Relocation.md) | Saved-map walking access and two-way travel tested in UE 5.8.2 |
| Put outdoor robots above edited terrain | [Robot ground repair](Robot-Ground.md) | Height-only placement verified against current Landscape collision, UE 5.8.2 |
| Paint roads and soil into terrain | [Landscape recipe](../Landscape-Paint-Workflow.md) | Native layer import and save/reopen verified in study map; direct brush input and spline grading not verified |
| Enable Mesh Terrain on the production map | [World Partition conversion](World-Partition-Mesh-Terrain.md) | In-place conversion, full-region load and Mesh Terrain Mode verified in UE 5.8.2 |
| Diagnose Play/PIE performance | [Performance diagnosis](Performance-Diagnosis.md) | Log-verified causes; main stall fixed 16 Sept 2026, UE 5.8.2 |
| Fix heavy navigation collision exports | [Heavy nav mesh collision](Heavy-Nav-Mesh-Collision.md) | Two heavy meshes fixed 17 Sept 2026, UE 5.8.2 |
| Keep interactions working under World Partition streaming | [Streaming interactions](World-Partition-Streaming-Interactions.md) | Always-loaded fix, self-healing hub, all 11 suits verified, UE 5.8.2 |
| Remove Mesh Partition and disable the suite | [Mesh Partition removal](MeshPartition-Removal.md) | Actor-safe removal, plugin-off start and play test verified in UE 5.8.2 |
| Prepare the control-room drawer cabinet | [Control-room drawers](Control-Room-Drawers.md) | Walnut/brass Blender finish and FBX/UCX export verified; Unreal import pending |
| Build and import explorable settlements | [Valley settlements](../Valley-Settlements.md) | 28 terrain-to-interior traversal and navigation checks passed at the recorded baseline |
| Diagnose missing pillar faces | [Pitfalls](Pitfalls.md) | [Pillar normals](../PillarNormalsCheck.json), [saved finish](../HabitatFinish.json) |
| Run a short repeatable inspection | [Iteration workflow](Iteration.md) | Windowed Landscape review captured two views and exited normally |
| Preserve five-dome habitat requirements | [Core habitat](../CoreHabitat.md) | Consult [canon](../GAME-CANON.md) and [styling](../../STYLING.md) before changes |
| Find reusable script entry points | [Script shelf](Scripts.md) | Inspect before running; several scripts modify assets |

## Keep it useful

After a useful discovery, update the existing recipe rather than duplicating it. Record the engine version, purpose, shortest reliable steps, affected assets, verification evidence and remaining limitations. Mark techniques **tested**, **researched only**, or **superseded**. A successful import is not proof of visual quality or playability.

Record a failed approach only when its cause or reliable workaround saves future time. Do not turn unexplained automation failures into claims about Unreal itself. Recheck version-dependent APIs when the engine changes. Keep John's decisions in PROJECT-MEMORY.md; keep this library focused on execution.

Next learning candidates, not completed work: Landscape spline grading; finer path boundaries; realistic gravel/soil material detail; foliage exclusion around roads; measured streaming and instance performance.

Tree centrepiece: [Olive positional assembly](Tree-Positional.md) covers the circular Blender planter, separate export and scoped replacement of the old centre oak/planter. This is a positional revision intended for later updates, not finished art.

Mountain rock paint: [Reddish-grey rock](Mountain-Rock-Paint.md) records the production map's independent ReddishGreyRock paint target, preserved base material, temporary UI fill/undo verification and procedural-surface limitations (UE 5.8.2, 14 September 2026).

Relocated VR suits: [Control Room triggers](Control-Room-Triggers.md) covers aim targets, pairing, independent station authorization and physical F/R verification at John's permanent new suit locations (UE 5.8.2, 14 September 2026).

