import hashlib
import json
import uuid

from django.core.cache import cache
from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Agreement, NegotiationHistory, PropertyListing, Transaction, VerificationRecord, VideoTour
from .agreement import build_signed_pdf_url, generate_agreement_content, send_to_esign_provider
from .negotiation import create_negotiation_entry, suggest_counter_offer
from .payment import create_escrow_order, hold_escrow_funds, release_escrow_funds
from .serializers import (
    AgreementGenerateSerializer,
    AgreementSendSerializer,
    AgreementSerializer,
    ListingSearchQuerySerializer,
    ListingVerificationRequestSerializer,
    NegotiationHistorySerializer,
    OfferCounterRequestSerializer,
    OfferRequestSerializer,
    PaymentCreateOrderSerializer,
    PaymentHoldSerializer,
    PaymentReleaseSerializer,
    PropertyListingSerializer,
    VideoTourScheduleSerializer,
)
from .verification import FACE_MATCH_THRESHOLD, evaluate_verification


class PropertyListingFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = PropertyListing
        fields = ['city', 'bhk', 'verification_status', 'broker_id', 'min_price', 'max_price']


class PropertyListingViewSet(viewsets.ModelViewSet):
    queryset = PropertyListing.objects.all()
    serializer_class = PropertyListingSerializer
    filterset_class = PropertyListingFilter
    search_fields = ['title', 'description', 'address', 'city']
    ordering_fields = ['price', 'created_at', 'bhk']
    ordering = ['-created_at']

    filter_backends = [
        filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]

    @action(detail=False, methods=['get'], url_path='search/advanced')
    def advanced_search(self, request):
        serializer = ListingSearchQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data

        cache_key = self._build_search_cache_key(params)
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response({**cached_response, 'cache_hit': True}, status=status.HTTP_200_OK)

        queryset = PropertyListing.objects.filter(verification_status=PropertyListing.VerificationStatus.VERIFIED)

        if city := params.get('city'):
            queryset = queryset.filter(city__iexact=city)
        if bhk := params.get('bhk'):
            queryset = queryset.filter(bhk=bhk)
        if min_price := params.get('min_price'):
            queryset = queryset.filter(price__gte=min_price)
        if max_price := params.get('max_price'):
            queryset = queryset.filter(price__lte=max_price)

        search_term = params.get('q', '').strip()
        if search_term:
            if connection.vendor == 'postgresql':
                from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

                vector = SearchVector('title', weight='A') + SearchVector('description', weight='B') + SearchVector('address', weight='C')
                query = SearchQuery(search_term)
                queryset = queryset.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.05).order_by('-rank', '-created_at')
            else:
                queryset = queryset.filter(
                    Q(title__icontains=search_term)
                    | Q(description__icontains=search_term)
                    | Q(address__icontains=search_term)
                    | Q(city__icontains=search_term)
                ).order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        page_size = params.get('page_size', 20)
        queryset = queryset[:page_size]

        results = PropertyListingSerializer(queryset, many=True).data
        payload = {
            'count': len(results),
            'results': results,
            'cache_hit': False,
            'latency_target_ms': 300,
        }
        cache.set(cache_key, payload)
        return Response(payload, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='verify')
    def verify_listing(self, request, pk=None):
        listing = self.get_object()
        serializer = ListingVerificationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data
        evaluation = evaluate_verification(payload)

        result = VerificationRecord.Result.PENDING_ADMIN if evaluation.passed else VerificationRecord.Result.FAILED

        record = VerificationRecord.objects.create(
            property_listing=listing,
            geo_lat=payload['image_metadata'].get('geo_lat'),
            geo_lng=payload['image_metadata'].get('geo_lng'),
            timestamp=payload['media_timestamp'],
            face_match_score=payload['face_match_score'],
            ai_fraud_score=evaluation.ai_fraud_score,
            gps_metadata_present=evaluation.gps_metadata_present,
            timestamp_valid=evaluation.timestamp_valid,
            result=result,
            admin_approval_required=True,
        )

        if not evaluation.passed:
            listing.verification_status = PropertyListing.VerificationStatus.REJECTED
            listing.save(update_fields=['verification_status', 'updated_at'])

        return Response(
            {
                'listing_id': listing.id,
                'verification_record_id': record.id,
                'result': record.result,
                'checks': {
                    'gps_metadata_present': record.gps_metadata_present,
                    'timestamp_valid': record.timestamp_valid,
                    'face_match_passed': payload['face_match_score'] >= FACE_MATCH_THRESHOLD,
                    'fraud_score': str(record.ai_fraud_score),
                },
                'admin_review_status': 'queued' if evaluation.passed else 'not_queued',
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _build_search_cache_key(params: dict) -> str:
        encoded = json.dumps(params, sort_keys=True, default=str)
        digest = hashlib.sha256(encoded.encode('utf-8')).hexdigest()
        return f'listing-search:{digest}'


class VideoTourScheduleAPIView(APIView):
    def post(self, request):
        serializer = VideoTourScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data
        listing = get_object_or_404(PropertyListing, id=payload['listing_id'])

        room_id = uuid.uuid4().hex[:16]
        metadata = {
            'recording_enabled': payload['recording_enabled'],
            'signaling_channel': f'estatex:tours:{room_id}',
            'webrtc': {'ice_transport_policy': 'all'},
        }

        tour = VideoTour.objects.create(
            room_id=room_id,
            listing=listing,
            host_id=payload['host_id'],
            scheduled_at=payload['scheduled_at'],
            metadata=metadata,
            status=VideoTour.Status.SCHEDULED,
        )

        return Response(
            {
                'tour_id': tour.id,
                'room_id': tour.room_id,
                'listing_id': tour.listing_id,
                'scheduled_at': tour.scheduled_at,
                'status': tour.status,
                'metadata': tour.metadata,
            },
            status=status.HTTP_201_CREATED,
        )


class VideoTourJoinAPIView(APIView):
    def get(self, request, room_id: str):
        tour = get_object_or_404(VideoTour, room_id=room_id)

        now = timezone.now()
        if tour.status == VideoTour.Status.SCHEDULED and tour.scheduled_at <= now:
            tour.status = VideoTour.Status.LIVE
            tour.save(update_fields=['status'])

        return Response(
            {
                'room_id': tour.room_id,
                'listing_id': tour.listing_id,
                'host_id': tour.host_id,
                'status': tour.status,
                'scheduled_at': tour.scheduled_at,
                'recording_url': tour.recording_url,
                'signaling': {
                    'type': 'socketio',
                    'channel': tour.metadata.get('signaling_channel', ''),
                },
            },
            status=status.HTTP_200_OK,
        )


class OfferCreateAPIView(APIView):
    def post(self, request):
        serializer = OfferRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        listing = get_object_or_404(PropertyListing, id=payload['listing_id'])
        offer = create_negotiation_entry(
            listing=listing,
            from_user=payload['from_user'],
            to_user=payload['to_user'],
            amount=payload['amount'],
            message=payload.get('message', ''),
            offer_type=NegotiationHistory.OfferType.OFFER,
        )

        suggestion = suggest_counter_offer(listing, payload['amount'])
        return Response(
            {
                'offer_id': offer.id,
                'status': 'created',
                'ai_suggestion': {
                    'suggested_counter': str(suggestion.suggested_counter),
                    'rationale': suggestion.rationale,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class OfferCounterAPIView(APIView):
    def post(self, request):
        serializer = OfferCounterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        listing = get_object_or_404(PropertyListing, id=payload['listing_id'])
        get_object_or_404(NegotiationHistory, id=payload['reference_offer_id'], listing=listing)

        counter = create_negotiation_entry(
            listing=listing,
            from_user=payload['from_user'],
            to_user=payload['to_user'],
            amount=payload['amount'],
            message=payload.get('message', ''),
            offer_type=NegotiationHistory.OfferType.COUNTER,
        )

        suggestion = suggest_counter_offer(listing, payload['amount'])
        return Response(
            {
                'counter_offer_id': counter.id,
                'status': 'created',
                'ai_suggestion': {
                    'suggested_counter': str(suggestion.suggested_counter),
                    'rationale': suggestion.rationale,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class OfferHistoryAPIView(APIView):
    def get(self, request):
        listing_id = request.query_params.get('listing_id')
        if not listing_id:
            return Response({'detail': 'listing_id query param is required'}, status=status.HTTP_400_BAD_REQUEST)

        listing = get_object_or_404(PropertyListing, id=listing_id)
        entries = listing.negotiations.all().order_by('timestamp')
        return Response(
            {
                'listing_id': listing.id,
                'count': entries.count(),
                'results': NegotiationHistorySerializer(entries, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


class PaymentCreateOrderAPIView(APIView):
    def post(self, request):
        serializer = PaymentCreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        listing = get_object_or_404(PropertyListing, id=payload['listing_id'])
        escrow = create_escrow_order(payload['amount'], listing.id, payload['buyer_id'], payload['seller_id'])

        transaction = Transaction.objects.create(
            buyer_id=payload['buyer_id'],
            seller_id=payload['seller_id'],
            listing=listing,
            amount=payload['amount'],
            status=Transaction.Status.ORDER_CREATED,
            provider_reference=escrow.provider_reference,
            provider_order_id=escrow.provider_order_id,
            metadata={'provider': 'razorpay', 'escrow': True},
        )

        return Response(
            {
                'transaction_id': transaction.id,
                'provider_order_id': transaction.provider_order_id,
                'provider_reference': transaction.provider_reference,
                'status': transaction.status,
            },
            status=status.HTTP_201_CREATED,
        )


class PaymentHoldAPIView(APIView):
    def post(self, request):
        serializer = PaymentHoldSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        transaction = get_object_or_404(Transaction, provider_reference=payload['provider_reference'])
        is_held = hold_escrow_funds(transaction.provider_order_id, payload['provider_payment_id'])

        transaction.provider_payment_id = payload['provider_payment_id']
        transaction.status = Transaction.Status.FUNDS_HELD if is_held else Transaction.Status.FAILED
        transaction.save(update_fields=['provider_payment_id', 'status', 'updated_at'])

        return Response(
            {
                'transaction_id': transaction.id,
                'provider_reference': transaction.provider_reference,
                'status': transaction.status,
            },
            status=status.HTTP_200_OK,
        )


class PaymentReleaseAPIView(APIView):
    def post(self, request):
        serializer = PaymentReleaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        transaction = get_object_or_404(Transaction, provider_reference=payload['provider_reference'])
        released = release_escrow_funds(transaction.provider_reference)
        transaction.status = Transaction.Status.RELEASED if released else Transaction.Status.FAILED
        transaction.save(update_fields=['status', 'updated_at'])

        return Response(
            {
                'transaction_id': transaction.id,
                'provider_reference': transaction.provider_reference,
                'status': transaction.status,
            },
            status=status.HTTP_200_OK,
        )



class AgreementGenerateAPIView(APIView):
    def post(self, request):
        serializer = AgreementGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        listing = get_object_or_404(PropertyListing, id=payload['listing_id'])
        content = generate_agreement_content(
            payload['template_name'],
            {
                'listing_title': listing.title,
                'buyer_id': payload['buyer_id'],
                'seller_id': payload['seller_id'],
                'amount': payload['amount'],
            },
        )

        agreement = Agreement.objects.create(
            listing=listing,
            buyer_id=payload['buyer_id'],
            seller_id=payload['seller_id'],
            template_name=payload['template_name'],
            content=content,
            status=Agreement.Status.GENERATED,
        )

        return Response(
            {
                'agreement_id': agreement.id,
                'status': agreement.status,
                'template_name': agreement.template_name,
            },
            status=status.HTTP_201_CREATED,
        )


class AgreementSendAPIView(APIView):
    def post(self, request):
        serializer = AgreementSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        agreement = get_object_or_404(Agreement, id=payload['agreement_id'])
        dispatch = send_to_esign_provider(payload.get('provider', ''), agreement.id)

        agreement.esign_provider = dispatch.provider
        agreement.esign_request_id = dispatch.request_id
        agreement.status = Agreement.Status.SENT
        agreement.save(update_fields=['esign_provider', 'esign_request_id', 'status', 'updated_at'])

        return Response(
            {
                'agreement_id': agreement.id,
                'status': agreement.status,
                'esign_provider': agreement.esign_provider,
                'esign_request_id': agreement.esign_request_id,
            },
            status=status.HTTP_200_OK,
        )


class AgreementDetailAPIView(APIView):
    def get(self, request, agreement_id: int):
        agreement = get_object_or_404(Agreement, id=agreement_id)

        if agreement.status == Agreement.Status.SENT and not agreement.signed_pdf_url:
            agreement.signed_pdf_url = build_signed_pdf_url(agreement.id)
            agreement.status = Agreement.Status.SIGNED
            agreement.save(update_fields=['signed_pdf_url', 'status', 'updated_at'])

        return Response(AgreementSerializer(agreement).data, status=status.HTTP_200_OK)
