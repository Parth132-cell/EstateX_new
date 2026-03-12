from django.contrib import admin

from .models import Agreement, NegotiationHistory, PropertyListing, Transaction, VerificationRecord, VideoTour


@admin.register(PropertyListing)
class PropertyListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'city', 'price', 'bhk', 'verification_status', 'created_at')
    list_filter = ('city', 'bhk', 'verification_status')
    search_fields = ('title', 'address', 'city', 'description')


@admin.register(VerificationRecord)
class VerificationRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'property_listing',
        'result',
        'face_match_score',
        'ai_fraud_score',
        'timestamp_valid',
        'gps_metadata_present',
        'created_at',
    )
    list_filter = ('result', 'timestamp_valid', 'gps_metadata_present', 'admin_approval_required')
    search_fields = ('property_listing__title', 'property_listing__city')


@admin.register(VideoTour)
class VideoTourAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'listing', 'host_id', 'scheduled_at', 'status')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('room_id', 'listing__title', 'listing__city')


@admin.register(NegotiationHistory)
class NegotiationHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'from_user', 'to_user', 'amount', 'offer_type', 'timestamp')
    list_filter = ('offer_type', 'timestamp')
    search_fields = ('listing__title', 'listing__city', 'message')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider_reference', 'buyer_id', 'seller_id', 'listing', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('provider_reference', 'provider_order_id', 'provider_payment_id')


@admin.register(Agreement)
class AgreementAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'buyer_id', 'seller_id', 'template_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('esign_request_id', 'template_name', 'listing__title')
