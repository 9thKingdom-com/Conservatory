# 9th Kingdom asset chest

Created 10 September 2026. Drop new assets into `00 Incoming`, one folder per asset or pack. Tell Codex the folder name when it is ready to inspect.

| Folder | What belongs here |
| --- | --- |
| 00 Incoming | New downloads and items awaiting review; original ZIPs are welcome. |
| 01 John Originals | John's editable Blender models, textures and exports. Potential Fab sale assets. |
| 02 Third Party | Acquired packs and their license/source information. Game-use assets, not John's standalone sale inventory. |
| 03 References | Mountain, stonework, planting and lighting reference photographs, with source links where known. |
| 04 Catalog | Asset notes, provenance, integration status and missing dependencies. |

For Blender assets, provide the `.blend`, any external textures (or pack them into the blend), and optionally FBX exports. Keep one asset folder together. Useful notes: intended use, approximate real dimensions, creator/source and whether this is original work.

For Fab downloads, keep the pack name, listing URL, creator, acquisition date and supplied license/readme with the download. Do not assume every free asset has the same license or that all Megascans are free.

For assets already in Epic's library, use Add to Project and select Conservatory where supported. Give Codex the pack name and its Content Browser folder. For packs distributed as complete projects, create their project and migrate the needed assets and dependencies through Unreal. Do not copy isolated `.uasset` files into this chest or rearrange imported Unreal folders in Explorer.

The chest holds source material. Imported Unreal assets live under the project's Content folder, retaining vendor paths when needed for references. Existing source assets remain at their current paths; this folder does not move or duplicate them automatically.

Fab Standard License permits assets in games but prohibits standalone resale/redistribution of the acquired assets. Keep third-party content out of John's Fab source packages unless its specific license explicitly permits that redistribution.

Sources: https://www.fab.com/eula and https://dev.epicgames.com/documentation/fab/purchasing-and-downloading-assets-in-fab

First environment asset priorities: convincing mountain silhouettes, rock outcrops, weathered stone steps and retaining walls, gravel/soil/leaf-litter surfaces, grasses, ferns and low shrubs. Audit existing assets before adding overlapping packs.
