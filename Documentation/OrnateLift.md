# Ornate service lift

Reference: the user's Downloads/lift1.png. This is an original geometric interpretation: dark green enamel, aged brass, fluted posts, scrolls, roundels, glazed side panels, an arched entrance and a small crowned glass roof. The bunker variant has a low cornice in place of the crown to fit its ceiling.

The upper cabin sits against the inland/west facade of the north dome. Its back clears the dome frame; its entrance faces toward the dome interior. The lower cabin retains its lobby location. Both use the existing E-triggered fade-transfer service lift; moving machinery and animated gates are not implemented.

Width 2.5 m, depth 2.35 m, upper height 4.32 m. The entrance is approximately 1.48 m clear. Exact coordinates and current map are in OrnateLift.json.

SourceAssets/OrnateLift contains FBX files and the editable Ornate-Service-Lift.blend. Scripts/make_ornate_lift.py generates the two mesh variants in background Blender. Scripts/save_lift_workbench.py assembles their editable Blender workbench. Scripts/apply_ornate_lift.py imports them and replaces only the lift enclosure, lighting and signs, preserving the runtime stations. Run it after apply_master_modules.py if regenerating the whole site.

The opt-in -OrnateLiftInspection game flag checks walking into the upper cabin, travel down, walking out of and back into the lower cabin, and travel up. Normal game launches do not run this script.
