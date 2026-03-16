from rest_framework import serializers

from .models import Agreement, Dispute, NegotiationHistory, PropertyListing, Transaction, VideoTour


class PropertyListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyListing
        fields = [
            'id',
            'broker_id',
            'title',
            'address',
            'city',
            'price',
            'bhk',
            'description',
            'amenities',
            'verification_status',
            'media_urls',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_amenities(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Amenities must be a list of strings.')
        return value

    def validate_media_urls(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Media URLs must be a list.')
        return value


class ListingVerificationRequestSerializer(serializers.Serializer):
    image_metadata = serializers.DictField(required=True)
    media_timestamp = serializers.DateTimeField(required=True)
    face_match_score = serializers.DecimalField(max_digits=4, decimal_places=3)
    owner_selfie_url = serializers.URLField(required=False, allow_blank=True)
    suspicious_flags = serializers.IntegerField(required=False, min_value=0, default=0)
    ai_fraud_score = serializers.DecimalField(max_digits=4, decimal_places=3, required=False)

    def validate_media_timestamp(self, value):
        from django.utils import timezone

        if value > timezone.now():
            raise serializers.ValidationError('Media timestamp cannot be in the future.')
        return value


class ListingSearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=False, allow_blank=True, max_length=160)
    city = serializers.CharField(required=False, max_length=120)
    bhk = serializers.IntegerField(required=False, min_value=1, max_value=20)
    min_price = serializers.DecimalField(required=False, max_digits=14, decimal_places=2)
    max_price = serializers.DecimalField(required=False, max_digits=14, decimal_places=2)
    page_size = serializers.IntegerField(required=False, min_value=1, max_value=100, default=20)

    def validate(self, attrs):
        min_price = attrs.get('min_price')
        max_price = attrs.get('max_price')
        if min_price is not None and max_price is not None and min_price > max_price:
            raise serializers.ValidationError({'max_price': 'max_price must be greater than or equal to min_price'})
        return attrs


class VideoTourScheduleSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(min_value=1)
    host_id = serializers.IntegerField(min_value=1)
    scheduled_at = serializers.DateTimeField()
    recording_enabled = serializers.BooleanField(required=False, default=False)


class VideoTourSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoTour
        fields = [
            'id',
            'room_id',
            'listing',
            'host_id',
            'scheduled_at',
            'recording_url',
            'status',
            'metadata',
            'created_at',
        ]
        read_only_fields = ['id', 'room_id', 'status', 'recording_url', 'metadata', 'created_at']


class OfferRequestSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(min_value=1)
    from_user = serializers.IntegerField(min_value=1)
    to_user = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=1)
    message = serializers.CharField(required=False, allow_blank=True, max_length=1000)


class OfferCounterRequestSerializer(OfferRequestSerializer):
    reference_offer_id = serializers.IntegerField(min_value=1)


class NegotiationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NegotiationHistory
        fields = [
            'id',
            'listing',
            'from_user',
            'to_user',
            'amount',
            'message',
            'offer_type',
            'timestamp',
        ]


class PaymentCreateOrderSerializer(serializers.Serializer):
    buyer_id = serializers.IntegerField(min_value=1)
    seller_id = serializers.IntegerField(min_value=1)
    listing_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=1)


class PaymentHoldSerializer(serializers.Serializer):
    provider_reference = serializers.CharField(max_length=120)
    provider_payment_id = serializers.CharField(max_length=120)


class PaymentReleaseSerializer(serializers.Serializer):
    provider_reference = serializers.CharField(max_length=120)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'buyer_id', 'seller_id', 'listing', 'amount', 'status', 'provider_reference',
            'provider_order_id', 'provider_payment_id', 'metadata', 'created_at', 'updated_at'
        ]



class AgreementGenerateSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(min_value=1)
    buyer_id = serializers.IntegerField(min_value=1)
    seller_id = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, min_value=1)
    template_name = serializers.CharField(max_length=120, default='estatex-sale-template-v1')


class AgreementSendSerializer(serializers.Serializer):
    agreement_id = serializers.IntegerField(min_value=1)
    provider = serializers.CharField(required=False, allow_blank=True, max_length=80, default='')


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = [
            'id', 'listing', 'buyer_id', 'seller_id', 'template_name', 'content', 'status',
            'esign_provider', 'esign_request_id', 'signed_pdf_url', 'created_at', 'updated_at'
        ]



class AdminVerifyListingSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(min_value=1)
    action = serializers.ChoiceField(choices=['approve', 'reject'])


class AdminResolveDisputeSerializer(serializers.Serializer):
    dispute_id = serializers.IntegerField(min_value=1)
    resolution_notes = serializers.CharField(max_length=2000)


class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = [
            'id', 'listing', 'raised_by_user_id', 'reason', 'resolution_notes',
            'status', 'created_at', 'resolved_at'
        ]
