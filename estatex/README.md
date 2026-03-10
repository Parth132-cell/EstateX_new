# EstateX Monorepo

Phase 1 delivers the backend foundation for a modular AI-powered real estate platform.

## Monorepo structure

```text
estatex/
  mobile_app/
  backend/
  api_gateway/
  auth_service/
  listing_service/
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

## Quick start (backend foundation)

```bash
cd estatex/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Health check: `GET /api/v1/health`
