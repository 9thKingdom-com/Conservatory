# Physical CIDCORE intercoms

21 brass-and-enamel stations serve all twelve bunker rooms, both domes, the connecting passage, both corridors, both lobbies and both stair landings. Outdoor stations have been removed. The north-dome station is offset 2.3 metres sideways from the lift entrance.

Approach a panel, face it and press **F**. This opens the same CIDCORE session as **C**, which remains available anywhere. Stations require a clear line of sight and a distance under 2.2 metres, so they cannot be operated through walls. **E** still operates the lift. The physical amber lamp follows the shared pending-request state and goes dark when idle or on failure.

Room panels sit on the room-facing side of the entry wall beside the doorway. Open areas use pedestal stations. The meshes are reusable C++ actor components; the current map placements and materials are saved as assets. No additional API calls or new sessions occur from approaching a station.

Regenerate with Scripts/place_intercoms.py after architecture passes. The script replaces only the `09 CIDCORE Intercoms` folder. Placement coordinates are recorded in IntercomStations.json. The pre-install map backup is Saved/Backups/L_Exterior_Modular_before_intercoms.umap.

Validation: ConservatoryEditor Win64 Development builds successfully. Run the game with -IntercomInspection for local reachability checks and room/dome screenshots. This inspection does not log in or send messages.

Before the outdoor removal and lift clearance adjustment, all 28 stations passed the in-game interaction check: opened from a nearby facing position and rejected interaction from 4 metres away. Results: IntercomStationTest.json. Material defaults are assigned by the reusable actor so they survive map reloads.


