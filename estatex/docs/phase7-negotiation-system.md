# EstateX Phase 7 — Negotiation System

## Architecture decisions
- Negotiation workflows are implemented in `listing_service` to stay close to listing pricing data and reduce cross-service latency.
- Offers and counter-offers are append-only records in `NegotiationHistory` for auditability and pattern-based AI recommendations.
- AI negotiation suggestion is encapsulated in `listings/negotiation.py` so future external ML microservice integration can replace local heuristics without API changes.

## Data model
`NegotiationHistory`
- `listing` FK
- `from_user`
- `to_user`
- `amount`
- `message`
- `offer_type` (`offer` / `counter`)
- `timestamp`

## Endpoints
- `POST /offers`
  - creates initial offer
  - returns AI counter suggestion
- `POST /offers/counter`
  - creates counter-offer against an existing offer
  - returns AI next-step suggestion
- `GET /offers/history?listing_id={id}`
  - returns ordered negotiation timeline

## AI suggestion logic (current heuristic)
- Anchors on listing price
- Adjusts with listing age (older listing tolerates larger discount)
- Incorporates average of recent negotiation entries
- Produces suggested counter and rationale

## Tests
- create offer returns AI suggestion and persists offer entry.
- counter-offer endpoint creates counter entry and history endpoint returns ordered timeline.
