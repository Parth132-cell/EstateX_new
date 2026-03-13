from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    BUYER = "buyer", "Buyer"
    SELLER = "seller", "Seller"
    BROKER = "broker", "Broker"
    ADMIN = "admin", "Admin"


class KYCStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    VERIFIED = "verified", "Verified"
    REJECTED = "rejected", "Rejected"


class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices)
    kyc_status = models.CharField(max_length=20, choices=KYCStatus.choices, default=KYCStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone"]


class BrokerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="broker_profile")
    agency_name = models.CharField(max_length=255)
    license_doc_url = models.URLField(max_length=1024)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self) -> str:
        return f"BrokerProfile<{self.user_id}>"
