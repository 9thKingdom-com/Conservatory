# Faster iteration

Baseline: UE 5.8, 11 September 2026.

1. Read the relevant existing recipe and project constraints. Define one visible or playable result to check.
2. Follow [the session-start check](Session-Start.md) for John's saved and unsaved edits. Inspect the active map and available source assets. Use an isolated map for experiments; preserve editable source and a recoverable production baseline.
3. Reuse the existing script or editor API for repeated operations. Use native UI where direct interaction is the thing being tested. If UI control repeatedly fails, inspect the cause or use a supported API instead of repeating blind clicks.
4. Make a small representative sample first. Inspect its appearance before applying it across the world.
5. Save, reopen, and verify the changed behavior. Geometry affecting access needs collision traversal; route changes need navigation checks. Material-only studies need visual review, not a repeat of unrelated tests.
6. Save one useful report and representative screenshots. Update the recipe with the finding and limits.

## Review without trapping John in game mode

Run game reviews windowed. Retain the project's Escape exit behavior and an automatic timeout for scripted runs. Close only the review process we launched. Do not use a fullscreen game as a default presentation method.

## Avoid spending time twice

Do not regenerate every asset to adjust one material. Do not rebuild navigation after an appearance-only change unless a separate issue warrants it. Do not rerun broad validation after targeted checks pass without a reason. Keep reusable scripts parameterized where practical, with explicit target checks before map mutations.

When a workflow feels slow, record the actual expensive step and measured duration before optimizing it. No timing benchmarks have been established for this library yet.
