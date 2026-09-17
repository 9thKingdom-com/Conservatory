# LIFT-MASTER

**12 September 2026 update:** John finished editing this master and authorised its Unreal replacement. Latest live source snapshot (425 renderable asset objects) is integrated into the upper conservatory lift in L_Exterior_RobotVR; Blender source remains untouched. Final walking entry, down/up travel and exit verified. Exported meshes and source-view image are in UnrealExport. See Documentation/Unreal-Reference/Finished-Lift-Import.md in the project for checkpoint locations and rendering/material limitations. Historical initial-build counts below are superseded by the new export report.

Editable Blender master for the 9th Kingdom service lift, authored 12 September 2026 in Blender 5.1.1 from John's supplied lift1-reference.png. John requested a new Blender build named LIFT-MASTER in Asset Chest, with refinement visible live in Blender.

Open **LIFT-MASTER.blend**. The supplied image is packed into the file. Asset components are organised into structure, columns, cast ornament, glazing, interior, controls/signage, crown and game anchors. Studio cameras/lights and the reference are separate collections. Blender materials include bottle-green enamel, aged brass, polished trim, ivory, glass and limestone. Text remains editable.

Dimensions: approximately 2.68 m wide, 2.44 m deep, 4.78 m from base underside to finial. Clear entry about 1.515 m wide and 2.657 m tall. Metres, front -Y, origin at floor base; finished cabin floor +0.08 m. The rear, depth and hidden construction are interpretations of the single front reference.

This is the detailed source master, not an optimised runtime prefab. 563 asset objects; approximately 453k evaluated triangles including curve bevels and lettering. Meshes have initial metric planar UVs; material textures are procedural. Packed reference, independent panes, editable ornament curves, separate control components and named interaction/arrival/door anchors are included. No imported third-party meshes or downloaded texture packs used. No claim about rights to resell the supplied reference image.

Geometry check: zero degenerate base-mesh faces and zero inward closed solids after correcting 42 scroll ribbons. Hero and interior renders used for visual review. Meshes/curves and modifiers remain editable. Production UV/baking, collision, LODs, door animation, shaft engineering and Unreal integration are later steps. This build does not alter the current Unreal lift or map.

The saved .blend is authoritative over the initial build scripts, which do not include every live adjustment. Prior saved version is retained as .blend1. MasterReport.json records geometry checks. Authoring scripts are in the project's Scripts folder: build_lift_master.py and refine_lift_master_live.py. They are not safe general-purpose regeneration commands for a manually edited master.
