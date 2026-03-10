# Phase 1 — Backend Foundation

## 1) Architecture decisions

- **Modular monorepo**: Service folders are created up front to reduce coupling and allow parallel implementation in later phases.
- **Django REST Framework as foundational backend**: Enables rapid API delivery, ORM-backed relational modeling, and mature auth ecosystem.
- **PostgreSQL + Redis baseline**: PostgreSQL for transactional consistency and rich indexing; Redis for future caching, OTPs, and rate-limit counters.
- **JWT-ready config**: Base settings include SimpleJWT so auth-service endpoints can be implemented in Phase 2 without rewiring.
- **Container-first**: Dockerfile, docker-compose, Kubernetes deployment, and CI are delivered in Phase 1 to enforce reproducible environments.

## 2) Folder structure

```text
estatex/
  backend/                  # DRF project + domain apps + tests
  api_gateway/              # scaffold
  auth_service/             # scaffold
  listing_service/          # scaffold
  crm_service/              # scaffold
  cobroker_service/         # scaffold
  payment_service/          # scaffold
  ai_service/               # scaffold
  notification_service/     # scaffold
  mobile_app/               # flutter scaffold placeholder
  database/                 # SQL schema source
  docker/                   # Dockerfile + compose
  kubernetes/               # k8s deployment manifest
  .github/workflows/        # CI pipeline
  docs/                     # architecture/phase docs
```

## 3) Data model coverage in Phase 1

Implemented core entities:
- `users`, `brokers`
- `properties`, `verification_records`
- `cobroker_requests`
- `negotiation_history`
- `transactions`
- `video_tours`
- `agreements`
- `crm_leads`, `disputes`

Django models are split across domain apps to support bounded contexts.

## 4) Phase 1 APIs

- `GET /api/v1/health`
  - Purpose: liveness check for orchestration and uptime monitors.
  - Response: `{ service, status, phase }`

- `GET /api/v1/services`
  - Purpose: enumerate planned service boundaries for gateway/service discovery bootstrap.
  - Response: `{ services: [] }`

## 5) Test cases delivered

- `test_health_endpoint_returns_ok`
  - Validates backend liveness endpoint returns 200 and `status=ok`.
- `test_service_catalog_lists_foundational_services`
  - Validates service-catalog endpoint includes key domain services.

## 6) Next steps for Phase 2

- Implement OTP provider abstraction and JWT issuance/refresh endpoints.
- Add user registration/login APIs and role-based authorization policies.
- Add Redis-backed OTP TTL store and rate limiting.
