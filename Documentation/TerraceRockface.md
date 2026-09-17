# Front terrace rockface

Basic fitted limestone outcrop added to the current default map, `L_Exterior_C17_Ready`, on 9 September 2026. It fills the valley-facing space beneath the terrace and tapers into the existing slope. A continuous closed bedrock mesh provides the main form, with 45 smaller toe stones from three reusable meshes.

Editable Blender source: `SourceAssets/TerraceRockface/Terrace-Rockface.blend`. Unreal assets: `/Game/Conservatory/Environment/TerraceRockface`. Actors are grouped under `07 Hill-edge terrace/Rockface` and tagged `TerraceRockface`.

This is an initial landscape integration pass, not a finished styling benchmark. Future refinement can add scanned surface detail, localized moss, and vegetation at the transitions.

Regenerate the source using Blender background mode with `Scripts/make_terrace_rockface.py`; apply it using Unreal's Python commandlet with `Scripts/apply_terrace_rockface.py`. The apply script reads the current default map, saves a dated map backup under `Saved/Backups/TerraceRockface`, and replaces only its own tagged actors. Run after any broader level regeneration that removes this layer. Existing actor positions, rotations, and scales are checked before saving. Collision uses the rock meshes' triangles; the bedrock top remains below the deck.

`Documentation/TerraceRockface.json` records the saved map, backup, actor count, and clearance verification. Launch with `-game -RockfaceInspection -RenderOffscreen` to take two runtime photographs and exit; ordinary launches do not run this inspection.

![Rockface exterior view](TerraceRockface.png)

![Rockface closer view](TerraceRockfaceDetail.png)
