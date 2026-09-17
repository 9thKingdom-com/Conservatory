# Computer setup review for Unreal and Blender

**Date:** 2026-09-17  
**Apps:** Unreal Engine 5.8.2, Blender 5.1  
**Conclusion:** The core system configuration is already in a good baseline for UE and Blender. No further hardware/configuration changes are needed right now.

## Verified system state
- **CPU:** AMD Ryzen 5 8600G
- **GPU 0:** NVIDIA GeForce RTX 4060 Laptop
- **GPU 1:** AMD Radeon 760M (integrated)
- **RAM:** 61.64 GB
- **Power plan:** High performance
- **NVIDIA driver:** 616.92 (32.0.16.1692), 2026-09-04

## Windows GPU preference
- `UnrealEditor.exe` is set to High Performance GPU.
- `Conservatory.exe` is set to High Performance GPU.
- This is correct for UE and means the RTX 4060 will be used for Unreal rendering.
- The AMD 760M is expected to remain active for desktop composition and other light display work. Seeing it active is normal on a hybrid laptop and not evidence that the RTX 4060 is being ignored.

## Blender GPU configuration
- Blender Cycles is configured to use **OptiX**, which is the correct API for NVIDIA RTX rendering.
- This is the preferred configuration for the RTX 4060.

## Unreal engine configuration
- The project is on **UE 5.8.2**.
- The rendering stack is **DirectX 12 / SM6**, correct for this GPU.
- Editor scalability is set to **High** for GI, reflections, shadows, post process and effects.
- Smooth frame-rate is disabled for accurate profiling.
- The Mesh Partition and related experimental plugins are disabled.

## Runtime verification after heavy nav mesh fix
- A 40 second standalone robot test was run on `L_Exterior_RobotVR`.
- All 11 robots were seen.
- All 10 outdoor robots moved more than 50 metres.
- Robot 11 remained docked.
- 1903/1903 robot samples were grounded.
- No errors or navigation regression were found.

Evidence: `Documentation/HeavyNavMeshRuntime.json`, `Documentation/HeavyNavMeshRuntime.png`.

## Summary
- The computer setup is already optimised for Unreal and Blender.
- The heavy navigation collision fix is verified by both map load and robot gameplay.
- No further system-level change is needed.