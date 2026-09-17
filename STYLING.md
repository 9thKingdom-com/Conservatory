# 9th Kingdom — The Conservatory: working styling guide

12 September 2026, finished lift integration: John declares his edited LIFT-MASTER finished and authorises replacing the positional conservatory lift. Latest live source includes more open glazing/ornament and revised crest/spire. Imported at the existing upper landing, preserving that design and its green/brass/ivory palette. Final Unreal screenshot inspected and walking/round-trip checks pass. Blender procedural shaders translated to Unreal materials; final in-engine material appearance has not separately received John's approval. See Documentation/Unreal-Reference/Finished-Lift-Import.md.

12 September 2026, lift source direction: John requests a new detailed Blender LIFT-MASTER from lift1-reference.png, using its dark green enamel, warm brass trim, fluted posts, open glazed cabin and ornamental crown. Asset stored in Asset Chest/01 John Originals/LIFT-MASTER. This is a reference-led Blender source build awaiting John's visual review, not a palette change to the white/ivory conservatory or a completed Unreal replacement.

12 September 2026, workflow revision: John is shaping landscape structure himself after removing trees/bushes and retaining one Landscape. He plans to redo town assets in Blender later; defer further town, village, farm and landscape dressing work. Preserve his rotated habitat and saved aesthetic edits. Requested upper lift repositioning is saved and visually checked, centred against the large dome's west-facing wall; access and round trip passed. See Documentation/Unreal-Reference/Lift-Relocation.md. This is a placement/mechanics check, not approval of a finished landscape.

Status: approved visual direction; implementation in progress. Established 9 September 2026.

This is the project's persistent art-direction reference. Read it before selecting assets, modeling in Blender, creating materials, lighting scenes, or dressing environments in Unreal. Update it as decisions are made; preserve the approved direction unless the user changes it. Read `Documentation/GAME-CANON.md` alongside it for setting and gameplay constraints.

## Approved base standard

![Approved four-view styling standard](Reference%20images/Styling-Base-Standard.png)

The user approved this board as exactly the intended look. The four panels establish woodland and glass, the growing dome, the human refuge, and the working habitat as parts of one coherent world.

The board is an AI-generated visual target, not an Unreal screenshot, engineering drawing, or promise of runtime fidelity. Its architectural proportions, equipment lettering, stairs, and incidental objects are illustrative. Preserve the approved project geometry, sealed-habitat requirements, functional circulation, and canon when translating it into playable spaces. In particular, an illustrative open exterior stair in the study does not authorize an unsealed outside entrance.

## Core direction: grounded botanical realism

Photorealistic materials, believable construction, natural vegetation, and readable lighting. The ornate conservatory sits above a practical survival habitat. The interior is maintained, useful, and lived in; the outside is biologically active and growing freely. The mood combines refuge, curiosity, solitude, and hope.

Realism is the requirement. Avoid cartoon proportions, flat placeholder surfaces, arbitrary decorative machinery, neon science-fiction styling, and exaggerated steampunk. Heritage ornament belongs to the established glasshouse architecture; modern survival equipment should look functional.

## Shared visual language

| Element | Standard |
| --- | --- |
| Painted metal | Deep muted green; credible coating thickness, restrained roughness variation, wear where hands or moving parts contact it. |
| Brass | A restrained accent on architectural details, handles, and fittings. Aged rather than uniformly bright gold. |
| Wood | Warm oak with plausible grain direction, joinery, edge treatment, and consistent texture scale. |
| Walls | Pale warm mineral surfaces; subtle surface variation and believable corners and joints. |
| Stone | Natural limestone-like tones, physical joints, modest irregularity, appropriate weathering outdoors. |
| Engineering | Brushed steel, functional copper where appropriate, green enamel housings, credible fasteners and service connections. |
| Fabric | Muted olive and neutral woven upholstery, credible seams and cushion forms. |
| Glass | Readable transparency and reflections, believable frame interfaces; condensation and dirt only where conditions justify them. |
| Vegetation | Varied natural greens, plausible species combinations and growth habits; layered planting rather than repeated isolated props. |

These are visual references, not fixed numerical shader values. Establish and record approved Unreal material instances after evaluating them under the benchmark lighting.

## Lighting and surface quality

