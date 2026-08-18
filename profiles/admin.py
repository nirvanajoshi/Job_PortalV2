from django.contrib import admin

from .models import JobSeekerProfile


@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "headline",
        "location",
        "experience_years",
        "created_at",
    )

    list_filter = (
        "experience_years",
        "created_at",
    )

    search_fields = (
        "user__username",
        "user__email",
        "headline",
        "location",
        "skills",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Profile Information",
            {
                "fields": (
                    "user",
                    "headline",
                    "bio",
                    "location",
                    "skills",
                    "experience_years",
                    "education",
                )
            },
        ),
        (
            "Social Links",
            {
                "fields": (
                    "website",
                    "linkedin_url",
                    "github_url",
                )
            },
        ),
        (
            "Resume",
            {
                "fields": ("resume",),
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"