# C-17 Conservatory salvage robot

Reference-led first character pass, based on `Reference images/robot-1.png`. Original mesh and animation source are included; the reference image is unchanged.

## Delivered assets

- `SourceAssets/C17/C17-Workbench.blend`: editable model, rigid skin, baked actions, materials, and studio setup.
- `SourceAssets/C17/C17-AnimationRig.blend`: additional optional hand/foot IK targets and elbow/knee pole controls. The `IK Authoring` custom property defaults to 0 so existing clips retain their baked motion. Use 1 when authoring a new action; bake visual bone transforms before FBX export. Controls are non-deforming and excluded from game export.
- `SourceAssets/C17/SK_C17.fbx`: skeletal mesh.
- `SourceAssets/C17/A_C17_*.fbx`: seven animation exports.
- `/Game/Conservatory/Robots/C17`: imported skeletal mesh, shared skeleton, physics asset, seven animations, seven materials, and three paint textures.
- `Source/Conservatory/C17Robot.*`: reusable NPC character with idle/walk patrol preview and a Blueprint-callable `PlayWorkAnimation(Action)` function.

The body is about 1.52 m tall; the antenna reaches 1.68 m. There are 47,696 triangles and 26,262 source vertices. All vertices have exactly one normalized bone influence, preserving rigid mechanical plates. The Blender deform rig has 38 bones; Unreal includes an additional FBX armature root (39 total). The separate authoring rig adds eight non-deforming controls.

## Skeleton and attachment points

The hierarchy includes pelvis, two spine joints, neck, head, clavicles, shoulders, elbows, wrists, two-joint three-finger grippers, hips, knees, ankles, and toes. `tool_l` and `tool_r` are gripper attachment bones; `camera_mount` follows the sensor head; `cargo_mount` follows the backpack. Unreal attachments can target these bone names directly.

These are mechanical humanoid bones, not a claim of automatic Manny/Quinn compatibility. Set up an IK Retargeter if reusing another character's animation library. Character collision currently uses its capsule; the imported physics asset is a starting point, not a tuned ragdoll.

## Animation set

| Clip | Duration | Purpose |
| --- | --- | --- |
| Idle | 3.0 s | Quiet sensor movement |
| Walk | 1.07 s | In-place patrol gait |
| CarryWalk | 1.33 s | In-place gait with arms holding a load |
| Lift | 3.0 s | Bend knees, reach low, recover |
| ShelfPick | 3.0 s | Reach forward and upward with grippers |
| Chop | 2.0 s | Two-handed wind-up and strike |
| BreakStone | 2.0 s | Lower working strike |

These are starter motion clips. They do not chop a world tree, fracture a rock, attach a carried object, or award resources. Tool meshes, exact contact alignment, gameplay IK, impact notifies, and resource transactions belong to the next integration stage. Locomotion is in-place; the character movement component supplies translation. The NPC currently uses single-clip playback; a production animation blueprint can add blending and terrain foot placement later.

## Level and workstation

The default level is `/Game/Conservatory/Maps/L_Exterior_C17_Ready`. Two preview units patrol the exterior terrace beside the conservatory glass. Both use the C-17 model. Patrol routes are short, fixed previews with collision and a stuck-direction fallback, not navigation or autonomous salvage planning.

One computer workstation occupies the space released by two surplus washroom cubicles. One northern toilet and basin remain behind their privacy partition. The computer is a physical prop reserved for future remote control; it does not yet possess the robot or display its camera feed. The player can inspect the units through the glass. Reopen the game or load the new level in the editor to see the additions.

## Rebuild and import

1. Run Blender with `Scripts/make_c17.py` to regenerate model, FBX files, actions, paint textures and studio render.
2. Run Blender on the workbench with `Scripts/c17_authoring_rig.py` to create the optional authoring rig copy.
3. Run Unreal's Python commandlet with `Scripts/import_c17.py`. Use this preset: the verified legacy FBX import uses uniform scale **100** for both mesh and animations, with force-front-X enabled. Importing at a different scale will break the physical dimensions.
4. Build the Conservatory module, then run `Scripts/place_c17.py` and `Scripts/finish_c17_workstation.py` to place the preview and workstation. These placement scripts replace their generated actors; preserve hand edits in a separate map.

The robot content directory is explicitly included in cooking so work animations loaded by name are retained. A redistributable cooked package has not been produced.

## Validation

- Blender skin audit: zero unweighted or non-rigid vertices; actions and rig saved successfully.
- Unreal reload/import: skeleton and physics asset persisted; imported bounds match the intended physical size.
- In-game patrol and pose checks: both units moved; all seven clips loaded and produced distinct hand poses at plausible scale. See `RuntimeValidation.json`.
- Studio model and in-game poses were visually inspected. See the PNGs in this directory.

Normal launches do not run tests. `-C17Inspection` runs the opt-in local preview audit and screenshots, without login or network calls.

Build validation: ConservatoryEditor Win64 Development passed before placement; the standalone Conservatory Win64 Development target also passed after the final source changes. The game target is compiled but requires cooking for distribution.


Final corrected import completed with zero errors and zero warnings. Foot-contact samples across all seven Blender clips passed the preview tolerance, including the corrected crouching lift; see FootContact.json. Both Editor and standalone Development builds passed.

