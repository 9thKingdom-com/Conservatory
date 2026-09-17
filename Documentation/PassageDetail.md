# Detailed modular conservatory passage

The connecting passage in the active `L_Exterior_C17_Ready` level now uses `SM_Passage_Detailed`. The original `Reference images/Conservatory-MASTER.blend` was inspected directly and remained unchanged; its SHA-256 is recorded in `PassageDetail.json`.

The old derivation filtered out the continuous longitudinal entablature, intermediate barrel hoops, foundation slab and original paving. Restoring those pieces reconnects the previously isolated dentils and returns the master corridor's architectural structure. Added details include slender side mullions/transoms, restrained roundels, glazing retention tabs and screws, low service sill covers, gasket strips, condensate channels, and flush threshold/inlay details. The glass shell follows the source roof bars centrally and meets the established dome portal profile at its ends.

## Reusable kit

- `SourceAssets/PassageDetail/Passage-Detailed-Workbench.blend`: editable derived parts. Body is centered at the origin; the shared arch is displayed at X=6 m for convenient editing. The master source scenes remain available in this derivative.
- `SM_Passage_Detailed.fbx`: connecting body with 35,092 triangles.
- `SM_Passage_JoinFrame.fbx`: separate ornate shared arch with 102,832 triangles; not placed over the current dome portal frames.
- Unreal assets: `/Game/Conservatory/Architecture/PassageDetail`.
- `SourceAssets/PassageDetail/PassageKit.json`: dimensions, socket datums, provenance and assembly rules.

The body retains native length 3.121445 m, floor datum 0.61 m and opposing `Attach_PositiveX` / `Attach_NegativeX` sockets. At the current scale of 1.5, each segment spans 4.682168 m. The existing dome sockets still coincide with the passage sockets. All existing actor transforms were preserved.

For future passage-to-passage runs, snap opposing socket positions and use exactly one JoinFrame at each shared seam. Its export origin is the arch's ground datum, so the floor socket offset must be subtracted when positioning it. Dome portals already supply their own frame. Do not double up columns or place frames across the walkway. Open-bay dome presets, final collision/LOD optimization, construction costs, sealing simulation and resource gates remain planned gameplay work. The detailed shared arch needs optimization before many copies are deployed.

## Rebuild and verification

Run Blender with the master loaded and `Scripts/make_passage_detail.py` to regenerate the kit. Run `Scripts/apply_passage_detail.py` through Unreal's Python commandlet to apply only the connector replacement to the default level, with a dated map backup. It verifies reference integrity, unchanged actor transforms, and socket coincidence before saving. Run this after older master-module regeneration, which restores the earlier passage asset.

The derived mesh bakes evaluated transforms and recalculates outward normals. This corrects the source paving top faces that pointed downward and blocked character step-up at the entrance. The supplied master file remains unchanged.

Use `-game -PassageDetailInspection -RenderOffscreen` for three runtime views and a bidirectional walk through both connections. Results are written to `PassageDetailWalkTest.json`; ordinary game launches do not run this inspection. Final verification passed in both directions: 14.88 m traversed per leg, grounded, crossing both dome connections without an obstruction.

![Original corridor reference](PassageMasterReference.png)

![Detailed passage exterior](PassageExteriorAfter.png)

![Detailed passage interior](PassageInteriorAfter.png)

![Glazing detail](PassageSideDetailAfter.png)


