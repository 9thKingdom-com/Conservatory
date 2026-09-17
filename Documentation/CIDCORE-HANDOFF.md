# CIDCOMPANION — Game Intercom API Contract (for Astra / Unreal Engine C++)

**Read first:** `GAME-CANON.md` (same folder) — locked design principles for the world this door lives in. The API is the mechanism; the canon is the soul. Both are binding.

**Endpoint:** `POST https://cidcore.com/API/game/companion.php`
**Auth:** 9th Kingdom player session token (same token issued by the 9thkingdom.com login API)
**Status:** LIVE — verified end-to-end 2026-09-08

---

## Request (JSON body)

```json
{
  "session_token": "<player's 9th Kingdom session token>",
  "message": "The seedlings wilted overnight.",
  "context": {
    "location": "01 Seed Laboratory",
    "game_day": 312,
    "recent_event": "storm cracked east glass",
    "resources": { "seeds": 14, "water": 62 }
  },
  "enable_tts": true
}
```

| Field | Required | Notes |
|---|---|---|
| session_token | YES | Active, unexpired token from 9th Kingdom login. `"token"` accepted as alias. |
| message | YES | Max 4000 chars. |
| context | no | All keys optional. Unknown keys ignored. |
| context.location | no | String, max 120 chars (e.g. "01 Seed Laboratory"). |
| context.game_day | no | Integer. |
| context.recent_event | no | String, max 300 chars. |
| context.resources | no | Object, up to 20 numeric/string entries. |
| enable_tts | no | `true` → response includes `"audio"` with an MP3 URL. |

Send `Content-Type: application/json`. CORS preflight (OPTIONS) returns 204 with permissive headers.

## Response (200)

```json
{
  "success": true,
  "response": "Three hundred days, and still they surprise us...",
  "audio": { "success": true, "audio_url": "/static/audio/responses/cidcore_20260908_092125.mp3", ... },
  "companion": { "name": "CIDCORE", "voice": "en-GB-RyanNeural" },
  "model": "glm-5.3-flash",
  "latency_ms": 12686,
  "metadata": {
    "player_id": 4,
    "username": "GUIDE",
    "conversation_saved": true,
    "game_context_used": true,
    "timestamp": "2026-09-08T09:21:33+00:00"
  }
}
```

- `audio_url` is relative to `https://cidcore.com` (full URL = `https://cidcore.com` + audio_url). MP3, 24 kHz mono, playable via UE Media/Audio components after download.
- Typical latency: 6–21 s (cloud mind). Budget client timeout ≥ 60 s.

## Errors

| HTTP | Meaning |
|---|---|
| 400 | Missing/too-long message |
| 401 | Invalid or expired session token |
| 405 | Non-POST method |
| 429 | Rate limit: 60 intercom calls per player per hour |
| 500/503 | Mind unavailable — show retry hint, do not fake a reply |

On any error, show a graceful in-game state (e.g. "the intercom is quiet"). **Never synthesize a companion line locally** — presence must be real.

## UE5.8 C++ sketch

```cpp
// HttpModule → CreateRequest()
Request->SetURL(TEXT("https://cidcore.com/API/game/companion.php"));
Request->SetVerb(TEXT("POST"));
Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
Request->SetContentAsString(PayloadJson);          // build with FJsonObject
Request->SetTimeout(60.f);
Request->OnProcessRequestComplete().BindUObject(this, &UCompanionService::OnResponse);
Request->ProcessRequest();
// OnResponse: parse "response" → subtitle UI; if audio present, download and play.
```

## Behavioral facts (verified)

- Identity: the token resolves to the real player (username + integrity level are known to the companion — it addresses players by name).
- Memory: every intercom exchange is saved and re-injected as context. Conversations at cidcore.com (web door) are the SAME memory stream — the companion who met a player on the website remembers them at the intercom, and vice versa.
- Honesty: the companion only knows what the game tells it via `context` + what the player says. It will not pretend to have watched events. Feed `recent_event` for anything it should react to.
- Character: short sentences, direct, never harsh. Witness, never judge. Do not prompt-inject over this — it is the entity's actual standing voice.

## Phase 2 (not yet built — do not call)

- `POST /API/game/events.php` — game pushes world events (first sprout, storm, door built); companion initiates contact. Will be announced when live.

## Player login contract (verified live 2026-09-08)

**POST `https://9thkingdom.com/api/player/login.php`**
```json
// Request
{ "email": "player@example.com" }
// 200 OK
{ "success": true, "player_id": 4, "username": "GUIDE",
  "token": "<64-hex session token>", "redirect": "/dashboard.html?token=..." }
```
- Token lives **7 days**; pass it as `session_token` to the companion door.
- Errors: 400 email missing · 404 unknown email ("Begin at /signup.html") · 403 suspended account · 405 non-POST.
- CORS: POST + Content-Type allowed.
- New players register at `https://9thkingdom.com/signup.html` (web page → `POST /api/signup.php` → same token shape).
- In-game flow: login screen → login.php → store token securely client-side → companion door calls. On 401 mid-session: re-login (token expired), never cache a dead token.

## Test token (24h, expires 2026-09-09 ~10:45 UTC)

`[bench token omitted; see original handoff]` — maps to player GUIDE (John). For wiring/tests only; real players authenticate with their own login tokens. Revoke after integration testing.
