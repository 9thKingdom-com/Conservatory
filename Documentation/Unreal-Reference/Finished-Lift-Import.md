# Import John's finished lift master

Tested Blender 5.1.1 / Unreal 5.8.2, 12 September 2026. Completed 19:43 Europe/Warsaw.

John explicitly finished LIFT-MASTER in Blender and requested replacing the positional conservatory lift. Used his latest live design, not the original generator. Source has 425 renderable asset objects and revised open ornament, medallions, stiles and spire. Blender was dirty: retained both last-saved and live snapshots in Saved/Backups/LiftMasterIntegration/20260912-192904. Original open Blender master and unsaved state remain untouched; import used live-LIFT-MASTER.blend from that checkpoint. FinishedSource.png in the UnrealExport folder was rendered and inspected.

Unreal was closed. Inspected latest saved L_Exterior_RobotVR, timestamp 13:01:46, and current lift transforms. Checkpoint: Saved/Backups/LiftMasterIntegration/Unreal-20260912-193636/L_Exterior_RobotVR.umap. No map generator ran.

## Saved result

- Original upper mesh actor replaced with SM_LiftMaster_Solid at unchanged position (-15838.309, -1384.282, 6244) cm and yaw 0.230 degrees. Separate glass actor shares that transform. Source front -Y rotated to +X in the derivative, and source floor lowered 6 cm to align the existing landing; source geometry is not rescaled.
- Removed the old duplicate upper text plaque because John's mesh includes lettering. Aligned the existing upper practical light to the new housing. Preserved both ServiceLift actors and their destinations/yaws exactly. Downstairs lift unchanged.
- New mesh/material assets only in /Game/Conservatory/Architecture/LiftMaster. No unrelated actor transforms changed; 2181 actors retained. Landscape, robots, settlements and architecture untouched.
- Source palette, metallic values and roughness recreated in Unreal. Blender procedural material graphs do not transfer via FBX: noise translated to Unreal procedural noise and glass to the previously tested Fresnel transparency material pattern. This is not a pixel-identical Blender shader conversion.

## Export and rendering lessons

Export script: Scripts/export_finished_lift.py, run in an isolated process on the snapshot. Evaluates authored modifiers/curves/text into derivative meshes. Several beveled leaf-tip vertices evaluated to non-finite coordinates; those invalid derivative vertices were discarded, without source edits. Regenerated finite UVs on the export copy; original materials are procedural and have no image texture mappings to preserve. Export log records affected objects: Saved/Logs/FinishedLiftExport.log.

Classify actual polygon material assignments, not object material-slot lists. John's mixed-material edits plus unused glass slots meant an initial solid bucket contained glass, preventing correct Nanite rendering. First runtime screenshot showed lost fine ornament. Final export separates faces and purges unused slots. Reimported via the tested legacy FBX importer with imported normals/tangents and Nanite disabled on this hero mesh. Final meshes: 519940 solid triangles, 6692 glass triangles. Full triangle collision preserves entrance and interior. This is a high-detail integration, not an optimised LOD release.

Scripts/import_finished_lift.py records initial new-asset/map integration; Scripts/reimport_lift_detail.py applies the final mesh import settings. Inspect current assets before reusing either. StaticMeshEditorSubsystem was unavailable in the headless commandlet; use import settings rather than assuming the subsystem exists.

## Verification

Reopened saved map in a bounded windowed game after final reimport. Player walked to within 65.45 cm of upper interaction point, travelled down, returned up, and walked 506.13 cm out onto the dome floor. All checks passed. Runtime screenshot visually inspected: full crest/scrolls/lettering/buttons/floor medallion present, cabin/entrance clear. Test calls the actual Travel function with its proximity guard; physical E-key press not separately tested. Review process exited normally. No Unreal editor was left with unsaved changes.

Evidence: Documentation/LiftMasterSourceAudit.json, LiftMasterIntegration.json, LiftMasterRuntime.json, LiftMasterUnreal.png; source export manifest: Asset Chest/01 John Originals/LIFT-MASTER/UnrealExport/ExportReport.json.
