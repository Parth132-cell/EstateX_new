from django.conf import settings
from django.db import models

from apps.listings.models import Property


class VideoTour(models.Model):
    listing = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="video_tours")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hosted_tours")
    scheduled_at = models.DateTimeField()
    recording_url = models.URLField(max_length=1024, blank=True)
