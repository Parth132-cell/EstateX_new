# EstateX Phase 11 — Admin Dashboard APIs

## Architecture decisions
- Admin moderation APIs are exposed from `listing_service` to keep listing verification and dispute resolution workflows close to source entities.
- Added a `Dispute` entity to persist dispute lifecycle and provide traceable resolution metadata.
- Admin operations are explicit endpoints for moderation actions rather than overloaded listing endpoints.

## Data model
`Dispute`
- `listing` FK
- `raised_by_user_id`
- `reason`
- `resolution_notes`
- `status` (`open`, `resolved`)
- `created_at`, `resolved_at`

## Endpoints
- `GET /admin/users`
  - returns user IDs observed in listings, transactions, and disputes (moderation snapshot)
- `GET /admin/listings`
  - returns listing moderation feed
- `POST /admin/verify-listing`
  - approve/reject listing verification status
- `POST /admin/dispute/resolve`
  - mark dispute resolved with notes

## Tests
- verify listing approval
- resolve dispute workflow
- admin users/listings endpoints return moderation data
