# Terrain robots â€” 10 September 2026

The ten exterior Manny robots now start around the approach, valley, town and woodland quadrants. They use Unreal's baked Recast navigation across the 1,260 m landscape (with a 10 m border inset), choosing reachable destinations at least 50 m away on their connected walkable surface. Native AI path following handles routes around obstacles; failed or stalled routes are retried. Steep cliffs, blocked surfaces and disconnected areas are not traversable. The eleventh robot is now stationary on a compact charging dock beside the upper lift, following the user’s later instruction.

Active map: `/Game/Conservatory/Maps/L_Exterior_TerrainRobots`. Previous terrace-only map remains available. Placement coordinates and stable robot IDs are in `TerrainRobotsPlacement.json`. IDs 1â€“10 are exterior units; 11 is the indoor unit.

## Sliding correction

Inspection of the prior `MM_Walk_InPlace` found less than 0.02 cm of forward/backward foot travel: it behaves as a marching animation and cannot counteract the character's forward movement. The corrected `A_MannyTerrainWalk` is a project-owned duplicate of Epic's `MM_Walk_Fwd`, with root translation locked. Source root travel is 648 cm in 2.7 seconds, or 240 cm/s. Playback now scales with measured character velocity divided by 240, including acceleration and slowdown, instead of a guessed constant maximum speed. All eleven skeletal meshes continue evaluating poses outside the camera view.

Ground collision and movement are still capsule-based; this pass does not implement terrain-adaptive foot IK. On uneven ground, foot placement can still differ from the ground surface. The change specifically corrects the incorrect marching cycle and playback-speed mismatch.

## Next-session handoff

See `FutureGameplay.md` for the user's suit/VR embodiment and wall-monitor requirements. The existing computer connection remains until that session. Stable IDs are implemented. Autonomous steering yields when a robot is player-possessed, but suit interaction, first-person input/camera, returning to the human, wall map and selectable eye feeds are not implemented in this pass.

## Reproduction

Build `ConservatoryEditor Win64 Development`. `Scripts/setup_terrain_robots.py` creates the animation copy, builds navigation and saves the distributed robot map. The command-line game flag `-TerrainRobotsInspection` runs the opt-in movement and stride inspection on that map and writes `TerrainRobotsRuntime.json` with gameplay screenshots.

## Validation

UE 5.8 Development Editor build passed. The 90-second terrain run passed for all ten exterior robots: approximately 63–153 m displacement, grounded in every sample, and roughly 90 cm of forward/backward foot swing. Median stance drift was 15–18 cm/s at 180 cm/s walking speed, substantially lower than the marching clip. Two units reached destinations and selected new routes during the run. Runtime stride screenshots were inspected. `TerrainRobotsRuntime.json` records that run before the indoor unit was parked; `IndoorRobotDockRuntime.json` covers the final stationary dock and lift access.

The physical dock has steel and green enamel construction, a low non-slip pad, brass contact plates and an identity plaque. Its centre is 2.5 m to the side of the upper lift; the station edge clears the cabin by about 75 cm. It is a visual charging station; battery/charging simulation remains future work.

Final dock validation passed: unit 11 remained grounded with 0 cm drift, all 11 robots were present, and the player walked into the upper lift without obstruction. The dock is on the opposite side from the intercom. The final screenshot was visually reviewed. The new terrain-robot map is now the editor and Walk Around default. After regenerating terrain placements, run `Scripts/park_indoor_robot.py` to restore the final dock placement.
