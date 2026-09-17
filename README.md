# Conservatory

**Current habitat — 10 September 2026:** the default Unreal map now uses the approved five-dome conservatory, with seven pillar positions per walkway side and fitted terrain. The existing lift and other gameplay objects are retained. All four walkway traversals and the lift round trip passed. See [Core habitat](Documentation/CoreHabitat.md). Older modular-layout descriptions below are historical.


Robot VR is now playable in the downstairs kitchen: use **Try Robot VR.cmd** to start at the wall monitor. **R1–R11** previews robot cameras while facing the wall monitor; **F** inspects the monitor or wears a numbered suit; **WASD/mouse** controls that outdoor robot; **R** returns indoors. See [Robot VR](Documentation/RobotVR.md).


Current robot scene (10 September 2026): ten Manny robots roam the walkable terrain with corrected locomotion; unit 11 stands on a charging dock beside the upper lift. See [Terrain robots](Documentation/TerrainRobots.md) and [next-session suit/VR direction](Documentation/FutureGameplay.md).





Unreal Engine **5.8.2**, Windows / DirectX 12. Use **Walk Around.cmd** for the game or **Open Editor.cmd** for editing. The default level is now **/Game/Conservatory/Maps/L_Exterior_C17_Ready**. Earlier Sealed, Library and original levels remain as snapshots.



## Current architecture



The two large domes and short connector now derive from **Reference images/Conservatory-MASTER.blend**. The original reference is unchanged. The master supplies the 16-sector decorative frame and cupola. Added glazing, floors and open connection bays make it walkable in Unreal.



The passage is **4.68 m long**, with approximately **4.08 m clear width**. It meets the lower arches below the dome eaves. The starter occupies approximately 53 x 25 m on the existing hill-edge terrace. The complete frame is detailed planning geometry; optimisation for many player-built copies remains future work.



See **Documentation/ModularMaster.md**, **MasterSockets.json** and **ModularPlacement.json** for dimensions and attachment conventions. The derived editable Blender file is **SourceAssets/ModularMaster/Conservatory-GameModules.blend**.



## Explore



You start in the connecting passage. The **service lift is inside the north dome**, to the left as you walk north through the passage. Enter the teal cabin and press **E**. E in the bunker cabin returns upstairs. The spiral staircase at the north end of the bunker connects its two floors.



| Input | Action |

| --- | --- |

| WASD / mouse | Walk / look |

| Shift / Space | Faster movement / jump |

| E inside lift | Travel |

| Home | Return to the conservatory passage |

| Escape in editor | Stop Play |

| Escape in game window | Close game and return to desktop (also works in panels and robot mode) |

| Shift + F1 in editor | Release mouse |

| Alt + F4 in game window | Close game |



The bunker has twelve furnished rooms: seed lab, study, sleeping quarters, food storage, clinic, kitchen/washrooms, water/pumping, oxygen/air filtration, batteries, workshop, waste treatment and stores. Solid room joins and a stair landing close the earlier circulation gaps. The lift is a fade transfer, with no excavated surface shaft.



The wooded hill, abandoned village, low valley fog and clear terrace balustrade remain. Village cottages are exterior set pieces. Owned Epic library foliage retains its licence; see Documentation/LibraryFoliage.md. The Poly Haven forest-floor texture is CC0; see SourceAssets/Textures/CREDITS.md.



## Organisation and regeneration



The current level also includes the front terrace rockface and the town's sudden-interruption pass: paved streets, a gas station, six abandoned cars, and a damaged shopfront. The town is deliberately free of overgrowth. See `Documentation/TerraceRockface.md` and `Documentation/TownToday.md` for editable Blender sources, backups, runtime views, and the scripts to reapply these layers after broader regeneration. `STYLING.md` is the persistent visual reference.



Content/Conservatory contains the maps, environment, architecture and bunker materials. Content/Medieval_Environment preserves vendor foliage paths. Source/Conservatory contains walking; Source/Habitat contains the lift; Source/ConservatoryEditor contains authoring helpers.



Save a separate map before regenerating hand edits. The complete authoring order is:



1. Build ConservatoryEditor Win64 Development.

2. Original source generation/import as needed: make_conservatory.py in Blender, then build_exterior.py in Unreal.

3. upgrade_library_foliage.py, position_conservatory.py and build_bunker.py in Unreal.

4. Load the supplied MASTER in background Blender and run derive_master_modules.py.

5. Run apply_master_modules.py in Unreal to apply the current architecture and relocate the upper lift.



Unreal commandlet pattern: UnrealEditor-Cmd.exe FULL_PROJECT_PATH -run=pythonscript -script="FULL/FORWARD/SLASH/PATH/Scripts/apply_master_modules.py" -unattended. Regeneration replaces the relevant generated actors. The standalone seal_bunker_joints.py updates only the structural joins.



## Validation and scope



The opt-in -game -ModularInspection test walks through both dome connections, captures views and checks the lift round trip. Results: Documentation/ModularWalkTest.json. Other opt-in scripts cover the bunker, landing and exterior. Normal launches do not run them.



No resource consumption, seed inventory, robot control, player construction or sealing simulation is implemented. These remain design work. The project is playable through the installed engine; it has not been cooked into a redistributable package.



The service lift now has an ornate brass-and-glass enclosure against the north dome's inland facade, with a matching low-roof bunker cabin. See Documentation/OrnateLift.md and OrnateLift.json. Run apply_ornate_lift.py after the master-module pass when regenerating. The source Blender workbench is SourceAssets/OrnateLift/Ornate-Service-Lift.blend.



## CIDCORE intercom



Press **C** to sign in and speak to CIDCORE. Replies appear as subtitles; voice is optional. Sessions are held in memory. See **Documentation/CIDCORE.md** for scope, bench setup and validation. The current email-only server login requires hardening before public release.





Physical CIDCORE panels now serve every bunker room and the shared indoor areas. Approach, face the panel and press **F**; **C** still works everywhere. See **Documentation/PhysicalIntercoms.md**.







## C-17 field robot



Two rigged C-17 preview units patrol outside the glass. Seven starter animations cover walking, carrying, lifting, shelf pickup, chopping and stone breaking. Editable Blender rigs and Unreal skeletal assets are included. A single computer workstation replaces two spare washroom cubicles; remote control and resource collection are the next stage. See **Documentation/C17/README.md**.



