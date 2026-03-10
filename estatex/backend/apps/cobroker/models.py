from django.conf import settings
from django.db import models

from apps.listings.models import Property


class CoBrokerRequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class CoBrokerRequest(models.Model):
    listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="cobroker_requests")
    requester_broker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requested_cobroker_requests")
    listing_broker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_cobroker_requests")
    split_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=CoBrokerRequestStatus.choices, default=CoBrokerRequestStatus.PENDING)
