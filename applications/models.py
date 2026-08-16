from django.db import models
from jobs.models import Job
from profiles.models import JobSeekerProfile


class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("reviewed", "Reviewed"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
        ("withdrawn", "Withdrawn"),
    )

    job_seeker = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="applications"
    )
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to="applications/resumes/")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("job_seeker", "job")

    def __str__(self):
        return f"{self.job_seeker.user.username} -> {self.job.title}"