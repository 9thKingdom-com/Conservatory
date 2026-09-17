# Known pitfalls and working corrections

## Landscape target layers — UE 5.8

Python exposes target-layer registration and the Layer Info name as read-only in the inspected API. The study uses a small C++ editor helper to register named native layers and write alpha data. See the Landscape recipe; the helper is deliberately restricted to L_LandscapePaintStudy. Do not assume older tutorial API names still apply.

Independent overlay masks use Blend Method None and Layer Sample nodes driving interpolation. They are not competing normalized weight layers. Existing 2.5 m vertex spacing visibly limits narrow road boundaries; improving a texture alone will not increase mask resolution.

## Material graph connections — observed in the study

Check the Boolean return from connect_material_expressions. In this engine, the Component Mask input accepted an empty pin name; 'Input' did not. Connecting World Position to the tested Noise node's 'Position' pin failed; its default position was used instead. A graph-building script must not silently ignore failed connections.

## Geometry can look present but fail navigation

The settlement approach repair corrected downward-facing ramp polygons. Double-sided collision alone did not make those surfaces usable by navigation. Verify normals and then test terrain-to-room traversal. See ValleyApproachNavigation.json and the settlement recipe for the recorded passing baseline.

The habitat pillar-base repair likewise corrected inverted closed solids during export. Preserve source geometry and inspect a representative corrected import before repeating the operation across the kit.

## UI automation is not engine behavior

Landscape Paint/Manage tab clicks did not reliably change tools during the study. The cause remains unresolved. Native layer import through the editor API succeeded. Do not report brush interaction as tested on that evidence.
