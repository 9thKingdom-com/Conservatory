# Epic library foliage upgrade

Imported from the user's existing local Epic library cache: **Medieval Houses Modular Vol. 2**, its included `Medieval_Environment/Real_Landscape` vegetation set.

The active level uses mature white oaks in two forms, younger oaks, textured short/long grass, and ferns. The conservatory planters also use young library oaks. Authored LODs are preserved (five for mature oaks, four for younger trees/ferns, three for grasses). Ground-cover distance culling limits distant draw cost.

`LibraryFoliage.json` records the selected asset paths and the 50 copied dependency files (about 206 MB). No unresolved project package references were found. Original paths under `Content/Medieval_Environment` are intentionally retained so materials, textures and material functions resolve. These are third-party assets from the user's Epic library and retain their original licensing; they are distinct from the project-authored FBX geometry.

The cached Megaplants Elder, Norway Spruce and Japanese Cypress packs were inspected but are not used in this version. The complete static-mesh oak/ground-cover set provides a cohesive woodland and fits the existing instanced-mesh implementation.

The upgraded working map is `/Game/Conservatory/Maps/L_Exterior_Sealed`. `/Game/Conservatory/Maps/L_Exterior` preserves the earlier procedural version. Run `Scripts/upgrade_library_foliage.py` in Unreal to rebuild the foliage variant from that original, then `Scripts/position_conservatory.py` to apply the enlarged hill-edge arrangement. Regeneration replaces the upgraded map, so preserve a separate copy before manually editing it.

