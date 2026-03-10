from django.db import models

from apps.payments.models import Transaction


class AgreementStatus(models.TextChoices):
    GENERATED = "generated", "Generated"
    SENT = "sent", "Sent"
    SIGNED = "signed", "Signed"


class Agreement(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="agreements")
    template_version = models.CharField(max_length=30)
    s3_pdf_url = models.URLField(max_length=1024, blank=True)
    status = models.CharField(max_length=20, choices=AgreementStatus.choices, default=AgreementStatus.GENERATED)
    created_at = models.DateTimeField(auto_now_add=True)