- Use motivated daylight and practical fixtures, with convincing bounced light and contact shadows.
- Keep gameplay spaces readable. Preserve detail in shadows and avoid excessive bloom, indoor fog, or heavy orange-and-teal grading.
- Warmth comes from materials and local light sources; avoid applying a yellow wash to every room.
- Make materials respond differently to light. Avoid uniformly glossy, uniformly rough, or uniformly dirty surfaces.
- Use real-world texture scale, subtle bevels, credible thickness, seams, and construction details. Detail must hold up at player eye level.
- Compare daytime, artificial-light, and shadowed views before approving a shared material.

## Standards by environment

### Woodland and terrace

Build from canopy to ground: mature trees, younger growth, shrubs, ferns, grasses, leaf litter, exposed earth, stones, and roots. Distribute these according to terrain and plausible growth conditions. Use variation in silhouette and density, not random scattering alone. Preserve clear terrace circulation and views toward the living valley and abandoned village. Atmospheric perspective should support depth without hiding weak foreground work.

### Growing dome

Retain the established ornate ribbed dome and cupola identity. Repeat the green metal and restrained brass language. Planting is productive and maintained, with believable beds, irrigation, drainage, tools, and access. Respect the habitat's environmental systems and player movement. Avoid turning the dome into an ornamental jungle with no working space.

### Human refuge

Warm oak furniture, pale walls, tactile fabrics, books, useful personal objects, and welcoming task lights. Compact, comfortable rooms at believable human scale. Furniture should show how it was made and how it is used. Keep clutter purposeful and circulation clear.

### Working habitat

Practical pumps, tanks, filtration, cabinets, and work surfaces using the same palette. Show credible pipe routes, supports, valves, cables, and service access. Equipment should communicate function. Do not add machinery merely to fill a wall or invent functional claims from the generated board.

### Town — sudden interruption (user direction, 9 September 2026)

For the current town pass, show a recognisable small town shortly after daily life stopped: paved streets, pavements, a gas station, older ordinary cars, and localized crash damage. The user explicitly requested **no overgrowth** in the town. Remove facade vines and intrusive ground cover; keep roads, forecourts, and buildings legible. Weathering belongs to normal age and use rather than decades of abandonment. Concentrate disruption in a few believable incidents, such as a car left at a fuel pump and a damaged shopfront. This supersedes the earlier overgrown-village treatment for this area; it does not remove the surrounding living woodland.

## Asset and Blender workflow

Current furniture is acceptable for positioning while areas are built out. Replace it progressively with finished pieces; do not mistake placeholder geometry for the final aesthetic.

Before importing or buying packs, audit owned assets and identify a specific gap. Prioritize woodland layers, terrain surfaces, bark, rocks, stone, and strong base textures. Select assets for compatible realism, scale, biome, material response, and runtime cost. Preserve vendor licensing and dependency information.

For bespoke Blender pieces, use consistent real-world dimensions, sensible origins, reusable components, correct normals, suitable UVs, and believable construction. Include joinery, edge treatment, seams, and thickness where visible. Plan collision and optimization for the actual gameplay use. Favor a small excellent set of repeatable pieces over unrelated one-off furniture.

Build shared Unreal materials for green paint, oak, brass, mineral walls, stone, fabric, glass, and engineering metals. Reuse approved instances and document intentional variations. Imported assets must be evaluated alongside these materials before broad deployment.

## Implementation sequence

1. Audit current assets and establish the shared material palette.
2. Finish the study as the first benchmark: table, chair, bookcase, lamp, room surfaces, and lighting at normal gameplay height.
3. Finish one conservatory growing bay to validate glass, sunlight, planting, and structural materials.
4. Finish one woodland view to validate vegetation layers, terrain, and exterior depth.
5. Compare all three in the same playable Unreal build and assess runtime performance.
6. Expand the approved treatment room by room and across the landscape.

The first milestone is one finished study, one finished growing bay, and one finished woodland view running together in Unreal. These become the practical production reference alongside the original board.

## Review before expanding a finished area

- Does it belong beside all four approved reference panels?
- Are proportions, construction, texture scale, and material response credible from the player's viewpoint?
- Is lighting readable and motivated, with depth rather than flat illumination?
- Does wear reflect use and exposure, while the refuge still feels maintained?
- Do foliage and terrain have convincing layers and transitions?
- Are navigation, interaction, sealing, and service access preserved?
- Has the area been checked in gameplay, with performance appropriate to the target machine?

Record approved benchmark screenshots and their map locations here as they become available. Generated concepts alone do not constitute implementation approval.

