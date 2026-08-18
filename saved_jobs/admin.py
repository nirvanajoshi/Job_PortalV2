from django.contrib import admin
from .models import SavedJob


@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "job",
        "saved_at",
    )
    list_filter = ("saved_at",)
    search_fields = (
        "user__username",
        "user__email",
        "job__title",
        "job__company__name",
    )
    readonly_fields = ("saved_at",)

    fieldsets = (
        (
            "Saved Job Details",
            {
                "fields": (
                    "user",
                    "job",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("saved_at",),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ("-saved_at",)
    date_hierarchy = "saved_at"