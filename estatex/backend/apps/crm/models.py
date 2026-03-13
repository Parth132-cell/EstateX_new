from django.conf import settings
from django.db import models


class LeadStatus(models.TextChoices):
    NEW = "new", "New"
    CONTACTED = "contacted", "Contacted"
    NEGOTIATING = "negotiating", "Negotiating"
    CLOSED = "closed", "Closed"


class Lead(models.Model):
    broker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leads")
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)
    follow_up_at = models.DateTimeField(null=True, blank=True)