## Working decision log

10 September 2026, verified Unreal habitat integration: the approved five-dome assembly now replaces the old conservatory in default `L_Exterior_RobotVR`. Uses deep green frames, brass accents, fitted glazing and floors. Terrain supports the larger footprint; the habitat is offset four metres inland to clear the unchanged lift enclosure. Standalone tests passed all four walkway traversals and the lift round trip; final runtime views were inspected. See `Documentation/CoreHabitat.md` and `Documentation/CoreHabitatRuntime.json`. This is an implementation benchmark, not a claim of user approval of final material quality.

10 September 2026, core habitat approval: John approved the five-dome Blender layout including midpoint walkway pillars for replacement of the old Unreal conservatory. Preserve the existing lift as a positional placeholder and other gameplay content. He explicitly allowed terrain changes to fit the enlarged habitat. This approves the architecture/layout; completed Unreal visual and runtime verification will be documented separately.

10 September 2026, walkway midpoint revision: John requested central pillars to close the gap between the two walkway sections. Added a matching pillar pair and roof arch at the midpoint of each of the four walkways, retaining their width, length and existing ornament. This gives seven pillar positions per side. Saved and visually checked in Blender; see `Documentation/WalkwayMidpointPillars.json`.

10 September 2026, five-dome Blender assembly: John approved the corrected dome appearance and requested one larger central dome with four existing-size outer domes, connected by walkways six pillars long. Preserve the existing walkway arch dimensions. Built an editable planning scene in `Reference images/Conservatory-MAIN-PARTS1.blend`, using a 1.5x diameter/24-bay centre and four 16-bay outer domes. The 1.5x ratio is an adjustable implementation choice, not an independently approved dimension. Existing source scenes are preserved. See `Documentation/FiveDomeLayout.json`. This is Blender authoring progress, not a finished Unreal benchmark.

10 September 2026, Blender dome alignment: John requested that the dome bays meet and adjoining pillars meet centrally, and explicitly allowed the small top cap to be resized to fit. Corrected the open `Reference images/Conservatory-MAIN-PARTS1.blend` bay's offset/stretch, aligned pillar axes to the 16-bay boundaries, closed ring endpoint roundoff, and fitted the existing cap to the crown. Saved a pre-edit backup. Blender viewport inspected; this is not a finished asset approval or an Unreal replacement. Measurements and backup path: `Documentation/DomeAlignment-20260910.json`.

10 September 2026, terrain revision: User reported sliding and requested outdoor robots across the terrain. Replace the marching-style clip with a root-locked forward walk whose playback follows measured velocity. Spread the ten exterior Manny bots across the walkable landscape; retain one inside. The user also specified paired AI suits/VR sets and a wall map/eye-feed monitor for the next session; see `Documentation/FutureGameplay.md`. No finished visual benchmark approval is implied.

10 September 2026: User requested replacing the custom robot presentation with standard Unreal mannequin bots: ten wandering outdoors and one indoors. Use Epic Manny as a robotic stand-in with its matching idle/walk animation. This supersedes the custom C17 appearance for the active wandering-bot scene; retain its source assets. See `Documentation/WanderingBots.md` for implementation and verification, including the animation-pack compatibility limitation. This is not a finished visual benchmark approval.

| Date | Decision |
| --- | --- |
| 2026-09-09 | User approved the four-view concept board as the intended visual direction. Realism is required; current furniture may remain as positional placeholders pending Blender replacements. |
| 2026-09-09 | Persistent guide and original concept board saved in the master project folder. Study, growing bay, and woodland view are the proposed initial production benchmarks; none is recorded as finished yet. |
| 2026-09-09 | User requested today's town pass: roads, a gas station, older abandoned/crashed cars, a sudden-ending atmosphere, and no overgrowth. See `Documentation/TownToday.md` for implementation and runtime views. |
| 2026-09-09 | User requested closer master-reference detail on the modular connecting passage, intended for future resource-gated expansion. See `Documentation/PassageDetail.md`. |
| 2026-09-09 | User supplied front, side and back robot references for a detailed Blender model. The separate `SourceAssets/C17Detailed/C17-Detailed-Reference.blend` workbench is a reference-led derivative awaiting review, not a replacement of the deployed robot. See `Documentation/C17Detailed/README.md`. |

## Reference provenance

### Initial implementation: front terrace rockface

