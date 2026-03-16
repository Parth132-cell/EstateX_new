# EstateX Phase 6 — Video Tour System

## Architecture decisions
- Implemented tour scheduling and room-join APIs in `listing_service` for fast integration with existing listing lifecycle.
- Added `VideoTour` model with stable `room_id` to map application tours to WebRTC signaling channels.
- Kept signaling transport abstract in response (`socketio` channel), so a dedicated signaling server can subscribe/publish offers/answers/ICE candidates.
- State transition is lightweight: scheduled tour becomes `live` automatically when joined after scheduled time.

## Data model
`VideoTour`
- `room_id` (unique, indexed)
- `listing` FK
- `host_id`
- `scheduled_at`
- `recording_url`
- `status` (`scheduled|live|ended`)
- `metadata` (signaling + recording flags)

## Endpoints
- `POST /tours/schedule`
  - creates room + signaling metadata
  - returns room details and status
- `GET /tours/join/{room_id}`
  - fetches room join payload
  - returns signaling channel + current room state

## Signaling integration contract
- Join response includes:
  - `signaling.type = socketio`
  - `signaling.channel = estatex:tours:{room_id}`
- External signaling service should authorize participant, then relay SDP/ICE messages for that channel.

## Tests
- schedule endpoint creates a tour and returns room metadata.
- join endpoint transitions due tours to `live` and returns signaling payload.
