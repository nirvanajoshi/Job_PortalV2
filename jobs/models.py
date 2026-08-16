from django.db import models
from companies.models import Company


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
        ("freelance", "Freelance"),
    )

    WORK_MODE_CHOICES = (
        ("on_site", "On-site"),
        ("remote", "Remote"),
        ("hybrid", "Hybrid"),
    )

    EXPERIENCE_LEVEL_CHOICES = (
        ("entry", "Entry Level"),
        ("mid", "Mid Level"),
        ("senior", "Senior Level"),
    )

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("closed", "Closed"),
    )

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="jobs"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, default="full_time"
    )
    work_mode = models.CharField(
        max_length=20, choices=WORK_MODE_CHOICES, default="on_site"
    )
    experience_level = models.CharField(
        max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default="mid"
    )
    salary_min = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    salary_max = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    application_deadline = models.DateField(blank=True, null=True)
    skills_required = models.TextField(
        blank=True, null=True, help_text="Comma-separated list of skills"
    )
    vacancies = models.PositiveIntegerField(default=1)
    is_featured = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"