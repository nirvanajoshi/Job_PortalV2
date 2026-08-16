from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ("application", "Application Update"),
        ("job", "Job Opportunity"),
        ("system", "System Notification"),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20, choices=NOTIFICATION_TYPE_CHOICES, default="system"
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"