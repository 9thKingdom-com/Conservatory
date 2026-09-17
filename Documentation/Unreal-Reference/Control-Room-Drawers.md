# Control-room drawer cabinet finish and export

**Tested** in Blender 5.1.1 on 15 September 2026. Unreal import has not yet been performed.

John supplied `Asset-resources/Control-Room-Assets/Johns-Drawers/Control-room-5x3.blend` and a warm control-room concept reference. The live Blender source contained 13 mesh objects and was saved at session start; a pre-finish checkpoint is retained at `Asset-resources/Control-Room-Assets/Johns-Drawers/Backups/Control-room-5x3-pre-finish-20260915.blend`.

`Scripts/finish_control_room_drawers.py` applies a dark walnut body, darker walnut framing and aged-brass pulls, plus small non-destructive edge bevels on the cabinet parts. It adds a `PRESENTATION_ONLY` collection with a warm three-light studio setup, camera, stone floor and plaster backdrop. These context objects are excluded from the FBX.

The script also creates a hidden `GAME_EXPORT` collection. It evaluates and joins copies of the authored pieces into `SM_ControlRoom_Drawers_5x3`, moves the pivot to bottom centre, adds `UCX_SM_ControlRoom_Drawers_5x3_00`, and exports `GameReady/SM_ControlRoom_Drawers_5x3.fbx`. The authored geometry remains separate and editable. Recorded export size is 2.3278 × 0.5443 × 1.2595 m with 260,660 evaluated triangles. Material values and paths are in `GameReady/Control-room-5x3_GameReady.json`.

Evidence: `GameReady/Control-room-5x3_Walnut-Brass_Preview.png` was rendered and visually inspected. The full cabinet, dark walnut value separation and reflective brass pulls are readable under warm control-room lighting. This is a prepared review pass, not John's final visual approval.

Limitations: FBX carries named material slots and scalar PBR values but not a finished Unreal wood-grain shader. The ornate repeated hardware and evaluated cabinet mesh are high detail; use Nanite or author distance LODs during Unreal integration. The supplied cabinet currently reads as four columns by five rows; geometry was deliberately not remodelled. UCX is a simple cabinet-volume box. Unreal scale, normals, material reconstruction, collision and in-room appearance remain to be verified after import.
