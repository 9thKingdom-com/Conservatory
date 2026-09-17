LIFT-MASTER — ORNATE GLASS LIFT
Version 1.0 | September 2026

A detailed static architectural lift cabin with a glazed crown, bottle-green framing, brass ornament and a finished interior.

CONTENTS
Blender: LIFT-MASTER.blend — 424 model objects in organised collections, editable meshes and curves, eight model materials, studio lights/cameras/floor and placement anchors. Lettering is mesh geometry. Some damaged decorative meshes were repaired and their modifiers applied in this release copy.
FBX: SM_LiftMaster.fbx — one assembled mesh with eight material slots and a basic colour palette. FBX material support varies between applications.
GLB: LIFT-MASTER.glb — one assembled model with eight standard metallic/roughness materials, transmission glass and emission. This is the same geometry, using a simplified material appearance.
Documentation: this guide and MaterialParameters.csv.

GEOMETRY AND SCALE
506,691 evaluated triangles. 267,688 vertices before importer-dependent splits at material/normal/UV boundaries.
Dimensions: 2.748 m wide x 2.440 m deep x 5.005 m high.
Blender and FBX: metres, Z up, front/entrance -Y. GLB uses glTF's Y-up convention with the conversion encoded on export.
Origin: centre of the original base datum; underside Z=-0.0755 m, finished cabin floor approximately Z=+0.08 m in Blender. To rest the lowest base point on ground Z=0, place the model at Z=+0.0755 m.
The entrance is open. The rear is finished. There are no moving door panels.

BLENDER QUICK START
Open LIFT-MASTER.blend in Blender 5.1.1. Use Cycles for the supplied appearance; the five gallery images were rendered in Cycles with AgX.
Collections 01-07 contain the model. Collection 08 contains placement anchors. Collection 90 Studio contains lights, cameras and a presentation floor; hide that collection when integrating the cabin into another scene.
Append the model collections into your scene, or duplicate the file before editing. Preserve the root parent when moving the full assembly.
The source is self-contained: no image textures, fonts, linked libraries, external reference images or add-ons are required.

MATERIALS
Eight model materials: green enamel, aged brass, polished brass, dark bronze, ivory enamel, architectural glass, limestone and opal light.
Blender includes procedural colour/roughness variations and procedural stone bump. No baked texture maps are included.
FBX cannot reproduce the native procedural node graphs. GLB carries constant material values, not Blender's procedural noise or stone bump. For closest results, render the Blender file. In other applications rebuild shaders using MaterialParameters.csv and your preferred procedural/triplanar mapping.
Glass appearance depends on the renderer's transmission/refraction support and lighting. Emissive materials do not replace an actual cabin light in all engines.

UVS AND PERFORMANCE
UV0 uses overlapping metric planar projection; it is not a unique texture atlas or baked-lightmap UV set. Native curves remain editable. No texture baking, LOD chain, low-poly retopology, Nanite configuration or collision proxy is included.
This is a high-detail hero/source prop for architectural rendering, cinematics and custom integration. Optimise geometry, create collision/LODs and profile it for your own game/platform before shipping.

FUNCTIONAL SCOPE
Static geometry only. No rig, animation, opening-door system, shaft, cables, lift controller, travel logic, sounds or Unreal project is supplied. This release does not include the surrounding conservatory or any game content.

VALIDATION
Native file reopened and rendered in Blender 5.1.1 on Windows. FBX and GLB reimported into Blender; triangle counts and finite coordinates checked. FBX physical bounds match the Blender release. Other application versions and engines are not certified by these tests.

CREATION
AI-assisted procedural modelling with human editing and refinement. The supplied visual reference and third-party font files are excluded from this distribution. Images in the listing show the actual supplied model rendered in Blender.

LICENSE
Use is governed by the license selected on the Fab product listing and supplied with your purchase. This document does not add a separate license or change those terms.
