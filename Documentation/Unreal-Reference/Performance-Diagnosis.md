# Play / PIE performance diagnosis

**Status:** Diagnosed 16 September 2026 from saved logs, config and disk state. Engine: UE 5.8.2 (5.8.2-56702186+++UE5+Release-5.8). No editor session was open during the diagnosis and **no project content was modified**. This is evidence collection, not a fix.

## Scope

John asked why `Conservatory.uproject` struggles on Play and how it can be optimized **without changing any assets or functions**. This recipe records what was measured, ranked causes, and settings/workflow-only remedies. Anything that would touch content or C++ is listed only as a proposal requiring his approval.

## Environment (from `Conservatory_2.log`)

- CPU: AMD Ryzen 5 8600G (6 cores) - GPU: NVIDIA GeForce RTX 4060 Laptop, 7957 MB VRAM, driver 580.97 (2025-08-07), Windows 11, D3D12 SM6.
- Project rendering config (`DefaultEngine.ini`): Lumen GI (`r.DynamicGlobalIlluminationMethod=1`), Lumen reflections (`r.ReflectionMethod=1`), Virtual Shadow Maps (`r.Shadow.Virtual.Enable=1`), mesh distance fields on, static lighting disabled, AutoExposure off, MotionBlur off, frame-rate smoothing 30-90.
- Scalability: every `sg.*Quality=3` (Epic) in `Saved/Config/WindowsEditor/GameUserSettings.ini`; no `DefaultScalability.ini` exists.
- Production map: `L_Exterior_RobotVR`, World Partition + One File Per Actor since 15 Sept (conversion created 1,835 external actor / 36 external object packages; current disk holds 1,845 / 38 after later drawer work). Editor cell size 12,800 cm; Landscape grid 4 (four streaming proxies).

## Ranked causes (evidence)

1. **Mesh Partition (Mesh Terrain) content blocks PIE start for ~43-45 seconds.** Two independent PIE sessions (15 Sept, 14:43 and 18:09 local) show the same sequence: a `/Temp/MeshPartitionBuilderPackage` world initializes, four compiled sections build one-by-one, each running `ConvertMeshToComplexCollision` QEM simplification from a 251,001-vertex / 500,000-triangle source for **7.3-7.5 seconds** (simplified to 8 verts / 6 tris), and PIE prints `Waiting on static mesh ... CompiledSection_HighEndPlatform_RenderData_PIE ... being ready before playing` until finished. The engine then uninitializes the builder package and play begins. Actual play time in both observed sessions was under ~75 seconds after the stall.
2. **The partition is flat test geometry.** Repeated `MeshPartitionStaticMesh_0 has some nearly zero tangents / bi-normals` warnings at map load and PIE indicate an unsulpted rectangle-style partition (likely created while testing Mesh Terrain Mode on 15 Sept after the World Partition conversion; it is not recorded in PROJECT-MEMORY or any recipe, so its purpose should be confirmed with John in-editor before touching it). `MegaMeshMeshProvider` modifiers exist on three external-actor UAIDs inside level instances, which the experimental plugin warns are ignored as base modifiers.
3. **PIE duplicates the fully loaded editor world.** The workflow loads the whole region in the editor, so PIE copies it all: at PIE world init the log flushes **1,031 queued packages** in one batch, and World Partition streaming cannot reduce a PIE world that starts fully loaded. This inflates PIE start time and memory versus standalone.
4. **Epic rendering load on a mid-range 8 GB laptop GPU.** Lumen GI + Lumen reflections + VSM at Epic scalability, a glass-heavy conservatory (translucency), and **39 PointLights** in the map. During play the log warns `[VSM] One Pass Projection max lights overflow`, confirming many local lights per pixel. No FPS counters exist in the logs, so frame-rate pain is inferred from settings + hardware, not measured.
5. **Secondary CPU costs during play (small but additive).** 11 `C17Robot` actors tick every frame with `VisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones`; wander goal selection can call `GetRandomReachablePointInRadius` (1.8 km radius) plus up to 32 **synchronous** path finds in a single tick; 11 `VRSuitStation` + `RobotVRHub` do per-frame line traces when the player is near. Navmesh is baked (`RuntimeGeneration=Static`), so it is not a play-time cost, but two StaticMeshActors triggered `Exporting collision geometry with too many triangles` warnings during nav builds.
6. **HLOD layers exist but show no build logs.** Conversion auto-created `HLODLayer_Instanced`/`HLODLayer_Merged` settings assets; no HLOD generation appears in any log. Unbuilt HLODs mainly matter for standalone streaming tests (distant cells pop out), not for fully loaded PIE.
7. **Crash history is explained, not an active mystery.** Saved crashes: 15 Sept 08:16 `Could not write ... L_Exterior_RobotVR.umap` (the documented failed first conversion attempt while the editor held the map) and 8 Sept `ObjectTools.cpp` ensure. The ~44 CrashReportClient folders match rapid 15 Sept session restarts (17:13-17:21); the final sessions, including the one ending 18:11 with a Save All, closed cleanly.

## Remedies that do not change assets or functions

