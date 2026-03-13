from django.conf import settings
from django.db import models

from apps.listings.models import Property


class TransactionStatus(models.TextChoices):
    CREATED = "created", "Created"
    HELD = "held", "Held"
    RELEASED = "released", "Released"
    FAILED = "failed", "Failed"


class Transaction(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buy_transactions")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sell_transactions")
    listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=TransactionStatus.choices, default=TransactionStatus.CREATED)
    provider_reference = models.CharField(max_length=255, blank=True)
