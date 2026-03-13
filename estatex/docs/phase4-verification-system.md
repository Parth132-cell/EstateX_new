# EstateX Phase 4 — Listing Verification System

## Architecture decisions
- Verification remains in `listing_service` for now to minimize synchronous cross-service calls during listing submission.
- Verification outcomes are persisted as immutable `VerificationRecord` rows for auditability.
- Listing-level status is updated only for hard-fail checks; passed pre-checks are routed to admin moderation queue (`pending_admin`).
- AI fraud scoring is wrapped in a dedicated verification module so real microservice integration can replace the placeholder with no API contract changes.

## Data additions
- `VerificationRecord`
  - `property_listing` FK
  - GPS coordinates (`geo_lat`, `geo_lng`)
  - media `timestamp`
  - `face_match_score`
  - `ai_fraud_score`
  - booleans for `gps_metadata_present` and `timestamp_valid`
  - `result` (`pending_admin` / `failed`)
  - `admin_approval_required`

## Endpoint
- `POST /listings/{id}/verify/`

### Request
```json
{
  "image_metadata": {"geo_lat": 12.90, "geo_lng": 77.54},
  "media_timestamp": "2026-01-01T10:00:00Z",
  "face_match_score": 0.89,
  "suspicious_flags": 1
}
```

### Checks performed
1. GPS metadata presence.
2. Timestamp recency (`<= 180 days`).
3. Owner selfie face match threshold (`>= 0.75`).
4. AI fraud score threshold (`<= 0.70`).
5. If all pass, record is queued for admin approval (`pending_admin`); otherwise verification fails and listing becomes `rejected`.

## Test coverage
- Success path queues admin review and writes verification record.
- Failure path writes failed verification record and marks listing rejected.