On 9 September 2026, a basic fitted limestone outcrop and smaller toe stones were added beneath the valley-facing terrace. See [implementation notes and runtime views](Documentation/TerraceRockface.md). This is an initial integration pass, not an approved finished material or environment benchmark.

Base image: `Reference images/Styling-Base-Standard.png`, generated with the built-in image generation tool on 9 September 2026 using `Documentation/MasterReference.png` for architectural identity and `Documentation/LibraryStudy.png` for rough study layout. Prompt direction: four photorealistic views of one coherent ecological survival setting, combining ornate green-and-brass glasshouse architecture, layered oak woodland, a warm oak study, and practical survival engineering, with physically plausible materials and restrained wear.

### Robot refinement — 9 September 2026
User requested removal of the exposed cables and hydraulic details from the detailed C-17 model. Keep its silhouette clean, using the rotary joints and structural armour for mechanical definition; do not reintroduce decorative hoses, loose cable loops, hydraulic rams or their clamps without a new request.


### Mesh master — 9 September 2026
At the user's request, Conservatory-MASTER.blend was converted to real editable meshes in both scenes. The original procedural source is preserved at Saved/Backups/MasterMeshConversion/20260909-151158/Conservatory-MASTER.blend. Earlier geometry generators that inspect procedural instances must use that backup. See Documentation/MasterMeshConversion.json for conversion and reload verification.


### Indoor robot dock — 10 September 2026
User requested the indoor robot remain standing on a charging station next to the lift, out of circulation. Unit 11 is parked on a compact steel/green-enamel contact dock beside the upper lift; preserve its doorway and approach. Battery simulation is not implemented by this prop. See `Documentation/IndoorRobotDock.json` and `Documentation/TerrainRobots.md`.

### Kitchen robot VR room - 10 September 2026
User requested immediate implementation of the downstairs kitchen security monitor and ten paired VR suits. The new RobotVR map contains a live wall map/selected eye feed and ten matte green suit/headset racks. It replaces the old operations desk connection, preserves the kitchen fixtures and lift-side indoor dock, and implements possession/return. See Documentation/RobotVR.md. Runtime visuals have been inspected, but this is not a user-approved finished art benchmark.

## Valley settlement direction — 10 September 2026

John specifies a modern rural/country town in a valley, surrounded by scattered cottages, smaller villages and farms. Use contemporary rural buildings and infrastructure; medieval asset-pack names do not establish the architectural target. Retain the existing sudden-interruption and no-overgrowth direction for the main town. Plan settlements as credible places that can later support robot interior exploration and clues. Specific mysteries, interior implementation and geographic choice remain pending; no completed Unreal settlement revision is claimed.

11 September 2026: John authorises building this settlement replacement now and requires explorable interiors in every building. Rustic yet modern is approved; the initial stone/timber/pale-render/dark-metal-roof kit is an implementation interpretation awaiting visual feedback. Two outer hamlets and two farmsteads form the first layout. These are original authored working assets, not a claim of finished photorealistic production art. Preserve the white/brass habitat and sudden-interruption atmosphere. Geographic identity and individual mysteries remain undecided.

11 September 2026, verified working benchmark: the 28-building settlement pass is saved in Unreal, with readable interior lighting, solid porch foundations and terrain-fitted approaches. Town, street, interior, hamlet and farm screenshots were inspected after correcting the initial bright lighting and ramp gaps. All 28 full approach/interior walking and navigation checks pass. See Valley-Settlements.md and the Valley*.png screenshots. This records a verified playable working pass, not John's approval of final art quality; richer materials, garden/road-edge dressing and story-specific interior props remain refinement work.
## Conservatory palette revision — 10 September 2026

John explicitly restores white/ivory conservatory framing with brass trim. This supersedes the green-painted conservatory references above, including the growing dome; the wider environment palette remains unchanged. Reuse M_MasterIvoryFrame and M_MasterBrass. Import script updated; live asset restoration is pending. Pillar-base detailing needs review with this restored finish.


10 September 2026, verified palette/base repair: restored M_MasterIvoryFrame with M_MasterBrass accents on the five-dome habitat, including pillar mouldings and low perimeter trim. Corrected inverted closed faces during export; live Unreal close-up confirms solid base panels and plinths. Seven frame/cap meshes saved. The earlier pending restoration note is superseded. See Documentation/HabitatFinish.json. Original Blender source geometry is preserved; export applies the correction.


