# World Partition conversion for Mesh Terrain

**Status:** Tested in UE 5.8.2 on 15 September 2026.

## Purpose

Mesh Terrain Mode was already enabled at the plugin level, but the production map `L_Exterior_RobotVR` was a non-partitioned world. Mesh Terrain requires World Partition, so the existing default map was converted in place while retaining its `/Game/Conservatory/Maps/L_Exterior_RobotVR` path.

## Session-start evidence

- Unreal was open on `L_Exterior_RobotVR` and showed **All Saved**.
- The World Partition panel explicitly showed **World Partition is disabled for this map**.
- The live pre-conversion editor baseline showed 1,829 actors.
- The saved map was newer than its autosaves. No source-control repository is present.
- `Conservatory.uproject` already enabled `MeshPartition`, `MeshTerrainMode`, the two PCG interop plugins, and `FastGeoStreaming`; these user changes were preserved.

## Backup

The pre-conversion map, project file, and `DefaultEngine.ini` are stored at:

`Saved/Backups/WorldPartitionConversion/20260915-081600`

The first in-place attempt encountered a map file lock because the live editor still held the map. Its 538 incomplete external-actor packages were moved, not deleted, to `FailedAttempt-ExternalActors` under the same backup directory before retrying.

## Tested workflow

1. Run `WorldPartitionConvertCommandlet` with `-ReportOnly` and `-AllowCommandletRendering` against `/Game/Conservatory/Maps/L_Exterior_RobotVR`.
2. Confirm the report contains zero errors. This map reported existing missing-mip warnings for embedded Landscape heightmaps, but no conversion blocker.
3. Close the saved live editor before the write pass; otherwise the commandlet can fail with `Could not write ... L_Exterior_RobotVR.umap`.
4. Run the same commandlet without `-ReportOnly` to convert in place.
5. Reopen the production map, select its region in the World Partition panel, and use **Load Region From Selection**.
6. Enter Mesh Terrain Mode with `Shift+6`.

## Verified result

- Conversion commandlet completed with 0 errors and 1 unrelated GPU-driver warning.
- The default map path is unchanged, so `EditorStartupMap` and `GameDefaultMap` required no edits.
- The map now uses One File Per Actor: 1,835 external actor packages and 36 external object packages were generated.
- Unreal generated `Content/Conservatory/Maps/L_Exterior_RobotVR.ini` with a 12,800 cm editor cell size and Landscape grid size 4.
- Reopened editor shows the World Partition grid and a loaded region containing all 1,835 actors.
- The original Landscape and five-dome conservatory are visible after loading the region.
- Mesh Terrain Mode opens and exposes Create Rectangle, Import Heightmap, and Draw Spline.
- Editor remained **All Saved** after verification.

## Limitations

- This session verifies conversion, editor reload, region loading, scene visibility, and Mesh Terrain availability. It does not claim a full gameplay regression pass.
- World Partition may initially open with no editable region loaded. Select the desired cells in the World Partition panel and choose **Load Region From Selection** before editing them.
- The conversion splits the Landscape into streaming proxies, so actor/package counts differ from the pre-conversion monolithic map.



## Update, 16 September 2026

John decided to stop using Mesh Terrain entirely. All Mesh Partition content has been removed from L_Exterior_RobotVR and the whole Mesh Partition plugin suite is now disabled in Conservatory.uproject (see [MeshPartition-Removal.md](MeshPartition-Removal.md)). The World Partition conversion itself remains valid and unchanged. A plugin must never be disabled while saved actors still depend on it - UE 5.8 fatal-errors at startup on the actor-descriptor custom-version check.
