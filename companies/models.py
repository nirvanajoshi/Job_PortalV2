from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    COMPANY_SIZE_CHOICES = (
        ("1-10", "1-10 employees"),
        ("11-50", "11-50 employees"),
        ("51-200", "51-200 employees"),
        ("201-500", "201-500 employees"),
        ("500+", "500+ employees"),
    )

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="company"
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    industry = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    company_size = models.CharField(
        max_length=20, choices=COMPANY_SIZE_CHOICES, default="1-10"
    )
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name