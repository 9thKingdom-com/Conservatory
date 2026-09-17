# Future gameplay direction

Implementation update, 10 September 2026: the user requested this system now. The kitchen wall monitor, ten paired in-game suits, first-person robot possession, safe return to the human, and AI resumption are implemented in L_Exterior_RobotVR. See RobotVR.md and RobotVRRuntime.json. Earlier next-session statements below describe the original plan and are superseded by this implementation update.


## Approved next-session robot embodiment — 10 September 2026

Replace the computer-based robot connection with one physical AI control suit and VR headset per robot in the room. Each suit is paired with a stable robot ID. Wearing that robot's suit transfers full movement and look control to it; the player experiences the robot's eye-level first-person view as its body. The human remains safely inside the habitat. On exit, control returns to the human and the robot resumes autonomous behaviour.

A wall monitor shows the map with every robot's live location and identity, and the selected robot's live eye-camera perspective. The map marker, monitor feed and paired suit must all refer to the same robot ID. Robots need stable IDs and terrain-wide autonomous routes in preparation.

The suit/headset props, possession interaction, return-control flow, wall map display and monitor camera selection are requested for the next session. They are design intent, not completed features. Keep the existing terminal until that replacement session.

User direction recorded 7 September 2026. This document is design intent, not implemented functionality.

- No humans remain outside the conservatory. People survive inside its sealed environment.
- Robots roam outside and rely on solar charging stations to remain operational.
- The people inside can use those robots to collect external resources.
- Collected resources allow the inhabitants to extend the modular conservatory when more space is needed.
- The hill-edge location should let the player see the village and eventually observe outside robot activity through the glass.

Current implementation remains the environment and modular architectural shell. Robot control, charging, resource collection, construction costs, player expansion and sealing/trapping mechanics are future work.

Decisions still to make when that stage begins: how robots receive orders, how energy and weather affect charging, how resources enter the sealed conservatory, and how new modules attach without breaking the seal.

The bunker architecture now provides space for seed archives, water and pumping, oxygen storage and air filtration, food reserves, rest, study, healthcare, sanitation, waste treatment, power and repair. Later maintenance gameplay can use these existing rooms. Tank gauges and status displays currently depict equipment only; inventory and resource simulation are not connected.
