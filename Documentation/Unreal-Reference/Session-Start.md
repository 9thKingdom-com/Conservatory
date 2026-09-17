# Check for John's changes before Unreal work

User-approved collaboration rule, 11 September 2026: John will make manual aesthetic map edits to control cost and shape the environment himself. He currently intends to avoid mechanical changes. Check the actual project state at every Unreal session; do not assume that intent guarantees no gameplay effects.

## Before changing anything

1. Read project memory and the last relevant handoff. Check whether Unreal is already open, which map is active and whether there are unsaved changes. Disk checks cannot reveal unsaved editor work. Do not reload, close the editor, switch maps or run a generator over unresolved unsaved work.
2. Review source-control changes if available. Otherwise compare relevant map and asset modification times with the last recorded session. Include external actor/object packages when used, and materials, meshes, foliage or landscape assets referenced by the area being changed. Timestamps identify candidates, not what changed or who changed it.
3. Inspect the changed area in the current editor/project. Where useful, compare actor transforms, material assignments, lighting, foliage and Landscape settings against an existing report or snapshot. Binary package changes alone do not explain aesthetic differences. If there is no prior baseline, record the present state as the baseline and say that a historical comparison is unavailable.
4. Preserve the current state before overlapping edits: use a scoped backup or source-control checkpoint that includes affected dependencies and external packages. Prefer targeted updates over rerunning whole-map replacement scripts. Do not restore an older generated look simply because it differs from a previous screenshot.
5. Briefly report relevant changes noticed and adapt the current task to them. Ask John only if a real conflict or an unresolved unsaved state prevents safe progress; do not require him to explain every aesthetic edit.

## At the end

Record which map/area and assets we changed, whether they were saved, the baseline/checkpoint location when one was created, and any unresolved editor changes. Reuse existing inspection reports and capture a representative view when appearance changed. Record a session timestamp so the next check has a starting point.

Keep this check proportional to the task. Do not load, hash or rebuild the whole project for a small visual adjustment. Inspect changed candidates and affected dependencies first. Aesthetic edits to geometry, foliage collision or terrain may warrant a targeted access check, but not an automatic full gameplay test suite.

John can help by saving his work before handing over. A brief note about the edited area is useful but optional; the check remains our responsibility.
