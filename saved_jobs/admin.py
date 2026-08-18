from django.contrib import admin
from .models import SavedJob


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = (
        "job_seeker",
        "job",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "user__username",
        "user__email",
        "job__title",
        "job__company__name",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Saved Job Details",
            {
                "fields": (                    "job_seeker",
                    "job",
                )
            },
        ),
        ("Timestamps", {
            "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"