10 September 2026, environment direction: John requests more varied rustic realism in front of the conservatory, distant mountains with Montana or Switzerland inspiration, and exploration of the descending stone steps in Styling-Base-Standard.png. White/brass conservatory remains approved. Proposed first study: weathered stone terrace and exterior steps, embedded boulders, gravel-to-soil transitions, clustered low planting and layered mountain silhouettes. Geographic choice and completed Unreal benchmark remain pending.



11 September 2026, John requests native Landscape painting for natural roads, paths and farm soil rather than flat surface sheets. The isolated L_LandscapePaintStudy verifies terrain-integrated Gravel/Asphalt/Soil layers after save/reopen. It is a technique study, not an approved finished appearance: boundaries are too soft at the existing 2.5 m Landscape spacing and gravel/soil need richer material detail. Production map remains unchanged. See Documentation/Landscape-Paint-Workflow.md and LandscapePaintTown.png.

11 September 2026, website benchmark approved: John calls the live 9thkingdom.com homepage marketable. Browser inspection confirms the supplied conservatory concept hero, forest/ivory/brass palette and What will you preserve? headline. Use this as the approved website marketing appearance. Hero remains labelled concept art; approval does not establish new Unreal geometry or completed runtime fidelity.

13 September 2026, centrepiece reference direction: John supplies Downloads/tree.png for a monumental, gnarled fruit tree in the large dome. Build and refine in Blender before Unreal import. Twisted mature trunk, spreading roots, orchard leaves/fruit/blossom and rich low planting guide the tree asset. The image's dome, banners, benches and inscriptions do not replace approved architecture/canon. TREE-MASTER v0.2 and its renders are an initial modelling interpretation, not an approved final benchmark.

13 September 2026, explicit species revision: John changes the large-dome centrepiece to an ancient olive, superseding the apple/orchard direction. His three olive photos guide a broad silver-green crown, narrow leaves and heavily contorted, hollow old trunk. TREE-MASTER v0.3 is a reference-led Blender interpretation awaiting feedback, not a final approved model or Unreal result.

13 September 2026, circular tree base: John supplies tree2-base.png and requests its pale stone architectural planter style adapted to a circle. Authored stepped limestone courses, recessed curved panels, pilasters and restrained compass cartouches beneath the current olive. Original planter archived and pre-edit master backed up. John explicitly requests an Unreal positional version now, for further Blender refinement later; this supersedes the earlier import deferral and does not approve final model/material quality.

13 September 2026, city road draft: John requests the CITY-PLAN.png layout character, with a circular civic centre, regular core streets, curved residential crescents and winding northern roads. Road layout only is authorised now. The saved Unreal draft is terrain-surface colour, without height grading or replacement buildings. All pre-existing objects retained; final streetscape, materials, building positions and reference place names remain unresolved.

### Town hall positional benchmark — 2026-09-13
Verified in Unreal: simple pale stone massing with dark roofs, two wings, portico and central crowned tower; 38 x 30 m footprint and approximately 21 m height. User requested approximate map placement and relative scale only. This remains a placeholder, not approval of a final town-hall design.


14 September 2026, explicit rural revision: John requests clearing the city and surrounding roads, and will add farms, cottages and a gas station later. This supersedes the city-plan road layout and town-hall placeholder direction. Saved removal restores the original ground material and clears remaining settlement props/markers, preserving current terrain and habitat. No new rural dressing or finished visual benchmark is claimed.

14 September 2026, mountain material request: John wants reddish-grey rock for manually painting selected peaks. Use muted rusty-red mineral variation within grey rock, with a rough stone surface. This is a local peak surface option, not a change to the conservatory palette or permission to paint the entire range. Material implementation is awaiting visual review.

14 September 2026, working material verification: ReddishGreyRock appears as an assigned native Landscape Paint target; a temporary full-strength preview showed muted grey/rust mineral variation on mountain terrain. Preview undone; delivered peaks remain unpainted. This verifies shader/layer operation, not John's approval of final appearance. See Documentation/Unreal-Reference/Mountain-Rock-Paint.md.

15 September 2026, control-room cabinet review pass: John's drawer source now has a deep walnut body, darker framing, aged-brass pulls and warm amber presentation lighting derived from his supplied room draft. A full-cabinet render and game-export FBX/UCX package were generated. This is a Blender preparation pass awaiting John's visual approval and Unreal in-room verification; it does not make the draft's incidental plants, lamp or wall art part of the cabinet asset.
