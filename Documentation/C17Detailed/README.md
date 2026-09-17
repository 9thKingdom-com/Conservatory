# C-17 detailed Blender reference model

Editable file: `SourceAssets/C17Detailed/C17-Detailed-Reference.blend`.

Modeled from all three images supplied in `Downloads/Robot reference images`: front, side, and back. Copies are saved under `SourceAssets/C17Detailed/References` and packed into the Blender file's optional reference collection.

The model has 830 individually named mesh parts, 218,988 base mesh triangles, ten material definitions, and a 34-bone rigid mechanical rig. Collections separate the head, torso and power pack, arms, pelvis, legs, rig, references, and studio. Armour outlines, optics, bolts, joint bearings, fingers, feet, front designation and rear botanical badge are modeled geometry. The Blender file includes procedural material shading and five configured cameras.

The drawings have no measured dimensions. This derivative assumes a body approximately 1.8 m tall, with the antenna reaching approximately 1.91 m; front is -Y and up is +Z. It is a reference-led reconstruction, with interpreted hidden construction and simplified fine surface markings.

User refinement: exposed cables, hydraulic cylinders/piston rods, actuator collars, and hose clamps were removed. Rotary joints, armour, structural spars, grippers, and the radio antenna remain.

Use Pose Mode on `C17_Detailed_Rig` for FK articulation. Every mechanical mesh part is assigned to one bone with full weight. The new rig and proportions are not a drop-in replacement for the existing C17 animation clips. This file does not overwrite or replace the deployed Unreal robot. Retopology/LOD decisions, material baking, animation retargeting, and game import remain a separate integration step.

`Scripts/make_c17_detailed.py` regenerates the workbench and renders. `Scripts/validate_c17_detailed.py` reloads the file, audits rigid weights and packed references, then tests elbow-to-hand motion without saving the test pose. Results are in `Validation.json`.

![Three-quarter model](C17Detailed-Hero.png)

![Front](C17Detailed-Front.png)

![Side](C17Detailed-Side.png)

![Back](C17Detailed-Back.png)


