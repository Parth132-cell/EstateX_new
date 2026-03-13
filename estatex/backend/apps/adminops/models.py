from django.conf import settings
from django.db import models

from apps.listings.models import Property


class Dispute(models.Model):
    listing = models.ForeignKey(Property, on_delete=models.CASCADE)
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.TextField()
    resolution = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
