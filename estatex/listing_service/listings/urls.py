from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    AgreementDetailAPIView,
    AgreementGenerateAPIView,
    AgreementSendAPIView,
    OfferCounterAPIView,
    OfferCreateAPIView,
    OfferHistoryAPIView,
    PaymentCreateOrderAPIView,
    PaymentHoldAPIView,
    PaymentReleaseAPIView,
    PropertyListingViewSet,
    VideoTourJoinAPIView,
    VideoTourScheduleAPIView,
)

router = DefaultRouter()
router.register('listings', PropertyListingViewSet, basename='listings')

urlpatterns = [
    path('tours/schedule', VideoTourScheduleAPIView.as_view(), name='tour-schedule'),
    path('tours/join/<str:room_id>', VideoTourJoinAPIView.as_view(), name='tour-join'),
    path('offers', OfferCreateAPIView.as_view(), name='offer-create'),
    path('offers/counter', OfferCounterAPIView.as_view(), name='offer-counter'),
    path('offers/history', OfferHistoryAPIView.as_view(), name='offer-history'),
    path('payments/create-order', PaymentCreateOrderAPIView.as_view(), name='payment-create-order'),
    path('payments/hold', PaymentHoldAPIView.as_view(), name='payment-hold'),
    path('payments/release', PaymentReleaseAPIView.as_view(), name='payment-release'),
    path('agreements/generate', AgreementGenerateAPIView.as_view(), name='agreement-generate'),
    path('agreements/send', AgreementSendAPIView.as_view(), name='agreement-send'),
    path('agreements/<int:agreement_id>', AgreementDetailAPIView.as_view(), name='agreement-detail'),
]

urlpatterns += router.urls
