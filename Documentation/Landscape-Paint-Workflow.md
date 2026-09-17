# Native Landscape surface study — 11 September 2026

John requests roads, paths and crop-bed soil integrated into the Landscape instead of flat sheets above it. This is an isolated experiment in `/Game/Conservatory/Maps/L_LandscapePaintStudy`; the default production map remains `L_Exterior_RobotVR`.

## Workflow learned

1. Give the Landscape a material with named Landscape Layer Sample nodes. This study uses independent Gravel, Asphalt and Soil masks to blend over the existing forest ground. A zero mask leaves the base ground intact.
2. Create corresponding Landscape Layer Info assets and register them as target layers. For these independent overlays, UE 5.8 Blend Method is None. This differs from weight-normalized competing ground layers.
3. Import 8-bit weightmaps at the Landscape vertex resolution, or paint those target layers with a falloff brush in Landscape Paint mode. Smooth softens the mask transitions. Paint changes surface appearance, not elevation.
4. For road grading, Landscape splines can sculpt the terrain and paint a named target layer with width and falloff. A road mesh is optional. Spline grading was researched but is not part of this test.
5. Save the Layer Info assets and map; review again after reopening.

The existing Landscape has 505 × 505 vertices at 2.5 m spacing. This limits fine path edges: narrow wheel ruts and crisp boundaries need higher terrain weightmap density or supplementary detail. Painted soil is a bed surface; actual crops still need three-dimensional plants.

## Reproducible test

- Material: `/Game/Conservatory/Environment/LandscapePaintStudy/M_PaintedValley`.
- Native layer assets: LI_Gravel, LI_Asphalt, LI_Soil in the same folder.
- `Scripts/make_landscape_paint_masks.py` generates feathered masks from the existing settlement layout. Row zero is world Y=-630 m; column zero is X=-630 m. Raw imports are unsigned 8-bit, 505 × 505.
- `Scripts/prepare_landscape_study.py` builds the material and saves the separate map.
- `Scripts/make_study_foundations.py` removes road and soil faces from a derivative infrastructure export. Foundations, entrance ramps and short gravel threshold approaches remain. The original Blender file is preserved.
- `Scripts/paint_landscape_study.py` calls a narrowly scoped editor helper to write native Landscape alpha data. The helper rejects every map except this study and accepts only the three named layers. This bypasses editor UI control problems and Python read-only registration properties; it does not bake masks into a replacement mesh.
- `Documentation/LandscapePaintResult.json` records successful imports and saved target-layer names.
- `Scripts/run_landscape_review.ps1` reopens the saved map in a windowed game and automatically exits after capturing town and farm views.

The material uses simple procedural colour variation for the new layers. This is a technique study, not the finished photoreal surface-material benchmark. No production map replacement, terrain grading, new crops, or navigation certification is claimed by this experiment.

## Epic references

- [Landscape Paint mode](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-paint-mode-in-unreal-engine)
- [Landscape materials](https://dev.epicgames.com/documentation/unreal-engine/landscape-materials-in-unreal-engine)
- [Landscape splines](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-splines-in-unreal-engine)
- [Landscape edit layers](https://dev.epicgames.com/documentation/en-us/unreal-engine/landscape-edit-layers-in-unreal-engine)

## Verified review
The editor helper module built successfully. All three native imports returned true and the target-layer names persisted. A separate windowed game reopened the saved map and produced LandscapePaintTown.png and LandscapePaintFarm.png; both were visually inspected. The process exited normally with code 0. Surfaces follow terrain, but road boundaries are visibly too soft and colour-only material variation is insufficient for the intended realism. This confirms the native weightmap approach, not a final art pass. Direct brush-stroke interaction was not verified because the editor UI controls did not respond reliably during automation.
