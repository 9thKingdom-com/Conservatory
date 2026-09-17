# Three-module starter kit

The reference is the user-supplied `Reference images/conservatory-design1.png`. This starter translates its domed pavilions, glazed corridor, pale metal ribs and brass details into original geometry. It is a basic architectural interpretation, not a reproduction of every detail.

## Dimensions and connections

| Mesh | Local dimensions | Connection |
| --- | --- | --- |
| SM_Conservatory_Corridor | 18 m long, 8 m clear width, 9.2 m roof apex | Open ends at local X = ±9 m |
| SM_Conservatory_Dome | 14.4 m plinth diameter, about 13 m including finial | Wide corridor portal at local X = -5.744 m; exterior inspection entrance on +X |

Unreal uses centimetres. In the current L_Exterior_Sealed map all modules use uniform scale 1.5. The corridor is at (-10600, 0, 6200), yaw 90 degrees. Dome centres are (-10600, +/-2211.6, 6200), with north yaw 90 and south yaw 270. Pitches and rolls are zero. Python placement always uses named rotation arguments. The original L_Exterior retains the smaller inland arrangement.

The native tiled floor is 28.5 cm above the origin; at scale 1.5 its surface is Z=6242.75 cm. The enlarged kit occupies approximately 66 x 21.6 m on a supported 30 x 74 m terrace near the hill edge. The original plateau remains available inland for later expansion. The service-lift cabin is on the west side of the central corridor.

## Editing

Select the individual actors under `06 Conservatory / Modules` in the Outliner to move or duplicate modules. Architectural materials are under `/Game/Conservatory/Architecture/Materials`; the two reusable meshes are under `/Game/Conservatory/Architecture/Meshes`. Source geometry is in `SourceAssets/Conservatory`; the Blender generator is `Scripts/make_conservatory.py`.

The meshes have complex static collision, including floors and glazing, while the authored openings remain unobstructed. Entrances intentionally stay open for the inspection phase. There is no player construction interface, sealing logic, trapping system or survival gameplay yet. The dome/corridor roof connection is a simple overlapping starter junction; a dedicated transition module can replace it during the next architecture pass.


## Superseded starter geometry

The dimensions and placement above describe the earlier generated shell. The current L_Exterior_Modular level uses the supplied Blender master instead: two 16-sector domes with a 4.682 m passage attached below the eaves. See ModularMaster.md and MasterSockets.json for current dimensions and attachment conventions.
