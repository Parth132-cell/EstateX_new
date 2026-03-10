from django.conf import settings
from django.db import models

from apps.listings.models import Property


class NegotiationHistory(models.Model):
    listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="negotiations")
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers_sent")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="offers_received")
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
