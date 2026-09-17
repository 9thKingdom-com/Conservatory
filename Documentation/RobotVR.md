# Kitchen security monitor and robot VR suits

Implemented 10 September 2026 in `/Game/Conservatory/Maps/L_Exterior_RobotVR`. The previous terrain-robot map remains available.

The kitchen/washroom room on the main habitat deck now has a large security monitor on its east wall and ten numbered suit/headset racks along its south wall. The old operations desk connection is removed from this map. Cooking counters, the kitchen table, remaining sanitary fixtures and the indoor robot's lift-side charging dock are retained.

## Using it

- `Try Robot VR.cmd` starts the playable scene at the kitchen monitor.
- Stand in front of the wall monitor and type **R1** through **R11** to switch its live eye camera without wearing a suit or pressing Enter. Type the digits within two seconds of R; R10/R11 briefly selects R1 before the final digit selects R10/R11. Top-row and numpad digits work. The feed stays selected while you look at the monitor; walking away resumes the eight-second camera cycle.
- Look at the wall monitor and press **F** to inspect it. **View 01–10** selects a robot's eye feed. Close the monitor to walk to a suit. While unattended, the monitor cycles camera selection every eight seconds.
- Stand in front of a numbered suit, look at it and press **F**. The corresponding outdoor robot becomes the player-controlled character.
- **WASD** moves, **mouse** looks, and **Space** jumps. **R** removes the suit and returns control to the human at the same indoor position and facing direction.
- The robot's AI stops during possession and resumes after return. The human remains inside; the robot stays at its outdoor location. The lift's Home shortcut does not teleport an embodied robot into the habitat.

These are in-game suit interactions using the game's keyboard/mouse controls. Physical HMD tracking and motion-controller support are not part of this implementation.

## Security display

All ten exterior robots have live ID-labelled map markers and coordinate readouts. The terrain-derived map is north-up, covers 1.26 km and marks the habitat and town. The selected robot has a live eye-camera panel using the same eye position as player embodiment. Only the selected feed renders while the room is nearby or a suit is active; all map positions update independently. R11, the lift service robot, is included in the camera network. Type R11 to preview its eyes and task status. Press F at the monitor and click **Take control of R11** to possess it; R returns to the human. The ten existing physical suits remain paired to R1–R10. Active R11 tasks pause during control and resume afterward; interrupted collection re-approaches the reserved resource before restarting work.

## Verification

The UE 5.8 Development Editor build passed. The saved-map integration test exercised all ten physical suit stations: correct robot pairing, movement, stationary human body, return position, eye/feed alignment, and resumed AI movement. Monitor interaction and selection of robot 10 passed; the old terminal count is zero. See `RobotVRRuntime.json`, `RobotVRPlacement.json`, `RobotSecurityDisplay.png`, `KitchenSecurityMonitor.png`, `KitchenVRSuits.png` and `RobotVREyeView.png`.

Run the map with `-game -RobotVRInspection` to repeat the interaction test. `-RobotVRPhotos` captures the physical room. `Scripts/install_robot_vr_room.py` creates the map; `Scripts/finalize_vr_materials.py` saves the cloth material's skeletal-mesh shader usage. Static and runtime screenshots must be distinguished; this pass is not an approved final art benchmark.

R11 update: the Development Editor build and `-R11Inspection` saved-map regression passed, including an assigned task paused during possession and retained when AI control resumes. Results: `R11Runtime.json`. The test creates a transient resource only for that opt-in run.

## Permanent Control Room relocation — 14 September 2026
John moved all eleven suits and the monitor to the former library and renamed it Control Room. This supersedes the kitchen location above. Interaction fixes and verification are in [Control Room triggers](Unreal-Reference/Control-Room-Triggers.md). Approach the intended suit, look at its torso or headset, press F to take control; R returns to the same Control Room standing position. Current map placements preserved. Historical kitchen launch/photo scripts may still target the earlier room and must be reviewed before reuse.
