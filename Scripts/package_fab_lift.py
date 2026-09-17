import json,zipfile,hashlib,csv,io
from pathlib import Path
R=Path('C:/Users/ASUS TUF/Documents/1 conservatory');O=R/'Asset Chest/01 John Originals/LIFT-MASTER/FabRelease/v1.0'
a=json.loads((O/'Seller/GeometryAudit.json').read_text());v=json.loads((O/'Seller/Validation.json').read_text());m=json.loads((O/'Seller/MaterialSpec.json').read_text())
assert a['triangles']==v['native_evaluated_triangles']
T=f"{a['triangles']:,}";N=v['native_asset_objects'];dims=[a['bounds_m']['max'][i]-a['bounds_m']['min'][i] for i in range(3)]
docs=O/'Product/Documentation';docs.mkdir(exist_ok=True);uploads=O/'Uploads';uploads.mkdir(exist_ok=True)
guide=f'''LIFT-MASTER — ORNATE GLASS LIFT
Version 1.0 | September 2026

A detailed static architectural lift cabin with a glazed crown, bottle-green framing, brass ornament and a finished interior.

CONTENTS
Blender: LIFT-MASTER.blend — {N} model objects in organised collections, editable meshes and curves, eight model materials, studio lights/cameras/floor and placement anchors. Lettering is mesh geometry. Some damaged decorative meshes were repaired and their modifiers applied in this release copy.
FBX: SM_LiftMaster.fbx — one assembled mesh with eight material slots and a basic colour palette. FBX material support varies between applications.
GLB: LIFT-MASTER.glb — one assembled model with eight standard metallic/roughness materials, transmission glass and emission. This is the same geometry, using a simplified material appearance.
Documentation: this guide and MaterialParameters.csv.

GEOMETRY AND SCALE
{T} evaluated triangles. {a['vertices']:,} vertices before importer-dependent splits at material/normal/UV boundaries.
Dimensions: {dims[0]:.3f} m wide x {dims[1]:.3f} m deep x {dims[2]:.3f} m high.
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
'''
(docs/'README.txt').write_text(guide,encoding='utf-8')
stream=io.StringIO();w=csv.writer(stream);w.writerow(['Slot','Blender material','Base colour linear RGB','Metallic','Roughness','Glass transmission','Emission linear RGB','Emission strength','Procedural colour ramp linear RGB','Procedural roughness range'])
for name,d in m.items():w.writerow([d['slot'],name,d['color'],d['metal'],d['rough'],1 if d['glass'] else 0,d['emission'],d['emission_strength'],d['ramp'],d['rough_range']])
(docs/'MaterialParameters.csv').write_text(stream.getvalue(),encoding='utf-8')
listing=f'''# Fab listing — ready to copy

Title: Ornate Glass Lift

Product type: 3D Model. Choose the closest architectural prop category available in the publishing form.

## Description

Bring an ornate focal point to a conservatory, grand hotel, museum or atmospheric interior. LIFT-MASTER combines bottle-green framing, warm brass scrollwork and a glass crown with a finished cabin interior, raised service-lift lettering, control buttons and a stone floor medallion.

This is a detailed static architectural model for close-up rendering, cinematics and custom game integration. The open entrance, glazed sides and finished rear let you frame the cabin from multiple angles.

Included: an organised Blender master with editable meshes and curves, an assembled FBX, an assembled GLB, eight model materials and a setup/material guide. The Blender file also includes its studio cameras and lighting.

Technical details: {T} triangles; {N} Blender model objects; one assembled mesh in each exchange format; approximately {dims[0]:.2f} x {dims[1]:.2f} x {dims[2]:.2f} metres. Tested with Blender 5.1.1 on Windows. FBX and GLB were reimported for validation.

Materials are procedural in Blender. There are no baked texture maps. FBX provides material slots and basic colours; GLB supplies simplified metallic/roughness, glass and emission materials. Exchange formats do not reproduce Blender's procedural surface variation. Gallery images are Cycles renders of the supplied Blender model.

High-detail geometry with overlapping metric projection UVs; no unique UV atlas, lightmap UVs, LODs or collision proxies. Static model only: no rig, animations, moving doors, shaft, elevator controls, travel functionality or Unreal project. Game optimisation and engine integration are buyer tasks.

Created through AI-assisted procedural modelling and human refinement.

## Suggested tags

lift, elevator, ornate, glass, brass, conservatory, architecture, interior, art nouveau, victorian, steampunk, cinematic, high poly

## Technical fields

- Unique model: 1
- Blender model objects: {N}
- Triangles: {T}
- Export mesh vertices before application-specific splits: {a['vertices']:,}
- Materials: 8 model materials; Blender studio has an additional presentation material
- Image textures: 0
- UV mapping: Yes, overlapping planar projection; no unique atlas
- Rigged / animated: No / No
- LODs / collision proxies: No / No
- Native format: Blender 5.1.1
- Exchange formats: FBX and GLB
- Unreal Engine project / Nanite / Blueprints: Not included
- AI usage: Disclose AI-assisted creation; select Yes for Created with AI when that question is presented

## FAQ

Does it work as an elevator? It is a static cabin model. Add your own doors, shaft and gameplay system.

Will the FBX look identical to the images? The images use Blender's procedural materials and studio lighting. Other formats have simplified materials; use the included parameters to adapt them.

Is it low poly or mobile/VR optimised? No. It is a high-detail source/hero prop with {T} triangles and no LODs.

Can I edit the model? Yes. The Blender file retains separate meshes and curves. Lettering is geometry rather than editable font text.
'''
(O/'Seller/Listing.md').write_text(listing,encoding='utf-8')
start='''# LIFT-MASTER — Fab upload kit

Prepared from your latest saved master. This release sells the detailed Blender model with FBX and GLB alternatives. Your game project and original master are unchanged.

## Upload these files

| Fab section | File |
|---|---|
| Add format → Blender | Uploads/LIFT-MASTER-Blender.zip |
| Add format → FBX | Uploads/LIFT-MASTER-FBX.zip |
| Add format → GLB | Uploads/LIFT-MASTER-GLB.zip |
| Additional files | Uploads/LIFT-MASTER-Documentation.zip |
| Thumbnail / first gallery image | Media/01_Hero.jpg |
| Remaining gallery | Media/02_Front.jpg through Media/05_Rear.jpg |

Each format ZIP contains only that format. If Fab requests a raw model file instead, extract its ZIP and select the model inside. Do not upload this entire seller kit as a product format.

## Finish your listing

1. On Fab, open Publish → Listings → Create new listing. Set it up as a 3D Model / architectural prop and use the title **Ornate Glass Lift**.
2. Add the three formats and buyer documentation above. Copy the description, technical information and FAQs from Seller/Listing.md.
3. Add the five gallery images in numbered order. These are actual model renders, all 1920×1080 and below Fab's image-size limits. The Blender studio is included; a conservatory environment is not.
4. Set your publisher details, license and prices in your account. No price or account setting has been chosen for you.
5. Disclose the AI-assisted creation. Review your publisher rights declarations for the finished model/reference-based design; the reference image and font files themselves are not distributed.
6. Preview the listing and submit it for Fab review. Select manual publication if you want to control when the approved listing goes live.

No Unreal format is included in this release. The game-specific integration contains separate mechanics and project dependencies, and is not part of this static model product. Do not tick engine/plugin/animation/LOD features that are absent.

## What was verified

The native release reopens and renders. FBX and GLB reimport with matching triangle counts. The original Blender master hash matches its starting hash. The release contains no external images, fonts or linked libraries. Product files and ZIP integrity are checked; details are in Seller/Validation.json and Seller/PackageManifest.json.

This is prepared for submission, not an approval from Fab. Their review and your account setup remain outside this local preparation.

## Official references checked 12 September 2026

- [Publishing workflow](https://dev.epicgames.com/documentation/en-us/fab/publishing-assets-for-sale-or-free-download-in-fab)
- [File structure and gallery requirements](https://dev.epicgames.com/documentation/en-us/fab/asset-file-format-and-structure-requirements-in-fab)
- [Technical requirements, DCC and Exchange Formats](https://www.fab.com/o/technical-requirements)
- [Publisher guide](https://dev.epicgames.com/documentation/fab/publisher-get-started-in-fab)

The DCC requirements were read from the expanded section of the live technical-requirements page. The public distribution-agreement page did not expose its body during this check; use the agreement shown in your publisher account for the final declarations.
'''
(O/'START-HERE.md').write_text(start,encoding='utf-8')
manifest=[]
for fmt in ['Blender','FBX','GLB','Documentation']:
 paths=sorted((O/'Product'/fmt).glob('*'));out=uploads/('LIFT-MASTER-'+fmt+'.zip')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in paths:
   if p.is_file():z.write(p,p.name)
 with zipfile.ZipFile(out) as z:assert z.testzip() is None
 manifest.append({'file':str(out.relative_to(O)),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'contents':[p.name for p in paths]})
(O/'Seller/PackageManifest.json').write_text(json.dumps(manifest,indent=2))
kit=O/'LIFT-MASTER-Fab-Seller-Kit.zip'
with zipfile.ZipFile(kit,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for folder in ['Uploads','Media','Seller']:
  for p in sorted((O/folder).rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(O)))
 z.write(O/'START-HERE.md','START-HERE.md')
with zipfile.ZipFile(kit) as z:assert z.testzip() is None
print('PACKAGED',kit,kit.stat().st_size)