- **Decide the fate of the test Mesh Partition (John's call).** Options: keep it and accept the ~45 s PIE stall; have a session inspect it in the World Outliner and try the Mesh Partition build/commit flow so PIE may reuse baked data; or (content change, needs approval + backup) remove/relocate it to a study map. Do not delete anything unverified - it may be his Mesh Terrain experiment.
- **Play test from a smaller loaded region.** Before PIE, unload distant cells, or use the existing `Walk Around.cmd` standalone launcher for performance measurements. Standalone also avoids paying editor + PIE rendering at once and exercises real World Partition streaming.
- **Drop runtime scalability from Epic to High for testing.** Either editor scalability settings or a `DefaultScalability.ini` with `sg.GlobalIlluminationQuality/ReflectionQuality/ShadowQuality/PostProcessQuality/EffectsQuality=2` (start there; keep Textures 3). These are runtime quality switches, not content edits; compare against `Reference images/Styling-Base-Standard.png` before keeping any level.
- **Measure before/after.** `stat unit`, `stat gpu`, `stat fps` in PIE/standalone; the existing 30-90 smooth frame-rate range hides hitches during profiling, so temporarily disable smoothing (`bSmoothFrameRate=False`) or use `t.MaxFPS` while measuring.
- **VSM light overflow:** if shadow artifacts appear, test `r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel` (settings-only). A real reduction in light count or shadow-casting flags is a content change and needs approval.
- **Build HLODs once content settles** (World Partition panel). Distant-view appearance changes slightly; get John's visual approval.

## Proposal-only items (require explicit approval; NOT implemented)

- Content: add UCX simple collision to the two navmesh-flagged meshes; audit shadow-casting flag / distance falloff on the 39 point lights; remove or relocate the flat test partition.
- Code (functions would change internally, behavior preserved): distance/visibility-based anim tick option for robots; limit or make asynchronous the wander path-find attempts.

## Limitations

- Logs contain no FPS/FrameTime numbers; the frame-rate diagnosis is settings-and-hardware inference until `stat` is captured.
- The editor was not opened, per session-start rules, so the exact Mesh Partition actor, World Partition runtime cell size/loading range, and per-light shadow settings need quick in-editor confirmation next session.
- The plugin suite (MeshPartition, MeshTerrainMode, PCG interop, FastGeoStreaming) is Epic experimental tooling shipped with UE 5.8; FastGeoStreaming showed no measurable runtime cost in the observed PIE window (per-cell transformer stats 0-7 us), so it is not currently a suspect beyond its association with the partition workflow.


## Remediation applied - 16 September 2026 (tested)

- Cause 1 eliminated: the flat test Mesh Partition actor and its four orphaned section actors were removed from the production map (actor counts and transform evidence in MeshPartitionProviderRemoval.json); the entire Mesh Partition plugin suite is disabled in Conservatory.uproject. PIE world-to-playable measured ~0.1 s in John's own editor session the same day, versus ~43-45 s before.
- Cause 3 addressed for this hardware: editor scalability Shadow/GI/Reflections/PostProcess/Effects set to High (Textures/AA/Foliage/Shading/Landscape stay Epic); SmoothFrameRate=False.
- Windows: High Performance power plan and forced high-performance GPU for UnrealEditor.exe/Conservatory.exe.
- Incident lesson: disabling MeshPartition before removing the four saved section actors caused the startup fatal Missing custom version for actor descriptor (see [MeshPartition-Removal.md](MeshPartition-Removal.md)); recovered by re-enabling the plugin, removing the actors, then disabling it.
- Verification: plugin-off load clean (1,846 actors, zero leftovers); 40 s windowed play test passed with moving robots and screenshot MeshPartitionFix-Runtime.png.
- Not yet changed (need John's approval): navmesh over-triangle meshes, robot always-tick pose, synchronous wander path-finds, point-light shadow auditing, HLOD build.


## Note, 16 September 2026 evening: always-loaded set

To keep the robot network, VR suit system and navigation permanently resident under World Partition streaming, 30 actors are now always loaded (11 robots, 11 suit stations, hub, RecastNavMesh, NavMeshBoundsVolume and the 4 landscape streaming proxies). This restores the pre-conversion memory behaviour for terrain and gameplay systems while the 1,700+ prop actors still stream. The 11 robots already always ticked pose (noted earlier in this report), so the runtime CPU profile is essentially unchanged. Editor-only interaction-range wireframes were also added (no collision, hidden in game). See [World-Partition-Streaming-Interactions.md](World-Partition-Streaming-Interactions.md).

## Update, 17 September 2026: heavy nav mesh fix and NVIDIA driver update

After John updated the NVIDIA driver to 616.92, the two remaining heavy navigation collision exports were inspected and fixed. `SM_TreeMaster_Structure` and `SM_LiftMaster_Solid` now use simple collision for navigation (`CTF_USE_SIMPLE_AS_COMPLEX`) and have convex collision shapes. A clean map reload showed 1,865 actors, both target actors retained, and no remaining navigation collision-export warnings. See `Documentation/Unreal-Reference/Heavy-Nav-Mesh-Collision.md` and the 17 September evidence files.

## Runtime verification after heavy nav mesh fix - 17 September 2026
A 40-second standalone robot test ran on `L_Exterior_RobotVR`: all 11 robots were seen, all 10 outdoor robots moved more than 50 m, robot 11 stayed docked, and 1,903/1,903 samples were grounded. No navigation regression was found. The test did not modify map content. Evidence: `Documentation/HeavyNavMeshRuntime.json`, `Documentation/HeavyNavMeshRuntime.png`, `Scripts/verify_heavy_nav_mesh_runtime.py`, `Scripts/run_heavy_nav_mesh_runtime.ps1`. This closes the pending gameplay check after the heavy navigation collision fix.
