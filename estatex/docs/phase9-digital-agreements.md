# EstateX Phase 9 — Digital Agreements

## Architecture decisions
- Agreements are persisted in `listing_service` to stay tightly coupled to listings and escrow transactions.
- Agreement lifecycle is explicit (`generated` -> `sent` -> `signed`) for auditability.
- eSign provider integration is abstracted into `listings/agreement.py` so external providers can be integrated without API contract changes.
- Signed document URL is stored as `signed_pdf_url` (S3-compatible URL pattern).

## Data model
`Agreement`
- `listing` FK
- `buyer_id`
- `seller_id`
- `template_name`
- `content`
- `status` (`generated`, `sent`, `signed`)
- `esign_provider`
- `esign_request_id`
- `signed_pdf_url`

## Endpoints
- `POST /agreements/generate`
  - create agreement content from template and transaction context
- `POST /agreements/send`
  - dispatch to eSign provider
- `GET /agreements/{id}`
  - retrieve agreement details and signed document URL

## Flow
1. Generate agreement from selected template.
2. Send agreement to eSign provider.
3. Persist signed PDF URL (S3) and mark status `signed`.

## Tests
- full agreement workflow test covering generate -> send -> get signed agreement.
