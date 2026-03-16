from django.db import models
from django.utils import timezone


class PropertyListing(models.Model):
    class VerificationStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'

    broker_id = models.BigIntegerField(db_index=True)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=120, db_index=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, db_index=True)
    bhk = models.PositiveSmallIntegerField(db_index=True)
    description = models.TextField()
    amenities = models.JSONField(default=list)
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
    )
    media_urls = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city', 'price']),
            models.Index(fields=['city', 'bhk']),
            models.Index(fields=['price', 'bhk']),
        ]


class VerificationRecord(models.Model):
    class Result(models.TextChoices):
        PENDING_ADMIN = 'pending_admin', 'Pending Admin Approval'
        FAILED = 'failed', 'Failed'

    property_listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='verification_records')
    geo_lat = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    geo_lng = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    face_match_score = models.DecimalField(max_digits=4, decimal_places=3)
    ai_fraud_score = models.DecimalField(max_digits=4, decimal_places=3)
    gps_metadata_present = models.BooleanField(default=False)
    timestamp_valid = models.BooleanField(default=False)
    result = models.CharField(max_length=20, choices=Result.choices)
    admin_approval_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class VideoTour(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        LIVE = 'live', 'Live'
        ENDED = 'ended', 'Ended'

    room_id = models.CharField(max_length=64, unique=True, db_index=True)
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='video_tours')
    host_id = models.BigIntegerField(db_index=True)
    scheduled_at = models.DateTimeField(db_index=True)
    recording_url = models.URLField(blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at']


class NegotiationHistory(models.Model):
    class OfferType(models.TextChoices):
        OFFER = 'offer', 'Offer'
        COUNTER = 'counter', 'Counter'

    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='negotiations')
    from_user = models.BigIntegerField(db_index=True)
    to_user = models.BigIntegerField(db_index=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    message = models.TextField(blank=True, default='')
    offer_type = models.CharField(max_length=20, choices=OfferType.choices, default=OfferType.OFFER, db_index=True)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['timestamp']
        indexes = [models.Index(fields=['listing', 'timestamp'])]


class Transaction(models.Model):
    class Status(models.TextChoices):
        ORDER_CREATED = 'order_created', 'Order Created'
        FUNDS_HELD = 'funds_held', 'Funds Held'
        RELEASED = 'released', 'Released'
        FAILED = 'failed', 'Failed'

    buyer_id = models.BigIntegerField(db_index=True)
    seller_id = models.BigIntegerField(db_index=True)
    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ORDER_CREATED, db_index=True)
    provider_reference = models.CharField(max_length=120, unique=True, db_index=True)
    provider_order_id = models.CharField(max_length=120, blank=True, default='')
    provider_payment_id = models.CharField(max_length=120, blank=True, default='')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']



class Agreement(models.Model):
    class Status(models.TextChoices):
        GENERATED = 'generated', 'Generated'
        SENT = 'sent', 'Sent for eSign'
        SIGNED = 'signed', 'Signed'

    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='agreements')
    buyer_id = models.BigIntegerField(db_index=True)
    seller_id = models.BigIntegerField(db_index=True)
    template_name = models.CharField(max_length=120)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.GENERATED, db_index=True)
    esign_provider = models.CharField(max_length=80, blank=True, default='')
    esign_request_id = models.CharField(max_length=120, blank=True, default='', db_index=True)
    signed_pdf_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']



class Dispute(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        RESOLVED = 'resolved', 'Resolved'

    listing = models.ForeignKey(PropertyListing, on_delete=models.CASCADE, related_name='disputes')
    raised_by_user_id = models.BigIntegerField(db_index=True)
    reason = models.TextField()
    resolution_notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
