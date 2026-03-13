from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"service": "estatex-backend", "status": "ok", "phase": 1})


class ServiceCatalogView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(
            {
                "services": [
                    "api_gateway",
                    "auth_service",
                    "listing_service",
                    "crm_service",
                    "cobroker_service",
                    "payment_service",
                    "ai_service",
                    "notification_service",
                ]
            }
        )
