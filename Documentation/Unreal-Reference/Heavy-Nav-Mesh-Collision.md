# Heavy navigation mesh collision fix

**Status:** Tested in UE 5.8.2 on 17 September 2026. Fixes navigation collision exports on two heavy static meshes in `L_Exterior_RobotVR` without changing visual geometry.

## Purpose

UE can warn when navigation uses a high-triangle static mesh as collision:

```text
Exporting collision geometry with too many triangles (NNNNNN).
Add a simple collision or change GeometryExportVertexCountWarningThreshold.
```

This is not just a warning to suppress; it means the navigation build is paying for a full visual mesh. Use this recipe when the warning points to a large `StaticMeshActor` that should still block navigation but does not need full-mesh collision.

## Tested workflow

1. Identify the offending actors from the Unreal log (`Navigation: Warning: Exporting collision geometry...`).
2. Load the map headlessly with `-nullrhi` and inspect the target `StaticMeshActor` labels and mesh paths.
3. Use `StaticMeshEditorSubsystem` to inspect the asset:
   - `get_collision_complexity()`
   - `get_simple_collision_count()`
   - `get_convex_collision_count()`
4. If the mesh is `CTF_USE_COMPLEX_AS_SIMPLE` and has high triangle/vertex counts, add a simple collision shape with `add_simple_collisions()` (tested with `ScriptCollisionShapeType.NDOP26`).
5. Set the mesh's `body_setup.collision_trace_flag` to `CTF_USE_SIMPLE_AS_COMPLEX`.
6. Save the static mesh.
7. Reload the production map and confirm the navigation warning is gone.

## Evidence - 17 September 2026

- `SM_TreeMaster_Structure`:
  - Before: `CTF_USE_COMPLEX_AS_SIMPLE`, 634,862 triangles, 0 simple/convex collision shapes.
  - After: `CTF_USE_SIMPLE_AS_COMPLEX`, 1 convex collision shape.
- `SM_LiftMaster_Solid`:
  - Before: `CTF_USE_COMPLEX_AS_SIMPLE`, 502,834 triangles, 1 convex collision shape.
  - After: `CTF_USE_SIMPLE_AS_COMPLEX`, 2 convex collision shapes.
- Map reload after the asset changes:
  - `L_Exterior_RobotVR` loaded cleanly.
  - Actor count remained 1,865.
  - Both target actors remained present.
  - No navigation collision-export warnings remained.
- Backups: `Saved/Backups/HeavyNavMeshFix/20260917-1140`.
- Reports:
  - `Documentation/HeavyNavMeshInspect.json`
  - `Documentation/HeavyNavMeshFixResult.json`
  - `Documentation/HeavyNavMeshLiftSimpleCollision.json`
  - `Documentation/HeavyNavMeshMapLoadAfterFix.json`

## Limitations

- This reduces navigation collision export, not the visual triangle count.
- It does not replace a gameplay/robot pathing test; a clean map load was verified, not a full play session.
- It does not address unrelated heavy meshes or general scene optimisation.
- The added collision shapes are simple convex approximations; if robot access changes, compare the path behaviour before continuing.

## When not to use

Do not use this to remove an object from navigation if the object is supposed to block movement. Keep the actor or add an explicit nav obstacle/volume if needed.
## Gameplay robot test - 17 September 2026
A 40-second standalone robot test on `L_Exterior_RobotVR` passed after the collision change: all 11 robots were seen, all 10 outdoor robots moved more than 50 m, robot 11 stayed docked, and all 1,903 sampled robot states were grounded. No map content was changed. Evidence: `Documentation/HeavyNavMeshRuntime.json` and `Documentation/HeavyNavMeshRuntime.png`. The reusable test is `Scripts/verify_heavy_nav_mesh_runtime.py`, launched by `Scripts/run_heavy_nav_mesh_runtime.ps1`.
