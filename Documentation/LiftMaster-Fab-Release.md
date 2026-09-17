# LIFT-MASTER Fab submission preparation

12 September 2026. John requested preparing the finished asset for sale; he will upload it to his own Fab account. No upload, listing creation, pricing decision or agreement acceptance was performed.

Release: `Asset Chest/01 John Originals/LIFT-MASTER/FabRelease/v1.0`.

Prepared a static DCC product: Blender 5.1.1 native master, assembled FBX and GLB, customer documentation, five 1920x1080 actual-model renders, seller listing copy, upload instructions and format-specific ZIPs. The game-specific Unreal integration is not included. No Unreal map or project content was modified during this preparation; both editors were closed at the initial process check. Original master preservation verified by SHA-256.

## Tested cleanup and validation

The latest saved master, modified at 19:43, superseded the previous integration snapshot. Release contains 424 model objects. Four edited mesh pieces had non-finite coordinates in their base mesh: apex scroll, a stile leaf and two lower crown curls. Reconstructed affected coordinates from connected finite neighbours, welded coincident points and dissolved degenerate edges in the release copy. This retains complete surfaces rather than discarding the invalid vertices and leaving holes. Audit logs exact affected objects. Original source untouched.

Converted font objects to mesh outlines and removed unused packed reference/font data. Localised used geometry-node dependencies recursively and purged unused linked groups and library records. Merely calling make_local on all node groups did not remove nested dependencies; explicitly relinking node-tree references was required. No external files, fonts, libraries or custom add-ons are required by the release.

Final export: 506,691 triangles, 267,688 vertices before normal/UV/material splits, eight materials, dimensions 2.748 x 2.440 x 5.005 m. Reopened Blender file, evaluated finite vertices, rendered final hero, then freshly imported FBX and GLB. Triangle counts match; FBX world bounds match within 0.1 mm; exchange UVs are finite. ZIP CRC checks pass. Gallery views inspected. These are Blender round-trip checks, not independent engine compatibility certification.

## Deliberate product limits

High-detail source/hero prop, not low-poly runtime package. Blender has procedural shaders; FBX and GLB use simplified material values. No baked maps, unique UV atlas, lightmap UV set, LODs, collision proxies, rigs, animations, doors, shaft, lift travel code or Unreal project. These limits are stated in listing and buyer guide. AI-assisted creation is disclosed. Fab acceptance, publisher rights/account declarations and prices remain with John and Fab.

## Reproduce in isolation

Scripts/prepare_fab_lift.py operates on a background-loaded original and writes only release derivatives. Scripts/localize_fab_lift.py removes external node-library dependencies in the release. Scripts/validate_fab_lift.py reopens and checks native/exchange files and creates GLB. Scripts/package_fab_lift.py writes documentation and ZIPs only after matching audit/validation counts. Inspect current source and release versions before rerunning.

Evidence: release Seller/GeometryAudit.json, Validation.json, PackageManifest.json; Saved/Logs/FabLiftPrep.log and FabLiftValidation.log. Initial failed validation attempts were not packaged. Media includes no AI-generated substitute views.
