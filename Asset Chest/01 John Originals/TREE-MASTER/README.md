# TREE-MASTER

Blender review master for the large dome centrepiece, created 13 September 2026 from John's supplied tree.png. Version 0.2 is an initial editable interpretation, awaiting his visual feedback; it is not an approved final asset or a precise reconstruction of the reference.

Open TREE-MASTER.blend. Metres, ground origin at (0,0,0). Approximate bounds: 14.32 m wide, 13.50 m deep, 13.30 m tall, including planter. These are provisional asset dimensions; final clearance against the current dome must be checked before import.

Separate collections contain heartwood/limbs, roots, bark, 20,000 canopy leaves, white/pink blossoms, apples, climbing foliage, ferns and a limestone/green/brass planter. Studio cameras/lights and the packed reference image are separate. The image's surrounding conservatory, banners and benches are not modelled here. No inscriptions or incidental concept-image text have been adopted as game canon.

The trunk has editable subdivision/displacement stacks; foliage/flowers/fruit are organised as batch meshes. Materials are procedural and require no downloaded texture pack. Hero, root-detail and rear renders are included. Source geometry checked for finite coordinates; approximately 1.18 million evaluated triangles across 389 model objects.

This is the high-detail authoring version. Further work should concentrate on reference fidelity of the silhouette, more natural branch junctions, bark fissures, foliage attachment and the planting density. UV baking, collision, LODs and wind are not implemented. No Unreal content was imported or changed. Keep refinement in Blender until John approves the result.

Build/refinement scripts in the project's Scripts folder are historical creation tools. Do not rerun them over John's later manual edits. TREE-MASTER.blend is authoritative; TREE-MASTER.blend1 preserves the previous saved pass.

## Current version: 0.3 ancient olive
John explicitly changed the species to olive. TREE-MASTER.blend now contains the olive conversion in the same working file. The apple version is preserved separately in TREE-MASTER-Apple-Checkpoint.blend; the earlier description/counts above are historical. Current review images: OLIVE-TREE-Hero.png and OLIVE-TREE-Trunk.png. OliveReport.json records the current geometry check. The shorter broad canopy uses 60,000 narrow leaves with silver undersides; apples and orchard blossoms were removed, with 240 small olives added. The trunk has open spaces between its contorted living ribs and knot/scar forms. Reference images are packed. Planter and low planting retained. Still an editable interpretation for visual refinement before any Unreal import.

## 2026-09-13: sculptable olive wood
At John's request, the trunk, roots and branches were fused into one connected mesh using the voxel-remesh step from Critical Giants' Artistic Trees In Blender (https://www.youtube.com/watch?v=MDXB3SDQHYw). Tested live in Blender 5.1.1 with a 0.025 m voxel size. Small disconnected fragments were removed; the resulting mesh has 607,816 vertices and 607,850 faces, with one connected component. This adapts the tutorial's voxel-union step to the existing model; it does not reproduce its entire Skin/Array workflow.

TREE-MASTER.blend is saved in Sculpt Mode with OLIVE | SCULPT trunk roots branches active. Foliage, planter and other scene objects are preserved but hidden in the viewport. TREE-MASTER-Olive-PreSculpt.blend preserves the previous editable assembly. OliveSculptReport.json records the mesh check. Viewport inspected after saving. This is a sculpting work in progress, not an approved finished asset or an Unreal import.

## Current revision: circular base and positional game counterpart — 2026-09-13
The current master now shows the olive tree with a pale limestone circular planter inspired by John's tree2-base.png. The sculptable wood is preserved as one mesh; the base is separately editable in 08 Circular limestone planter. The old planter is hidden in 98 Archived original planter. The full pre-edit checkpoint is TREE-MASTER-PreCircularBase-20260913-140643.blend.

John explicitly requested importing this unfinished assembly for positioning, superseding the earlier import deferral. The default Unreal map now uses this assembly at the large dome's current centre. Later work should refine this master and re-export/reimport the two assets under /Game/Conservatory/Botanical/TreeMaster, retaining the latest map placement. Do not rerun initial authoring scripts over John's edits. See Documentation/Unreal-Reference/Tree-Positional.md and TreePositionalImport.json for placement and preservation evidence.
