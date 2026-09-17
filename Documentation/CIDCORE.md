# CIDCORE stage-one intercom

Press **C** while exploring to open the intercom. Sign in with your 9th Kingdom email, type a message, and press Send or Enter. Enable **Play CIDCORE's voice** for MP3 playback; subtitles remain available if voice fails. **Return to game** restores walking and mouse look. **Sign out** cancels pending work and clears the session and displayed reply.

## Scope

The game posts directly over HTTPS to the two endpoints in CIDCORE-HANDOFF.md. Tokens exist only in process memory; restarting requires login. A 401 clears the token and asks for login. The current server authenticates email alone; this is development wiring, not production-ready account security. Adding a password field alone would not fix that server behavior. Backend password verification and an updated contract are needed before public use.

Each intercom request sends the player's measured room/location and the most recent observed location transition. Spatial bounds match the current modular map and bunker layout. Unclassified positions are identified honestly, not assigned to the nearest room. No invented inventory, game day, biology, continuous event stream, or local companion replies. Room bounds must be updated when architecture changes. CIDCORE's VPS handles persistence; Unreal does not connect directly to PostgreSQL.

Requests have a 65-second timeout, one request at a time, and no automatic retry (avoids duplicate stored exchanges). Explicit messages cover invalid input, expired session, missing/suspended account, rate limits, transport failures, malformed replies and voice failure. Closing the panel allows an outstanding exchange to finish; reopen to read it. Voice streams only from the contracted CIDCORE audio path. A 30-second media-open timeout falls back to subtitles.

## Bench testing

Non-shipping builds accept `-CidcoreBench` only when `CIDCORE_BENCH_TOKEN` is set in their launch environment. Obtain the temporary test token from the original handoff; do not put tokens in source, logs or command-line arguments. Normal launch never selects the test identity. The supplied token expires around 2026-09-09 10:45 UTC; revoke it server-side after live validation. No revocation endpoint was provided.

The additional explicit `-CidcoreSmokeTest` flag opens the panel, sends ONE identified integration-test message if a bench token is present, requests voice, writes Saved/CidcoreSmokeTest.json and a screenshot, and exits. Without a token it tests the disconnected panel only and sends nothing. This live test writes to the GUIDE companion memory when enabled with a valid token.

## Validation (2026-09-08)

- ConservatoryEditor Win64 Development compiled successfully against UE 5.8.2.
- Unreal automation `Conservatory.CIDCORE.Location` passed: passage, dome, lab, utilities room, corridor and unclassified area.
- Live authenticated exchange and voice playback remain unverified: automatic approval review blocked the proposed live test command without a detailed reason.
- No successful real-player login was attempted: no player email was supplied for that test.

See GAME-CANON.md and CIDCORE-HANDOFF.md for the supplied design and API references. These are reference snapshots, not an expanded implementation scope.

The disconnected panel was exercised in the running game and visually checked after adjusting contrast and text size. Screenshot: CidcoreIntercom.png. No network request was sent in this local panel test.


## Transmit indicator

The amber transmit lamp is driven by the actual pending HTTP request. It goes dark when the request completes, fails, cannot start, or is cancelled. The label distinguishes authentication from awaiting a companion reply; it does not claim to observe server-side thinking. No synthetic voice or sound is used for failures. The explicit live bench test now sends exactly **Hello?** as its opening transmission.

