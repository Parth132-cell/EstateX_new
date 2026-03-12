# EstateX Architecture Overview

## Target platform
- Mobile: Flutter
- Core APIs: Django REST Framework microservices
- DB: PostgreSQL
- Cache/queues: Redis
- Media/doc storage: AWS S3
- Live tours: WebRTC + Socket-based signaling
- Payments: Razorpay/Stripe escrow flow
- Auth: JWT + OTP
- AI microservices: fraud, pricing, negotiation, suitability
- Deployment: Docker + Kubernetes + AWS

## Service decomposition
- `auth_service`: registration, OTP login, JWT refresh, RBAC claims.
- `listing_service`: listing CRUD, media references, search/filter, verification state.
- `cobroker_service`: co-broker invites, split negotiations, agreements.
- `crm_service`: leads, reminders, pipeline stages.
- `payment_service`: escrow creation/hold/release and webhook processing.
- `ai_service`: model serving endpoints for risk/price/negotiation recommendations.
- `notification_service`: push/SMS/email.
- `api_gateway`: routing, auth enforcement, rate limiting, observability hooks.

## Phase plan
1. Backend foundation
2. Authentication
3. Property listings ✅
4. Verification workflow ✅ (implemented in current patch)
5. Search engine hardening ✅ (implemented in current patch)
6. Video tours ✅ (implemented in current patch)
7. Negotiation system ✅ (implemented in current patch)
8. Escrow payments ✅ (implemented in current patch)
9. Digital agreements ✅ (implemented in current patch)
10. Mobile app ✅ (implemented in current patch)
11. Admin dashboard
12. Deployment
