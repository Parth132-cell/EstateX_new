# EstateX Phase 5 — Search Engine Hardening

## Architecture decisions
- Added a dedicated advanced search action in `listing_service` to support optimized read patterns without changing listing CRUD contracts.
- Search is restricted to `verified` inventory for buyer trust and cleaner ranking.
- Introduced cache-backed query responses (Redis in production, local memory in dev) to reduce repeated query latency.
- Implemented dual-mode search strategy:
  - PostgreSQL full-text ranking (`SearchVector`/`SearchRank`) when DB vendor is PostgreSQL.
  - Portable fallback (`icontains`) for local/dev databases.

## Endpoint
- `GET /listings/search/advanced/`

### Query params
- `q`: text query
- `city`
- `bhk`
- `min_price`
- `max_price`
- `page_size` (1..100)

### Response
- `count`
- `results`
- `cache_hit`
- `latency_target_ms`

## Performance notes
- Base filters are index-friendly (city/bhk/price) from Phase 3 indexes.
- First query computes results; repeated identical queries return from cache.
- Target is to keep median search response under 300ms with Redis and PostgreSQL tuning.

## Tests added
- advanced search returns only verified listings and applies query filters.
- repeated advanced search request returns cache hit.
