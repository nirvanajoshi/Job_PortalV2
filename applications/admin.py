from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "job",
        "job_seeker",
        "status",
        "applied_at",
    )

    list_filter = (
        "status",
        "applied_at",
    )

    search_fields = (
        "job__title",
        "job_seeker__user__username",
        "job_seeker__user__email",
    )

    readonly_fields = (
        "applied_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Application Information",
            {
                "fields": (
                    "job",
                    "job_seeker",
                    "resume",
                    "cover_letter",
                    "status",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "applied_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ("-applied_at",)

    date_hierarchy = "applied_at"