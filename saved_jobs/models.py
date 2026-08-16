from django.db import models
from jobs.models import Job
from profiles.models import JobSeekerProfile


class SavedJob(models.Model):
    job_seeker = models.ForeignKey(
        JobSeekerProfile, on_delete=models.CASCADE, related_name="saved_jobs"
    )
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="saved_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["job_seeker", "job"],
                name="unique_saved_job",
            )
        ]

    def __str__(self):
        return f"{self.job_seeker.user.username} - {self.job.title}"
    