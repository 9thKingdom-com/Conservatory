# World Partition streaming and interaction systems

**Status:** Tested in UE 5.8.2 on 16 September 2026, after John reported the monitor and F-suit possession had stopped working.

## Why it broke (root cause chain)

The 15 September World Partition conversion replaced "every actor always exists in memory" with "actors stream in and out around the player". The robot network was built on the old assumption:

1. `RobotVRHub` registered all robots **once at BeginPlay**. Outdoor robots were outside the streaming range around the player, so they were never registered: the monitor showed them as OFFLINE, typing R1-R11 did nothing, and F at a suit failed because `EnterRobot` could not find the robot.
2. Making the robots always-loaded exposed the second problem: they can wander anywhere, but the **terrain streams** - robots standing on unloaded landscape have no ground collision and fall. One verification run showed a possessed far robot auto-return within 34 ms because it was already below the Z<-5000 safety line.
3. Possessing a far robot moves the streaming centre away from the Control Room, risking the human body being streamed out while the player is remote.

## The permanent fix (no gameplay function changes)

1. **Always-loaded actors** - `Is Spatially Loaded = false` set and saved on 30 actors: the 11 `C17Robot`, 11 `VRSuitStation`, 1 `RobotVRHub`, `RecastNavMesh`, `NavMeshBoundsVolume`, and the 4 `LandscapeStreamingProxy` actors (the main `Landscape` was already non-spatial). The robot network and terrain are permanently resident exactly as they were before the conversion, while the 1,700+ prop actors still stream normally. All 1,867 retained actor transforms were verified identical across every save/reload.
2. **C++ hardening**: `RobotVRHub::RefreshRobots()` re-scans the robot roster every 2 seconds (self-healing if actors ever stream again); `EnterRobot` now marks the human body `SetIsSpatiallyLoaded(false)` - guarded by `CanChangeIsSpatiallyLoadedFlag()` - so the body can never be streamed out while the player is in a robot.
3. **Editor-only trigger wireframes** (John's request): each `VRSuitStation` shows a 210 cm interaction sphere centred 90 cm up (its real proximity point), the hub shows 480 cm, and the drawer cabinet class shows its editable `InteractRange`. No collision, hidden in game, visible in edit mode.

## Verification (all passed)

- Fresh `-game` start: **11/11 robots present and registered; hub SelectRobot R1-R11 all true**.
- **All 11 suits**: CanUse true, WearSuit true, correct robot possessed, robot moved 190-214 cm, ReturnToHuman true, return position error 0.0 cm.
- **Far-robot long-hold**: 6+ seconds possessing robot 8 (~640 m away), stable ground altitude, clean return, human body intact.
- Map load with the rebuilt DLLs: 1,867 actors, all InteractionRange components present, no errors.
- Evidence: `RobotAlwaysLoadedFix.json`, `TerrainAlwaysLoadedFix.json`, `RobotStreamingFix-Runtime.json`, `SuitInteractionDiagnostic.json`, `RobotStreamingFix-EditorLoad.json`. Backup before changes: `Saved/Backups/RobotStreamingFix/20260916-143247`.

## The recurring pattern (for future reference)

John noted this class of failure has happened several times. Each world-structure change has broken an invisible link in a new way: cached actor lists (this time), per-actor reference properties (Sept 13-14 suit relocation), placement assumptions (Sept 10 habitat swap). **Rule: after any world-structure change, re-run the scripted runtime verification** (`Scripts/verify_robot_streaming_fix.py`, `Scripts/verify_control_room.py`) before calling the map healthy.

## Known behaviour pending John's decision

Outdoor robots 1-10 can path into building interiors: the navmesh covers interiors and the wandering bounds constrain X/Y only. During one verification run a wandering robot transiently stood in the Control Room and blocked the suit sightlines (can_use false for nine suits until it moved on). If John wants outdoor robots strictly outdoors, that is a targeted follow-up change to the wander goal selection.
