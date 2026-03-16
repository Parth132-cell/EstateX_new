# EstateX Phase 10 — Flutter Mobile App Functional MVP

## Architecture decisions
- Kept the feature-first Flutter module under `estatex/mobile_app` and upgraded it from static pages to a working MVP flow.
- Introduced lightweight app-level state via `ChangeNotifier` + `InheritedNotifier` to avoid external state dependencies while enabling real user interactions.
- Extended `go_router` with path-parameter routes (`/detail/:id`, `/tour/:id`, `/negotiation/:id`, `/escrow/:id`, `/ar/:id`) to support listing-centric workflows.
- Added a reusable `ScreenScaffold` + navigation drawer pattern to keep cross-screen navigation consistent.

## Functional flows implemented
- **Authentication:** Login/signup form with role selection and OTP entry action simulation.
- **KYC Upload:** Document number capture and persisted “submitted” state.
- **Property Feed:** Filtered listing stream with verified badges and navigation to details.
- **Property Detail:** Listing context + actionable CTAs for tours, negotiation, escrow, and AR preview.
- **Search Filters:** City, max-price slider, and BHK chip filtering that updates the feed.
- **Video Tours:** Schedule and join actions with status transitions (`not_scheduled -> scheduled -> live`).
- **Negotiation:** Offer/counter forms with persisted thread and AI suggestion simulation.
- **Escrow Payment:** Transaction state progression (`none -> order_created -> funds_held -> released`).
- **AR Interior Preview:** Select room + design theme and render preview configuration.
- **Broker Dashboard:** Live metrics derived from app state (leads, live tours, active/closed deals).

## Implemented structure
- `lib/core/models` for mobile domain entities (`PropertyListing`)
- `lib/core/state` for shared app state container (`AppState`, `AppStateScope`)
- `lib/core/router` for route map with listing-aware paths
- `lib/features/*/presentation/screens` for screen-level UI + interactions
- `lib/shared/widgets` for common scaffold and navigation drawer

## Backend connectivity added
- Added an HTTP `ApiClient` with JSON helpers and timeout/error handling.
- Added `EstateXRepository` to consume listings, negotiation, payments, and video-tour APIs.
- Updated app state to load listings/history from backend with offline fallback for resiliency.

## Next implementation steps
- Add secure token persistence and refresh handling.
- Replace placeholder user IDs with authenticated principals from auth tokens.
- Integrate production SDKs (WebRTC, payment provider, e-sign callbacks).
- Add widget/integration tests for each core user journey.
