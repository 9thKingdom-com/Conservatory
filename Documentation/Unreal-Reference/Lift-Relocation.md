# Relocate a service lift after manual map edits

Tested UE 5.8.2, 12 September 2026. Session completed at 12:43 Europe/Warsaw.

The upper ornate enclosure, plaque and light had followed John's 45.230-degree habitat rotation and translation; ServiceLift_0 and the downstairs station's Destination retained their old coordinates. AServiceLift uses a 230 cm pawn-to-station distance check, not a separate collision trigger volume. Moving the visible mesh alone does not move that interaction location. Destination is a stored world-space vector; update the opposite station when relocating an endpoint. Set its DestinationYaw to face through the new entrance.

Worked directly from John's L_Exterior_RobotVR saved at 11:24:46 on 12 September. The editor exited cleanly during initial inspection; no live editor was reloaded or overwritten. No Git repository exists. Latest map and two johnmaster generated assets were the changed disk candidates. Backed up the saved map and johnmaster dependencies to Saved/Backups/LiftManual/20260912-124130. No external actor packages were changed.

Upper enclosure is now centred on the large dome's west-facing wall, between the two corridor directions, with its entrance facing inward. Upper station: (-15838.309, -1384.282, 6336) cm; yaw 0.230 degrees. Changed only upper enclosure/plaque/light/station transforms and lower return Destination/DestinationYaw. Retained all 2182 actors and the single Landscape; unrelated actor transforms checked unchanged. No landscape, foliage, settlement, dock, mesh or material edits. Saved original map path.

Runtime reopened the saved map: walked into the lift, called the actual Travel function within 69 cm of the interaction point, arrived downstairs, returned upstairs, and walked 509 cm out onto the floor. All passed. Screenshot visually inspected: centred enclosure, open entrance and wall clearance. This exercises the same travel/proximity path used by E; a physical E keypress was not tested. Review process exited normally. No editor remains open with unresolved unsaved changes.

Evidence: ../LiftManualBaseline.json, ../LiftManualRepair.json, ../LiftManualRuntime.json and ../LiftManualView.png. Scripts: Scripts/audit_lift_manual.py, repair_lift_manual.py and test_lift_manual.py. Repair script is specific to this recorded baseline, not a general generator; inspect current map state before reuse. Existing navigation-origin warning predates repair; navigation was not rebuilt for this player-lift fix.
