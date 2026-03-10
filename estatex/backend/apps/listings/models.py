from django.conf import settings
from django.db import models


class VerificationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class Property(models.Model):
    broker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=120, db_index=True)
    price = models.DecimalField(max_digits=14, decimal_places=2, db_index=True)
    bhk = models.PositiveSmallIntegerField(db_index=True)
    description = models.TextField()
    amenities = models.JSONField(default=list)
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class VerificationRecord(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="verification_records")
    geo_lat = models.DecimalField(max_digits=9, decimal_places=6)
    geo_lng = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField()
    face_match_score = models.DecimalField(max_digits=5, decimal_places=2)
    result = models.CharField(max_length=50)
