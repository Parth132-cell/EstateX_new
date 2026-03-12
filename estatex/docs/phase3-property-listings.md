# EstateX Phase 3 — Property Listings Service

## 1) Architecture decisions

- **Service boundary**: Listings are isolated in `listing_service` to keep high-read search and listing lifecycle independent from auth, payment, and CRM write patterns.
- **API style**: DRF `ModelViewSet` + router for uniform CRUD and extensibility (future verification hooks, moderation states, media policies).
- **Search/filter strategy**:
  - Structured filters via `django-filter` (`city`, `bhk`, `broker_id`, `verification_status`, `min_price`, `max_price`).
  - Free-text search across title/description/address/city for lightweight relevance.
  - DB indexes on `(city, price)`, `(city, bhk)`, `(price, bhk)` for Phase-3 performance baseline.
- **Media abstraction**: `media_urls` stored as JSON list so S3 object references and multiple assets are supported immediately.
- **Verification readiness**: `verification_status` enum included in listing model to support Phase 4 verification workflow.

## 2) Folder structure (monorepo)

```text
estatex/
  mobile_app/
  backend/
  api_gateway/
  auth_service/
  listing_service/
    config/
    listings/
    manage.py
    requirements.txt
    Dockerfile
  crm_service/
  cobroker_service/
  payment_service/
  ai_service/
  notification_service/
  database/
  infrastructure/
  docker/
  kubernetes/
  docs/
```

## 3) Data model (Phase 3 scope)

Table: `PropertyListing`
- `id` (PK)
- `broker_id` (indexed)
- `title`
- `address`
- `city` (indexed)
- `price` (indexed)
- `bhk` (indexed)
- `description`
- `amenities` (JSON)
- `verification_status` (`pending|verified|rejected`, indexed)
- `media_urls` (JSON)
- `created_at`, `updated_at`

## 4) Implemented APIs

Base URL from router:
- `POST /listings/` — create listing
- `GET /listings/` — list listings with filters/search/order
- `GET /listings/{id}/` — retrieve listing details
- `PUT /listings/{id}/` — full update
- `PATCH /listings/{id}/` — partial update
- `DELETE /listings/{id}/` — remove listing

Supported query params on `GET /listings/`:
- `city`
- `bhk`
- `verification_status`
- `broker_id`
- `min_price`
- `max_price`
- `search`
- `ordering` (`price`, `created_at`, `bhk`; prefix `-` for desc)

## 5) Test cases (implemented)

- Create listing returns `201`.
- Filter listing by `city` + `bhk` returns matching row only.
- Search by text in description returns expected listing.
- Partial update (`PATCH`) updates price correctly.
- Delete listing returns `204` and removes row.

## 6) How to run

```bash
cd estatex/listing_service
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Run tests:

```bash
python manage.py test
```
