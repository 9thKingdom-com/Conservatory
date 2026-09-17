# Reddish-grey mountain rock paint — UE 5.8.2, 14 September 2026

John requested a rock material for his own peak painting. Session start: live L_Exterior_RobotVR showed All Saved, current map timestamp 11:48:30, newer terrain than robot repair. Closed saved editor normally for editor-helper compilation. Scoped baseline: see ReddishGreyRockBackup.txt; backup contains current map, M_Ground and previous editor helper sources.

## Ready to paint
Landscape Mode > Paint > ReddishGreyRock. Layer Info is already assigned with No Weight Blending (UE 5.8 Blend Method None). Brush strength .3 and falloff .5 are the current UI settings. Paint builds the rock overlay over existing ground; Shift while painting removes this independent overlay. Peaks are intentionally unpainted in the delivered map.

Assets in /Game/Conservatory/Environment/MountainRock:
- M_MountainLandscape: duplicate of current M_Ground with ReddishGreyRock layer blends for colour, normal and roughness. Other original outputs retained.
- LI_ReddishGreyRock: independent native Landscape paint layer.
- M_ReddishGreyRock: standalone material for rock meshes, sharing the generated rock graph.

RockGrey, RockOxide, RockRedAmount, RockScale, RockRelief and RockRoughness are exposed material parameters. Defaults: grey with subdued reddish oxide variation, scale 1, relief 1.8, roughness .88. Source shader SourceAssets/ReddishGreyRock.hlsl uses world-space procedural mineral patches, grain and fissures with derivative-based surface relief. No third-party textures, displacement, height sculpting or physical collision changes. This is an initial procedural surface for John's review, not a photogrammetry asset or a final approved art benchmark. Fine procedural detail can alias at distance; production performance and filtering have not been benchmarked.

Implementation: Scripts/create_reddish_grey_rock.py (initial setup; expects original M_Ground and must not be rerun over later painting). C++ RegisterReddishGreyRockLayer restricts itself to L_Exterior_RobotVR and a single Landscape, registers only this layer, and does not write height/weight data. The Layer Info was duplicated from LI_Soil and renamed/reconfigured before assignment; no study map was changed. MaterialExpressionTransform uses the empty input pin name in this engine, not Input.

## Verification
Editor helper build passed. Saved map reopened in UE with correct material and assigned named Paint target; all 2,023 actor transforms preserved. UI brush stroke caused layer allocation/compilation; subtle short stroke was undone. A temporary Fill Layer preview showed the fully rendered grey/rust rock across curved mountain terrain; this was also undone. Final UI confirmed original ground restored, All Saved, ReddishGreyRock selected in Paint mode. No preview weight painting was saved. No material compilation errors found. Navigation auto-rebuilt during UI preview and reported completion; no gameplay changes requested or tests rerun. Material setup report: ReddishGreyRock.json.
