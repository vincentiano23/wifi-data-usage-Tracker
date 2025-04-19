from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UsageSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    uploaded_bytes = models.BigIntegerField(default=0)
    downloaded_bytes = models.BigIntegerField(default=0)

    def total_data_used_mb(self):
        return round((self.uploaded_bytes + self.downloaded_bytes) / (1024 * 1024), 2)

    def duration_minutes(self):
        if self.end_time:
            return round((self.end_time - self.start_time).total_seconds() / 60, 2)
        return 0